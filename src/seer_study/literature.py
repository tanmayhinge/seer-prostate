"""Phase 1: reproducible PubMed search through NCBI E-utilities.

Queries, date limits and pacing live in config/literature.yaml. Every search is
logged with its exact term, PubMed's query translation, the hit count and the
time it ran, so the search can be repeated and reported.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from pathlib import Path

from seer_study.config import ConfigError, load_typed_yaml


class LiteratureError(RuntimeError):
    """Raised when PubMed returns an error or cannot be reached."""


@dataclass(frozen=True)
class SearchQuery:
    key: str
    topic: str
    term: str


@dataclass(frozen=True)
class LiteratureConfig:
    database: str
    esearch_url: str
    efetch_url: str
    tool: str
    date_from: str
    date_to: str
    retmax: int
    efetch_batch_size: int
    request_interval_seconds: float
    output_dir: Path
    seer_markers: tuple[str, ...]
    queries: tuple[SearchQuery, ...]


@dataclass(frozen=True)
class Article:
    pmid: str
    title: str
    journal: str
    year: int | None
    epub_date: str
    authors: tuple[str, ...]
    abstract: str
    doi: str
    mesh_terms: tuple[str, ...]
    publication_types: tuple[str, ...]
    query_keys: tuple[str, ...] = ()
    uses_seer: bool = False


@dataclass(frozen=True)
class SearchResults:
    config: LiteratureConfig
    log: list[dict]
    articles: list[Article]
    unfetched: list[str]


def load_literature_config(path: str | Path, root: str | Path | None = None) -> LiteratureConfig:
    path = Path(path)
    root = Path(root) if root is not None else path.resolve().parent.parent
    config = load_typed_yaml(path, LiteratureConfig)
    keys = [query.key for query in config.queries]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        raise ConfigError(f"queries: duplicate key(s) {duplicates}")
    if not config.output_dir.is_absolute():
        config = replace(config, output_dir=root / config.output_dir)
    return config


def build_esearch_params(query: SearchQuery, config: LiteratureConfig) -> dict[str, str]:
    return {
        "db": config.database,
        "term": query.term,
        "retmode": "json",
        "retmax": str(config.retmax),
        "sort": "pub_date",
        "datetype": "pdat",
        "mindate": config.date_from,
        "maxdate": config.date_to,
        "tool": config.tool,
    }


def parse_esearch(text: str) -> tuple[int, list[str], str]:
    data = json.loads(text)
    if "error" in data:
        raise LiteratureError(str(data["error"]))
    result = data.get("esearchresult", {})
    if "ERROR" in result:
        raise LiteratureError(str(result["ERROR"]))
    return int(result["count"]), list(result.get("idlist", [])), result.get("querytranslation", "")


def _text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def _year(pub_date: ET.Element | None) -> int | None:
    if pub_date is None:
        return None
    year = pub_date.findtext("Year")
    if year and year.strip().isdigit():
        return int(year)
    match = re.search(r"\d{4}", pub_date.findtext("MedlineDate") or "")
    return int(match.group()) if match else None


def _epub_date(article: ET.Element) -> str:
    node = article.find("ArticleDate")
    if node is None:
        return ""
    year, month, day = (node.findtext(part, "") for part in ("Year", "Month", "Day"))
    if not (year and month and day):
        return year
    return f"{year}-{int(month):02d}-{int(day):02d}"


def parse_efetch(xml_text: str) -> list[Article]:
    root = ET.fromstring(xml_text.encode("utf-8"))
    articles = []
    for node in root.findall("PubmedArticle"):
        citation = node.find("MedlineCitation")
        article = citation.find("Article")
        abstract_parts = []
        for part in article.findall("Abstract/AbstractText"):
            label = part.get("Label")
            content = _text(part)
            abstract_parts.append(f"{label}: {content}" if label else content)
        authors = []
        for author in article.findall("AuthorList/Author"):
            collective = author.find("CollectiveName")
            if collective is not None:
                authors.append(_text(collective))
            else:
                authors.append(f"{author.findtext('LastName', '')} {author.findtext('Initials', '')}".strip())
        doi = next(
            (_text(i) for i in node.findall("PubmedData/ArticleIdList/ArticleId") if i.get("IdType") == "doi"),
            next((_text(e) for e in article.findall("ELocationID") if e.get("EIdType") == "doi"), ""),
        )
        articles.append(
            Article(
                pmid=_text(citation.find("PMID")),
                title=_text(article.find("ArticleTitle")),
                journal=_text(article.find("Journal/Title")),
                year=_year(article.find("Journal/JournalIssue/PubDate")),
                epub_date=_epub_date(article),
                authors=tuple(authors),
                abstract=" ".join(abstract_parts),
                doi=doi,
                mesh_terms=tuple(_text(d) for d in citation.findall("MeshHeadingList/MeshHeading/DescriptorName")),
                publication_types=tuple(_text(p) for p in article.findall("PublicationTypeList/PublicationType")),
            )
        )
    return articles


def mentions_seer(article: Article, markers: tuple[str, ...]) -> bool:
    text = " ".join([article.title, article.abstract, *article.mesh_terms])
    return any(re.search(rf"\b{re.escape(marker)}\b", text, flags=re.IGNORECASE) for marker in markers)


def http_get(url: str, params: dict[str, str], timeout: float = 60.0, retries: int = 3) -> str:
    request = urllib.request.Request(f"{url}?{urllib.parse.urlencode(params)}", headers={"User-Agent": params.get("tool", "")})
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read().decode("utf-8")
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            time.sleep(2**attempt)
    raise LiteratureError(f"{url}: failed after {retries} attempts: {last_error}")


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_searches(
    config: LiteratureConfig,
    fetch: Callable[[str, dict[str, str]], str] = http_get,
    sleep: Callable[[float], None] = time.sleep,
    now: Callable[[], str] = _utc_now,
) -> SearchResults:
    def call(url: str, params: dict[str, str]) -> str:
        text = fetch(url, params)
        sleep(config.request_interval_seconds)
        return text

    log: list[dict] = []
    hits: dict[str, list[str]] = {}
    for query in config.queries:
        count, ids, translation = parse_esearch(call(config.esearch_url, build_esearch_params(query, config)))
        log.append(
            {
                "key": query.key,
                "topic": query.topic,
                "term": query.term,
                "query_translation": translation,
                "count": count,
                "retrieved": len(ids),
                "run_at": now(),
            }
        )
        for pmid in ids:
            hits.setdefault(pmid, []).append(query.key)

    pmids = list(hits)
    fetched: dict[str, Article] = {}
    for start in range(0, len(pmids), config.efetch_batch_size):
        batch = pmids[start : start + config.efetch_batch_size]
        params = {"db": config.database, "id": ",".join(batch), "retmode": "xml", "tool": config.tool}
        for article in parse_efetch(call(config.efetch_url, params)):
            if article.pmid in hits and article.pmid not in fetched:
                fetched[article.pmid] = replace(
                    article,
                    query_keys=tuple(hits[article.pmid]),
                    uses_seer=mentions_seer(article, config.seer_markers),
                )
    return SearchResults(
        config=config,
        log=log,
        articles=[fetched[p] for p in pmids if p in fetched],
        unfetched=[p for p in pmids if p not in fetched],
    )


def write_results(results: SearchResults, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    config = results.config
    log = {
        "database": config.database,
        "date_from": config.date_from,
        "date_to": config.date_to,
        "retmax_per_query": config.retmax,
        "sort": "pub_date",
        "queries": results.log,
        "unique_pmids": len(results.articles) + len(results.unfetched),
        "fetched": len(results.articles),
        "unfetched": results.unfetched,
    }
    (output_dir / "search_log.json").write_text(json.dumps(log, indent=2) + "\n")
    (output_dir / "articles.json").write_text(json.dumps([asdict(a) for a in results.articles], indent=2) + "\n")
    lines = ["pmid\tyear\tuses_seer\tqueries\tjournal\ttitle"]
    for article in results.articles:
        lines.append(
            "\t".join(
                [
                    article.pmid,
                    str(article.year or ""),
                    str(article.uses_seer),
                    ",".join(article.query_keys),
                    article.journal,
                    article.title,
                ]
            )
        )
    (output_dir / "articles.tsv").write_text("\n".join(lines) + "\n")

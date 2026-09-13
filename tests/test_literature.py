import json

import pytest
import yaml

from seer_study.config import ConfigError
from seer_study.literature import (
    LiteratureConfig,
    LiteratureError,
    build_esearch_params,
    load_literature_config,
    mentions_seer,
    parse_efetch,
    parse_esearch,
    run_searches,
    write_results,
)

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


@pytest.fixture
def lit_config(fixtures_dir):
    return load_literature_config(fixtures_dir / "mini_literature.yaml", root=fixtures_dir)


@pytest.fixture
def efetch_xml(fixtures_dir):
    return (fixtures_dir / "efetch_sample.xml").read_text()


def _esearch_json(ids, count=None):
    return json.dumps(
        {"esearchresult": {"count": str(len(ids) if count is None else count), "idlist": ids, "querytranslation": "translated"}}
    )


def test_config_loads_typed(lit_config, fixtures_dir):
    assert isinstance(lit_config, LiteratureConfig)
    assert lit_config.queries[0].key == "timeliness"
    assert lit_config.queries[0].term == 'prostate AND "time to treatment"'
    assert lit_config.efetch_batch_size == 1
    assert lit_config.output_dir == fixtures_dir / "reports/phase1_search"


def test_config_rejects_unknown_key(tmp_path, fixtures_dir):
    raw = yaml.safe_load((fixtures_dir / "mini_literature.yaml").read_text())
    raw["api_key"] = "secret"
    path = tmp_path / "lit.yaml"
    path.write_text(yaml.safe_dump(raw))
    with pytest.raises(ConfigError, match="api_key"):
        load_literature_config(path, root=tmp_path)


def test_config_rejects_duplicate_query_keys(tmp_path, fixtures_dir):
    raw = yaml.safe_load((fixtures_dir / "mini_literature.yaml").read_text())
    raw["queries"][1]["key"] = "timeliness"
    path = tmp_path / "lit.yaml"
    path.write_text(yaml.safe_dump(raw))
    with pytest.raises(ConfigError, match="timeliness"):
        load_literature_config(path, root=tmp_path)


def test_esearch_params(lit_config):
    params = build_esearch_params(lit_config.queries[0], lit_config)
    assert params["db"] == "pubmed"
    assert params["term"] == 'prostate AND "time to treatment"'
    assert params["retmode"] == "json"
    assert params["sort"] == "pub_date"
    assert params["retmax"] == "50"
    assert params["datetype"] == "pdat"
    assert params["mindate"] == "2000/01/01"
    assert params["maxdate"] == "2026/09/13"
    assert params["tool"] == "seer_prostate_timeliness_study"
    assert "email" not in params


def test_parse_esearch():
    count, ids, translation = parse_esearch(_esearch_json(["1", "2"], count=40))
    assert count == 40
    assert ids == ["1", "2"]
    assert translation == "translated"


def test_parse_esearch_error_raises():
    with pytest.raises(LiteratureError, match="bad term"):
        parse_esearch(json.dumps({"esearchresult": {"ERROR": "bad term"}}))


def test_parse_efetch_fields(efetch_xml):
    first, second = parse_efetch(efetch_xml)
    assert first.pmid == "11111111"
    assert first.title == "Time to radical prostatectomy and survival in SEER data."
    assert first.journal == "Journal of Test Oncology"
    assert first.year == 2024
    assert first.epub_date == "2023-12-01"
    assert first.authors == ("Smith J", "Jones A")
    assert first.abstract == (
        "BACKGROUND: Delay matters. METHODS: We used the Surveillance, Epidemiology, and End Results database."
    )
    assert first.doi == "10.1000/test.1"
    assert "SEER Program" in first.mesh_terms
    assert first.publication_types == ("Journal Article",)


def test_parse_efetch_handles_medline_date_and_missing_parts(efetch_xml):
    second = parse_efetch(efetch_xml)[1]
    assert second.year == 2021
    assert second.abstract == ""
    assert second.authors == ("Study Group",)
    assert second.doi == ""
    assert second.epub_date == ""


def test_mentions_seer(efetch_xml, lit_config):
    first, second = parse_efetch(efetch_xml)
    assert mentions_seer(first, lit_config.seer_markers)
    assert not mentions_seer(second, lit_config.seer_markers)


def _fake_fetch_factory(efetch_xml, calls):
    def fetch(url, params):
        calls.append((url, dict(params)))
        if url == ESEARCH_URL:
            return _esearch_json(["11111111", "22222222"])
        return efetch_xml

    return fetch


def test_run_searches_dedupes_and_tracks_queries(lit_config, efetch_xml):
    calls, sleeps = [], []
    results = run_searches(
        lit_config,
        fetch=_fake_fetch_factory(efetch_xml, calls),
        sleep=sleeps.append,
        now=lambda: "2026-09-13T00:00:00Z",
    )
    assert [a.pmid for a in results.articles] == ["11111111", "22222222"]
    assert results.articles[0].query_keys == ("timeliness", "rural")
    assert results.articles[0].uses_seer is True
    assert [entry["key"] for entry in results.log] == ["timeliness", "rural"]
    assert results.log[0]["count"] == 2
    assert results.log[0]["term"] == 'prostate AND "time to treatment"'
    assert results.log[0]["run_at"] == "2026-09-13T00:00:00Z"


def test_run_searches_batches_efetch_and_paces_requests(lit_config, efetch_xml):
    calls, sleeps = [], []
    run_searches(lit_config, fetch=_fake_fetch_factory(efetch_xml, calls), sleep=sleeps.append, now=lambda: "t")
    efetch_calls = [params for url, params in calls if url != ESEARCH_URL]
    assert [params["id"] for params in efetch_calls] == ["11111111", "22222222"]  # batch size 1, deduplicated ids
    assert len(sleeps) == len(calls)
    assert set(sleeps) == {0.4}


def test_write_results(lit_config, efetch_xml, tmp_path):
    results = run_searches(
        lit_config, fetch=_fake_fetch_factory(efetch_xml, []), sleep=lambda s: None, now=lambda: "t"
    )
    write_results(results, tmp_path)
    log = json.loads((tmp_path / "search_log.json").read_text())
    articles = json.loads((tmp_path / "articles.json").read_text())
    assert [entry["key"] for entry in log["queries"]] == ["timeliness", "rural"]
    assert log["database"] == "pubmed"
    assert {a["pmid"] for a in articles} == {"11111111", "22222222"}
    assert articles[0]["query_keys"] == ["timeliness", "rural"]

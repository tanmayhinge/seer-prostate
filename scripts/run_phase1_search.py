"""Phase 1 literature search: run the configured PubMed queries and save the raw results."""

import argparse
from pathlib import Path

from seer_study.literature import load_literature_config, run_searches, write_results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/literature.yaml"))
    args = parser.parse_args()
    config = load_literature_config(args.config)
    results = run_searches(config)
    write_results(results, config.output_dir)
    for entry in results.log:
        print(f"{entry['key']}: {entry['count']} hits, {entry['retrieved']} retrieved")
    print(f"{len(results.articles)} unique articles fetched, {len(results.unfetched)} not fetched")
    print(config.output_dir)


if __name__ == "__main__":
    main()

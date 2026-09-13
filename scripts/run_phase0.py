"""Phase 0 inventory: profile the raw SEER export and write reports/phase0.md."""

import argparse
from pathlib import Path

from seer_study.config import load_config
from seer_study.phase0 import write_phase0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/study.yaml"))
    args = parser.parse_args()
    report = write_phase0(load_config(args.config))
    print(report)


if __name__ == "__main__":
    main()

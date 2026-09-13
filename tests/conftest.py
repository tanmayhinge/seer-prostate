from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES


@pytest.fixture
def mini_config():
    from seer_study.config import load_config

    return load_config(FIXTURES / "mini_study.yaml", root=FIXTURES)


@pytest.fixture
def mini_frame(mini_config):
    from seer_study.io import read_dictionary, read_export

    names = read_dictionary(mini_config.paths.dictionary)
    return read_export(mini_config.paths.export, names)

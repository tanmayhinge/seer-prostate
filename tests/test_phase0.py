import dataclasses

from seer_study.phase0 import render_phase0, run_phase0, write_phase0
from seer_study.report import assert_style


def test_run_phase0_on_fixture(mini_config):
    results = run_phase0(mini_config)
    assert results.row_summary.rows == 6
    assert results.sequence.first_primary_inclusive == 5
    assert results.provenance.session_file_present is False
    assert results.provenance.archive_matches is None


def test_rendered_report_has_all_seven_items_and_obeys_style(mini_config):
    text = render_phase0(run_phase0(mini_config))
    for heading in [f"## {i}." for i in range(1, 8)]:
        assert heading in text
    assert "## Provenance" in text
    assert_style(text)


def test_write_phase0_creates_report_and_tables(mini_config, tmp_path):
    paths = dataclasses.replace(mini_config.paths, reports_dir=tmp_path, tables_dir=tmp_path / "tables")
    config = dataclasses.replace(mini_config, paths=paths)
    report = write_phase0(config)
    assert report == tmp_path / "phase0.md"
    assert report.read_text().startswith("# Phase 0")
    assert any((tmp_path / "tables").glob("frequency_*.csv"))

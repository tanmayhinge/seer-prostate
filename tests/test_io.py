import zipfile
from pathlib import Path

import pytest

from seer_study.io import (
    FrameIntegrityError,
    file_sha256,
    read_dictionary,
    read_dictionary_options,
    read_export,
    validate_frame,
    zip_member_sha256,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REAL_DIC = PROJECT_ROOT / "data" / "raw" / "export.dic"


def _write_bytes(path: Path, content: bytes) -> Path:
    path.write_bytes(content)
    return path


def test_read_dictionary_returns_names_in_var_order(fixtures_dir):
    names = read_dictionary(fixtures_dir / "mini.dic")
    assert len(names) == 12
    assert names[0] == "Patient ID"
    assert names[2] == "Time from diagnosis to treatment in days recode"
    assert names[-1] == "Reason no cancer-directed surgery"


def test_read_dictionary_options_excludes_variables(fixtures_dir):
    options = read_dictionary_options(fixtures_dir / "mini.dic")
    assert options["Variable names included"] == "false"
    assert options["Field delimiter"] == "tab"
    assert "Var1Name" not in options


def test_read_dictionary_orders_by_number_not_text(tmp_path):
    dic = tmp_path / "x.dic"
    lines = [f"Var{i}Name=col{i}" for i in (10, 2, 1, 3, 4, 5, 6, 7, 8, 9)]
    dic.write_text("[Variables]\n" + "\n".join(lines) + "\n")
    assert read_dictionary(dic) == [f"col{i}" for i in range(1, 11)]


def test_read_dictionary_gap_raises(tmp_path):
    dic = tmp_path / "gap.dic"
    dic.write_text("[Variables]\nVar1Name=a\nVar3Name=c\n")
    with pytest.raises(FrameIntegrityError, match="Var2"):
        read_dictionary(dic)


@pytest.mark.skipif(not REAL_DIC.exists(), reason="raw SEER dictionary not present")
def test_real_dictionary_has_41_columns():
    names = read_dictionary(REAL_DIC)
    assert len(names) == 41
    assert names[0] == "Patient ID"
    assert names[-1] == "COD to site recode ICD-O-3 2023 Revision"


def test_loader_keeps_every_value_as_string(mini_frame):
    assert all(isinstance(v, str) for v in mini_frame.to_numpy().ravel())


def test_loader_preserves_leading_zeros(mini_frame):
    assert mini_frame.loc[0, "Patient ID"] == "00000225"
    assert mini_frame.loc[0, "RX Summ--Surg Prim Site (1998-2022)"] == "00"
    assert mini_frame.loc[4, "Time from diagnosis to treatment in days recode"] == "0"


def test_loader_keeps_sentinel_labels_verbatim(mini_frame):
    assert mini_frame.loc[0, "RX Summ--Surg Prim Site 2023 (2023+)"] == "Blank(s)"
    assert mini_frame.loc[0, "Time from diagnosis to treatment in days recode"] == "Unable to calculate"


def test_na_like_strings_are_not_converted(tmp_path):
    dic = _write_bytes(tmp_path / "t.dic", b"[Variables]\nVar1Name=a\nVar2Name=b\nVar3Name=c\n")
    data = _write_bytes(tmp_path / "t.txt", b"NA\tNone/Unknown\tN/A\r\nnan\tnull\t\r\n")
    frame = read_export(data, read_dictionary(dic))
    assert frame["a"].tolist() == ["NA", "nan"]
    assert frame["b"].tolist() == ["None/Unknown", "null"]
    assert frame["c"].tolist() == ["N/A", ""]


def test_crlf_does_not_leak_into_last_column(tmp_path):
    dic = _write_bytes(tmp_path / "t.dic", b"[Variables]\nVar1Name=a\nVar2Name=b\n")
    data = _write_bytes(tmp_path / "t.txt", b"1\tAlive\r\n2\tDead\r\n")
    frame = read_export(data, read_dictionary(dic))
    assert frame["b"].tolist() == ["Alive", "Dead"]


def test_short_row_raises(tmp_path):
    dic = _write_bytes(tmp_path / "t.dic", b"[Variables]\nVar1Name=a\nVar2Name=b\nVar3Name=c\n")
    data = _write_bytes(tmp_path / "t.txt", b"1\t2\t3\r\n4\t5\r\n")
    with pytest.raises(FrameIntegrityError):
        read_export(data, read_dictionary(dic))


def test_long_row_raises(tmp_path):
    dic = _write_bytes(tmp_path / "t.dic", b"[Variables]\nVar1Name=a\nVar2Name=b\nVar3Name=c\n")
    data = _write_bytes(tmp_path / "t.txt", b"1\t2\t3\r\n4\t5\t6\t7\r\n")
    with pytest.raises(FrameIntegrityError):
        read_export(data, read_dictionary(dic))


def test_uniformly_wide_file_raises(tmp_path):
    dic = _write_bytes(tmp_path / "t.dic", b"[Variables]\nVar1Name=a\nVar2Name=b\n")
    data = _write_bytes(tmp_path / "t.txt", b"1\t2\t3\r\n4\t5\t6\r\n")
    with pytest.raises(FrameIntegrityError):
        read_export(data, read_dictionary(dic))


def test_validate_frame_accepts_mini(mini_frame, mini_config):
    validate_frame(mini_frame, mini_config.data)


def test_validate_frame_rejects_row_count(mini_frame, mini_config):
    with pytest.raises(FrameIntegrityError, match="rows"):
        validate_frame(mini_frame.iloc[:5], mini_config.data)


def test_validate_frame_rejects_year_out_of_range(mini_frame, mini_config):
    frame = mini_frame.copy()
    frame.loc[0, "Year of diagnosis"] = "2009"
    with pytest.raises(FrameIntegrityError, match="2009"):
        validate_frame(frame, mini_config.data)


def test_zip_member_checksum_matches_source(tmp_path):
    source = _write_bytes(tmp_path / "export.txt", b"a\tb\r\n" * 1000)
    archive = tmp_path / "export.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(source, arcname="export.txt")
    assert file_sha256(source) == zip_member_sha256(archive, "export.txt")

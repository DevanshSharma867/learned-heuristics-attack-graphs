import json
import sys

import pytest

from ahg import runlog


def test_provenance_records_hardware_and_libraries():
    prov = runlog.provenance([0, 1], {"name": "t"})
    hw = prov["hardware"]
    assert set(hw) == {"cpu_model", "logical_cores", "physical_cores", "ram_bytes"}
    assert isinstance(hw["logical_cores"], int) and hw["logical_cores"] > 0
    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        assert hw["cpu_model"] and hw["ram_bytes"] > 0
    libs = prov["libraries"]
    assert "pytest" in libs and "ahg" in libs  # the test runner and the package itself
    assert all(isinstance(v, str) and v for v in libs.values())


def test_write_run_never_overwrites(tmp_path, monkeypatch):
    monkeypatch.setattr(runlog, "LANDSCAPE", tmp_path)
    monkeypatch.setattr(runlog, "provenance", lambda seeds, config: {"date_utc": "2026-01-01T00:00:00+00:00",
                                                                   "git_commit": "abcdef0123"})
    out = runlog.write_run("r", {"x": 1}, "# r\n", [0], {})
    assert sorted(p.name for p in out.iterdir()) == ["provenance.json", "raw.json.gz", "report.md"]
    try:
        runlog.write_run("r", {"x": 2}, "# r\n", [0], {})
    except FileExistsError:
        pass
    else:
        raise AssertionError("second write to the same run directory was not refused")


def test_write_run_root_overrides_landscape(tmp_path, monkeypatch):
    monkeypatch.setattr(runlog, "LANDSCAPE", tmp_path / "landscape")
    monkeypatch.setattr(runlog, "provenance", lambda seeds, config: {"date_utc": "2026-01-01T00:00:00+00:00",
                                                                   "git_commit": "abcdef0123"})
    out = runlog.write_run("r", {"x": 1}, "# r\n", [0], {}, root=tmp_path / "feasibility")
    assert out.parent == tmp_path / "feasibility" / "r"
    assert not (tmp_path / "landscape").exists()


def test_load_raw_round_trips_both_formats(tmp_path, monkeypatch):
    """load_raw reads a D18 run (raw.json.gz) and a pre-D18 run (raw.json) to the same object."""
    monkeypatch.setattr(runlog, "provenance", lambda seeds, config: {"date_utc": "2026-01-01T00:00:00+00:00",
                                                                   "git_commit": "abcdef0123"})
    raw = {"config": {"name": "r", "x": [1, 2.5, None]}, "instances": [{"s": "é", "v": 3}]}
    gz_run = runlog.write_run("r", raw, "# r\n", [0], {}, root=tmp_path)
    assert runlog.load_raw(gz_run) == raw
    old_run = tmp_path / "old"
    old_run.mkdir()
    (old_run / "raw.json").write_text(json.dumps(raw, indent=1) + "\n")
    assert runlog.load_raw(old_run) == raw
    (old_run / "raw.json.gz").write_bytes((gz_run / "raw.json.gz").read_bytes())
    with pytest.raises(ValueError):
        runlog.load_raw(old_run)


def test_write_run_gzip_is_deterministic(tmp_path, monkeypatch):
    stamps = iter(["2026-01-01T00:00:00+00:00", "2026-01-01T00:00:01+00:00"])
    monkeypatch.setattr(runlog, "provenance", lambda seeds, config: {"date_utc": next(stamps),
                                                                   "git_commit": "abcdef0123"})
    a = runlog.write_run("r", {"x": 1}, "# r\n", [0], {}, root=tmp_path)
    b = runlog.write_run("r", {"x": 1}, "# r\n", [0], {}, root=tmp_path)
    assert (a / "raw.json.gz").read_bytes() == (b / "raw.json.gz").read_bytes()


def test_committed_pre_d18_run_still_loads():
    """A committed raw.json run (left untouched, rule 11) reads through load_raw."""
    run = runlog.ROOT / "results/landscape/landscape_small_n/2026-10-22T114620Z-4f00c1b"
    assert (run / "raw.json").exists() and not (run / "raw.json.gz").exists()
    assert len(runlog.load_raw(run)["instances"]) > 0

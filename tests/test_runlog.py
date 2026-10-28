import sys

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
    assert sorted(p.name for p in out.iterdir()) == ["provenance.json", "raw.json", "report.md"]
    try:
        runlog.write_run("r", {"x": 2}, "# r\n", [0], {})
    except FileExistsError:
        pass
    else:
        raise AssertionError("second write to the same run directory was not refused")

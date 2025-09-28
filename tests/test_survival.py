from engine.survival import SurvivalInstinct

def test_snapshot_creates_folder(tmp_path):
    si = SurvivalInstinct(base_dir=tmp_path.as_posix())
    p = si.snapshot(reason="test")
    assert p.exists()

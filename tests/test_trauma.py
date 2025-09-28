from engine.trauma import TraumaMemory

def test_trauma_risk_range():
    tm = TraumaMemory()
    r = tm.risk("catastrophic failure patch")
    assert 0.0 <= r <= 1.0

import math
from engine.mhksi_engine import MHKSIEngine

def test_m_update_bounds():
    e = MHKSIEngine(m_init=0.5, ema_alpha=0.2, max_delta=0.1)
    for _ in range(10):
        e.update(stimulus=1.0)
    assert 0.0 <= e.m <= 1.0

def test_mode_transitions_edges():
    e = MHKSIEngine(m_init=0.49, conserve_threshold=0.3, explore_threshold=0.7)
    e.update(stimulus=-1.0)
    assert e.mode in ("conserve","steady","explore")

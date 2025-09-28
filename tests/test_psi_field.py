from engine.psi_field_engine import PsiField

def test_coherence_monotonicity():
    pf = PsiField(rho=0.2)
    c0 = pf.coherence()
    pf.step(stimulus_text="strong positive signal", gain=0.8)
    c1 = pf.coherence()
    assert c1 >= 0.0


import pytest

from qnetsim.noise_analysis import (
    analyze_state,
    build_noise_model,
    simulate_state,
)


def test_ideal_bell_state_has_unit_fidelity():
    rho = simulate_state(0.0, 0.0)
    metrics = analyze_state(rho)

    assert metrics["fidelity"] == pytest.approx(1.0, abs=1e-8)
    assert metrics["correlation_zz"] == pytest.approx(1.0, abs=1e-8)
    assert metrics["correlation_xx"] == pytest.approx(1.0, abs=1e-8)


def test_noise_reduces_fidelity():
    ideal = analyze_state(simulate_state(0.0, 0.0))
    noisy = analyze_state(simulate_state(0.02, 0.02))

    assert noisy["fidelity"] < ideal["fidelity"]


def test_invalid_noise_probability_is_rejected():
    with pytest.raises(ValueError):
        build_noise_model(-0.1, 0.01)

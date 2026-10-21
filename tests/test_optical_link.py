
import pytest

from qnetsim.optical_link import OpticalLink


def test_zero_distance_probability_equals_detector_efficiency():
    link = OpticalLink(
        distance_km=0,
        attenuation_db_per_km=0.2,
        detector_efficiency=0.9,
    )

    assert link.transmission_probability == pytest.approx(0.9)


def test_longer_distance_reduces_transmission_probability():
    short_link = OpticalLink(distance_km=5)
    long_link = OpticalLink(distance_km=50)

    assert (
        long_link.transmission_probability
        < short_link.transmission_probability
    )


def test_zero_detector_efficiency_means_zero_success_probability():
    link = OpticalLink(distance_km=10, detector_efficiency=0)

    assert link.transmission_probability == 0


def test_invalid_distance_is_rejected():
    with pytest.raises(ValueError):
        OpticalLink(distance_km=-1)


def test_simulation_is_reproducible_with_same_seed():
    link = OpticalLink(distance_km=20)

    first = link.simulate_attempts(attempts=1000, seed=42)
    second = link.simulate_attempts(attempts=1000, seed=42)

    assert first == second


def test_simulation_counts_add_up():
    link = OpticalLink(distance_km=20)
    result = link.simulate_attempts(attempts=1000, seed=42)

    assert result["successes"] + result["failures"] == 1000
    assert result["attempts"] == 1000

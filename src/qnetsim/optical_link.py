
"""Probabilistic single-photon transmission over a simplified fiber link."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class OpticalLink:
    """An idealized optical fiber link.

    Attributes:
        distance_km: Fiber length in kilometres.
        attenuation_db_per_km: Fiber attenuation in dB/km.
        detector_efficiency: Effective detection efficiency from 0 to 1.
    """

    distance_km: float
    attenuation_db_per_km: float = 0.2
    detector_efficiency: float = 0.9

    def __post_init__(self) -> None:
        if not np.isfinite(self.distance_km) or self.distance_km < 0:
            raise ValueError("distance_km must be finite and non-negative")

        if (
            not np.isfinite(self.attenuation_db_per_km)
            or self.attenuation_db_per_km < 0
        ):
            raise ValueError(
                "attenuation_db_per_km must be finite and non-negative"
            )

        if (
            not np.isfinite(self.detector_efficiency)
            or not 0 <= self.detector_efficiency <= 1
        ):
            raise ValueError("detector_efficiency must be between 0 and 1")

    @property
    def transmission_probability(self) -> float:
        """Return the modelled probability of photon detection."""
        fiber_transmission = 10 ** (
            -self.attenuation_db_per_km * self.distance_km / 10
        )
        return self.detector_efficiency * fiber_transmission

    def simulate_attempts(
        self,
        attempts: int = 1000,
        seed: int | None = None,
    ) -> dict[str, float | int]:
        """Simulate independent photon-transmission attempts."""
        if not isinstance(attempts, int) or isinstance(attempts, bool):
            raise TypeError("attempts must be an integer")

        if attempts <= 0:
            raise ValueError("attempts must be positive")

        rng = np.random.default_rng(seed)
        probability = self.transmission_probability

        successes = int(
            rng.binomial(n=attempts, p=probability)
        )

        return {
            "attempts": attempts,
            "successes": successes,
            "failures": attempts - successes,
            "theoretical_probability": probability,
            "empirical_probability": successes / attempts,
        }


if __name__ == "__main__":
    link = OpticalLink(
        distance_km=20,
        attenuation_db_per_km=0.2,
        detector_efficiency=0.9,
    )

    print(f"Distance: {link.distance_km} km")
    print(
        "Theoretical detection probability: "
        f"{link.transmission_probability:.4f}"
    )
    print("Simulation:", link.simulate_attempts(attempts=10_000, seed=42))


"""Noise analysis for a two-qubit Bell pair using Qiskit Aer."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import (
    DensityMatrix,
    SparsePauliOp,
    state_fidelity,
)
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


OUTPUT_DIR = Path("results")


def create_bell_circuit() -> QuantumCircuit:
    """Prepare |Phi+> and save its final density matrix."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.save_density_matrix()
    return circuit


def build_noise_model(
    single_qubit_error: float,
    two_qubit_error: float,
) -> NoiseModel:
    """Apply depolarizing noise after H and CX gates."""
    for name, probability in (
        ("single_qubit_error", single_qubit_error),
        ("two_qubit_error", two_qubit_error),
    ):
        if not np.isfinite(probability) or not 0 <= probability <= 1:
            raise ValueError(f"{name} must be between 0 and 1")

    noise_model = NoiseModel()

    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(single_qubit_error, 1),
        ["h"],
    )
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(two_qubit_error, 2),
        ["cx"],
    )

    return noise_model


def simulate_state(
    single_qubit_error: float,
    two_qubit_error: float,
) -> DensityMatrix:
    """Return the noisy Bell-pair density matrix."""
    circuit = create_bell_circuit()
    noise_model = build_noise_model(
        single_qubit_error,
        two_qubit_error,
    )

    simulator = AerSimulator(
        method="density_matrix",
        noise_model=noise_model,
    )
    compiled = transpile(circuit, simulator)

    result = simulator.run(compiled).result()
    rho = result.data(0)["density_matrix"]

    return DensityMatrix(rho)


def analyze_state(rho: DensityMatrix) -> dict[str, float]:
    """Calculate fidelity and two-qubit Pauli correlations."""
    ideal_circuit = QuantumCircuit(2)
    ideal_circuit.h(0)
    ideal_circuit.cx(0, 1)
    ideal_state = DensityMatrix.from_instruction(ideal_circuit)

    zz = SparsePauliOp("ZZ")
    xx = SparsePauliOp("XX")

    return {
        "fidelity": float(state_fidelity(rho, ideal_state)),
        "correlation_zz": float(np.real(rho.expectation_value(zz))),
        "correlation_xx": float(np.real(rho.expectation_value(xx))),
    }


def run_experiment() -> list[dict[str, float]]:
    """Sweep noise strengths and save reproducible results."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Illustrative model parameters, not measured hardware error rates.
    error_levels = [0.0, 0.001, 0.005, 0.01, 0.03, 0.05]
    rows: list[dict[str, float]] = []

    for error in error_levels:
        rho = simulate_state(
            single_qubit_error=error,
            two_qubit_error=error,
        )
        metrics = analyze_state(rho)

        row = {
            "single_qubit_error": error,
            "two_qubit_error": error,
            **metrics,
        }
        rows.append(row)

        print(
            f"Noise={error:.3f} | "
            f"Fidelity={metrics['fidelity']:.4f} | "
            f"ZZ={metrics['correlation_zz']:.4f} | "
            f"XX={metrics['correlation_xx']:.4f}"
        )

    csv_path = OUTPUT_DIR / "bell_noise_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    # Plot fidelity and correlation changes against gate noise.
    fig, ax = plt.subplots()
    ax.plot(
        [row["single_qubit_error"] for row in rows],
        [row["fidelity"] for row in rows],
        marker="o",
        label="Bell-state fidelity",
    )
    ax.plot(
        [row["single_qubit_error"] for row in rows],
        [row["correlation_zz"] for row in rows],
        marker="s",
        label="ZZ correlation",
    )
    ax.plot(
        [row["single_qubit_error"] for row in rows],
        [row["correlation_xx"] for row in rows],
        marker="^",
        label="XX correlation",
    )

    ax.set_xlabel("Depolarizing error parameter per gate")
    ax.set_ylabel("Fidelity / correlation")
    ax.set_title("Effect of Gate Noise on a Bell Pair")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "bell_noise_analysis.png", dpi=200)
    plt.close(fig)

    print(f"\nSaved results to: {csv_path}")
    print(f"Saved plot to: {OUTPUT_DIR / 'bell_noise_analysis.png'}")

    return rows


if __name__ == "__main__":
    run_experiment()


"""Bell-pair generation and simulation using Qiskit Aer."""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def create_bell_pair_circuit(measure: bool = True) -> QuantumCircuit:
    """Create a circuit that prepares the Bell state |Phi+>.

    Args:
        measure: If True, measure both qubits into classical bits.

    Returns:
        A Qiskit quantum circuit.
    """
    circuit = QuantumCircuit(2, 2) if measure else QuantumCircuit(2)

    # Put qubit 0 into an equal superposition of |0> and |1>.
    circuit.h(0)

    # Entangle qubit 0 with qubit 1.
    circuit.cx(0, 1)

    if measure:
        circuit.measure([0, 1], [0, 1])

    return circuit


def simulate_bell_pair(shots: int = 2048) -> dict[str, int]:
    """Simulate Bell-pair measurements on an ideal Aer simulator.

    Args:
        shots: Number of circuit executions.

    Returns:
        A dictionary of measurement bitstrings and their counts.
    """
    if shots <= 0:
        raise ValueError("shots must be a positive integer")

    circuit = create_bell_pair_circuit(measure=True)
    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)

    result = simulator.run(compiled_circuit, shots=shots).result()
    return result.get_counts()


if __name__ == "__main__":
    counts = simulate_bell_pair()

    print("Bell-pair measurement results:")
    for bitstring, count in sorted(counts.items()):
        print(f"  {bitstring}: {count}")

    total = sum(counts.values())
    correlated = counts.get("00", 0) + counts.get("11", 0)

    print(f"\nTotal shots: {total}")
    print(f"Same-bit measurement fraction: {correlated / total:.3f}")

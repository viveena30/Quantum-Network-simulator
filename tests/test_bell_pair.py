
import pytest

from qnetsim.bell_pair import (
    create_bell_pair_circuit,
    simulate_bell_pair,
)


def test_bell_circuit_has_two_qubits():
    circuit = create_bell_pair_circuit(measure=False)

    assert circuit.num_qubits == 2
    assert circuit.num_clbits == 0


def test_bell_circuit_has_measurements_when_requested():
    circuit = create_bell_pair_circuit(measure=True)

    assert circuit.num_qubits == 2
    assert circuit.num_clbits == 2
    assert circuit.count_ops()["measure"] == 2


def test_ideal_bell_measurements_are_correlated():
    counts = simulate_bell_pair(shots=2048)

    assert set(counts).issubset({"00", "11"})
    assert sum(counts.values()) == 2048


def test_bell_simulation_rejects_non_positive_shots():
    with pytest.raises(ValueError):
        simulate_bell_pair(shots=0)


# QNetSim

QNetSim is a Python-based research prototype for studying entanglement
distribution and resource management in noisy quantum networks.

## Current features

- Bell-pair preparation and measurement with Qiskit.
- Ideal quantum-circuit simulation using Qiskit Aer.
- Probabilistic single-photon transmission over an idealized fiber link.
- Configurable fiber distance, attenuation, and detector efficiency.
- Reproducible stochastic simulations using random seeds.
- Automated tests using pytest.

## Research question

Can adaptive entanglement management improve useful entanglement
delivery in a network with optical loss and limited quantum memory?

## Scope and limitations

The current version is a foundational prototype. The optical-link model
is a simplified transmission model, not a complete photonic entanglement
generation protocol. Memory decoherence, entanglement fidelity under
network noise, multi-hop routing, and scheduling will be added and
validated in subsequent stages.

## Setup

Create and activate a virtual environment, then install:

```bash
python -m pip install -e ".[dev]"
```

## Run the examples

```bash
python -m qnetsim.bell_pair
python -m qnetsim.optical_link
```

## Run tests

```bash
python -m pytest -v
```

## Technology

Python, Qiskit, Qiskit Aer, NumPy, NetworkX, Matplotlib, pytest.

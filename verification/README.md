# Reproducing the finite checks

The scientific claims are established by the arguments in [the science account](../science/README.md). The checks here target concrete implementation and normalization mistakes: coherent Pauli order, the correct adjoint, mixed-state spectral weights, phase-estimation tails, and acceptance-to-trace conversions.

## Run

From the repository root, using Python 3.10 or later:

```bash
python -m pip install -r verification/requirements.txt
python verification/checks.py --output verification/results.json
```

The script exits unsuccessfully when an identity exceeds its stated tolerance. On success it writes a JSON report and prints a compact summary. The checked NumPy and SciPy versions are pinned; the report also records its script hash and random seed. Small floating-point differences across platforms are expected within the tolerances.

## What is checked

| Check | Independent comparison | Scope |
|---|---|---|
| Pauli averaging | Enumerate every generator tuple and compare mean spectral variance with the exact contraction formula | One- and two-qubit Hermitian contractions |
| Coherent walk | Build the full SELECT circuit and compare its signal block and weighted eigenphase moments with the separately computed averaged matrix | Generic unitary, both spectral endpoints, and a scalar complex phase |
| Branch phases | Change the phase of each SELECT branch while retaining its actual adjoint | Confirms that branch phases cancel in conjugation |
| Phase estimation | Evaluate its exact Dirichlet-kernel outcome distribution | 4,097 phase values with a 128-dimensional clock |
| Acceptance reductions | Compare direct signal compression and the product-of-reflections trace with an independently computed acceptance probability | Four-qubit circuits with one, two, or three initial clean qubits |
| Boundaries | Exhibit a bad fixed Pauli seed and two equal uncontrolled channels with distinct controlled unitaries | Guards the seed-averaged guarantee and the controlled-access assumption |

[results.json](results.json) contains the recorded output. These finite cases do not establish the asymptotic theorem, certify an optimal purity requirement, or establish novelty. They also do not simulate hardware noise, fault tolerance, or end-to-end application runtimes.

## Analytical dependencies

The exact averaging identity is proved in [Pauli averaging](../science/pauli-averaging.md). The mixed-input walk law, phase-estimation success probability, and query count are proved in [the estimator](../science/trace-estimator.md). Perturbations and controlled-oracle accuracy are treated in [robustness](../science/robustness.md); the acceptance identities are used in [few-clean amplification](../science/few-clean-amplification.md).

# Purity-Efficient Trace Estimation

How much initial purity is needed to estimate the normalized trace of a quantum operation at the optimal query precision?

For a supplied unitary $U$ on $n$ qubits, this repository develops an estimator of $\tau_n(U)=2^{-n}\operatorname{Tr}(U)$ with additive error $\epsilon$, constant success probability, $O(1/\epsilon)$ controlled forward/inverse queries, and $O(\log(1/\epsilon))$ initially clean qubits. The target is initialized maximally mixed, without access to a purification. The clean-qubit count is independent of $n$; the mixed-register width and known-gate cost are counted separately.

The mechanism is coherent averaging over products of random Pauli generators. It concentrates the spectrum around the normalized trace in normalized Hilbert–Schmidt mean square. Phase estimation of a qubitized walk then reads a representative eigenvalue from the mixed initialization. The complete circuit uses no intermediate measurement, reset, or postselection.

## Results and resources

The [main theorem and proof](science/trace-estimator.md) also cover the Hermitian part of a supplied unitary block encoding. For one real estimate of precision $0<\eta\leq1/4$, define

$$
s=\left\lceil\log_2(64/\eta^2)\right\rceil,\qquad
M=2^{\lceil\log_2(4\pi/\eta)\rceil},\qquad
r=\log_2M.
$$

| Resource | One real-estimator run |
|---|---|
| Success probability | At least $15/(2\pi^2)>3/4$ |
| Initially clean qubits | $a+s+r+2$, including the encoding's $a$ signal qubits |
| Initially mixed target | $n$ qubits |
| Supplied oracle calls | $M-1$ controlled $V$ and $M-1$ controlled $V^\dagger$ |
| Known elementary gates | $O((ns+a+s+1)M+r^2)$ |
| External random seed | $2ns$ classical bits |
| Fixed-circuit alternative | Replace the external seed with $2ns$ additional initially mixed qubits |

Six independent real runs give a complex estimate within $\epsilon$ with success at least $11/16>2/3$. A strict circuit with every register initialized at the start counts all six copies: $6n$ mixed target qubits and $6(s+r+2)$ clean qubits for the unitary case, with $\eta=\epsilon/2$. These constant factors preserve the stated asymptotic bounds.

The [robustness theorem](science/robustness.md) separates fixed block-encoding bias from accumulated execution error. The [amplification consequence](science/few-clean-amplification.md) starts from a known unitary circuit with $k=O(\log m)$ initially clean qubits, supplied or efficiently computable acceptance thresholds, and a known inverse-polynomial gap $\Delta$. It produces a constant gap without resets, using $k+O(\log(2/\Delta))$ clean qubits and $O(1/\Delta)$ calls to the original circuit and its inverse.

Controlled access and inverse access are explicit assumptions. The physical cost and clean workspace of an oracle implementation remain charged. The matching $\Omega(1/\epsilon)$ precision lower bound is a standard query bound; no lower bound on initial purity is proved. [Related work](references/related-work.md) explains the distinction from one-clean-qubit sampling, pure-state amplitude estimation, compressed trace estimators, and existing few-clean-qubit amplification.

## Read and reproduce

- **[Scientific account](science/README.md):** the question, mechanism, theorem dependencies, and routes through the proofs.
- **[Model and conventions](science/model.md):** initialization, controlled access, gate costs, and output precision.
- **[Primary-source comparison](references/related-work.md)** and **[BibTeX](references/references.bib)**.
- **[Verification](verification/README.md):** exact small-ensemble identities and finite coherent-circuit diagnostics, with [recorded results](verification/results.json).

From the repository root:

~~~bash
python3 -m pip install -r verification/requirements.txt
python3 verification/checks.py
~~~

The finite checks test signs, normalizations, phase handling, and spectral sampling. The asymptotic guarantees follow from the analytic proofs.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).

## License

[MIT](LICENSE).

# Related work and scope of the resource claim

This page compares normalized trace estimators by **oracle calls, initially clean qubits, and the treatment of repetition**. These are distinct resources. Throughout, $d=2^n$, $\tau(A)=\mathrm{Tr}(A)/d$, and $\varepsilon$ denotes additive normalized-trace accuracy unless a relative-error parameter is explicitly identified. The comparison concerns constant success probability.

The result developed in this repository estimates the trace of an arbitrary supplied unitary using $O(1/\varepsilon)$ controlled forward/inverse calls and $O(\log(1/\varepsilon))$ initially clean qubits, with the target initially maximally mixed. The clean-qubit bound is independent of $n$. For a supplied block encoding, its clean signal workspace must also be counted. The query exponent alone, and all the basic circuit ingredients, have precedents.

## Comparison at the theorem level

| Source and inspected location | Relevant guarantee | Resource distinction |
|---|---|---|
| [Knill–Laflamme](#knill1998), DQC1 construction; [Shor–Jordan](#shor2008), §1 | A one-clean-qubit interference experiment reads out a normalized unitary trace. Independent bounded-outcome sampling uses $O(\varepsilon^{-2})$ experiments. | One clean qubit per experiment; external statistical repetition must be distinguished from a single circuit with no resets. |
| [Luongo–Shao](#luongo2024), Lemma 39 and its proof | Additive normalized trace of a supplied $(\alpha,q,\delta)$ block encoding, with $O(\alpha/\varepsilon)$ forward/inverse calls when $\delta\leq\varepsilon/2$. | The proof prepares a Bell purification of the system before amplitude estimation. |
| [Bravyi–Chowdhury–Gosset–Wocjan](#bravyi2023), Theorem 7, Lemma 15, Eq. (154) | For $M=A^\dagger A$, relative error $\epsilon_{\rm TR}$ costs $O(1/(\epsilon_{\rm TR}\sqrt{\tau(M)}))$ block-encoding calls and $n+a+O(\log(1/\epsilon_{\rm TR}))$ total qubits. | Clifford compression reduces total width; the displayed initial state still uses a pure $n$-qubit system. |
| [Cade–Montanaro](#cade2018), §1.1, §3.1, Corollary 6, Appendix A.3 | Spectral-function estimation in the one-clean-qubit framework, using phase estimation to construct a trace-accessible unitary. | The final DQC1 trace readout retains independent statistical repetitions. |
| [Zhang–Shao](#zhang2026), Theorem 6.5, Remark 6.6 | Spectral trace estimation with very few clean ancillas, and optimal dependence on the function's approximate degree in the specified model. | Theorem 6.5 explicitly retains an $\varepsilon^{-2}$ sampling factor; its degree lower bound is a different parameter statement. |
| [Fujii et al.](#fujii2016), Theorems 4–5; §3.4 and §9 of the full version | Strong error reduction for fixed-gap logarithmic-clean computation, including a two-clean-qubit circuit with exponentially small two-sided error. | Polynomial-time class simulations do not by themselves preserve a particular precision–query exponent. |

### Optimal-query estimators and purification

In Luongo–Shao's Lemma 39, the state used by amplitude estimation is built from

$$
\lvert\phi\rangle=d^{-1/2}\sum_{j=0}^{d-1}\lvert j\rangle\lvert0^q\rangle\lvert j\rangle.
$$

This supplies a pure state whose expectation is the normalized trace. Replacing either half by an unpurified maximally mixed register does not preserve the rank-one preparation/reflection used by that proof. The comparison here concerns the initial purity of that realization, rather than a lower bound on every possible realization. [Primary source, Lemma 39](https://arxiv.org/html/2011.06475v2).

BCGW is a stronger width comparator than the full-purification method. Its Eq. (154) prepares a pure state from $\lvert0^a\rangle\lvert0^{n-k}\rangle\lvert\Phi_k\rangle$ and a random Clifford. Thus it removes the need for a second full $n$-qubit register while retaining purity across the system and the smaller reference. Its relative-error theorem should also not be silently relabeled as an additive-error theorem. The present resource improvement is therefore not a claim that all previous efficient trace estimators require $2n$ clean qubits. [Primary source, Theorem 7 and Eq. (154)](https://arxiv.org/html/2110.15466v2).

### Spectral functions and the final sampling cost

Cade–Montanaro's phase-estimation/function-phase/uncomputation circuit provides a unitary whose trace contains the desired spectral sum. Its construction cost and the cost of statistically reading out that trace are separate. The original §1.1 explicitly describes repeated trace experiments, and Appendix A.3 budgets a separate final trace-estimation error. Corollary 6 is a polynomial-time statement. A linear phase-estimation precision factor should consequently not be read as a complete $O(1/\varepsilon)$ trace-estimation bound. [Published primary source](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2018.4).

For a Hermitian decomposition with coefficient sum $\alpha$ and $L$ terms, Zhang–Shao Theorem 6.5 gives total cost

$$
\widetilde O \left(\frac{\alpha L \widetilde{\deg}_{\varepsilon/3}(f)}{\varepsilon^2}\right),
$$

with per-experiment depth omitting the sampling factor and a doubly logarithmic clean-ancilla bound in the stated parameters. Its proof repeats an ancilla expectation measurement. The lower bound in Theorem 6.12 concerns approximate degree. Their low-ancilla block encodings can be inputs to the estimator here; their construction and approximation errors remain charged. [Primary source, §§6.2–6.3](https://arxiv.org/html/2607.01843v2).

## Mixed computation and error reduction

The original DQC1 model establishes that a highly mixed register can support useful computation. The standard controlled-unitary experiment has mean $\mathrm{Re}\tau(U)$ or $\mathrm{Im}\tau(U)$, and ordinary independent sampling gives the quadratic precision cost. This repository changes the coherent processing before the final readout. It does not change the historical attribution of the trace task. [Knill–Laflamme](https://doi.org/10.1103/PhysRevLett.81.5672).

Shor–Jordan describe simulating additional clean qubits through a trace construction, with signal attenuation exponential in the number of simulated clean bits. This establishes polynomial-complexity relations for logarithmic workspace, but inserting a precision-dependent number of virtual clean qubits does not automatically retain an optimal precision–query bound. [Primary source, §1](https://arxiv.org/pdf/0707.2831v3).

Fujii et al. work in the strict model with initialization only at the start, no intermediate measurements, and one measured output qubit. Their full-version Theorem 4 assumes fixed constants $0\lt s\lt c\lt 1$. Sections 3.4 and 9 explicitly distinguish the inverse-polynomial-gap question from that theorem. These locations motivate the operational amplification consequence below. They establish the historical question; they do not establish its status throughout all subsequent literature. [Full version](https://arxiv.org/html/1509.07276v1); [published version](https://doi.org/10.4230/LIPIcs.ICALP.2016.13).

### Operational consequence for a known weak gap

Suppose a polynomial-time uniform unitary circuit $V_x$ uses $k=O(\log m)$ initially clean qubits and polynomially many maximally mixed qubits, where $m$ is the input length. Suppose its acceptance thresholds $c(m),s(m)$ can be computed or are supplied to adequate polynomial precision, and a known lower bound satisfies $c-s\geq1/\mathrm{poly}(m)$. Define, with acceptance corresponding to output zero,

$$
H_x=V_x^\dagger Z_{\rm out}V_x,
\qquad
A_x=(\langle0^k\rvert\otimes I)H_x(\lvert0^k\rangle\otimes I).
$$

Then $H_x$ is a Hermitian involution and $p_x=(1+\tau(A_x))/2$. Applying the mixed-target estimator at accuracy below the promised gap gives a fixed-gap decision circuit with $O(\log m)$ clean qubits. The Pauli seed can be held in additional initially maximally mixed bits that are retained as unchanged computational-basis controls. A reversible comparison with the supplied threshold leaves one output bit for the sole terminal measurement. Circuit inversion and control are available from the uniform gate description of $V_x$.

Composing this **operational, uniform-threshold statement** with Fujii et al.'s fixed-gap Theorem 4 gives a two-clean-qubit, exponentially small two-sided-error implementation with polynomial overhead. The composition does not claim to preserve the trace estimator's $O(1/\varepsilon)$ oracle bound. No unrestricted class identity for unspecified threshold functions is needed. The current comparison supports this explicit reduction and a connection to the historically posed question, without an exhaustive priority claim.

Lowe et al.'s 2026 subspace-DQC1 construction is a relevant neighboring amplification result. In §III.1, its Marriott–Watrous step uses a perfectly accepting subspace and an eigenvector soundness bound on the complement. This differs from amplifying an arbitrary small gap in **average** acceptance probability. Appendix E also uses repeated eigenvalue samples for additive estimates. [Primary source, §III.1 and Appendix E](https://arxiv.org/html/2607.03278v2).

## Known ingredients and the role of coherent averaging

Pauli conjugation, randomization in operator space, coherent linear combinations, block encodings, qubitization, and phase estimation are established methods. Amplitude estimation already supplies inverse-linear precision scaling when its required pure preparation and inverse operations are available. Relevant foundational sources include [Brassard et al.](https://arxiv.org/abs/quant-ph/0005055), [Low–Chuang](https://doi.org/10.22331/q-2019-07-12-163), and [Gilyén et al.](https://arxiv.org/abs/1806.01838).

Quantum expanders are a particularly close conceptual antecedent: they contract the traceless part of an operator in Hilbert–Schmidt norm using mixtures of unitary conjugations. Gross–Eisert provide a constant-degree construction and efficient implementation in their odd-dimensional setting; Harrow gives a representation-theoretic route from classical Cayley expanders. [Gross–Eisert, Observation 1 and Theorem 2](https://arxiv.org/html/0710.0651v2); [Harrow, construction and efficiency conditions](https://arxiv.org/html/0709.1142v2).

As a direct inference from these ingredients, any efficiently selectable mixed-unitary expander with constant contraction can be coherently iterated for $O(\log(1/\varepsilon))$ steps and used in the same spectral-sampling architecture. This makes contraction toward a scalar an existing mathematical route, rather than a new principle introduced here. The Pauli construction supplies an explicit circuit on arbitrary qubit registers, an exact ensemble variance identity, and a simple gate/resource ledger without a large lookup table.

The operative identity for the present construction is

$$
\mathbb E_G \tau \left[(B_G-\tau(A)I)^2\right]
=2^{-s}\tau \left[(A-\tau(A)I)^2\right],
\qquad
B_G=2^{-s}\sum_{z\in\lbrace 0,1\rbrace ^s}P_z^\dagger A P_z.
$$

The eigenvalue sampled from a maximally mixed target has this normalized spectral variance. Consequently, the algorithm needs concentration of the joint random-seed/eigenvalue experiment, rather than operator-norm closeness for every seed. Coherent selection and its actual adjoint preserve phases even when the generators anticommute. The contribution claimed here is the resulting simultaneous oracle, initial-purity, and no-reset resource theorem, together with the explicit uniform implementation.

## Boundaries of the claim

Boixo–Somma already achieve Heisenberg-type precision in mixed-state computation for structured parameter estimation. Arbitrary normalized unitary trace estimation is a different task, so this project makes no claim to the first inverse-linear precision scaling in mixed-state computation. [Primary source](https://doi.org/10.1103/PhysRevA.77.052320).

Controlled inverse access is an explicit resource. Tang–Wright give trace-based instances demonstrating the loss of generic amplitude-estimation speedups with forward-only access. Their lower-bound setting is relevant to the access assumption, rather than to the clean-qubit upper bound. [Primary source, arXiv:2507.23787v2](https://arxiv.org/abs/2507.23787v2).

The $\Omega(1/\varepsilon)$ query lower bound follows from the standard scalar-phase discrimination argument and is not a new lower-bound mechanism. No lower bound on the number of initially clean qubits is proved here. No claim is made that a one-clean-qubit optimal-query algorithm is impossible, that supplying a block encoding is free, or that the oracle improvement alone guarantees a practical runtime advantage.

## Primary-source record

The selected theorem-level comparisons were checked on 31 October 2026. Versioned preprints below identify the inspected text; journal metadata and full-version metadata are kept distinct. The search was directed toward the closest task, access-model, purity, and amplification comparators and is not an exhaustive historical survey. BibTeX records are in [references.bib](references.bib).

| Citation key | Primary source and inspected version |
|---|---|
| <a id="knill1998"></a>`knill1998` | Knill and Laflamme, *Power of One Bit of Quantum Information*, PRL 81, 5672–5675 (1998); [arXiv:quant-ph/9802037v1](https://arxiv.org/abs/quant-ph/9802037v1). |
| <a id="shor2008"></a>`shor2008` | Shor and Jordan, *Estimating Jones polynomials is a complete problem for one clean qubit*, QIC 8, 681–714 (2008); [arXiv:0707.2831v3](https://arxiv.org/abs/0707.2831v3). |
| <a id="fujii2016"></a>`fujii2016` | Fujii et al., *Power of Quantum Computation with Few Clean Qubits*, ICALP 2016, 13:1–13:14; full version [arXiv:1509.07276v1](https://arxiv.org/abs/1509.07276v1). |
| <a id="cade2018"></a>`cade2018` | Cade and Montanaro, *The Quantum Complexity of Computing Schatten p-norms*, TQC 2018, 4:1–4:20; [published full text](https://doi.org/10.4230/LIPIcs.TQC.2018.4). |
| <a id="luongo2024"></a>`luongo2024` | Luongo and Shao, *Quantum algorithms for spectral sums*, [arXiv:2011.06475v2](https://arxiv.org/abs/2011.06475v2), revised 10 June 2024. |
| <a id="bravyi2023"></a>`bravyi2023` | Bravyi et al., *On the complexity of quantum partition functions*, [arXiv:2110.15466v2](https://arxiv.org/abs/2110.15466v2), revised 20 September 2023; journal article *Quantum Hamiltonian complexity in thermal equilibrium*, Nature Physics 18, 1367–1370 (2022). |
| <a id="zhang2026"></a>`zhang2026` | Zhang and Shao, *Quantum space-depth tradeoffs for coherent block encodings*, [arXiv:2607.01843v2](https://arxiv.org/abs/2607.01843v2), revised 30 September 2026. |
| <a id="lowe2026"></a>`lowe2026` | Lowe et al., *Complexity of Normalized Persistence Problems for Topological Data Analysis and Local Hamiltonians*, [arXiv:2607.03278v2](https://arxiv.org/abs/2607.03278v2), revised 29 September 2026. |


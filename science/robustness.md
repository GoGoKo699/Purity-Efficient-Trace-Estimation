# Robustness and implementation error

This page gives a perturbation theorem for the [real estimator](trace-estimator.md). It distinguishes a fixed error in the encoded matrix from errors incurred when executing the circuit. The first changes the quantity being estimated; the second changes the output distribution.

Write

$$
\tau_n(A)=2^{-n}\operatorname{Tr}(A),\qquad
D(\rho,\sigma)=\frac12\|\rho-\sigma\|_1,
\qquad
d_\diamond(\mathcal E,\mathcal F)
=\frac12\|\mathcal E-\mathcal F\|_\diamond.
$$

All operational error budgets below use these normalized distances. The nominal oracles are unitary. An implemented oracle may be a general quantum channel, provided its error is bounded in the stated controlled-oracle model.

## 1. Approximate block encodings can be Hermitianized exactly

Let $A=A^\dagger$ act on $n$ qubits. Let $V$ be a unitary on $a+n$ qubits, and define

$$
J_a|\psi\rangle=|0^a\rangle|\psi\rangle,
\qquad C=J_a^\dagger VJ_a.
$$

Suppose

$$
\|C-A\|\le\epsilon_{\rm BE}.
\tag{1}
$$

The actual Hermitian signal matrix is

$$
\widehat A=\frac{C+C^\dagger}{2}.
\tag{2}
$$

It obeys $\widehat A=\widehat A^\dagger$, $\|\widehat A\|\le1$, and

$$
\|\widehat A-A\|\le\epsilon_{\rm BE},\qquad
|\tau_n(\widehat A)-\tau_n(A)|\le\epsilon_{\rm BE}.
\tag{3}
$$

The contraction bound follows because $C$ is a compression of a unitary. The error bound follows by taking the Hermitian part of $C-A$; the normalized trace bound follows from $|\operatorname{Tr}X|\le2^n\|X\|$.

To implement (2), introduce a signal qubit $b$ and form

$$
F_V=\begin{pmatrix}0&V^\dagger\\ V&0\end{pmatrix}.
\tag{4}
$$

This is an exact Hermitian involution for every unitary $V$. Its compression onto $|+\rangle_b|0^a\rangle$ is $\widehat A$. Conjugating by a Hadamard on $b$ changes this to an all-zero signal convention. Therefore the exact Pauli-averaging and mixed-state spectral-sampling proofs apply to $\widehat A$, even if $C$ is not Hermitian.

In particular, no perturbation bound on individual eigenvectors, spectral gaps, or the function $\arccos$ is required. A fixed block error contributes $\epsilon_{\rm BE}$ once to the final additive trace error. It does not automatically incur a query-count multiplier.

The distinction relies on having a fixed unitary $V$ and its matching adjoint. A nonunitary implementation channel cannot simply be substituted for $V$ in (4) and called a Hermitian involution. Such execution errors are covered separately below.

If every use instead implements the same fixed unitary $\widetilde V$ and its matching adjoint exactly, then the algorithm can be analyzed directly on $\widetilde V$. For example, $\|\widetilde V-V\|\le\xi$ increases the fixed signal-block bound by at most $\xi$, giving trace error $\eta+\epsilon_{\rm BE}+\xi$ without a query-count multiplier on $\xi$. This conclusion requires the same consistent pair throughout the run; call-dependent errors or a separately imperfect inverse require the execution-error analysis.

### Scaled encodings

If the supplied convention is

$$
\|A-\alpha C\|\le\epsilon_{\rm BE},\qquad \alpha>0,
$$

the same construction estimates $\tau_n(A)$ with error at most
$\alpha\eta+\epsilon_{\rm BE}$, by multiplying an $\eta$-accurate estimate of $\tau_n(\widehat A)$ by $\alpha$. Its query count is $O(1/\eta)$ for $\eta\le1/4$. Choosing $\eta=\min\{1/4,(\epsilon-\epsilon_{\rm BE})/\alpha\}$ gives $O(\max\{1,\alpha/(\epsilon-\epsilon_{\rm BE})\})$ queries for desired final error $\epsilon>\epsilon_{\rm BE}$. The initialization and workspace required to realize the supplied encoding remain part of the resource budget.

## 2. Hybrid bound for an imperfect execution

Consider an ideal circuit

$$
\mathcal C=\mathcal E_L\circ\cdots\circ\mathcal E_1
$$

with ideal initial state $\rho_0$, and an implemented circuit with initial state $\widetilde\rho_0$ and step maps $\widetilde{\mathcal E}_j$. Assume

$$
D(\widetilde\rho_0,\rho_0)\le\zeta,
\qquad
d_\diamond(\widetilde{\mathcal E}_j,\mathcal E_j)\le\delta_j.
\tag{5}
$$

Then the final states, and consequently every final measurement distribution, differ by at most

$$
\mathcal E_{\rm run}:=\zeta+\sum_{j=1}^L\delta_j.
\tag{6}
$$

For the states this is a trace-distance bound; for the distributions it is a total-variation bound.

**Proof.** Insert one implemented step at a time. Contractivity of trace distance controls the input perturbation and every subsequent ideal or implemented channel. The definition of normalized diamond distance bounds each inserted step, including when its input is entangled with the rest of the circuit. Sum the bounds and then apply measurement contractivity. No independence or stochastic cancellation of the errors is used. $\square$

The per-step assumptions concern the complete computational registers and controls. For noise with a retained environment, the same proof requires corresponding bounds on the extended step maps including that memory. A bound on an isolated reduced gate does not by itself establish that stronger hypothesis.

### Controlled-oracle accuracy is the relevant accuracy

The general trace theorem assumes controlled-$V$ and controlled-$V^\dagger$ access. Their implementation errors must therefore be measured for those controlled channels. Closeness of the uncontrolled conjugation channels alone is insufficient: $V$ and $-V$ induce the same uncontrolled channel, while their controlled versions differ by a phase on the control.

If a real run uses $q_+$ forward and $q_-$ inverse oracle calls, and $g$ known gates with error bounds $\gamma_1,\ldots,\gamma_g$, a useful form of (6) is

$$
\mathcal E_{\rm run}
\le \zeta+q_+\delta_++q_-\delta_-+
\sum_{\ell=1}^{g}\gamma_\ell.
\tag{7}
$$

The real estimator uses $q_++q_-=2(M-1)$ in the specified Hermitianization implementation. Thus a constant total execution budget permits controlled-oracle error $O(1/M)=O(\eta)$ per call when the forward and inverse accuracies are comparable. Constant per-call error independent of $\eta$ is not sufficient for this worst-case guarantee.

If two known unitaries satisfy $\|U-\widetilde U\|\le\xi$, then

$$
d_\diamond(\operatorname{Ad}_U,
\operatorname{Ad}_{\widetilde U})\le\xi.
\tag{8}
$$

This follows by expanding the difference of the two conjugations into two terms and using the operator/trace-norm inequality. The same statement applies to controlled unitaries when their operator-norm difference, with a consistent phase convention, is the quantity bounded.

## 3. Robust real-estimator theorem

Choose

$$
s=\left\lceil\log_2\frac{64}{\eta^2}\right\rceil,
\quad
M=2^{\lceil\log_2(4\pi/\eta)\rceil},
\quad r=\log_2M,
\qquad 0<\eta\le\frac14.
$$

For an ideal execution on the exact Hermitian signal $\widehat A$, the [real estimator theorem](trace-estimator.md) gives

$$
\Pr\!\left[|\widehat\tau-\tau_n(\widehat A)|\le\eta\right]
\ge p_*:=\frac{15}{2\pi^2}>\frac34.
\tag{9}
$$

Here the probability is joint over the Pauli seed and the quantum outcomes. The lower bound is a product: a uniformly sampled eigenvalue is close to the trace with probability at least $15/16$, and the phase-estimation guarantee of $8/\pi^2$ holds conditioned on every such eigenvalue.

Combining (3), (6), and (9) proves

$$
\boxed{
\Pr\!\left[|\widehat\tau-\tau_n(A)|
\le\eta+\epsilon_{\rm BE}\right]
\ge p_*-\mathcal E_{\rm run}.
}
\tag{10}
$$

For example, the sufficient conditions

$$
\epsilon_{\rm BE}\le\epsilon/2,
\quad\eta=\epsilon/2,
\quad\mathcal E_{\rm run}\le1/32
$$

give additive error at most $\epsilon$ with success probability greater than $2/3$. The allocations within $\mathcal E_{\rm run}$ can be changed to reflect the actual implementation.

### Complex estimates and confidence amplification

The ideal six-run construction in the [complex trace theorem](trace-estimator.md) has success probability at least $11/16$. Apply (6) to the entire six-run circuit, including final median computation if it is performed coherently. If its aggregate initialization and implementation budget is at most $1/96$, its success is at least

$$
\frac{11}{16}-\frac1{96}=\frac{65}{96}>\frac23.
$$

This aggregate guarantee does not require an independence assumption about implementation errors between the runs. Fixed structural errors in the real and imaginary signal blocks must additionally fit the requested complex-error budget. Alternatively, ensure a per-run operational budget at most $1/128$, so that each real run still succeeds with probability above $3/4$, and use independent runs with the original median proof. The aggregate hybrid formulation is preferable when independence has not been established.

## 4. Initialization error and bias

The ideal target is $I/2^n$, independent of the clean registers and the Pauli seed. Suppose the actual target state $\rho$ satisfies

$$
D(\rho,I/2^n)\le\zeta_{T}.
$$

Every output-event probability changes by at most $\zeta_{T}$, by (6). In addition, for any Hermitian contraction $B$, its underlying spectral mean obeys

$$
|\operatorname{Tr}(\rho B)-\tau_n(B)|
\le2\zeta_{T}.
\tag{11}
$$

Equation (11) is the elementary expectation-bias bound. Equation (6), rather than the bias alone, controls the probability of an accurate estimate. An arbitrary nonuniform target does not receive the ideal uniformly weighted spectral-sampling guarantee.

The same treatment covers approximate clean initialization or an imperfect internal seed distribution, provided the **joint** initial state is within $\zeta$ of the required product state. For independent tensor-product preparation errors, the total trace distance is bounded by the sum of the individual distances. Small marginal errors alone do not bound correlations in a joint initialization.

For an internal classical seed, a total-variation error in its distribution contributes at most that error to $\zeta$. The seed must be independent of the supplied matrix and must remain the same throughout the coherent run.

## 5. Known-gate synthesis and preservation of the model

Known gates contribute to (7). With arbitrary one-qubit rotations and two-qubit gates, and the returned control workspace used for the signal reflection, the known-gate count for a real run is

$$
L_{\rm known}
=O\!\left(M\bigl[ns+a+s+1\bigr]+r^2\right),
$$

as detailed in the core resource ledger. Uniformly allocating a known-gate error budget $\beta$ gives per-gate accuracy $\beta/L_{\rm known}$. Fixed finite universal gate sets can achieve this with a polylogarithmic compilation overhead and without adding a fresh pure register for every synthesized rotation; the standard constructive Solovay–Kitaev theorem suffices for this conservative statement [DN06]. General controlled-gate decompositions are described in [BBC+95].

For inverse-polynomial $\eta$ in a polynomial-size input, all required accuracies have polynomial bit descriptions and the compiled circuit remains polynomial-size and polynomial-time uniform. This statement concerns unitary gate synthesis: it introduces no measurement, reset, or postselection.

When compiling a conjugation $T^\dagger F T$, using an implemented $\widetilde T$ and its exact circuit adjoint preserves the Hermitian-involution structure when $F$ is Hermitian and unitary. The circuit should not replace an adjoint by a forward product merely because its individual Pauli generators are Hermitian. Branchwise Pauli phases are harmless when the matching adjoint is used.

An outer controlled conjugation can be implemented as $T$, controlled-$F$, and $T^\dagger$, with the appropriate operator ordering. The uncontrolled conjugating gates cancel on the inactive branch. This avoids adding an outer control to every gate of SELECT. With a classical seed, SELECT retains its Clifford implementation; with a seed stored in mixed qubits, the extra seed controls require known Toffoli or controlled-phase gates, whose costs are still $O(ns)$.

## References

- **[BBC+95]** A. Barenco et al., *Elementary gates for quantum computation*, Physical Review A **52**, 3457–3467 (1995). [arXiv:quant-ph/9503016](https://arxiv.org/abs/quant-ph/9503016); [DOI](https://doi.org/10.1103/PhysRevA.52.3457).
- **[DN06]** C. M. Dawson and M. A. Nielsen, *The Solovay–Kitaev algorithm*, Quantum Information & Computation **6**, 81–95 (2006). [arXiv:quant-ph/0505030](https://arxiv.org/abs/quant-ph/0505030).

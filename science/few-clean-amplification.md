# Amplifying an inverse-polynomial gap without resets

The trace estimator gives a direct circuit transformation from a computation with logarithmically many clean qubits and a known inverse-polynomial acceptance gap to a computation with a fixed constant gap. The transformed computation has one output qubit and no intermediate measurement, initialization, reset, or postselection. Its circuit description is generated deterministically: the Pauli seed is stored in initially maximally mixed qubits.

The threshold assumptions are part of the theorem. The separating acceptance thresholds must be supplied or efficiently computable; knowledge that some separating gap exists is not sufficient to implement a uniform comparison.

## 1. Model and statement

Let $x$ have length $m$. Let $V_x$ be a polynomial-time uniformly generated unitary circuit of size $L(m)$ on $w(m)$ qubits. Its input is

$$
\rho_{\rm in}
=|0^k\rangle\langle0^k|\otimes I_D/d,
\qquad
n=w-k,\quad d=2^n,
\tag{1}
$$

where $k(m)=O(\log m)$ and $w,L$ are polynomially bounded. The original circuit measures one designated output qubit at the end; take outcome zero to mean acceptance. Let $p_x$ be that acceptance probability.

Assume supplied or polynomial-time computable thresholds $c(m),s(m)$, and an efficiently known positive lower bound $\Delta(m)$, satisfy

$$
0\le s<c\le1,\qquad c-s\ge\Delta\ge1/\operatorname{poly}(m),
\tag{2}
$$

with the promise

$$
x\in A_{\rm yes}\Longrightarrow p_x\ge c,
\qquad
x\in A_{\rm no}\Longrightarrow p_x\le s.
\tag{3}
$$

Polynomial-time computability here includes computing the thresholds to the $O(\Delta)$ accuracy used below. Rational thresholds of polynomial bit length are a sufficient special case.

**No-reset amplification theorem.** Under these assumptions, one can deterministically generate a polynomial-size unitary circuit with one final output measurement, completeness at least $2/3$, and soundness at most $1/3$. It uses

$$
k+O(\log(2/\Delta))=O(\log m)
$$

initially clean qubits and

$$
O\!\left((w-k)\log(2/\Delta)+1\right)
$$

initially mixed qubits. Before finite-gate synthesis, it makes $O(1/\Delta)$ uses of $V_x$ and $V_x^\dagger$ in total and has gate count

$$
O\!\left(
\frac{L+n\log(2/\Delta)+k+\log(2/\Delta)}{\Delta}
+\log^2(2/\Delta)
\right).
\tag{4}
$$

A fixed finite gate set adds a polynomial or polylogarithmic compilation overhead as detailed in [robustness](robustness.md); all resources remain polynomial in $m$. The clean count includes the original clean signal register, averaging labels, the phase-estimation clock, the final output, and reversible-comparison workspace. It does not count a purified copy of the mixed target.

The inverse in this statement is available because $V_x$ is a supplied, known unitary circuit: reverse the gate order and invert each gate. The statement is not a reduction from forward-only black-box access to an unknown channel, nor from a circuit with unaccounted intermediate resets.

## 2. Direct Hermitian-block reduction

Let $Q_o=|0\rangle\langle0|_o\otimes I$ be the acceptance projector and put

$$
Z_o=2Q_o-I,\qquad H_x=V_x^\dagger Z_oV_x.
\tag{5}
$$

Then $H_x$ is an exact Hermitian involution. Define

$$
J_k|\psi\rangle=|0^k\rangle|\psi\rangle,
\qquad A_x=J_k^\dagger H_xJ_k.
\tag{6}
$$

The matrix $A_x$ is a Hermitian contraction on the $n$ mixed qubits and has the exact trace identity

$$
\tau_n(A_x)=2p_x-1.
\tag{7}
$$

Indeed,

$$
\tau_n(A_x)
=\operatorname{Tr}\!\left[Z_oV_x\rho_{\rm in}V_x^\dagger\right]
=2\operatorname{Tr}\!\left[Q_oV_x\rho_{\rm in}V_x^\dagger\right]-1.
$$

Thus the original $k$ clean input qubits are exactly the signal register of a block encoding. They need not be purified again or replaced by a pure copy of the $n$-qubit target.

The [Pauli averaging construction](pauli-averaging.md) acts only on the $n$ mixed target qubits. With a label register of size $s_{\rm P}$, it turns (5) into a Hermitian involution whose all-zero $(k+s_{\rm P})$-qubit signal block is

$$
B_G=2^{-s_{\rm P}}\sum_{z\in\{0,1\}^{s_{\rm P}}}
P_z^\dagger A_xP_z.
\tag{8}
$$

There is no need for the extra Hermitianization qubit used for a general non-Hermitian block encoding: $H_x$ is already Hermitian and unitary.

### Controlled calls and original-circuit cost

To apply controlled-$H_x$, apply $V_x$, then controlled-$Z_o$, then $V_x^\dagger$. On the inactive control branch the two circuit calls cancel. This construction uses one forward and one inverse call and does not require a separately supplied controlled-$V_x$ oracle.

Likewise, the known conjugating SELECT and label-basis-change gates need not receive the outer phase-estimation control. Conjugate controlled-$H_x$ by those known gates, and add the controlled reflection about the all-zero signal subspace. A clean comparison-work bit, not yet used for the final comparison, can supply the returned workspace for the linear-size reflection construction [BBC+95, Corollary 7.12]. Each controlled walk use then costs one $V_x$, one $V_x^\dagger$, and $O(ns_{\rm P}+k+s_{\rm P}+1)$ known gates. A quadratic-size reflection without that workspace is also a valid, weaker alternative.

Known circuits are used as unitaries on their entire declared workspace. All qubits that their implementation requires initially pure must already be included in $k$. A description that discards or reinitializes hidden workspace does not satisfy the hypothesis.

## 3. Constant gap from one coherent estimate

Use the real trace estimator with

$$
\eta=\Delta/8,\quad
s_{\rm P}=\left\lceil\log_2(64/\eta^2)\right\rceil,
\quad
M=2^{\lceil\log_2(4\pi/\eta)\rceil},
\quad r=\log_2M.
\tag{9}
$$

The circuit makes $M-1$ controlled walk uses. Its phase clock $Y$ has the associated value

$$
\widehat a(Y)=\cos(2\pi Y/M).
$$

The [mixed-state spectral-sampling proof](trace-estimator.md) gives

$$
\Pr\left[|\widehat a(Y)-(2p_x-1)|\le\Delta/8\right]
\ge p_*:=\frac{15}{2\pi^2}>\frac34.
\tag{10}
$$

The probability is over the seed and the final quantum measurement; the seed is internalized in Section 4. No classical repetition is needed to obtain this fixed constant success probability.

The separating trace threshold is

$$
\theta=c+s-1.
\tag{11}
$$

On yes-instances, $2p_x-1\ge\theta+\Delta$; on no-instances, $2p_x-1\le\theta-\Delta$. Therefore an estimate satisfying (10) can be classified correctly using a threshold within $\Delta/8$ of $\theta$. The extra margin will absorb numerical threshold computation and circuit synthesis.

## 4. A fixed circuit with an internal mixed seed

A classical description of $s_{\rm P}$ independent uniform $n$-qubit Paulis needs $2ns_{\rm P}$ bits. Introduce that many additional initially maximally mixed qubits and denote their computational-basis string by $g$. These qubits are controls only; the circuit never changes their computational-basis values.

For each generator and each target position, one seed bit controls whether an $X$ is used and a second controls whether a $Z$ is used. Together with the corresponding averaging-label bit, these give known doubly controlled $X$ or $Z$ operations. They have constant-size decompositions over Clifford and Toffoli gates, so SELECT still costs $O(ns_{\rm P})$ gates. It need not remain Clifford in this internal-seed implementation.

The product $X^xZ^z$ is a valid representative of a Pauli modulo phase. The averaging and signal block depend on conjugation, so these branchwise phases cancel when SELECT is paired with its actual adjoint. Inverting SELECT requires reversing the ordered gate product; reusing its forward ordering is not generally correct.

For fixed seed $g$, let $C_g$ be the complete estimator circuit, including phase estimation and its final comparison. The single fixed circuit on the seed and computation has the form

$$
C_{\rm all}=\sum_g|g\rangle\langle g|\otimes C_g.
\tag{12}
$$

Consequently, for $N_S=2ns_{\rm P}$,

$$
C_{\rm all}\left(\frac{I_S}{2^{N_S}}\otimes\rho\right)C_{\rm all}^\dagger
=2^{-N_S}\sum_g |g\rangle\langle g|\otimes C_g\rho C_g^\dagger.
\tag{13}
$$

Measuring the designated output qubit therefore reproduces exactly the success probability averaged over the random seed. The seed need not be measured. Equation (13) also explains why the same seed must be retained through every controlled power in phase estimation: resampling a generator at each walk call would define a different operator.

The circuit generator deterministically writes the seed-controlled gates. It neither chooses a random circuit description nor searches for a good seed. Its description has polynomial length despite the exponentially many possible seed values.

This is a different mixed-space ledger from the classical-seed trace theorem. The latter uses $n$ mixed target qubits and external classical random bits. The strictly uniform internal-seed construction uses $n+2ns_{\rm P}$ mixed qubits, in addition to bounded compilation workspace. Both have $O(\log(1/\eta))$ new clean qubits.

## 5. One reversible output comparison

It is unnecessary to compute a real-valued cosine inside the quantum circuit. The predicate $\cos(2\pi y/M)\ge t$ is a union of two integer intervals.

First compute a classical approximation $\widetilde\theta$ satisfying

$$
|\widetilde\theta-\theta|\le\Delta/16.
$$

Since $c-s\ge\Delta$, the exact $\theta$ lies in
$[-1+\Delta,1-\Delta]$. Thus $\widetilde\theta$ is safely in $(-1,1)$. Choose an integer $0\le K\le M/2$ satisfying

$$
\left|K-\frac{M}{2\pi}\arccos(\widetilde\theta)\right|\le1.
$$

A sufficiently accurate classical approximation followed by rounding gives such a $K$ uniformly in polynomial time. Define $t_K=\cos(2\pi K/M)$. Because cosine is 1-Lipschitz and $M\ge32\pi/\Delta$,

$$
|t_K-\theta|
\le2\pi/M+\Delta/16
\le\Delta/8.
\tag{14}
$$

The circuit computes the Boolean function

$$
f_K(y)=\mathbf 1\{y\le K\text{ or }y\ge M-K\}
\tag{15}
$$

into one initially zero output bit. This is implemented with two reversible comparisons to known binary constants, using $O(r)$ reusable clean carry bits and $O(r^2)$ gates conservatively. The phase register is retained; the comparison work is uncomputed. A final $X$ on the output can convert acceptance value one to the outcome-zero convention in (1)–(3).

Equations (10) and (14) imply that the output is correct with probability at least $p_*>3/4$ in the ideal rotation model. Only this one bit is measured. All label, clock, target, and seed registers may be retained to the end and left unmeasured.

The numerical calculation of $K$ takes place in the classical circuit generator, using the supplied threshold data. No clean quantum register storing $c$, $s$, an arccosine, or an unbounded-precision answer is assumed.

## 6. Uniform finite-gate implementation

The original known circuit can be inverted by reversing its finite gate sequence. For the usual Hadamard, $T$, and CNOT gate set, $T^\dagger=T^7$, while Hadamard and CNOT are self-inverse. The seed-control gates and reversible comparisons have exact finite-gate decompositions. The phase-estimation Fourier rotations can be approximated to an allocated inverse-polynomial accuracy by uniform finite-gate synthesis [DN06]. These conventions are compatible with the few-clean-qubit circuit model of [FKM+16, Sections 3.3–3.5].

Allocate total operational/synthesis error at most $1/32$ to the complete first-stage circuit. The hybrid theorem in [robustness](robustness.md) then makes its success probability at least

$$
\frac{15}{2\pi^2}-\frac1{32}>\frac23.
\tag{16}
$$

For a known polynomial-size circuit and inverse-polynomial $\Delta$, this accuracy has a uniform polynomial-size compilation. Unitary uncomputation of carry bits and borrowed workspace is allowed: it is part of the reversible circuit, not a fresh initialization or a reset.

If a supplied approximation to (6) has signal-block error $\epsilon_{\rm BE}$, the same proof tolerates that error by adding it to the trace-estimation error. For example, $\epsilon_{\rm BE}\le\Delta/8$ leaves a positive separation after (10) and (14). For approximate physical executions of $V_x$ and its inverse, use the accumulated per-call error budget; the number of calls is $O(1/\Delta)$. In this direct construction those calls are unconditional, so their ordinary channel diamond errors suffice. The separate controlled-oracle phase convention needed for the arbitrary unitary-trace task is not an additional assumption on this known-circuit reduction.

## 7. An alternative reduction through a unitary trace

The direct Hermitian-block route avoids attenuating the original acceptance gap. For completeness, a reduction using only the unitary-trace theorem is also available.

Let $D=2^w$, $P=|0^k\rangle\langle0^k|\otimes I_d$, and $R=2P-I$. Define the known unitary

$$
W_x=Z_oV_xRV_x^\dagger.
\tag{17}
$$

Because $\operatorname{Tr}Z_o=0$,

$$
\begin{aligned}
\tau_w(W_x)
&=\frac{2}{D}\operatorname{Tr}[Z_oV_xPV_x^\dagger]\\
&=2^{1-k}(2p_x-1).
\end{aligned}
\tag{18}
$$

The trace in (18) is real. The yes/no gap becomes at least $2^{2-k}\Delta$. A trace estimate of precision $\eta_W=2^{-k}\Delta/8$, together with an adequately rounded threshold, is sufficient for a constant-success decision and always lies within the estimator's precision range.

This route uses a fully mixed $w$-qubit target, $O(k+\log(2/\Delta))$ clean estimator qubits, and

$$
O(2^k/\Delta)
$$

calls to the known unitary circuits. Since $k=O(\log m)$, the cost remains polynomial, so it also proves the operational no-reset theorem. Its seed can be internalized with $O(w[k+\log(2/\Delta)])$ mixed bits. The direct route improves the query dependence by avoiding the factor $2^k$.

| Resource or feature | Direct Hermitian block | Attenuated unitary trace |
|---|---|---|
| Matrix whose trace is estimated | $A_x=J_k^\dagger V_x^\dagger Z_oV_xJ_k$ | $W_x=Z_oV_x(2P-I)V_x^\dagger$ |
| Relevant trace | $2p_x-1$ | $2^{1-k}(2p_x-1)$ |
| Target initially mixed | $w-k$ qubits | $w$ qubits |
| Total initial clean qubits | $k+O(\log(2/\Delta))$ | $O(k+\log(2/\Delta))$ |
| Original circuit/inverse calls | $O(1/\Delta)$ | $O(2^k/\Delta)$ |
| Dependence on a generic block extension | Uses the Hermitian-block estimator | Needs only the unitary-trace estimator |

Both reductions require the original unitary circuit or its adjoint, and both keep every intermediate register within one no-reset computation.

## 8. Consequences inherited from constant-gap amplification

After (16), the computation is within the constant-gap, logarithmically many clean qubits model. Fujii et al. prove the following further circuit transformations in that model [FKM+16, Theorems 4 and 5 in the full version].

- With **two initially clean qubits**, the two-sided error can be reduced to $2^{-p(m)}$ for any polynomially bounded $p$, at polynomial overhead.
- With **one initially clean qubit**, one can obtain completeness at least $1-2^{-p(m)}$ and soundness at most $1/p(m)$, or the complementary guarantee with the two error bounds exchanged. These are separately obtainable guarantees; they do not assert exponentially small error on both sides with one clean qubit.

Composing their compiler with the circuit constructed here gives those conclusions for the computable-threshold inverse-gap inputs in (1)–(3). This is a composition of circuit transformations: it does not execute a logarithmic-clean circuit and then replenish clean qubits before a second experiment.

The one- and two-clean final circuits inherit the polynomial overhead of [FKM+16]. The $O(1/\Delta)$ query count proved for the logarithmic-clean first stage is not claimed for those final compilers. These are ideal finite-gate computational-error statements; physical execution errors must additionally satisfy the applicable accumulated-error budget.

The contribution established on this page is the explicit operational transformation with known thresholds, fixed internal mixed randomness, and one terminal output. Historical priority and any equality between differently defined few-clean complexity classes require a separately specified uniform-parameter convention and literature comparison.

## References

- **[BBC+95]** A. Barenco et al., *Elementary gates for quantum computation*, Physical Review A **52**, 3457–3467 (1995). [arXiv:quant-ph/9503016](https://arxiv.org/abs/quant-ph/9503016); [DOI](https://doi.org/10.1103/PhysRevA.52.3457). Corollary 7.12 gives linear size with one returned clean bit; Corollary 7.6 gives the quadratic-size alternative.
- **[FKM+16]** K. Fujii, H. Kobayashi, T. Morimae, H. Nishimura, S. Tamate, and S. Tani, *Power of Quantum Computation with Few Clean Qubits*, ICALP 2016, LIPIcs **55**, 13:1–13:14. [Published paper](https://doi.org/10.4230/LIPIcs.ICALP.2016.13); [full version, arXiv:1509.07276v1](https://arxiv.org/html/1509.07276v1). The full-version Theorems 4 and 5 are the constant-gap amplification results used here; Sections 3.3–3.5 specify the circuit and uniformity conventions.
- **[DN06]** C. M. Dawson and M. A. Nielsen, *The Solovay–Kitaev algorithm*, Quantum Information & Computation **6**, 81–95 (2006). [arXiv:quant-ph/0505030](https://arxiv.org/abs/quant-ph/0505030).

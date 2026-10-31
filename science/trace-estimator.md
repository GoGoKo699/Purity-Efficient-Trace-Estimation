# Trace estimation with a mixed target

The estimator combines [coherent Pauli averaging](pauli-averaging.md) with phase estimation of a qubitized walk. The target remains unpurified: its maximally mixed initialization gives uniform eigenvalue sampling, and averaging makes a sampled eigenvalue close to the normalized trace with constant probability.

All statements use the controlled-oracle, initialization, and elementary-gate conventions in [Model](model.md). The walk construction is a special case of [Low and Chuang, *Hamiltonian Simulation by Qubitization*](https://doi.org/10.22331/q-2019-07-12-163); the mixed-state sampling argument and the resource accounting are given explicitly below.

## 1. Real estimator theorem

Let $V$ be a unitary on $a+n$ qubits, with all-zero $a$-qubit signal block $C$. Let $A=\mathrm{Re}C$, $t=\tau_n(A)$, and $0\lt \eta\leq1/4$. Define

$$
s=\left\lceil\log_2\frac{64}{\eta^2}\right\rceil,
\qquad
M=2^{\left\lceil\log_2(4\pi/\eta)\right\rceil},
\qquad r=\log_2 M,
\qquad b=a+s+1.
$$

**Theorem (real estimator).** For every fixed such $V$, there is an algorithm whose output $\widehat t\in[-1,1]$ satisfies

$$
\Pr\bigl[|\widehat t-t|\leq\eta\bigr]
\geq\frac{15}{2\pi^2}>\frac34.
$$

One run uses:

- $n$ initially maximally mixed target qubits;
- $a+s+r+2$ initially clean qubits;
- exactly $M-1$ supplied controlled $V$ calls and $M-1$ supplied controlled $V^\dagger$ calls;
- $2ns$ independent classical random bits;
- $O((ns+a+s+1)M+r^2)$ known elementary gates.

The run has no intermediate quantum measurement or reset. Its only quantum output is the terminal measurement of the $r$-qubit phase register. Alternatively, the classical seed can be replaced by $2ns$ additional initially mixed qubits, with the same clean-qubit and query counts.

The output is represented exactly by a phase outcome $y$ and the formula $\widehat t=\cos(2\pi y/M)$. Numerical rounding can be allocated additional error as described in [Model](model.md#5-output-convention-and-scope).

## 2. Algorithm

1. Draw $s$ independent uniform Pauli generators and form the known SELECT circuit described in [Pauli averaging](pauli-averaging.md#4-coherent-averaging-circuit).
2. Initialize the $b$ signal qubits, an $r$-qubit phase register, and one temporary control qubit to zero. Initialize the target to $I/2^n$.
3. Form the Hermitian involution $W_G$ with signal block $B_G$ and the walk $Q=RW_G$. The signal embedding and reflection are defined below.

4. Apply standard $M$-point phase estimation of $Q$: Hadamards on the phase register, powers $Q^{2^j}$ controlled by its individual bits, and the inverse Fourier transform. Each power is implemented by repeated controlled walk steps.
5. Measure the phase register, obtaining $y\in\lbrace 0,\ldots,M-1\rbrace$, and return $\cos(2\pi y/M)$.

Here the embedding $\mathcal J|\psi\rangle=|0^b\rangle|\psi\rangle$ defines

$$
\Pi=\mathcal J\mathcal J^\dagger,
\qquad R=2\Pi-I,
\qquad Q=R W_G.
$$

No measurement is made to determine an eigenstate or to project the signal register. In particular, the algorithm does not postselect the all-zero signal subspace after the walk.

## 3. Mixed-state spectral sampling

**Lemma (mixed-state spectral sampling).** Fix a seed $G$. Let $B_G|v_j\rangle=\lambda_j|v_j\rangle$ be an orthonormal eigenbasis, with eigenvalues listed with multiplicity. On initial state $\mathcal J(I/d)\mathcal J^\dagger$, phase estimation of $Q=RW_G$ has the distribution obtained by choosing $j$ uniformly and applying phase estimation to eigenphase $+\arccos\lambda_j$ or $-\arccos\lambda_j$, with equal probabilities when $|\lambda_j|\lt 1$. At $\lambda_j=\pm1$, the two phases coincide modulo $2\pi$. Both phase choices have cosine $\lambda_j$.

**Proof.** Put $|\psi_j\rangle=\mathcal J|v_j\rangle$. Because $\mathcal J^\dagger W_G\mathcal J=B_G$,

$$
\Pi W_G|\psi_j\rangle=\lambda_j|\psi_j\rangle.
$$

For $|\lambda_j|\lt 1$, define

$$
|\phi_j\rangle=
\frac{W_G|\psi_j\rangle-\lambda_j|\psi_j\rangle}
{\sqrt{1-\lambda_j^2}}.
$$

Then $\Pi|\phi_j\rangle=0$, and $|\phi_j\rangle$ is normalized and orthogonal to $|\psi_j\rangle$. Using $W_G^2=I$, with $\mu_j=\sqrt{1-\lambda_j^2}$,

$$
W_G|\psi_j\rangle=\lambda_j|\psi_j\rangle+\mu_j|\phi_j\rangle,
\qquad
W_G|\phi_j\rangle=\mu_j|\psi_j\rangle-\lambda_j|\phi_j\rangle.
$$

Since $R$ acts as $+1$ on $\psi_j$ and $-1$ on $\phi_j$, the matrix of $Q$ in the ordered basis $(\psi_j,\phi_j)$ is

$$
\begin{pmatrix}
\lambda_j&\mu_j\\
-\mu_j&\lambda_j
\end{pmatrix}.
$$

Its orthonormal eigenvectors $(\psi_j\pm i\phi_j)/\sqrt2$ have eigenvalues $\lambda_j\pm i\mu_j$. The vector $\psi_j$ has squared overlap $1/2$ with each. If $|\lambda_j|=1$, norm preservation gives $W_G\psi_j=\lambda_j\psi_j$, hence $Q\psi_j=\lambda_j\psi_j$ directly.

For different indices, the invariant subspaces are orthogonal. In particular, $\langle\psi_i|W_G|\psi_j\rangle=\lambda_j\delta_{ij}$ and $W_G$ is unitary, which give the required zero cross inner products. Finally,

$$
\mathcal J\frac{I}{d}\mathcal J^\dagger
=\frac1d\sum_{j=1}^d|\psi_j\rangle\langle\psi_j|.
$$

Phase estimation leaves orthogonal eigenvectors orthogonal, so tracing out the walk registers removes the cross terms between different eigenphases. Its phase-register distribution is therefore the claimed mixture. $\square$

This is uniform sampling of eigenvectors, equivalently of eigenvalues weighted by multiplicity. It does not assign equal probability to distinct eigenvalue values. No Bell state, pure target state, or reflection about an unknown target eigenvector is used.

## 4. Accuracy and confidence

By the averaging identity and the preceding lemma,

$$
\Pr_{G,j}\left[|\lambda_j-t|>\frac\eta2\right]
\leq\frac{4 2^{-s}}{\eta^2}
\leq\frac1{16}.
$$

For any fixed eigenphase $\theta$, standard $M$-point phase estimation returns $y$ satisfying

$$
\mathrm{dist}_{2\pi}\left(\frac{2\pi y}{M},\theta\right)
\leq\frac{2\pi}{M}
$$

with probability at least $8/\pi^2$. Here $\mathrm{dist}_{2\pi}$ is the shortest circular distance. The bound includes exact grid phases, for which the phase is recovered with probability one. This is [Brassard et al., *Quantum Amplitude Amplification and Estimation*, Theorem 11](https://arxiv.org/abs/quant-ph/0005055).

For completeness, the phase-register amplitude at $y$ is

$$
\frac1M\sum_{k=0}^{M-1}e^{ik(\theta-2\pi y/M)}.
$$

The two adjacent grid points have total probability at least $8/\pi^2$; both are within the stated circular distance. Because cosine is 1-Lipschitz for that distance and $M\geq4\pi/\eta$, good phase estimation implies

$$
\left|\cos\left(\frac{2\pi y}{M}\right)-\lambda_j\right|
\leq\frac\eta2.
$$

The phase-estimation success bound holds conditionally for every seed and every eigenphase. Thus the probability that both spectral concentration and phase estimation succeed is at least

$$
\left(1-\frac1{16}\right)\frac8{\pi^2}
=\frac{15}{2\pi^2}>\frac34.
$$

On that event the triangle inequality gives $|\widehat t-t|\leq\eta$, proving the accuracy assertion. The product bound does not assume independence of the two events; it uses the uniform conditional phase-estimation guarantee.

## 5. Resource proof

### Oracle calls

Binary phase estimation uses

$$
\sum_{j=0}^{r-1}2^j=M-1
$$

controlled walk steps. A controlled $W_G$ uses one supplied controlled $V$ and one supplied controlled $V^\dagger$, by [the explicit control construction](pauli-averaging.md#5-controlling-the-walk-without-a-stronger-oracle). The reflection uses no oracle call. This gives exactly $M-1$ calls of each type, or $2(M-1)$ total. Since

$$
\frac{4\pi}{\eta}\leq M\lt \frac{8\pi}{\eta},
$$

the total is less than $16\pi/\eta$.

### Clean qubits and mixed qubits

The clean register consists of $a$ original signal bits, $s$ coherent label bits, one Hermitianization bit, $r$ phase bits, and one returned temporary bit. Its size is exactly

$$
q=a+s+r+2=a+3\log_2(1/\eta)+O(1).
$$

The phase controls are bits of the phase register; no extra outer-control register is needed. The target has $n$ mixed qubits. An internal mixed seed, if used, adds $2ns$ mixed qubits and no clean ones.

### Known gates and the controlled reflection

Conjugating the controlled central involution by the unconditional $T_G$ and $T_G^\dagger$ costs $O(ns+s)$ known gates per walk step. The temporary oracle-control bit returns to zero before the signal reflection.

It is important to implement the sign of the reflection correctly when it is controlled. For the current phase bit $c$,

$$
\mathrm C_c(R)
=Z_c\left(I-2|1\rangle\langle1|_c\otimes\Pi\right).
$$

The second factor is a phase flip on $c=1$ and all signal bits zero. After $X$ gates on the signal bits, it is a multiply controlled $Z$. Reusing the returned temporary bit, [Barenco et al., Corollary 7.12](https://arxiv.org/abs/quant-ph/9503016) implements it with $O(b+1)$ elementary gates and returns that bit to zero. Concretely, compute the AND of the shifted signal bits into the clean temporary bit, using $c$ as returned borrowed workspace in the linear multi-controlled-NOT construction of their Corollary 7.4. Then apply a controlled $Z$ between the temporary bit and $c$, and uncompute the AND. The borrowed bit is restored before the controlled $Z$, so its entanglement with other registers causes no restriction. The extra $Z_c$ supplies the displayed sign. Dropping it would replace controlled $R$ by controlled $-R$, which shifts the measured phases.

Thus each controlled walk costs $O(ns+a+s+1)$ known gates. Initialization Hadamards and the inverse Fourier transform add $O(r^2+s)$, giving

$$
O\bigl((ns+a+s+1)M+r^2\bigr).
$$

For a unitary input, $a=0$, this becomes

$$
O\left(
\frac{(n+1)\log(1/\eta)}{\eta}
+\log^2(1/\eta)
\right).
$$

An implementation that does not reuse the temporary bit for the reflection can use the ancilla-free $O(b^2)$ construction of Barenco et al., Corollary 7.6, with a correspondingly weaker gate bound. Native rotation synthesis and the cost of executing the supplied controlled oracle are additional costs under [the stated gate convention](model.md#4-known-gate-costs).

## 6. Complex trace theorem and higher confidence

**Theorem (complex trace).** Let $0\lt \epsilon\leq1/4$. For a supplied unitary $U$ on $n$ qubits, controlled $U$ and controlled $U^\dagger$ access suffices to output $\widehat z$ such that

$$
\Pr\bigl[|\widehat z-\tau_n(U)|\leq\epsilon\bigr]
\geq\frac{11}{16}>\frac23,
$$

using $O(1/\epsilon)$ queries, $O(\log(1/\epsilon))$ initially clean qubits, and $O(n)$ mixed target qubits in a strict circuit with no intermediate measurement or reset. The known gate count is $O((n+1)\log(1/\epsilon)/\epsilon+\log^2(1/\epsilon))$. External Pauli seeds use $O(n\log(1/\epsilon))$ classical bits; internalizing them adds that many mixed qubits.

**Construction and constants.** Use the real estimator with $\eta=\epsilon/2$. Perform three independent runs for $V=U$ and three for $V=-iU$. Take the median of the three real estimates in each coordinate and combine them as a complex number. A controlled $-iU$ is obtained from the supplied controlled $U$ by a known phase $-i$ on its control; its inverse is handled similarly. This changes no query count.

A coordinate median fails only if at least two of its three independent real runs fail. With each failure probability at most $1/4$, the median failure probability is at most

$$
3\left(\frac14\right)^2\frac34+
\left(\frac14\right)^3=\frac5{32}.
$$

The union bound over the coordinates gives success at least $1-10/32=11/16$. On success the complex error is at most $\sqrt2\eta=\epsilon/\sqrt2\leq\epsilon$.

For these six runs, the exact total query count is $12(M-1)$, where $M$ is defined using $\eta=\epsilon/2$. A direct strict realization uses six disjoint target registers and six sets of clean registers: $6n$ mixed target qubits and $6(a+s+r+2)$ clean qubits, with $a=0$ for $U$. Each run's measurements can be postponed until every run has finished. The same argument estimates the normalized trace of a general signal block $C$, with its $a$ signal qubits included in each copy.

The finite phase outcomes are exact descriptions of the coordinate estimates. If numerical coordinates are desired, rounding each final coordinate within $\epsilon/8$ still gives total error at most $5\sqrt2\epsilon/8\lt \epsilon$ on the same success event.

### Failure probability $\delta$

For $0\lt \delta\lt 1/2$, use an odd number $R_{\mathrm{rep}}\geq8\ln(2/\delta)$ of independent real runs in each coordinate. A Hoeffding bound gives coordinate-median failure probability at most $e^{-R_{\mathrm{rep}}/8}\leq\delta/2$. The query count is then

$$
O\left(\frac{\log(1/\delta)}{\epsilon}\right).
$$

The direct strict realization counts all $2R_{\mathrm{rep}}$ initial copies: it has $2R_{\mathrm{rep}}(a+s+r+2)$ clean qubits and $2R_{\mathrm{rep}}n$ mixed target qubits, plus any internal seed registers. The constant-confidence theorem is independent of $n$ in its clean-qubit count; this repetition construction does not assert an additive $\log(1/\delta)$ clean-qubit overhead at arbitrary confidence. Reusing hardware between separately initialized experiments preserves the per-run width but involves repeated initialization.

## 7. Scaled and approximate block encodings

For a Hermitian $H$ with an $(\alpha,a,\epsilon_{\mathrm{BE}})$ block encoding $V$, the real estimator returns $\alpha\widehat t$ satisfying

$$
|\alpha\widehat t-\tau_n(H)|
\leq\alpha\eta+\epsilon_{\mathrm{BE}}
$$

with the same success probability. The statement follows from the fixed signal-block bias in [Model](model.md#approximate-signal-block) and does not require accumulating that bias over oracle calls.

For example, if $\epsilon_{\mathrm{BE}}\leq\epsilon/2$ and $\eta=\epsilon/(2\alpha)\leq1/4$, the final error is at most $\epsilon$. The query count is $O(\alpha/\epsilon)$ and the clean count is $a+O(\log(\alpha/\epsilon))$. If the proposed $\eta$ is larger than $1/4$, using $\eta=1/4$ gives the corresponding constant-precision guarantee. Nonunitary execution errors and an imperfectly mixed target are separately analyzed in [Robustness](robustness.md).

## 8. Query lower bound

**Proposition (ordinary precision lower bound).** For $0\lt \epsilon\leq1/4$, any algorithm that estimates $\mathrm{Re}\tau_n(U)$ to additive error $\epsilon$ with probability at least $2/3$ for every unitary $U$ requires at least $1/(12\epsilon)$ controlled forward or inverse queries in the worst case. The algorithm may have arbitrarily many clean qubits. Thus this is a query lower bound, not a purity lower bound.

**Proof.** Consider the two scalar unitaries

$$
U_0=iI,
\qquad
U_1=e^{i(\pi/2+4\epsilon)}I.
$$

Their real normalized traces are $0$ and $-\sin(4\epsilon)$. Since $4\epsilon\leq1\lt \pi/2$,

$$
\sin(4\epsilon)\geq\frac{8\epsilon}{\pi}>2\epsilon.
$$

An estimator meeting the stated accuracy on both inputs therefore distinguishes them with success at least $2/3$, using a threshold between the disjoint accuracy intervals. The resulting output distributions have total variation distance at least $1/3$.

For either a controlled forward query or a controlled inverse query, the operator-norm difference between the two possible gates is

$$
|1-e^{4i\epsilon}|\leq4\epsilon.
$$

The usual query hybrid argument bounds the trace distance of the final states after $T$ queries by $4T\epsilon$. One may purify an arbitrary initial state and defer intermediate measurements for this lower bound; these allowances strengthen the competing model. Interleaving oracle-independent channels does not increase trace distance. A final measurement cannot increase it either. Hence $4T\epsilon\geq1/3$, or $T\geq1/(12\epsilon)$. $\square$

This is the standard precision hybrid argument, originating in quantum query lower-bound methods such as [Bennett et al., *Strengths and Weaknesses of Quantum Computing*](https://arxiv.org/abs/quant-ph/9701001). The inverse-linear precision scaling is also the familiar unconstrained amplitude-estimation scale of [Brassard et al.](https://arxiv.org/abs/quant-ph/0005055). The role of the present upper bound is to attain that query scaling while initializing the target maximally mixed and using only logarithmically many additional clean qubits. No claim that the query endpoint itself is new is needed.

The same lower bound applies to complex trace estimation, since a complex estimate within $\epsilon$ gives a real-part estimate within $\epsilon$. It applies for every target size, including scalar-phase families with no nontrivial target dynamics.

## 9. Finite verification

The accompanying [verification script](../verification/checks.py) checks the exact averaging identity on small Pauli ensembles, full coherent SELECT and walk matrices, branch-phase cancellation, spectral endpoints, mixed-state eigenphase weights, and the phase-estimation distribution. The recorded [results](../verification/results.json) and [reproduction instructions](../verification/README.md) make those checks inspectable. They are diagnostics for implementation and normalization errors; the asymptotic claims follow from the proofs above.

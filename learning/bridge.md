# From Nielsen–Chuang to purity-efficient trace estimation

Suppose a circuit implements an $n$-qubit unitary $U$. A single clean control qubit, together with a target initialized in $I/2^n$, gives an interference experiment whose mean is the normalized trace of $U$. The question here is how to estimate that mean to additive accuracy $\epsilon$ with $O(1/\epsilon)$ controlled oracle calls while the number of initially clean qubits grows only as $O(\log(1/\epsilon))$.

This bridge uses Nielsen and Chuang's *Quantum Computation and Quantum Information*, **10th Anniversary Edition (2010)**, as its sole educational anchor. The [anchor page](anchor.md) identifies the source and section map; the publisher's [official contents](https://assets.cambridge.org/97811070/02173/frontmatter/9781107002173_frontmatter.pdf) verify the section numbers and printed page numbers below. The derivations here connect that background to the project's operator construction. The authoritative assumptions, theorem statements, and full resource proofs are in the [scientific account](../science/README.md); the [milestone map](milestones.md) records the conceptual dependencies.

## 1. The familiar interference experiment

**Source connection:** density operators and reduced states, §§2.4–2.4.3, pp. 98–108; controlled operations, §4.3, p. 177; measurement, §4.4, p. 185.

Prepare a clean control in $|+\rangle=(|0\rangle+|1\rangle)/\sqrt2$ and an independent target in a density operator $\rho$. Applying controlled-$U$ gives the joint state

$$
\frac12
\begin{pmatrix}
\rho&\rho U^\dagger\\
U\rho&U\rho U^\dagger
\end{pmatrix}.
$$

Tracing out the target leaves the control state

$$
\rho_c=\frac12
\begin{pmatrix}
1&z^*\\
z&1
\end{pmatrix},
\qquad z=\operatorname{Tr}(\rho U).
$$

Consequently, measuring $X$ on the control has mean $\operatorname{Re}z$, and measuring $Y$ has mean $\operatorname{Im}z$. An $X$ measurement can be implemented by a Hadamard followed by computational-basis measurement. When the target is maximally mixed,

$$
\rho=I/d,\qquad d=2^n,\qquad
z=\tau_n(U):=\frac{\operatorname{Tr}U}{d}.
$$

This is the normalized-trace experiment underlying the one-clean-qubit model of [Knill and Laflamme](https://arxiv.org/abs/quant-ph/9802037v1). Independent bounded measurement outcomes give an $O(1/\epsilon^2)$ sampling method at constant confidence. Each repetition must have its own initialized registers, or the hardware must be reinitialized between experiments.

The project replaces those independent samples with a coherent spectral experiment. It retains the same normalized quantity: an additive error $\epsilon$ in $\tau_n(U)$ corresponds to an additive error $d\epsilon$ in the unnormalized trace. A dimension-independent bound for normalized trace is therefore not a dimension-independent bound for estimating $\operatorname{Tr}U$ to fixed absolute accuracy.

## 2. What initial purity means

**Source connection:** ensembles and reduced density operators, §§2.4.1 and 2.4.3, pp. 99 and 105; Schmidt decomposition and purifications, §2.5, p. 109.

The maximally mixed state has many ensemble descriptions. In particular, for every orthonormal basis $\{|v_j\rangle\}_{j=1}^d$,

$$
\frac{I}{d}=\frac1d\sum_{j=1}^d|v_j\rangle\langle v_j|.
$$

This identity allows analysis in an unknown operator's eigenbasis. It does not provide the circuit with that basis, with a classical label $j$, or with a reference system recording $j$.

A purification would be a different resource. For example,

$$
|\Phi_d\rangle=\frac1{\sqrt d}\sum_{j=0}^{d-1}|j\rangle_R|j\rangle_S
$$

has reduced state $I_S/d$ and satisfies

$$
\langle\Phi_d|(I_R\otimes U)|\Phi_d\rangle=\tau_n(U).
$$

This offers a familiar pure-state route to the trace problem, but preparing these $n$ Bell pairs from computational-basis states uses $2n$ initially clean qubits and access to the reference $R$. The present model supplies neither that purification nor its preparation circuit. This example identifies a resource cost of that particular route; it is not a lower bound on every possible trace algorithm.

Here a run starts in

$$
|0^q\rangle\langle0^q|\otimes I_S/d,
$$

with all supplied registers independent. The number $q$ counts **initially** clean qubits. Unitary operations may later entangle the registers or change their marginal states. Even a SWAP between a clean qubit and a mixed qubit changes which marginal is pure. The proof does not assume that the target remains maximally mixed throughout the circuit; it propagates the specified initial density operator through the full unitary evolution. The exact convention is in [Model, §1](../science/model.md#1-registers-normalization-and-initialization).

### Notation translation

| Familiar source notation or object | Meaning in this project |
|---|---|
| Density operator $\rho$ and expectation $\operatorname{Tr}(\rho A)$ | The initial target has $\rho=I/2^n$, so its expectation is $\tau_n(A)$. |
| Pauli matrices $\sigma_x,\sigma_y,\sigma_z$ | Written $X,Y,Z$; their tensor products form the Hermitian Pauli basis. |
| Ordinary trace $\operatorname{Tr}A$ | $\tau_n(A)=2^{-n}\operatorname{Tr}A$ includes the normalization. |
| Eigenphase convention $U\lvert u\rangle=e^{2\pi i\varphi}\lvert u\rangle$ | The walk has eigenvalues $e^{i\theta}$, with $\theta=2\pi\varphi$ modulo $2\pi$. |
| Phase-estimation output bits | An $r$-bit integer $y$, with $M=2^r$, represents angle $2\pi y/M$. |
| A reflection in a search or counting circuit | Here $R=2\Pi-I$, where $\Pi$ fixes only the clean signal bits and acts as the identity on the whole target. |

The symbol $U$ denotes the unitary whose trace is sought. The more general input is a unitary $V$ containing a matrix as a signal block. The walk to which phase estimation is applied is a third unitary, $Q$.

## 3. From a matrix block to a Hermitian involution

**Source connection:** tensor products, §2.1.7, p. 71; adjoints and Hermitian operators, §2.1.6, p. 69; controlled operations, §4.3, p. 177. The block-encoding language is a research ingredient, used in the convention of [Gilyén et al.](https://arxiv.org/abs/1806.01838).

A unitary $V$ acting on an $a$-qubit signal register $E$ and an $n$-qubit target $S$ has the signal block

$$
C=(\langle0^a|_E\otimes I_S)V(|0^a\rangle_E\otimes I_S).
$$

The surrounding bras and kets mean a matrix compression: retain the rows and columns with signal label zero. Since $V$ preserves norm, $\|C\|\le1$. The construction does not measure the signal bits and postselect that outcome. It uses the complete unitary $V$, including the other blocks.

The real estimator concerns

$$
A=\operatorname{Re}C=\frac{C+C^\dagger}{2}.
$$

For a unitary trace, take $a=0$ and $V=U$, so $\tau_n(A)=\operatorname{Re}\tau_n(U)$. To treat this potentially non-Hermitian $V$, introduce one clean signal qubit $h$ and form

$$
W(V)=
\begin{pmatrix}
0&V^\dagger\\
V&0
\end{pmatrix}_h.
$$

Direct multiplication gives $W(V)^\dagger=W(V)$ and $W(V)^2=I$. Such a unitary is a **Hermitian involution**. Its compression is

$$
(\langle+|_h\langle0^a|_E\otimes I_S)
W(V)
(|+\rangle_h|0^a\rangle_E\otimes I_S)=A.
$$

The state on $h$ is $|+\rangle$, not $|0\rangle$, in this displayed formula. Hadamard conjugation on $h$ converts it to an all-zero signal convention. This distinction fixes the block that the walk will encode. The full construction is [Pauli averaging, §3](../science/pauli-averaging.md#3-a-hermitian-involution-from-the-input-unitary).

The input capabilities are controlled-$V$ and controlled-$V^\dagger$, each charged as one query. An uncontrolled channel $\rho\mapsto V\rho V^\dagger$ cannot determine the global phase of $V$, although that phase changes its complex trace. Hence controlled access with a fixed phase convention is a substantive assumption. Any initially clean workspace needed inside the supplied oracle must also be counted; see [Model, §2](../science/model.md#2-oracle-access).

## 4. Coherently averaging the observable

**Source connection:** Pauli matrices, §2.1.3, p. 65; commutators and anticommutators, §2.1.9, p. 76; the stabilizer formalism, §10.5.1, p. 454. The relevant connection is Pauli commutation algebra. The randomly selected generators below need not commute, so they are not being asserted to define a stabilizer code.

Expand the Hermitian contraction $A$ in the Pauli basis:

$$
A=\sum_{P\in\{I,X,Y,Z\}^{\otimes n}}a_PP,
\qquad a_P=\tau_n(PA),
\qquad a_I=t:=\tau_n(A).
$$

Pauli orthogonality gives $\sum_Pa_P^2=\tau_n(A^2)\le1$. Draw $s$ independent uniform Pauli strings $G_1,\ldots,G_s$. For a binary label $z=(z_1,\ldots,z_s)$, let

$$
P_z=G_s^{z_s}\cdots G_1^{z_1},
\qquad
B_G=2^{-s}\sum_zP_z^\dagger A P_z.
$$

Every conjugation preserves trace, so $\tau_n(B_G)=t$ for **every** seed. Averaging by one generator sends a Pauli term $P$ to

$$
\frac{P+G_jPG_j}{2}
=\begin{cases}
P,&G_jP=PG_j,\\
0,&G_jP=-PG_j.
\end{cases}
$$

Every nonidentity $P$ commutes with exactly half the possible generators. Its coefficient therefore survives all $s$ independent choices with probability $2^{-s}$. Squaring the Pauli coefficients and using orthogonality yields the exact identity

$$
\mathbb E_G\,\tau_n\bigl((B_G-tI)^2\bigr)
=2^{-s}\bigl(\tau_n(A^2)-t^2\bigr)
\le2^{-s}.
$$

This calculation needs no independence between the survival events for different Pauli terms. A sampled list may contain linearly dependent Pauli labels or anticommuting generators; the draws themselves remain independent. The proof is in [the averaging identity](../science/pauli-averaging.md#2-averaging-identity).

For fixed $G$, let $\lambda_1(G),\ldots,\lambda_d(G)$ list the eigenvalues of $B_G$ with multiplicity. If $J$ is uniform on these $d$ indices, the identity becomes

$$
\mathbb E_{G,J}(\lambda_J(G)-t)^2\le2^{-s},
\qquad
\Pr_{G,J}(|\lambda_J(G)-t|>u)\le\frac{2^{-s}}{u^2}.
$$

Thus a uniformly sampled eigenvalue is usually near the trace. The statement concerns normalized mean square deviation, not the largest eigenvalue deviation. A small spectral subspace may still be far from $t$. The input is fixed before the seed is drawn; neither every seed nor one universal seed is promised to work.

### Where the averaging takes place

Use a clean $s$-qubit label register $L$ and the unitary

$$
S_G=\sum_z|z\rangle\langle z|_L\otimes P_z.
$$

Its circuit applies $G_1$ controlled by the first label bit, then $G_2$ controlled by the second, and so on. Each controlled Pauli string uses $O(n)$ known gates. The total SELECT cost is $O(ns)$, even though the operator formula displays $2^s$ branches.

Define

$$
T_G=S_G(H_L^{\otimes s}\otimes H_h\otimes I_{ES}),
\qquad
W_G=T_G^\dagger(I_L\otimes W(V))T_G.
$$

There are $b=a+s+1$ signal qubits. For

$$
\mathcal J|\psi\rangle=|0^b\rangle|\psi\rangle,
$$

the label Hadamards produce equal branch amplitudes, and compression gives

$$
\mathcal J^\dagger W_G\mathcal J=B_G.
$$

The complete $W_G$ remains a Hermitian involution. The average is encoded in its signal block; it is not implemented by randomly decohering the target or by resetting the label. The exact circuit is in [Pauli averaging, §4](../science/pauli-averaging.md#4-coherent-averaging-circuit).

Ordered Pauli products can acquire phases. Any branchwise phase convention is valid when SELECT is paired with its actual adjoint, because those phases cancel in the conjugation. Reusing the forward SELECT circuit as its inverse is generally invalid when the generators do not commute.

## 5. A walk whose phase reveals an eigenvalue

**Source connection:** phase estimation and its performance, §§5.2–5.2.1, pp. 221–225; quantum counting, §6.3, p. 261. Quantum counting provides the useful geometric connection: a rotation angle encodes an answer. The projected walk below is a qubitization construction in the sense of [Low and Chuang](https://doi.org/10.22331/q-2019-07-12-163).

Let

$$
\Pi=\mathcal J\mathcal J^\dagger
=|0^b\rangle\langle0^b|\otimes I_S,
\qquad R=2\Pi-I,
\qquad Q=RW_G.
$$

The reflection $R$ tests the signal subspace. It is the identity on every target vector within that subspace, whose dimension is $d$; it is not a reflection about a prepared pure target.

To see why $Q$ is useful, fix an eigenvector $B_G|v_j\rangle=\lambda_j|v_j\rangle$ and set $|\psi_j\rangle=\mathcal J|v_j\rangle$. Compression gives

$$
\Pi W_G|\psi_j\rangle=\lambda_j|\psi_j\rangle.
$$

For $|\lambda_j|<1$, define

$$
|\phi_j\rangle=
\frac{W_G|\psi_j\rangle-\lambda_j|\psi_j\rangle}
{\sqrt{1-\lambda_j^2}}.
$$

This is a normalized vector orthogonal to the signal subspace. Since $W_G^2=I$, the span of $\psi_j,\phi_j$ is invariant, and the walk in that ordered basis is

$$
Q\big|_j=
\begin{pmatrix}
\lambda_j&\sqrt{1-\lambda_j^2}\\
-\sqrt{1-\lambda_j^2}&\lambda_j
\end{pmatrix}.
$$

Its eigenphases are $\pm\arccos\lambda_j$. Both have cosine $\lambda_j$, and $\psi_j$ has squared overlap $1/2$ with each eigenvector. At $\lambda_j=1$ or $-1$, the input is already a walk eigenvector with phase $0$ or $\pi$.

Now use the actual mixed initial state:

$$
\mathcal J\frac{I}{d}\mathcal J^\dagger
=\frac1d\sum_j|\psi_j\rangle\langle\psi_j|.
$$

Linearity turns the phase-register outcome distribution into the uniform mixture over $j$. Within each $j$, the two walk eigenvectors stay orthogonal during phase estimation, so tracing out the walk registers removes their cross terms. Operationally, the clock therefore behaves as though an eigenvector index were sampled uniformly and then one of its two eigenphases were estimated. No eigenvector is prepared or identified by the algorithm. Uniform indices mean eigenvalues weighted by multiplicity, not equal weights on the distinct numerical eigenvalues.

The entire argument, including orthogonality between different invariant subspaces, is proved in [mixed-state spectral sampling](../science/trace-estimator.md#3-mixed-state-spectral-sampling). It is the point where the initial density operator replaces a purification in the algorithm.

## 6. A complete one-qubit example

Take $U=Z$, $a=0$, and a target initialized in $I/2$. Then

$$
A=Z,\qquad t=\tau_1(Z)=0.
$$

The eigenvalues $+1$ and $-1$ each occur with probability $1/2$ under mixed-state sampling. Sampling an eigenvalue of $A$ itself would not return its trace. Averaging changes this distribution while preserving the trace.

### One explicit averaging branch

Choose $s=1$ and the particular generator $G_1=X$. Since $XZX=-Z$,

$$
B_X=\frac{Z+XZX}{2}=0.
$$

The generic Hermitianization is $W(U)=X_h\otimes Z_S$. After Hadamard conjugation on $h$, it is $Z_h\otimes Z_S$. SELECT is a CNOT from the label $L$ to $S$. In register order $h,L,S$, the full coherently averaged involution is

$$
W_X=Z_h\otimes X_L\otimes Z_S.
$$

Indeed, CNOT conjugation sends $Z_S$ to $Z_LZ_S$, and the outer label Hadamards send $Z_L$ to $X_L$. Compressing $h,L$ to zero gives the zero matrix, as required.

The signal reflection is

$$
R=2|00\rangle\langle00|_{hL}\otimes I_S-I.
$$

The walk preserves $h=0$. On this sector, $R=Z_L\otimes I_S$, so

$$
Q\big|_{h=0}=Z_LX_L\otimes Z_S=iY_L\otimes Z_S.
$$

If the target computational-basis value is zero, the label evolves under $iY$; if it is one, the label evolves under $-iY$. In either case the label input $|0\rangle$ has equal weights on walk eigenvalues $+i$ and $-i$.

With a two-qubit phase register, $M=4$. These phases are exact grid points, so the only terminal outcomes are

| Phase-register outcome $y$ | Probability | Returned value $\cos(2\pi y/4)$ |
|---|---:|---:|
| $1$ | $1/2$ | $0$ |
| $3$ | $1/2$ | $0$ |

Either outcome returns the exact trace. This is a conditional example with the specified seed and exact grid phases, not the general accuracy theorem's parameter choice. The generic circuit ledger for it is five initially clean qubits—one Hermitianization bit, one label bit, two clock bits, and one returned temporary bit—plus one initially mixed target qubit. Implementing the three controlled walk steps through the generic oracle construction uses three controlled-$Z$ calls and three controlled-$Z^\dagger$ calls. Knowledge that this particular oracle is $Z$ would permit simplifications, but those are unnecessary for the example.

### All random seeds and the theorem's parameters

For one uniformly random generator, $X$ and $Y$ kill the $Z$ coefficient, while $I$ and $Z$ preserve it. For $s$ generators, the coefficient survives exactly when every generator lies in $\{I,Z\}$. Therefore

$$
B_G=\begin{cases}
Z,&\text{with probability }2^{-s},\\
0,&\text{with probability }1-2^{-s}.
\end{cases}
$$

This gives $\mathbb E_G\tau_1(B_G^2)=2^{-s}$, attaining equality in the second-moment bound. If $M$ is divisible by four, all relevant phases are grid points: the output is zero on the scalar-block branches and is $+1$ or $-1$, equally likely, on the surviving branches.

For the actual general-theorem choice $\eta=1/4$,

$$
s=10,\qquad M=64,\qquad r=6.
$$

The exact count is **18 clean qubits, one mixed target qubit, 63 forward queries, and 63 inverse queries**. The external random seed contains 20 classical bits. Internalizing it instead gives 21 initially mixed qubits in total, with the same clean and query counts. For this input, the success probability at error tolerance $1/4$ is exactly $1-2^{-10}=1023/1024$. The general theorem only needs the smaller, input-independent lower bound derived next.

## 7. Accuracy, confidence, and the resource ledger

For a real estimate with $0<\eta\le1/4$, set

$$
s=\left\lceil\log_2\frac{64}{\eta^2}\right\rceil,
\qquad M=2^{\lceil\log_2(4\pi/\eta)\rceil},
\qquad r=\log_2M.
$$

The averaging bound gives

$$
\Pr_{G,J}(|\lambda_J-t|>\eta/2)
\le\frac{4\,2^{-s}}{\eta^2}\le\frac1{16}.
$$

For every fixed eigenphase $\theta$, $M$-point phase estimation returns a grid angle within circular distance $2\pi/M$ with probability at least $8/\pi^2$. The two adjacent grid outcomes give this constant; see [Brassard et al., Theorem 11](https://arxiv.org/abs/quant-ph/0005055). Because cosine is 1-Lipschitz and $M\ge4\pi/\eta$, the corresponding eigenvalue estimate differs from $\lambda_J$ by at most $\eta/2$.

The phase bound holds conditionally on every seed and eigenphase. Multiplying this uniform conditional guarantee by the spectral concentration probability gives

$$
\Pr\bigl[|\cos(2\pi y/M)-t|\le\eta\bigr]
\ge\frac{15}{16}\frac8{\pi^2}
=\frac{15}{2\pi^2}>\frac34.
$$

Independence between the two success events is unnecessary. The conditional guarantee, rather than a union bound, supplies the stated constant.

| Resource for one real run | Exact count or bound |
|---|---|
| Initially clean qubits | $a+s+r+2$: original signal, labels, one Hermitianization bit, clock, and one returned temporary bit |
| Initially mixed target qubits | $n$ |
| External seed | $2ns$ independent classical bits |
| Alternative internal seed | $2ns$ additional initially mixed qubits |
| Controlled forward queries | $M-1$ |
| Controlled inverse queries | $M-1$ |
| Total queries | $2(M-1)<16\pi/\eta$ |
| Known gates | $O((ns+a+s+1)M+r^2)$ |
| Quantum measurement | Terminal measurement of the $r$ clock bits |

Powers are not free queries: phase estimation uses $1+2+\cdots+2^{r-1}=M-1$ controlled walk steps. A controlled walk uses one supplied controlled-$V$ and one controlled-$V^\dagger$. The known conjugating gates $T_G,T_G^\dagger$ can remain unconditional around the controlled central involution; on the inactive branch they cancel. A returned temporary bit reduces the two-control oracle condition to the supplied singly controlled oracle. It can then be reused for the signal reflection. These details establish the count rather than assuming stronger oracle access; see [the control construction](../science/pauli-averaging.md#5-controlling-the-walk-without-a-stronger-oracle).

The sign of a controlled reflection also matters. With phase control $c$,

$$
\mathrm C_c(R)=Z_c\bigl(I-2|1\rangle\langle1|_c\otimes\Pi\bigr).
$$

Omitting $Z_c$ implements controlled-$(-R)$ and shifts the walk phases by $\pi$. The linear-size reflection construction with one returned clean bit is justified by [Barenco et al., Corollary 7.12](https://arxiv.org/abs/quant-ph/9503016), as explained in the [resource proof](../science/trace-estimator.md#5-resource-proof).

The gate convention is arbitrary one-qubit unitaries and CNOTs, corresponding to the elementary circuit setting of Nielsen–Chuang §4.5.2, p. 191. A fixed finite gate set requires synthesis precision and its additional cost (§4.5.3, p. 194). The finite pair $(y,M)$ exactly describes the mathematical output $\cos(2\pi y/M)$; numerical evaluation can take place classically. No clean quantum cosine register is hidden in the count.

### Complex traces and repetitions

For $0<\epsilon\le1/4$, use $\eta=\epsilon/2$ and perform six independent real-estimator runs, with independent initialized registers and fresh independent seeds: three with $V=U$ and three with $V=-iU$. The latter has real trace equal to the imaginary trace of $U$, and its controlled oracle needs only a known phase on the control in addition to the supplied query. Take a median in each coordinate.

Each median fails with probability at most $5/32$, so both coordinates are correct with probability at least $11/16>2/3$. Their combined error is at most $\sqrt2\eta\le\epsilon$. A strict realization without intermediate resets counts all six sets of registers: $6n$ mixed target qubits and $6(s+r+2)$ clean qubits for a unitary input. External seeds preserve the $O(n)$ mixed-width headline; internal seeds add $O(n\log(1/\epsilon))$ mixed qubits.

At failure probability $\delta$, the direct median construction uses $O(\log(1/\delta))$ independent copies. Both query count and initial register counts acquire that multiplicative factor. The arbitrary-confidence result does not promise an additive clean-qubit confidence overhead. These statements and the exact constants are in [the complex trace theorem](../science/trace-estimator.md#6-complex-trace-theorem-and-higher-confidence).

The [query lower bound](../science/trace-estimator.md#8-query-lower-bound) shows that $\Omega(1/\epsilon)$ queries are necessary even with unlimited clean workspace, by distinguishing nearby scalar phases. It therefore establishes optimal precision dependence for queries. It does not prove that logarithmically many clean qubits are necessary, or that one clean qubit attains the same query bound.

## 8. Fixed block error and execution error have different roles

**Source connection:** quantum operations, §8.2, p. 356; trace distance, §9.2.1, p. 403. The channel-distance bound below extends the state-distance reasoning to steps acting on possibly entangled circuit registers.

Suppose the desired Hermitian matrix is $A$, but the signal block obeys $\|C-A\|\le\epsilon_{\mathrm{BE}}$. The exact unitary $V$ still produces the exact Hermitian involution above. Its encoded observable is $\widehat A=(C+C^\dagger)/2$, with

$$
\|\widehat A-A\|\le\epsilon_{\mathrm{BE}},
\qquad
|\tau_n(\widehat A)-\tau_n(A)|\le\epsilon_{\mathrm{BE}}.
$$

The estimator can therefore be analyzed directly on $\widehat A$. A fixed block error contributes once to final additive bias. It does not accumulate once per query. This argument requires a consistent unitary and its matching adjoint; an arbitrary noisy channel cannot be inserted into the involution formula and retain that algebraic property.

For operational errors, use normalized distances

$$
D(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1,
\qquad
d_\diamond(\mathcal E,\mathcal F)
=\tfrac12\|\mathcal E-\mathcal F\|_\diamond.
$$

If the initial **joint** state is within trace distance $\zeta$ of the required product state and step $j$ has channel error at most $\delta_j$, contractivity and a telescoping hybrid give output-distribution distance at most

$$
\mathcal E_{\mathrm{run}}=\zeta+\sum_j\delta_j.
$$

Each channel bound includes its controls and entangled inputs. Consequently,

$$
\Pr\bigl[|\widehat t-\tau_n(A)|\le\eta+\epsilon_{\mathrm{BE}}\bigr]
\ge\frac{15}{2\pi^2}-\mathcal E_{\mathrm{run}}.
$$

For example, $\epsilon_{\mathrm{BE}}\le\epsilon/2$, $\eta=\epsilon/2$, and $\mathcal E_{\mathrm{run}}\le1/32$ suffice for error $\epsilon$ and success greater than $2/3$. With $O(1/\eta)$ queries, a fixed total worst-case budget allows per-query errors of order $\eta$, not a precision-independent constant. An error bound for the uncontrolled channel alone is insufficient for a general controlled-trace oracle.

If only the target preparation differs and $D(\rho,I/d)\le\zeta_T$, every output-event probability changes by at most $\zeta_T$. Its expectation of a Hermitian contraction can shift by at most $2\zeta_T$. The latter mean-bias statement does not replace control of the full success probability. Small marginal preparation errors also do not control unwanted correlations between registers; the initialization hypothesis is joint. The complete bounds, including scaled encodings and finite-gate synthesis, are in [Robustness](../science/robustness.md#3-robust-real-estimator-theorem).

## 9. From an acceptance gap to one final output bit

The same mechanism applies to a known unitary computation whose acceptance probability must be distinguished across a small gap. This consequence uses explicit threshold information and a different role for the original clean register.

Let a polynomial-time uniform, polynomial-size unitary circuit $V_x$ act on $k=O(\log m)$ initially clean qubits and $n$ initially mixed qubits, where $m$ is the input length and the total width is polynomially bounded. It measures one designated output qubit at the end, with outcome zero meaning acceptance and acceptance probability $p_x$. Assume supplied or efficiently computable thresholds $0\le s<c\le1$, together with an efficiently known lower bound

$$
c-s\ge\Delta\ge1/\operatorname{poly}(m).
$$

Yes-instances obey $p_x\ge c$ and no-instances obey $p_x\le s$. The threshold data must be computable to the accuracy used by the circuit generator; a promise that some separating threshold exists is not enough.

Let $Z_o$ assign $+1$ to acceptance and $-1$ to rejection. With $J_k|\psi\rangle=|0^k\rangle|\psi\rangle$, define

$$
H_x=V_x^\dagger Z_oV_x,
\qquad A_x=J_k^\dagger H_xJ_k.
$$

Then $H_x$ is already a Hermitian involution and

$$
\tau_n(A_x)=2p_x-1.
$$

The original $k$ pure input qubits serve as the signal register; the $n$ mixed target qubits stay unpurified. The additional Hermitianization bit is unnecessary. Controlled-$H_x$ is implemented by an unconditional $V_x$, controlled-$Z_o$, and unconditional $V_x^\dagger$. The inverse is available by reversing a known circuit and inverting its gates, rather than by assuming that an unknown forward-only channel can be inverted.

Use estimator precision $\eta=\Delta/8$ and let $s_{\mathrm P}=\lceil\log_2(64/\eta^2)\rceil$ denote the number of Pauli generators, to distinguish it from the soundness threshold $s$. The separating trace threshold is $\theta=c+s-1$, and the promised traces lie at least $\Delta$ on the appropriate side. The coherent phase result can be compared to this threshold without computing a real cosine in a quantum register. The circuit generator chooses an integer $K$ so that

$$
\left|\cos(2\pi K/M)-\theta\right|\le\Delta/8.
$$

Two reversible comparisons then compute

$$
f_K(y)=\mathbf 1\{y\le K\text{ or }y\ge M-K\}
$$

into one output bit. Retaining the clock and uncomputing the comparator's work permits a single terminal output measurement. The exact rounding rule and margin are in [the output comparison](../science/few-clean-amplification.md#5-one-reversible-output-comparison).

### Internal randomness and the no-reset convention

To obtain one deterministically generated circuit, place the $2ns_{\mathrm P}$ Pauli-seed bits in initially maximally mixed qubits and use them only as unchanged computational-basis controls. If $C_g$ denotes the circuit for seed $g$, the full unitary is

$$
C_{\mathrm{all}}=\sum_g|g\rangle\langle g|\otimes C_g.
$$

On a uniform mixed seed, this produces exactly the average of the conditional output distributions. No seed measurement or random circuit generator is needed. The same seed is retained for every walk power; drawing a fresh seed at each query would change the operator whose phase is being estimated. Seed-controlled Pauli gates can include Toffoli-type gates, so this implementation is not asserted to remain Clifford.

The resulting constant-gap circuit uses

$$
k+O(\log(2/\Delta))\quad\text{clean qubits},
\qquad
O(n\log(2/\Delta)+1)\quad\text{mixed qubits},
$$

and $O(1/\Delta)$ total uses of $V_x,V_x^\dagger$. All clean comparison workspace is counted. No new clean qubits, measurements, resets, or postselection occur between initialization and the single output measurement. A total implementation budget of $1/32$ leaves success above $2/3$.

An alternative reduction using only a unitary trace gives the signal $2^{1-k}(2p_x-1)$ and costs $O(2^k/\Delta)$ circuit calls. The direct Hermitian-block route avoids that attenuation. Both reductions and their resource assumptions are proved in [the amplification account](../science/few-clean-amplification.md#1-model-and-statement).

Finally, [Fujii et al., full-version Theorems 4 and 5](https://arxiv.org/html/1509.07276v1) supply further constant-gap circuit transformations. Composing them with this first stage yields two initially clean qubits with exponentially small two-sided computational error, or one initially clean qubit with exponentially small error on one side and inverse-polynomial error on the other. Their polynomial overhead must be retained. The $O(1/\Delta)$ call count of the logarithmic-clean first stage is not asserted for these one- or two-clean final circuits. This is a composition of complete circuit descriptions, with all purity present at the initial time, not a sequence that replenishes pure qubits midway.

## 10. How the proof dependencies fit together

Nielsen–Chuang supplies the density-operator, controlled-circuit, Pauli, Fourier, and phase-estimation background. The additional research ingredients and the project's exact uses are separated as follows.

| Ingredient | Primary research attribution | Canonical project argument |
|---|---|---|
| One-clean normalized-trace interference | [Knill and Laflamme](https://arxiv.org/abs/quant-ph/9802037v1) | [Model and initialization](../science/model.md#1-registers-normalization-and-initialization) |
| Pauli conjugation and approximate-randomization methods | [Ambainis and Smith](https://arxiv.org/abs/quant-ph/0404075) | [Exact second moment for this generator construction](../science/pauli-averaging.md#2-averaging-identity) |
| Block encodings and projected-unitary methods | [Gilyén et al.](https://arxiv.org/abs/1806.01838), [Low and Chuang](https://doi.org/10.22331/q-2019-07-12-163) | [Hermitianization and coherent averaging](../science/pauli-averaging.md#3-a-hermitian-involution-from-the-input-unitary), [mixed spectral proof](../science/trace-estimator.md#3-mixed-state-spectral-sampling) |
| Explicit phase-estimation success constant | [Brassard et al., Theorem 11](https://arxiv.org/abs/quant-ph/0005055) | [Accuracy and confidence](../science/trace-estimator.md#4-accuracy-and-confidence) |
| Controlled-gate decompositions with returned workspace | [Barenco et al., Corollary 7.12](https://arxiv.org/abs/quant-ph/9503016) | [Resource proof](../science/trace-estimator.md#5-resource-proof) |
| Few-clean constant-gap amplification | [Fujii et al., Theorems 4 and 5](https://arxiv.org/html/1509.07276v1) | [Explicit known-threshold reduction and inherited consequences](../science/few-clean-amplification.md#8-consequences-inherited-from-constant-gap-amplification) |

These are scientific attributions and proof dependencies, not additional educational anchors. The [related-work account](../references/related-work.md) places the combined result against earlier trace, spectral-sum, and few-clean-qubit algorithms. The [verification suite](../verification/README.md) checks small exact averaging ensembles, coherent circuits, walk spectra, and phase distributions. Those finite checks diagnose sign, normalization, and implementation errors; the dimension-independent statements rest on the analytical identities and proofs linked above.

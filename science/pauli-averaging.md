# Coherent Pauli averaging

This note proves the operator-averaging identity and its circuit implementation. The relevant concentration is in the normalized Hilbert–Schmidt norm: the estimator will sample an eigenvalue with its normalized multiplicity. No operator-norm approximation to a scalar is required.

The input and gate conventions are in [Model](model.md). The conversion of this averaging identity into a trace estimate is in [Trace estimator](trace-estimator.md).

## 1. Pauli expansion and random generators

Let $A=A^\dagger$ act on $n$ qubits, with $\|A\|\leq1$, and put $t=\tau_n(A)$. The Hermitian Pauli strings

$$
\mathcal P_n=\{I,X,Y,Z\}^{\otimes n}
$$

are orthonormal for the normalized trace inner product. Thus

$$
A=\sum_{P\in\mathcal P_n}a_P P,
\qquad
a_P=\tau_n(PA)\in\mathbb R,
\qquad
\sum_P a_P^2=\tau_n(A^2),
\qquad a_I=t.
$$

Choose $G_1,\ldots,G_s$ independently and uniformly from $\mathcal P_n$. For $z=(z_1,\ldots,z_s)\in\{0,1\}^s$, define the ordered product

$$
P_z=G_s^{z_s}\cdots G_1^{z_1}
$$

and the averaged operator

$$
B_G=2^{-s}\sum_{z\in\{0,1\}^s}P_z^\dagger A P_z.
$$

The product is unitary but need not be Hermitian. This distinction matters for implementing its inverse. Since $B_G$ is an average of unitary conjugations of $A$, it is a Hermitian contraction and

$$
\tau_n(B_G)=t
$$

for every seed $G$, without any probabilistic qualification.

Pauli diagonalization of random conjugations is a standard tool in approximate randomization; see, for example, [Ambainis and Smith, *Small Pseudo-Random Families of Matrices: Derandomizing Approximate Quantum Encryption*](https://arxiv.org/abs/quant-ph/0404075). The exact second-moment identity needed here is proved next.

## 2. Averaging identity

**Lemma (averaging identity).** For every fixed Hermitian contraction $A$ and every integer $s\geq0$,

$$
\mathbb E_G\,\|B_G-tI\|_{2,\tau}^2
=2^{-s}\bigl(\tau_n(A^2)-t^2\bigr)
\leq2^{-s}.
$$

**Proof.** For Hermitian Pauli strings $G,P$, let $\chi_G(P)\in\{+1,-1\}$ satisfy

$$
GPG=\chi_G(P)P.
$$

Repeated conjugation gives

$$
P_z^\dagger P P_z
=\left(\prod_{j=1}^s\chi_{G_j}(P)^{z_j}\right)P.
$$

Consequently,

$$
B_G=\sum_{P\in\mathcal P_n}a_P\,\xi_G(P)P,
\qquad
\xi_G(P)=\prod_{j=1}^s\frac{1+\chi_{G_j}(P)}{2}.
$$

The coefficient $\xi_G(P)$ is either zero or one: a Pauli term survives precisely when it commutes with every selected generator. The identity term always survives. For each fixed nonidentity $P$, exactly half of all Pauli strings commute with $P$ and half anticommute. One way to see the balance is to multiply Pauli labels by a fixed Pauli that anticommutes with $P$; this is a bijection between the two classes. Independence of the $G_j$ gives

$$
\mathbb E_G\xi_G(P)=2^{-s}\qquad(P\neq I).
$$

Orthogonality of the Pauli basis now yields

$$
\begin{aligned}
\mathbb E_G\,\|B_G-tI\|_{2,\tau}^2
&=\sum_{P\neq I}a_P^2\,\mathbb E_G\xi_G(P)^2\\
&=2^{-s}\sum_{P\neq I}a_P^2\\
&=2^{-s}\bigl(\tau_n(A^2)-t^2\bigr).
\end{aligned}
$$

Finally, $\tau_n(A^2)\leq1$. $\square$

The proof does not assume that survival events for different Pauli strings are independent. The generators themselves need not commute. Indeed, their conjugation superoperators commute because Pauli commutation phases cancel under conjugation. There is also no restriction $s\leq2n$: sampled generators may be linearly dependent, and the expectation above remains exact.

### Spectral concentration consequence

For a fixed seed, list the eigenvalues of $B_G$ with multiplicity as $\lambda_1(G),\ldots,\lambda_d(G)$. Let $J$ be a uniform random index in $\{1,\ldots,d\}$, independent of $G$. For any $u>0$,

$$
\Pr_{G,J}\bigl[|\lambda_J(G)-t|>u\bigr]
\leq\frac{2^{-s}}{u^2}.
$$

This follows because the mean squared deviation of this joint sample is exactly the quantity in the lemma. A rare eigenvalue can remain far from $t$; such an eigenvalue is harmless when its normalized multiplicity is sufficiently small. The lemma does not bound $\|B_G-tI\|$ independently of dimension.

## 3. A Hermitian involution from the input unitary

Let $V$ be the supplied unitary with signal block $C$, as in [Model](model.md#2-oracle-access). Introduce a qubit $h$ and define

$$
W(V)=
\begin{pmatrix}
0&V^\dagger\\
V&0
\end{pmatrix}_h
=\operatorname{diag}(V^\dagger,V)_h(X_h\otimes I).
$$

Then $W(V)^\dagger=W(V)$ and $W(V)^2=I$. Its compression to $|+\rangle_h|0^a\rangle_E$ is

$$
(\langle+|_h\langle0^a|_E\otimes I)
W(V)
(|+\rangle_h|0^a\rangle_E\otimes I)
=\operatorname{Re} C=A.
$$

This construction works whether or not $C$ is Hermitian. The input unitary need not already be an involution. One invocation of $W(V)$ can be implemented with one controlled $V$, one controlled $V^\dagger$, and known gates.

## 4. Coherent averaging circuit

Let $L$ be an $s$-qubit label register. Define

$$
S_G=\sum_{z\in\{0,1\}^s}|z\rangle\langle z|_L\otimes P_z,
$$

with identities on $h$ and $E$, and let

$$
T_G=S_G(H_L^{\otimes s}\otimes H_h\otimes I_{ES}),
\qquad
W_G=T_G^\dagger(I_L\otimes W(V))T_G.
$$

The total signal register is $F=LEh$, of size $b=s+a+1$. The order of tensor factors is immaterial when labels identify the registers. Let

$$
\mathcal J|\psi\rangle=|0^b\rangle_F|\psi\rangle_S.
$$

**Lemma (coherent signal block).** The operator $W_G$ is a Hermitian involution, and

$$
\mathcal J^\dagger W_G\mathcal J=B_G.
$$

**Proof.** Unitary conjugation preserves Hermiticity and the involution property. The label Hadamards give an equal superposition of $z$. Since $S_G$ is diagonal in $L$ and the central unitary acts trivially on $L$, compressing $L$ to its initial Hadamard state gives the average of the diagonal branches, with weight $2^{-s}$. Compressing $hE$ gives $A$, so the resulting block is $2^{-s}\sum_zP_z^\dagger A P_z$. $\square$

To apply $S_G$, apply $G_1$ controlled by $z_1$, then $G_2$ controlled by $z_2$, and continue through $G_s$. This realizes the stated right-to-left operator product. Each controlled Pauli string uses $O(n)$ known Clifford gates; the whole circuit has $O(ns)$ gates. Apply the actual inverse circuit for $S_G^\dagger$. There is no enumeration of the $2^s$ branches.

### Branch phases

An ordered Pauli product may acquire a phase in $\{1,-1,i,-i\}$. It is incorrect to infer $P_z^\dagger=P_z$ from the Hermiticity of the individual generators. However, arbitrary branch phases are harmless if the implemented SELECT and its matching adjoint are used.

More explicitly, replacing $S_G$ by $S'_G=D_LS_G$, for any diagonal unitary $D_L$, leaves the central conjugation unchanged:

$$
S_G'^\dagger(I_L\otimes W(V))S'_G
=S_G^\dagger(I_L\otimes W(V))S_G.
$$

Thus a canonical Pauli representative with its own inverse gives the same $W_G$ as an ordered product carrying the corresponding branch phase. The error to avoid is using a forward circuit in place of its adjoint when it is not self-inverse.

## 5. Controlling the walk without a stronger oracle

Let $c$ be a phase-estimation control bit. The identity

$$
\mathrm C_c(W_G)
=T_G^\dagger\,\mathrm C_c(I_L\otimes W(V))\,T_G
$$

allows $T_G$ and its inverse to be applied without the extra control $c$. When $c=0$, they cancel. Thus the Pauli SELECT remains a sequence of singly controlled Clifford gates even inside a controlled walk step.

To implement $\mathrm C_c(W(V))$, use the displayed factorization of $W(V)$. Its $X_h$ becomes a CNOT from $c$ to $h$. The two oracle branches are controlled by $(c=1,h=0)$ and $(c=1,h=1)$. Compute the required two-bit conjunction into one clean temporary qubit, invoke the supplied singly controlled oracle using that qubit, and uncompute it. Negative controls are implemented with $X$ gates. The same temporary qubit is reused for the second branch and returned to zero.

Therefore each controlled $W_G$ uses exactly one supplied $\mathrm C(V)$ call and one supplied $\mathrm C(V^\dagger)$ call, one returned clean temporary bit, and $O(ns+s+1)$ known gates. This is a reduction from the stated singly controlled input gates; a doubly controlled unknown oracle is not assumed free.

## 6. Internalizing the random seed

For a fixed-circuit version, store binary exponents $x_{j\ell},z_{j\ell}$ in $2ns$ initially maximally mixed qubits. On target qubit $\ell$, a generator can be represented by

$$
X^{x_{j\ell}}Z^{z_{j\ell}}.
$$

This differs from the corresponding Hermitian Pauli by a scalar phase only. Each such phase cancels between SELECT and its adjoint, as proved above. Apply $X$ and $Z$ controlled by the appropriate seed bit and label bit. These are known constant-size gates, so SELECT still uses $O(ns)$ elementary gates. The seed bits are used only as unchanged computational-basis controls.

The initial seed is the uniform classical mixture of all binary choices. The whole circuit is block diagonal in that basis, hence its terminal output distribution is exactly the average over the external random seeds. This uses additional mixed workspace but no additional clean qubits, no measurements of the seed, and no reset.

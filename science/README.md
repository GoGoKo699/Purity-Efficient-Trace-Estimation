# Scientific account

The central question is whether normalized trace estimation can attain inverse-linear query precision while keeping the large target register initially maximally mixed. The construction here gives a positive answer with logarithmically many initially clean qubits. Its resource statement separates initial purity, total width, oracle access, coherent depth, and repetition.

For an $n$-qubit unitary $U$, the output approximates

$$
\tau_n(U)=2^{-n}\operatorname{Tr}(U)
$$

to additive error $\epsilon$ with constant success probability. The query cost is $O(1/\epsilon)$, the initial clean width is $O(\log(1/\epsilon))$, and the strict constant-confidence complex estimator uses $O(n)$ mixed target qubits. The result assumes supplied controlled $U$ and controlled $U^\dagger$ gates. Their implementation cost is additional to the explicitly counted known gates.

## 1. Why concentrate a spectrum?

A mixed target gives a uniform mixture over any orthonormal eigenbasis. Phase estimation can therefore sample an eigenvalue, but an eigenvalue of the original operator need not resemble its average. The construction first replaces the operator by a trace-preserving average whose normalized spectral variance is small.

Let $A$ be a Hermitian contraction, $t=\tau_n(A)$, and let $G_1,\ldots,G_s$ be independent uniform Pauli strings. With the ordered product

$$
P_z=G_s^{z_s}\cdots G_1^{z_1},
\qquad
B_G=2^{-s}\sum_{z\in\{0,1\}^s}P_z^\dagger A P_z,
$$

the exact identity is

$$
\mathbb E_G\,\tau_n\!\left[(B_G-tI)^2\right]
=2^{-s}\bigl(\tau_n(A^2)-t^2\bigr).
$$

Every nonidentity Pauli coefficient survives one independent generator with probability one half. Orthogonality of the Pauli basis turns this observation into the identity. The argument does not require commuting generators, independent survival of different coefficients, or a bound on the operator norm of $B_G-tI$.

With $s=2\log_2(1/\epsilon)+O(1)$, a uniformly sampled eigenvalue of $B_G$ is close to $t$ with constant probability, jointly over the seed and the sample. This is precisely the concentration that the mixed initialization makes useful. The guarantee is for every fixed input before the seed is drawn; it is not a guarantee for every seed.

## 2. How the average becomes a circuit

The $2^s$ branches need not be enumerated. An $s$-qubit clean label controls a product of $s$ Pauli strings. This SELECT operation costs $O(ns)$ known gates. Conjugating an appropriate Hermitian involution by SELECT and the label Hadamards produces the averaged signal block.

For a general supplied unitary $V$ with all-zero signal block $C$, one extra qubit forms the Hermitian involution

$$
W(V)=
\begin{pmatrix}
0&V^\dagger\\
V&0
\end{pmatrix}.
$$

Compressing its extra qubit onto $|+\rangle$ and the original signal register onto $|0^a\rangle$ gives $\operatorname{Re}C$. A Hadamard on the extra qubit converts this to the all-zero signal convention. The averaged involution $W_G$ has signal block $B_G$. Reflecting about the clean signal subspace gives a walk

$$
Q=(2\Pi-I)W_G.
$$

On the two-dimensional space associated with an eigenvalue $\lambda$ of $B_G$, this walk has phases $\pm\arccos\lambda$. Both have cosine $\lambda$. The initially mixed target supplies the uniform spectral weights, and the logarithmic phase register estimates the phase with $O(1/\epsilon)$ controlled walk uses.

The [Pauli averaging page](pauli-averaging.md) proves the circuit and control identities. It explicitly handles anticommuting products and branch phases: SELECT must be paired with its actual adjoint. The [estimator page](trace-estimator.md) proves spectral sampling, the constants in the success guarantee, and every resource count.

## 3. What the theorem counts

For a real estimate, the clean bits are the supplied encoding's $a$ signal bits, the $s$ averaging labels, one Hermitianization bit, the $r$ phase bits, and one returned temporary bit. The exact count is $a+s+r+2$. No target purification is supplied. The controlled reflection reuses the temporary bit and has linear known-gate cost in the signal width.

External random seeds cost $2ns$ classical bits. A deterministic circuit description can instead store the seed in that many additional initially mixed bits, retained as controls for the entire coherent experiment. This changes mixed width without changing initial clean width or query count.

Constantly many independent copies estimate the real and imaginary coordinates and raise success above $2/3$. At arbitrary failure probability $\delta$, the direct repetition construction uses $O(\epsilon^{-1}\log(1/\delta))$ queries and multiplies the initialized register counts by $O(\log(1/\delta))$. Reinitializing a device between experiments is a separate convention.

The [model](model.md) states the full access and initialization assumptions. The known-gate bound uses arbitrary one-qubit gates and CNOT; a fixed gate set adds the explicitly budgeted synthesis overhead.

## 4. Error and a computational consequence

A fixed approximate block encoding changes the trace being estimated by its normalized signal bias. That bias is counted once. Execution errors can alter the output distribution at every query; their worst-case bound is the sum of the normalized diamond errors plus the initial-state error. For a general trace oracle, the error bound must concern the controlled channel, since an uncontrolled channel does not determine the unitary's global phase. [Robustness](robustness.md) gives the complete theorem.

There is also an operational amplification consequence. For a known unitary circuit $V_x$ whose input has $k$ clean qubits, the Hermitian involution

$$
H_x=V_x^\dagger Z_{\mathrm{out}}V_x
$$

has a clean-zero signal block $A_x$ satisfying $\tau(A_x)=2p_x-1$, where $p_x$ is the original acceptance probability. Estimating this trace turns a known inverse-polynomial gap $\Delta$ into a fixed constant gap using $k+O(\log(2/\Delta))$ clean qubits and $O(1/\Delta)$ circuit/inverse calls. The seed can be internalized and the phase result compared reversibly with a known threshold, leaving one terminal output bit.

The [amplification proof](few-clean-amplification.md) makes threshold computability and finite-gate uniformity explicit. It also separates this first-stage query bound from the polynomial overhead of the established one- and two-clean-qubit compilers that can be applied afterward.

## 5. Proof and evidence map

| Page | Role in the argument |
|---|---|
| [Model](model.md) | Declares the input, initial state, access, randomness, and cost conventions |
| [Pauli averaging](pauli-averaging.md) | Proves the exact variance identity and efficient coherent signal block |
| [Trace estimator](trace-estimator.md) | Proves spectral sampling, precision, confidence, resource bounds, and the standard query converse |
| [Robustness](robustness.md) | Separates fixed signal bias, initialization error, controlled execution error, and synthesis |
| [Few-clean amplification](few-clean-amplification.md) | Gives the known-gap, one-output, no-reset circuit transformation |
| [Related work](../references/related-work.md) | Compares the actual access, purity, repetition, and precision conventions with primary sources |
| [Verification](../verification/README.md) | Reproduces finite algebraic and coherent-circuit checks |

The contribution is the simultaneous purity and query upper bound and its explicit implementation. The inverse-linear query endpoint and the circuit ingredients have prior origins, credited in the source comparison. The query lower bound does not establish optimal initial purity. The finite checks help detect errors in the construction; they do not substitute for the proofs or certify an exhaustive priority claim.

# Model and resource conventions

The task is to estimate a normalized trace with a target register initialized maximally mixed. The resource claim concerns the simultaneous use of $O(1/\epsilon)$ controlled oracle calls and $O(\log(1/\epsilon))$ initially clean qubits. The target dimension contributes mixed qubits and known gates, but does not contribute clean qubits unless the supplied oracle itself requires them.

The averaging construction is proved in [Pauli averaging](pauli-averaging.md). Its estimator and complete query and qubit counts appear in [Trace estimator](trace-estimator.md).

## 1. Registers, normalization, and initialization

Let $\mathcal H_S=(\mathbb C^2)^{\otimes n}$ and $d=2^n$. For an operator on $S$, write

$$
\tau_n(A)=\frac{\mathrm{Tr}(A)}{2^n},
\qquad
\Vert A\Vert _{2,\tau}^2=\tau_n(A^\dagger A).
$$

The norm $\Vert A\Vert$ without a subscript is the operator norm. A Hermitian contraction satisfies $A=A^\dagger$ and $\Vert A\Vert \leq 1$.

A **clean qubit** is initialized in $|0\rangle$. A register of **maximally mixed qubits** is initialized in the identity state divided by its dimension. All initially supplied registers are independent. A run with $q$ clean qubits and an $n$-qubit target begins in

$$
|0^q\rangle\langle0^q|\otimes\frac{I_S}{d}.
$$

The algorithm has no access to a purification of $I_S/d$. Registers may become entangled during the computation; the initialization convention is the resource being counted. The estimator does not require any intermediate measurement, postselection, reset, or supply of new clean qubits during a run. At the end, its phase register is measured and a classical function of the outcome is returned.

Independent repetitions can be performed on separate copies of these registers, with every measurement postponed to the end. This gives a strict, single initialized circuit with no reset. The cost of all copies is counted in that convention. If a device is instead reinitialized between experiments, the same register hardware can be reused; that is a different accounting of initialization and is labeled explicitly.

This resource distinction follows the few-clean-qubit circuit setting, where the number of initially pure qubits is separated from total width. See [Fujii et al., *Power of Quantum Computation with Few Clean Qubits*](https://arxiv.org/abs/1509.07276).

## 2. Oracle access

### Exact signal block

Let $V$ be an exact unitary on an $a$-qubit signal register $E$ and the target $S$. Its all-zero signal block is

$$
C=(\langle0^a|_E\otimes I_S)V(|0^a\rangle_E\otimes I_S).
$$

Consequently $\Vert C\Vert \leq 1$. The real estimator applies to the Hermitian contraction

$$
A=\mathrm{Re} C=\frac{C+C^\dagger}{2}.
$$

For an exact block encoding of a Hermitian contraction, $C=A$. For the unitary trace task, $a=0$, $V=U$, and the desired real quantity is $\tau_n(\mathrm{Re}U)=\mathrm{Re}\tau_n(U)$. Applying the same algorithm to $-iV$ gives $\mathrm{Im}\tau_n(C)$.

The supplied query gates are

$$
\mathrm C(V)=|0\rangle\langle0|\otimes I+
|1\rangle\langle1|\otimes V
$$

and $\mathrm C(V^\dagger)$, with their relative phases fixed by this definition. Each application costs one query. We report forward and inverse counts separately as well as their sum. A controlled power is implemented by repeated controlled calls; powers are not available at unit cost. The block-encoding convention is the standard one used in [Gilyén et al., *Quantum Singular Value Transformation and Beyond*](https://arxiv.org/abs/1806.01838).

Controlled access is an input capability. The construction does not infer it from a black box that only implements the channel $\rho\mapsto V\rho V^\dagger$. Such a channel does not reveal the global phase of $V$, whereas its normalized complex trace depends on that phase. If $V$ is given as a known circuit, the cost of constructing and executing a controlled version belongs to the input-oracle implementation cost.

Any clean workspace required *inside* an implementation of $V$ or its controlled form must be included in the oracle's clean workspace or charged separately. A unit-cost oracle convention does not make that physical workspace free.

### Approximate signal block

For a Hermitian target operator $H$, suppose $V$ is an $(\alpha,a,\epsilon_{\mathrm{BE}})$ block encoding in the convention

$$
\Vert H-\alpha C\Vert \leq\epsilon_{\mathrm{BE}},
\qquad \alpha>0.
$$

Hermitianization is contractive in operator norm, so

$$
\Vert H-\alpha\mathrm{Re}C\Vert 
\leq\epsilon_{\mathrm{BE}}.
$$

Estimating $\tau_n(\mathrm{Re}C)$ to accuracy $\eta$ and multiplying by $\alpha$ therefore gives an estimate of $\tau_n(H)$ with error at most

$$
\alpha\eta+\epsilon_{\mathrm{BE}}.
$$

This is a fixed input bias. It does not accumulate once per use of the same exact unitary $V$. Approximation or noise in the *execution* of each query is a distinct issue; see [Robustness](robustness.md).

## 3. Randomness and quantifiers

The input operator is fixed before the random seed is drawn. For a given integer $s$, the algorithm chooses independent uniformly random Hermitian Pauli strings

$$
G_1,\ldots,G_s\in\lbrace I,X,Y,Z\rbrace ^{\otimes n}.
$$

The seed uses $2ns$ classical random bits. It can be sampled and translated into the known part of the circuit in time $O(ns)$. There is no list of all $2^s$ Pauli products, no quantum random-access memory assumption, and no arbitrary state-loading operation.

The probability statement has the form

$$
\text{for every fixed admissible }V,\qquad
\Pr_{G, \mathrm{measurement}}
\bigl[|\widehat t-\mathrm{Re}\tau_n(C)|\leq\eta\bigr]
\geq p_0.
$$

It is an average over the chosen seed and the terminal quantum measurement. It does not assert that every seed works, that one seed works for every oracle, or that the oracle may be selected after observing the seed. Different repetitions use independent seeds and independent initialized registers.

### A fixed circuit with a mixed seed register

Classical randomness is optional. The same output distribution is obtained by storing the $2ns$ seed bits in an initially maximally mixed register and preserving their computational-basis values as controls throughout the circuit. The implemented unitary is block diagonal in the seed. Discarding the seed at the end averages the same conditional experiments.

With this convention, a real run uses $n+2ns$ mixed qubits instead of $n$ mixed qubits and external classical random bits. It uses the same number of clean qubits and oracle calls. The known circuit is polynomially uniform: each Pauli factor can be represented by its binary $X$ and $Z$ exponents, and its application uses constant-size controlled known gates. The proof and the treatment of branch phases appear in [Pauli averaging](pauli-averaging.md#6-internalizing-the-random-seed).

## 4. Known gate costs

The exact gate ledger counts arbitrary one-qubit unitaries and CNOT gates. Toffoli, controlled Pauli gates, and controlled one-qubit phases have constant cost in this convention. An $r$-qubit quantum Fourier transform has $O(r^2)$ such gates. Classical arithmetic used to describe or evaluate the output is reported separately from quantum gates.

The controlled signal reflection acts on the signal register and the current phase-estimation control bit. It can reuse the one clean temporary bit already allocated for controlling the oracle. [Barenco et al., *Elementary Gates for Quantum Computation*, Corollary 7.12](https://arxiv.org/abs/quant-ph/9503016) gives an exact linear-size implementation of a multiply controlled one-qubit gate with one returned clean workspace bit. Corollary 7.6 gives a quadratic-size implementation without any additional workspace. We use the former bound and count the temporary bit.

The exact elementary-gate count is not an exact finite-gate-set claim. A fixed universal gate set requires approximation of the non-native rotations, together with a total error budget. This changes gate counts by the chosen synthesis overhead and leaves the query count unchanged. A clean ancilla used by a chosen synthesis method must also be counted. The logical resource theorem can use ancilla-free one-qubit synthesis; operational error budgets are treated in [Robustness](robustness.md).

If implementing one supplied controlled oracle costs $g_V$ native gates, the physical gate count includes the corresponding number of oracle implementations in addition to the known gates stated here. An oracle-query improvement alone is not a claim of a runtime advantage for every circuit family.

## 5. Output convention and scope

A phase-estimation outcome $y\in\lbrace 0,\ldots,M-1\rbrace$ represents the real number $\cos(2\pi y/M)$. The pair $(y,M)$ is a finite exact description of that number. Numerical evaluation to additional accuracy $\eta_{\mathrm{out}}$ adds at most $\eta_{\mathrm{out}}$ to the stated error and can be performed classically with polynomial cost in $\log M$ and $\log(1/\eta_{\mathrm{out}})$. No pure quantum arithmetic register is needed when the desired output is a classical estimate.

The main result is a clean-qubit **upper bound** together with optimal dependence of the query count on additive precision. The scalar-phase lower bound in [Trace estimator](trace-estimator.md#8-query-lower-bound) proves only a query lower bound. It places no nontrivial lower bound on the number of clean qubits.

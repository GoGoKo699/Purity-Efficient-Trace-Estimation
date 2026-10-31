# Thirty milestones for purity-efficient trace estimation

This map follows the scientific question: how can a normalized trace be estimated with inverse-linear query precision when the large target register is initialized maximally mixed? It contains exactly **30 project-defined milestones**, organized by the project's conceptual dependencies.

The sole educational anchor is Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, **10th Anniversary Edition (2010)**, abbreviated **NC** below. Section numbers are checked against the [publisher's official contents](https://assets.cambridge.org/97811070/02173/frontmatter/9781107002173_frontmatter.pdf). The [anchor guide](anchor.md) identifies the selected material, and the [source-to-project bridge](bridge.md) explains the additions needed for this result. An NC pointer identifies foundations; the accompanying project pointer identifies the authoritative definition, construction, or proof. Modern block encodings, qubitization, the exact averaging identity, and the few-clean-qubit consequences are supplied by the project and its credited research sources.

## Allocation and route

| Phase | Milestones | Progression |
|---|---|---|
| Background/preliminaries | M01–M12 | Registers and operators become a framework for mixed-state measurements, coherent spectral estimation, and explicit resource and error accounting. |
| Narrative/innovation | M13–M30 | A local Pauli cancellation rule becomes an averaged signal block, a complete estimator, and a uniform circuit transformation with a known acceptance gap. |

The **12/18 allocation** reflects this project's structure. Its prerequisites come from a connected part of quantum information and circuit theory, while the main work lies in assembling those tools under a restricted initialization model. Eighteen narrative milestones leave room for the mathematical mechanism, the circuit implementation, confidence and error costs, and the computational consequence. M12 integrates the background into the exact problem contract; M30 integrates the complete contribution and its limits. Specialist derivations remain in the linked scientific sources.

## Phase I: Background and preliminaries

### M01. Registers and independent preparation

**Central question:** What information is specified by a register's size and its initial state?

**Understanding target:** Relate an $n$-qubit register to dimension $2^n$, distinguish a register from a particular state in it, and interpret the independent product preparation of clean ancillary qubits and a maximally mixed target.

**Dependencies and story role:** No earlier milestone is required. This establishes the physical and mathematical objects that every later resource statement counts.

**Conceptual connection:** Tensor products describe both the total workspace and the independence assumed at initialization; the number of target qubits alone does not determine how much initial purity is supplied.

**Source pointers:** NC §§1.2.1, 2.1.7, 2.2.8; [Model §1, Registers, normalization, and initialization](../science/model.md#1-registers-normalization-and-initialization).

### M02. Operators, spectra, and adjoints

**Central question:** How do unitary, Hermitian, and contractive operators play different roles?

**Understanding target:** Distinguish reversible evolution from a Hermitian signal matrix, read eigenvalues and adjoints, and recognize that a Hermitian involution is both unitary and Hermitian while a Hermitian contraction may have any eigenvalue in $[-1,1]$.

**Dependencies and story role:** Uses M01. It supplies the operator vocabulary needed to represent a desired quantity inside a larger reversible circuit.

**Conceptual connection:** The project turns a general unitary oracle into an involution, then reads a Hermitian contraction from a specified signal block.

**Source pointers:** NC §§2.1.2, 2.1.5–2.1.6, 2.2.2; [Model §2, Oracle access](../science/model.md#2-oracle-access); [Pauli averaging §3, A Hermitian involution from the input unitary](../science/pauli-averaging.md#3-a-hermitian-involution-from-the-input-unitary).

### M03. Mixed states and unavailable purifications

**Central question:** Why is access to a maximally mixed register different from access to a purification of it?

**Understanding target:** Interpret $I/2^n$ as the same uniform mixture in every orthonormal basis, distinguish a reduced state from a joint pure state, and explain why an inaccessible purifying register cannot be used as workspace. Initial mixing does not require the target to remain maximally mixed during execution.

**Dependencies and story role:** Uses M01–M02. This makes the project's initialization restriction precise before considering algorithms that exploit it.

**Conceptual connection:** The estimator gains uniform spectral weights from mixed initialization while avoiding the resource assumption of an available Bell purification.

**Source pointers:** NC §§2.4.1–2.4.3, 2.5; [Model §1, Registers, normalization, and initialization](../science/model.md#1-registers-normalization-and-initialization); [Trace estimator §3, Mixed-state spectral sampling](../science/trace-estimator.md#3-mixed-state-spectral-sampling).

### M04. Measurements, expectations, and normalized traces

**Central question:** When does an observable's expectation equal the average of all its eigenvalues?

**Understanding target:** Connect measurement probabilities to $\mathrm{Tr}(\rho A)$ and recognize $\tau_n(A)=2^{-n}\mathrm{Tr}(A)$ as the expectation in $I/2^n$. Eigenvalues contribute according to their multiplicities; a single spectral outcome need not be close to this average.

**Dependencies and story role:** Uses M02–M03. It connects the physical measurement setting to the numerical task.

**Conceptual connection:** The gap between sampling an eigenvalue and estimating its average is the problem that coherent Pauli averaging will address.

**Source pointers:** NC §§2.2.3, 2.2.5, 2.4.2; [Scientific account §1, Why concentrate a spectrum?](../science/README.md#1-why-concentrate-a-spectrum); [Model §1, Registers, normalization, and initialization](../science/model.md#1-registers-normalization-and-initialization).

### M05. Pauli strings as operator coordinates

**Central question:** How can Pauli strings expose structure in an arbitrary many-qubit operator?

**Understanding target:** View tensor products of $I,X,Y,Z$ as an orthogonal operator basis, interpret the normalized coefficients $\tau_n(PA)$, and distinguish a Pauli commutation sign from an overall phase of a Pauli product.

**Dependencies and story role:** Uses M02 and M04. It supplies coordinates in which the project's averaging map becomes simple.

**Conceptual connection:** Orthogonality turns squared coefficients into normalized Hilbert–Schmidt variance, while commutation signs determine which coefficients survive conjugation.

**Source pointers:** NC §§2.1.3, 2.1.4, 2.1.7, 2.1.9; [Pauli averaging §1, Pauli expansion and random generators](../science/pauli-averaging.md#1-pauli-expansion-and-random-generators).

### M06. Coherent control, relative phase, and reversal

**Central question:** What additional capability does a controlled unitary supply?

**Understanding target:** Explain how a unitary's otherwise global phase becomes a relative phase under coherent control, distinguish supplied controlled access from an uncontrolled channel, and identify the matching inverse of an ordered circuit. Reversible uncomputation is distinct from resetting a register.

**Dependencies and story role:** Uses M01–M03. It establishes the access assumptions that must survive every circuit transformation.

**Conceptual connection:** General trace estimation requires controlled forward and inverse oracle gates; the project implements additional controls with known gates and counted temporary workspace.

**Source pointers:** NC §§2.1.6, 2.2.7, 4.3–4.4; [Model §2, Oracle access](../science/model.md#2-oracle-access); [Pauli averaging §5, Controlling the walk without a stronger oracle](../science/pauli-averaging.md#5-controlling-the-walk-without-a-stronger-oracle).

### M07. Projectors and the geometry of reflections

**Central question:** How can reflections convert an overlap into a rotation?

**Understanding target:** Interpret a subspace projector $\Pi$ and its reflection $2\Pi-I$, and connect products of reflections with invariant two-dimensional spaces and rotation angles.

**Dependencies and story role:** Uses M02, M04, and M06. It supplies the geometric language for the walk used later in the estimator.

**Conceptual connection:** Quantum search provides the foundational geometry. The project's proof applies related geometry to a clean signal subspace and a Hermitian involution, with no reflection about a purified target state.

**Source pointers:** NC §§2.2.5, 6.1.2–6.1.3; [Trace estimator §2, Algorithm](../science/trace-estimator.md#2-algorithm); [Trace estimator §3, Mixed-state spectral sampling](../science/trace-estimator.md#3-mixed-state-spectral-sampling).

### M08. Phase estimation and its actual cost

**Central question:** How does a short phase register resolve a small eigenphase difference?

**Understanding target:** Connect the Fourier transform, controlled powers, and a terminal phase outcome; distinguish $r=\log_2 M$ phase qubits from the $M-1$ controlled walk calls needed to implement the powers. A power of an oracle is not a free query.

**Dependencies and story role:** Uses M06–M07. This introduces the spectral measurement primitive without yet assuming that its sampled eigenvalue estimates a trace.

**Conceptual connection:** Phase resolution scales inversely with coherent evolution length, while the storage needed to record a phase scales logarithmically.

**Source pointers:** NC §§5.1–5.2.1, 6.3; [Trace estimator §4, Accuracy and confidence](../science/trace-estimator.md#4-accuracy-and-confidence); [Trace estimator §5, Resource proof](../science/trace-estimator.md#5-resource-proof).

### M09. Variance, conditional success, and repetition

**Central question:** Which probability statement is sufficient for a reliable estimate?

**Understanding target:** Distinguish an ensemble average, an individual outcome, and a worst-case deviation; connect a mean-square bound to a tail bound; and combine a conditional success guarantee with a separate concentration event. Independent repetitions have explicit confidence and initialization costs.

**Dependencies and story role:** Uses M03–M04 and M08. It joins the probabilistic meaning of mixed states to the statistical guarantees of an algorithm.

**Conceptual connection:** The proof averages over both a Pauli seed and a spectral sample. Its phase-estimation bound is uniform conditional on the sampled phase, so an unjustified independence assumption is unnecessary.

**Source pointers:** NC Appendix 1, p. 608, and §5.2.1; [Pauli averaging, Spectral concentration consequence](../science/pauli-averaging.md#spectral-concentration-consequence); [Trace estimator §4, Accuracy and confidence](../science/trace-estimator.md#4-accuracy-and-confidence).

### M10. Separate computational resources

**Central question:** What does a query advantage say about purity, width, gates, and repetition?

**Understanding target:** Read separate ledgers for initially clean qubits, initially mixed qubits, external randomness, oracle calls, known gates, and independent copies. Distinguish the width of one run from all registers initialized in a strict computation without resets.

**Dependencies and story role:** Uses M01, M06, and M08–M09. It places the earlier circuit primitives inside the resource question the project asks.

**Conceptual connection:** A dimension-independent clean-qubit bound can coexist with target width and known gate costs that grow with $n$; a query bound alone does not establish a hardware runtime advantage.

**Source pointers:** NC §§3.2.1, 4.5.5, 6.1.1; [Model §1, Registers, normalization, and initialization](../science/model.md#1-registers-normalization-and-initialization); [Model §4, Known gate costs](../science/model.md#4-known-gate-costs).

### M11. Operational error and finite gates

**Central question:** How does an ideal circuit statement become a statement about an approximate implementation?

**Understanding target:** Distinguish a changed target quantity from a changed output distribution, understand trace distance as an operational error measure, and recognize that approximating gates requires an accumulated error budget. A channel bound must cover the controls and any retained memory used by the computation.

**Dependencies and story role:** Uses M03, M06, and M10. It equips the resource framework with the error distinctions needed for realistic implementation.

**Conceptual connection:** NC supplies quantum operations, state distance, and gate synthesis foundations; the project's normalized diamond-distance budget and fixed-block analysis provide the precise extension.

**Source pointers:** NC §§8.2.1–8.2.3, 9.2.1, 4.5.3, and Appendix 3, p. 617; [Robustness §2, Hybrid bound for an imperfect execution](../science/robustness.md#2-hybrid-bound-for-an-imperfect-execution); [Robustness §5, Known-gate synthesis and preservation of the model](../science/robustness.md#5-known-gate-synthesis-and-preservation-of-the-model).

### M12. The complete trace-estimation contract

**Central question:** What exactly is given, what must be returned, and what resource improvement is sought?

**Understanding target:** Integrate the background into the problem: an initially maximally mixed $n$-qubit target, a supplied unitary with $a$ clean signal bits, controlled forward and matching inverse access, and an additive normalized-trace estimate with specified success probability. Interpret a block encoding as a specified matrix block, with its access and normalization explicitly charged.

**Dependencies and story role:** Uses M04–M11. This is the background synthesis and the starting contract for the narrative phase.

**Conceptual connection:** The scientific question is simultaneous query precision and low initial purity. It is neither a free state-loading task nor an assertion that logarithmic purity is necessary.

**Source pointers:** NC §§2.4.2–2.5, 3.2.1, 4.3, 5.2.1; [Model §2, Oracle access](../science/model.md#2-oracle-access); [Model §3, Randomness and quantifiers](../science/model.md#3-randomness-and-quantifiers); [Scientific account §3, What the theorem counts](../science/README.md#3-what-the-theorem-counts).

## Phase II: Narrative and innovation

### M13. One Pauli average removes selected components

**Central question:** What happens to an operator when it is averaged with one Pauli conjugate?

**Understanding target:** Explain why averaging $A$ and $GAG$ preserves the terms commuting with $G$, cancels the anticommuting terms, and preserves the normalized trace.

**Dependencies and story role:** Uses M05, M09, and M12. This is the smallest mechanism from which the project's concentration argument is built.

**Conceptual connection:** A general operator transformation becomes a binary selection rule in Pauli coordinates. The rule concerns an averaged operator; its coherent implementation is developed separately.

**Source pointers:** NC §§2.1.3, 2.1.9; [Pauli averaging §2, Averaging identity](../science/pauli-averaging.md#2-averaging-identity).

### M14. Independent generators give exact survival probabilities

**Central question:** Why does each nonidentity Pauli coefficient survive with probability $2^{-s}$?

**Understanding target:** Connect balanced Pauli commutation signs to independent generator choices. Distinguish independence of the choices from independence of survival events for different coefficients, and explain why anticommuting generators or linearly dependent sampled Pauli labels do not invalidate the proof.

**Dependencies and story role:** Uses M06 and M13. It turns the single-generator cancellation rule into the full random average.

**Conceptual connection:** Products of Pauli conjugations commute even when the Pauli operators themselves anticommute. This makes a short generator description compatible with the exact ensemble calculation.

**Source pointers:** NC §§2.1.7, 2.1.9 and Appendix 1, p. 608; [Pauli averaging §1, Pauli expansion and random generators](../science/pauli-averaging.md#1-pauli-expansion-and-random-generators); [Pauli averaging §2, Averaging identity](../science/pauli-averaging.md#2-averaging-identity).

### M15. Concentrate a sampled eigenvalue around the trace

**Central question:** Why is normalized spectral variance the right concentration measure?

**Understanding target:** Connect the exact factor $2^{-s}$ contraction of normalized Hilbert–Schmidt variance, in expectation over the seed, to the probability that a uniformly sampled eigenvalue lies near the trace. Distinguish this seed-and-sample guarantee from an operator-norm bound or a guarantee for every seed.

**Dependencies and story role:** Uses M09 and M14. This identifies the statistical property that the circuit must exploit.

**Conceptual connection:** Rare outlying eigenvalues may persist; their multiplicity-weighted probability is the relevant quantity for a maximally mixed input.

**Source pointers:** NC §§2.1.4–2.1.5, 2.4.1 and Appendix 1, p. 608; [Pauli averaging §2, Averaging identity](../science/pauli-averaging.md#2-averaging-identity); [Pauli averaging, Spectral concentration consequence](../science/pauli-averaging.md#spectral-concentration-consequence).

### M16. Make a general oracle into a Hermitian involution

**Central question:** How can the real part of a signal block be placed inside an exact reflection-like unitary?

**Understanding target:** Explain how the two off-diagonal blocks $V$ and $V^\dagger$ form a Hermitian involution and why compression onto the extra $|+\rangle$ qubit produces $\mathrm{Re}C$. The original signal bits remain counted.

**Dependencies and story role:** Uses M02, M06, and M12. It prepares the oracle for the spectral construction without assuming that the supplied unitary is Hermitian.

**Conceptual connection:** Hermitianization converts the numerical quantity of interest into a signal block while preserving exact unitary evolution and explicit forward/inverse access.

**Source pointers:** NC §§2.1.6–2.1.7, 4.2–4.3; [Pauli averaging §3, A Hermitian involution from the input unitary](../science/pauli-averaging.md#3-a-hermitian-involution-from-the-input-unitary); [Model §2, Oracle access](../science/model.md#2-oracle-access).

### M17. Represent exponentially many branches with a short circuit

**Central question:** Why does the coherent average avoid a table containing all Pauli products?

**Understanding target:** Interpret SELECT as a label-controlled ordered product of $s$ Pauli strings. Explain why $s$ clean label bits describe $2^s$ branches while implementing the product needs only $O(ns)$ known gates.

**Dependencies and story role:** Uses M06, M14, and M16. It supplies the efficient coherent representation of the averaging operation.

**Conceptual connection:** The efficiency comes from the shared generator structure, not from free quantum memory access or arbitrary state preparation.

**Source pointers:** NC §§2.1.7, 4.3; [Pauli averaging §4, Coherent averaging circuit](../science/pauli-averaging.md#4-coherent-averaging-circuit).

### M18. Read the averaged matrix from the coherent signal block

**Central question:** Why does conjugating by SELECT produce exactly the desired average?

**Understanding target:** Connect uniform label preparation, SELECT, and its adjoint to the signal block $B_G$. Explain why the whole operator remains a Hermitian involution and why arbitrary branch phases cancel with a matching adjoint.

**Dependencies and story role:** Uses M16–M17. This completes the local construction that turns the abstract average into a usable unitary.

**Conceptual connection:** Compressing the label gives equal weights to its branches. The ordered product may be non-Hermitian, so its actual adjoint is essential even though its individual generators are Hermitian.

**Source pointers:** NC §§2.1.6, 2.2.7, 4.3; [Pauli averaging §4, Coherent averaging circuit](../science/pauli-averaging.md#4-coherent-averaging-circuit); [Pauli averaging, Branch phases](../science/pauli-averaging.md#branch-phases).

### M19. Convert the averaged eigenvalues into walk phases

**Central question:** How does an eigenvalue of the signal block determine an eigenphase of the walk?

**Understanding target:** Explain the invariant two-dimensional space associated with each eigenvector of $B_G$ and the phases $\pm\arccos\lambda$ of $Q=(2\Pi-I)W_G$. Treat $\lambda=\pm1$ directly rather than dividing by a vanishing normalization.

**Dependencies and story role:** Uses M07 and M18. This links the coherently encoded matrix to the phase-estimation primitive.

**Conceptual connection:** Both phase signs have cosine $\lambda$. The geometry uses the clean signal projector and the involution, not a rank-one reflection about the target's unknown state.

**Source pointers:** NC §§2.1.5, 2.2.5, 6.1.3; [Trace estimator §3, Mixed-state spectral sampling](../science/trace-estimator.md#3-mixed-state-spectral-sampling).

### M20. Obtain the correct spectral weights from mixed initialization

**Central question:** Which eigenvalue distribution does the initialized target actually supply?

**Understanding target:** Trace the decomposition of $I/2^n$ through the walk construction and obtain weight $1/2^n$ for each orthonormal eigenvector of $B_G$. Distinct eigenvalue values are weighted by their multiplicities, and the two walk-phase branches give the same cosine.

**Dependencies and story role:** Uses M03 and M19. It connects the physical initialization to the concentration measure established in M15.

**Conceptual connection:** No eigenstate preparation, target purification, or postselection is required to obtain the spectral sample used in the proof.

**Source pointers:** NC §§2.4.1–2.4.3, 5.2; [Trace estimator §3, Mixed-state spectral sampling](../science/trace-estimator.md#3-mixed-state-spectral-sampling); [Model §1, Registers, normalization, and initialization](../science/model.md#1-registers-normalization-and-initialization).

### M21. Assemble the real-estimate accuracy guarantee

**Central question:** How do spectral concentration and phase resolution combine into one reliable trace estimate?

**Understanding target:** Allocate half the error to each mechanism, understand why $s=2\log_2(1/\eta)+O(1)$ and $M=O(1/\eta)$ suffice, and combine the conditional phase success with concentration to obtain $15/(2\pi^2)>3/4$.

**Dependencies and story role:** Uses M08–M09, M15, and M20. This is the first complete correctness guarantee for the estimator.

**Conceptual connection:** Cosine converts phase error to eigenvalue error without a spectral-gap assumption. The final probability remains joint over the seed and the quantum outcome.

**Source pointers:** NC §§5.2–5.2.1 and Appendix 1, p. 608; [Trace estimator §1, Real estimator theorem](../science/trace-estimator.md#1-real-estimator-theorem); [Trace estimator §4, Accuracy and confidence](../science/trace-estimator.md#4-accuracy-and-confidence).

### M22. Account for every control and initialized qubit

**Central question:** Does the complete circuit satisfy the promised access and resource model?

**Understanding target:** Reconstruct the exact $a+s+r+2$ clean-qubit count and $2(M-1)$ total oracle calls. Explain how unconditional conjugating gates, a returned temporary bit, and the correctly signed controlled reflection avoid an uncharged stronger oracle. Keep known gates and oracle implementation cost separate.

**Dependencies and story role:** Uses M10, M17–M18, and M21. It turns correctness into the project's simultaneous resource theorem.

**Conceptual connection:** Logarithmic label and phase widths coexist with inverse-linear query cost; using a clean signal reflection does not require initializing the target purely.

**Source pointers:** NC §§3.2.1, 4.3, 4.5.2, 5.2.1; [Pauli averaging §5, Controlling the walk without a stronger oracle](../science/pauli-averaging.md#5-controlling-the-walk-without-a-stronger-oracle); [Trace estimator §5, Resource proof](../science/trace-estimator.md#5-resource-proof).

### M23. Obtain a complex estimate and account for confidence

**Central question:** What changes when both trace coordinates or a smaller failure probability are required?

**Understanding target:** Connect the imaginary coordinate to $-iU$, understand the three-run median in each coordinate and the resulting success bound $11/16$, and distinguish constant-confidence resources from the factor $\log(1/\delta)$ in the direct high-confidence repetition construction.

**Dependencies and story role:** Uses M09 and M21–M22. It completes the complex-output task and specifies its repetition convention.

**Conceptual connection:** A strict computation without resets counts every independently initialized copy. Reusing device hardware between separately initialized experiments does not remove that initialization cost from the strict model.

**Source pointers:** NC §§2.2.7, 4.4, 5.2.1 and Appendix 1, p. 608; [Trace estimator §6, Complex trace theorem and higher confidence](../science/trace-estimator.md#6-complex-trace-theorem-and-higher-confidence); [Model §5, Output convention and scope](../science/model.md#5-output-convention-and-scope).

### M24. Separate fixed bias from accumulated execution error

**Central question:** Which imperfections alter the estimated trace once, and which can alter every step of the computation?

**Understanding target:** Distinguish fixed signal-block error, imperfect joint initialization, and per-call execution error. Explain the bound on success loss from the initial trace distance plus accumulated normalized diamond errors, and include finite-gate synthesis in that budget.

**Dependencies and story role:** Uses M11 and M21–M23. It extends the ideal theorem without changing the meaning of its purity or query claims.

**Conceptual connection:** A consistently implemented nearby unitary with its matching adjoint can be treated as a changed input. General imperfect controlled operations require the execution bound; uncontrolled channel closeness alone does not fix relative phase.

**Source pointers:** NC §§8.2.2–8.2.3, 9.2.1, 4.5.3 and Appendix 3, p. 617; [Robustness §1, Approximate block encodings can be Hermitianized exactly](../science/robustness.md#1-approximate-block-encodings-can-be-hermitianized-exactly); [Robustness §2, Hybrid bound for an imperfect execution](../science/robustness.md#2-hybrid-bound-for-an-imperfect-execution); [Robustness §3, Robust real-estimator theorem](../science/robustness.md#3-robust-real-estimator-theorem).

### M25. Interpret the standard query lower bound correctly

**Central question:** What is proved optimal by distinguishing two nearby scalar-phase oracles?

**Understanding target:** Follow how separated trace values imply distinguishability and how a query hybrid bound gives $\Omega(1/\epsilon)$ calls, even with unrestricted clean workspace. Distinguish optimal query dependence from any claim that the clean-qubit upper bound is necessary.

**Dependencies and story role:** Uses M06, M11, and M22. It identifies the precise optimality statement supported by the construction.

**Conceptual connection:** The contribution attains an existing precision scale under a low-purity initialization model; it does not supply a new purity lower bound.

**Source pointers:** NC §§2.2.4, 6.7, 9.2.1; [Trace estimator §8, Query lower bound](../science/trace-estimator.md#8-query-lower-bound); [Scientific account §5, Proof and evidence map](../science/README.md#5-proof-and-evidence-map).

### M26. Internalize randomness without adding purity

**Central question:** How can a randomized construction become one fixed circuit description?

**Understanding target:** Replace the external Pauli seed by $2ns$ initially maximally mixed control bits, retain their values through the entire computation, and explain why the final distribution equals the seed average. Count the enlarged mixed width while leaving the clean-qubit and query counts unchanged.

**Dependencies and story role:** Uses M03, M06, M17, and M22. It prepares the estimator for a uniform circuit transformation with one terminal output.

**Conceptual connection:** Block-diagonal control by a classical mixture implements the required random choice internally. Resampling during different walk powers would change the operator and invalidate the phase-estimation argument.

**Source pointers:** NC §§2.4.1, 4.3–4.4; [Pauli averaging §6, Internalizing the random seed](../science/pauli-averaging.md#6-internalizing-the-random-seed); [Few-clean amplification §4, A fixed circuit with an internal mixed seed](../science/few-clean-amplification.md#4-a-fixed-circuit-with-an-internal-mixed-seed).

### M27. Turn acceptance probability into a signal trace

**Central question:** How can the estimator amplify a computation whose acceptance gap is small?

**Understanding target:** Explain why $V_x^\dagger Z_{\mathrm{out}}V_x$ is an involution whose clean-zero signal block has normalized trace $2p_x-1$. The original $k$ clean bits become signal bits, and controlled access to this involution uses unconditional $V_x$ and $V_x^\dagger$ around a known controlled observable.

**Dependencies and story role:** Uses M04, M12, M21, and M26. It connects trace estimation to a complete computation rather than to an isolated matrix.

**Conceptual connection:** The direct block reduction preserves the acceptance gap. The alternative full-unitary trace reduction remains valid but attenuates the signal and incurs an additional $2^k$ query factor.

**Source pointers:** NC §§2.2.3, 2.4.2, 4.3; [Few-clean amplification §2, Direct Hermitian-block reduction](../science/few-clean-amplification.md#2-direct-hermitian-block-reduction); [Few-clean amplification §7, An alternative reduction through a unitary trace](../science/few-clean-amplification.md#7-an-alternative-reduction-through-a-unitary-trace).

### M28. Produce one output with a known uniform threshold

**Central question:** How can a phase estimate become a uniformly generated decision circuit without intermediate measurements?

**Understanding target:** Use supplied or efficiently computable completeness and soundness thresholds with a known inverse-polynomial gap $\Delta$. Explain how a classically computed phase cutoff becomes two reversible integer comparisons, yielding one output bit with $k+O(\log(2/\Delta))$ clean qubits and $O(1/\Delta)$ original-circuit calls.

**Dependencies and story role:** Uses M08, M10–M11, and M26–M27. It completes the operational amplification transformation.

**Conceptual connection:** Threshold computation, reversible workspace, internal randomness, and finite-gate error all belong to the uniform construction. Merely knowing that some separating thresholds exist does not provide this circuit.

**Source pointers:** NC §§3.1.2, 4.4, 4.5.3, 4.5.5, 5.2.1; [Few-clean amplification §1, Model and statement](../science/few-clean-amplification.md#1-model-and-statement); [Few-clean amplification §5, One reversible output comparison](../science/few-clean-amplification.md#5-one-reversible-output-comparison); [Few-clean amplification §6, Uniform finite-gate implementation](../science/few-clean-amplification.md#6-uniform-finite-gate-implementation).

### M29. Compose the consequence with established few-clean compilers

**Central question:** Which stronger error guarantees follow after the first-stage gap has become constant?

**Understanding target:** Separate the proved logarithmic-clean first stage from the credited one- and two-clean-qubit circuit transformations. Distinguish exponentially small two-sided error with two clean qubits from the one-clean asymmetric guarantees, and keep the compilers' polynomial overhead separate from the first stage's $O(1/\Delta)$ bound.

**Dependencies and story role:** Uses M10, M24, and M28. It places the new operational transformation inside the existing computational framework.

**Conceptual connection:** Composition is a transformation of circuit descriptions, not a sequence of experiments that replenishes clean qubits. The imported compiler theorems come from the cited research sources, beyond NC's foundational circuit model.

**Source pointers:** NC §§3.2.2, 3.2.4, 4.5.5–4.6; [Few-clean amplification §8, Consequences inherited from constant-gap amplification](../science/few-clean-amplification.md#8-consequences-inherited-from-constant-gap-amplification); [Few-clean amplification, References](../science/few-clean-amplification.md#references).

### M30. Integrate the contribution, evidence, and boundaries

**Central question:** What complete scientific claim survives after all resources, assumptions, and imported ingredients are counted?

**Understanding target:** Connect Pauli variance contraction, an efficient coherent signal block, mixed-state spectral weights, and phase resolution into simultaneous inverse-linear query precision and logarithmic initial clean width. Integrate complex confidence costs, controlled inverse access, operational errors, the known-threshold amplification consequence, and the absence of a purity lower bound.

**Dependencies and story role:** Uses M12 and M23–M29, which integrate the preceding mechanisms. This is the narrative synthesis.

**Conceptual connection:** Analytical proofs establish the theorem; finite coherent-circuit checks target implementation mistakes; source comparisons identify prior ingredients and the remaining contribution. None of those roles substitutes for the others.

**Source pointers:** NC §§3.2.1, 4.6, 5.2.1, 6.7; [Scientific account §3, What the theorem counts](../science/README.md#3-what-the-theorem-counts); [Scientific account §4, Error and a computational consequence](../science/README.md#4-error-and-a-computational-consequence); [Scientific account §5, Proof and evidence map](../science/README.md#5-proof-and-evidence-map); [Trace estimator §9, Finite verification](../science/trace-estimator.md#9-finite-verification).

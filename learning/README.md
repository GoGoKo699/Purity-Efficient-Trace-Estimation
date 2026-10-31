# Learning route

The guiding source is Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010). Its treatment of density operators, purification, controlled circuits, and phase estimation supplies the foundations. The project develops the additional steps needed to estimate a normalized trace with logarithmic initial clean width.

The central distinction is between the purity needed to initialize a computation and the accuracy obtainable from its oracle calls. A target initialized maximally mixed already contains the uniform spectral weights needed for a trace. The construction makes that observation useful by coherently concentrating the spectrum before phase estimation.

## Three connected routes

| Starting point | Route |
|---|---|
| Locate the relevant textbook foundations | [Selected anchor and notation](anchor.md) identifies the sections, translates conventions, and explains what is supplied by this project. |
| Understand the mechanism through an example | [From Nielsen–Chuang to the estimator](bridge.md) connects mixed states, coherent averaging, spectral sampling, and resource accounting. |
| Build an integrated understanding of the whole result | [The 30-milestone map](milestones.md) orders the background and contribution by conceptual dependencies. |

The map has 12 background/preliminaries milestones and 18 narrative/innovation milestones. The first phase assembles the state, circuit, probability, and resource framework. The second follows the averaging mechanism through the estimator, implementation, error analysis, and computational consequence. Each phase ends by combining its parts into a global account.

The milestones are common understanding targets for any reader. They identify what a concept explains and where its exact statement or proof lives. They do not replace the scientific account or imply that every technical calculation is included.

## Where the bridge ends and the proof begins

The textbook is the single educational anchor. Primary research sources retain their distinct role in attributing imported constructions and amplification theorems. Modern block encodings, qubitization, the Pauli variance identity, and the resulting initial-purity theorem are explained through the project pages and their research citations.

Specialists can begin with the [model](../science/model.md) and [main estimator theorem](../science/trace-estimator.md), then use [Pauli averaging](../science/pauli-averaging.md), [robustness](../science/robustness.md), and [few-clean amplification](../science/few-clean-amplification.md) for the supporting arguments. The [related-work comparison](../references/related-work.md) separates the simultaneous purity/query guarantee from established query exponents and circuit ingredients.

The [finite verification suite](../verification/README.md) gives concrete checks of the averaging identity, coherent circuit, phase-estimation distribution, and acceptance reductions. Its diagnostics complement the analytic reasoning.

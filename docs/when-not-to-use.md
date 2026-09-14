# When Not to Add a Boundary

> [English](when-not-to-use.md) | [日本語](ja-JP/when-not-to-use.md)

Clean Architecture is a way to isolate details; it is not an obligation to add abstractions or split systems. Add a boundary only when its benefit to independent change, testing, development, or release exceeds its cost.

## Signals not to add a boundary

Prefer the existing design or a weaker boundary when:

- The separated components always require the same team, release, and data change.
- A port nearly reproduces SQL, ORM, SDK, or HTTP types and methods.
- An interface abstracts one implementation rather than the caller’s need.
- A DTO merely copies an outer data structure with no meaningful translation.
- Separation broadens the set of code to change, retest, or coordinate.
- The owner, update API, or concurrent-update rules for mutable state are unknown.

In these cases, remove abstractions, narrow the use case, or return to observation.

## Do not rush into service decomposition

A network service is a strong boundary, but it introduces communication failure, monitoring, contract management, shared data, deployment order, distributed transactions, and operational responsibility. Splitting a service does not by itself correct inward dependencies or mixed responsibilities inside it.

Do not propose service decomposition without explaining:

- what must become independently developed, tested, released, or operated
- how shared data and coordinated deployments will be avoided
- how communication failure and contract mismatch will be handled
- why source-level separation or a component is insufficient

## Stop refinement when

Do not proceed to another use case when:

- current behavior cannot be fixed with tests
- the new boundary repeats implementation details
- mutable-state ownership has become ambiguous
- forbidden dependencies or cycles increase
- the added boundary has no explainable independence benefit

Stopping is not failure. It is a decision to revisit the design hypothesis before adding needless abstraction or physical distribution.

## Requests this skill does not fit

- naming or formatting only
- performance measurement only
- framework-specific API research only
- a wholesale rewrite without evidence

These have different goals and verification methods. To treat work as design improvement, first state which change must be made safer and which behavior must remain true.

## Next

- [Why Clean Architecture Design](why-clean-architecture-design.md)
- [From Diagnosis to Incremental Refinement](diagnosis-to-refinement.md)

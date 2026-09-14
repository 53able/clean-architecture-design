# Why Clean Architecture Design

> [English](why-clean-architecture-design.md) | [日本語](ja-JP/why-clean-architecture-design.md)

Clean Architecture is not a template for arranging folders into four layers or multiplying interfaces. It is a way to decide which policies must remain stable and which details should stay replaceable, so that software can absorb change.

Applying that idea to an existing codebase is difficult. Principles alone do not answer questions such as “Should we extract a repository?”, “Do we need an interface?”, or “Should this become a service?”

`clean-architecture-design` turns those questions into a sequence of observations about change reasons, use cases, dependencies, state, and verification.

## Stop before adding abstractions

Design work can easily start with attractive structure: a `controller`, `interactor`, `presenter`, and `repository` for every feature. Without an independently changing reason, that structure only adds types and hops.

The skill starts by identifying the actor, use case, preserved behavior, external I/O, and current tests. It groups policies that change for the same reason and treats only differently changing concerns as possible boundaries. A port or adapter is proposed only when it isolates a concrete change or external dependency.

The goal is not to make a codebase look like Clean Architecture. It is to keep a small change from spreading into unrelated UI, database, framework, or coordination work.

## Choose boundaries from reasons for change

Technology-oriented folders can hide a system’s business boundaries.

```text
controllers/
services/
repositories/
```

They show technical roles, but not use cases such as confirming an order, reviewing a refund, or issuing an invoice. When rules for different users or departments live in the same `service`, the likely impact of a change is difficult to see.

The skill maps actors to use cases first. It then groups policies by shared reasons for change and considers boundaries only where those reasons differ. This prevents the technical layer structure from being fixed before real change pressure is understood.

For example, a direct database call from an HTTP handler does not automatically require “the Repository pattern.” The skill traces the use case’s input, rules, output, and external I/O before deciding whether a port owned by the inner policy is useful.

## Treat details as details, not as forbidden technology

Clean Architecture does not ban databases or web frameworks. They are necessary details in many systems. The risk is allowing their types and constraints to define the use case or domain rules.

The skill looks for cases such as these:

- A use case accepts ORM entities or HTTP requests directly.
- Domain code refers to a cloud SDK or framework type.
- A controller bypasses a use case and calls persistence directly.
- Inner policy depends on an interface defined by the outer implementation.

When separation is justified, the inner use case defines a port in its own vocabulary and an outer adapter implements it. Concrete implementations, configuration, and dependency injection belong in the composition root. This lets a system use external services in production while increasing the portion of use-case behavior that can be verified without starting them.

## Avoid boundaries that are stronger than necessary

A boundary is not automatically a package, process, or microservice. Stronger boundaries can provide more isolation, but they also add communication failure, shared-data, compatibility, deployment, observability, and operational costs.

The skill compares the smallest viable options:

- source-level separation in one process
- a deployable component
- a local process
- a network service

If independent development, testing, or release benefits cannot be explained, it keeps the existing boundary. It does not justify service decomposition merely by invoking Clean Architecture.

## Make design claims testable

A design review should not end with a tidy diagram. The skill begins with one use case, fixes current behavior with tests, extracts a thin entry point, moves external I/O behind ports one dependency at a time, and then checks dependency direction, cycles, boundary-crossing types, external-I/O failures, and concurrent updates.

It also stops refinement when a port copies implementation details, when the changed or retested surface expands, when mutable-state ownership becomes unclear, or when the new boundary has no explainable independence benefit.

Clean Architecture is not knowledge for selecting the “correct” folder layout. It is a way to locate where the structure resists change and introduce only the boundaries that resolve that resistance.

## Next

- [From Diagnosis to Incremental Refinement](diagnosis-to-refinement.md)
- [When Not to Add a Boundary](when-not-to-use.md)

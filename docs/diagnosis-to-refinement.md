# From Diagnosis to Incremental Refinement

> [English](diagnosis-to-refinement.md) | [日本語](ja-JP/diagnosis-to-refinement.md)

This skill does not prescribe a target architecture first. It improves one use case at a time while preserving existing behavior.

## 1. Observe

Record the following as facts:

- actors and use cases
- inputs, outputs, and external I/O
- reasons and frequency of change, plus modules that change together
- imports, references, public APIs, framework types, and database models
- mutable-state owner, writers, and rules for concurrent updates
- current tests, builds, deployments, and owning teams

Do not infer responsibility from folder or class names alone. Classify code from its actual dependencies and change impact.

## 2. Compare boundary candidates

Use observed facts to identify candidates: external details leaking inward, dependency cycles, or rules for different actors living together.

Do not begin with a service. Compare increasingly strong choices instead:

1. no new boundary
2. source-level separation in the same process
3. a deployable component
4. a local process or network service

For each option, compare the resulting independence of change, test, and release against the costs of new contracts, operations, compatibility management, communication, and shared data. Do not add a boundary without an explainable independence benefit.

## 3. Add the smallest useful port and adapter

When separation is justified, the high-level policy that uses a port owns it.

- Do not pass HTTP requests or CLI arguments directly as use-case input.
- Do not return ORM entities or HTTP responses directly as use-case output.
- Express a gateway in the operations required by the use case, not generic CRUD.
- Keep translations between external and inner models in adapters.
- Gather concrete implementations, configuration, and DI in the composition root.

Reconsider an interface that merely copies the methods of one implementation.

## 4. Refine one use case

Make changes in small steps.

1. Fix the current behavior of the target use case with tests.
2. Extract a thin entry point that calls the use case from the handler or controller.
3. Move references to databases, SDKs, HTTP, and ORMs behind ports one at a time.
4. Move translation to adapters and wiring to the composition root.
5. Check dependency direction, cycles, and types that cross the boundary.

Before widening the scope, verify that the change and retest surface actually became smaller.

## 5. Look for counterexamples

A passing test does not prove a design correct. Look for examples that contradict its claims.

At minimum, consider the happy path, invalid input, boundary values, external-I/O failure, concurrent updates, and contract violations. Check whether inner policy can be tested without external I/O, whether forbidden dependencies increased, and whether external detail types cross a boundary.

## Example request

```text
Plan an incremental separation of direct database access from this HTTP handler using ports and adapters.

Target use case:
Behavior to preserve:
Current inputs and outputs:
External I/O:
Current tests:

Separate observations, inferences, the minimum change, and a verification plan.
Do not propose a boundary whose independence benefit cannot be explained.
```

## Next

- [Why Clean Architecture Design](why-clean-architecture-design.md)
- [When Not to Add a Boundary](when-not-to-use.md)

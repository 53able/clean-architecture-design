# Clean Architecture Design

> [English](README.md) | [日本語](docs/ja-JP/README.md)

An agent skill for diagnosing existing software design, selecting boundaries, planning incremental refinements, and reviewing dependency boundaries through Clean Architecture principles.

## Install

```bash
npx skills add 53able/clean-architecture-design
```

## What it helps with

- Map actors and use cases to their reasons for change and policy levels.
- Inspect inward dependency violations, dependency cycles, and leaked external details.
- Compare source-level separation, deployable components, and processes or services; choose the smallest boundary that provides the required independence.
- Design ports, adapters, and a composition root.
- Treat mutable-state ownership, concurrent updates, and recovery rules as boundary concerns.
- Refine one use case safely at a time.
- Test design claims and boundaries by looking for counterexamples.

## Examples

```text
Diagnose the order-processing code in this repository and propose the smallest improvement using Clean Architecture principles.
```

```text
Plan an incremental separation of direct database access from this HTTP handler using ports and adapters.
```

## Guides

- [Why Clean Architecture Design](docs/why-clean-architecture-design.md): The problem the skill addresses and the value of choosing boundaries from change cost.
- [From Diagnosis to Incremental Refinement](docs/diagnosis-to-refinement.md): A workflow for observation, minimum boundaries, ports and adapters, and verification.
- [When Not to Add a Boundary](docs/when-not-to-use.md): Guardrails against needless abstraction and premature service decomposition.

## Repository layout

- `SKILL.md`: workflow instructions
- `assets/`: templates for diagnosis, boundary decisions, migration plans, and reassessment
- `references/`: rules for design, boundaries, and incremental refinement
- `scripts/`: a script that checks dependency direction and cycles
- `docs/ja-JP/`: Japanese documentation

## License

[MIT License](LICENSE)

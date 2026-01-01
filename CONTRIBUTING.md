# Contributing to Kernels

This document describes the process for contributing to the Kernels project.

## Requirements

All contributions must satisfy the following requirements:

1. **Standard Library Only.** No external dependencies. Python 3.11+ standard library is the only permitted import source.

2. **Deterministic Behavior.** All code must produce identical outputs given identical inputs. No randomness, no system-dependent behavior, no floating-point comparisons.

3. **Type Annotations.** All public functions and methods must include complete type annotations.

4. **Test Coverage.** All new functionality must include corresponding unit tests. Tests must pass before merge.

5. **Invariant Compliance.** No contribution may violate the core invariants defined in the specification.

## Code Style

The project follows these conventions:

| Aspect              | Convention                                           |
|---------------------|------------------------------------------------------|
| Formatting          | PEP 8 compliant                                      |
| Line length         | 100 characters maximum                               |
| Imports             | Standard library only, grouped and sorted            |
| Naming              | snake_case for functions/variables, PascalCase for classes |
| Docstrings          | Required for all public APIs                         |
| Comments            | Minimal, explain why not what                        |

## Commit Conventions

Commit messages must follow this format:

```
<type>: <description>

[optional body]
```

Valid types:

| Type     | Usage                                    |
|----------|------------------------------------------|
| feat     | New feature                              |
| fix      | Bug fix                                  |
| docs     | Documentation changes                    |
| test     | Test additions or modifications          |
| refactor | Code restructuring without behavior change |
| spec     | Specification changes                    |

## Pull Request Process

1. Fork the repository and create a feature branch.

2. Ensure all tests pass: `python -m unittest discover -s tests -v`

3. Ensure examples run without error.

4. Update documentation if behavior changes.

5. Submit pull request with clear description of changes.

6. Address review feedback.

7. Maintainer merges after approval.

## Specification Changes

Changes to the formal specification require:

1. Discussion in an issue before implementation.

2. Clear rationale for the change.

3. Assessment of backward compatibility impact.

4. Version bump according to semantic versioning rules.

5. Migration guide if breaking.

## Invariant Changes

Modifications to core invariants are exceptional events requiring:

1. RFC-style proposal document.

2. Consensus among maintainers.

3. Major version bump.

4. Complete migration guide.

5. Deprecation period for previous behavior.

## Adding Kernel Variants

New kernel variants are welcomed. Requirements:

1. Must implement the `Kernel` protocol completely.

2. Must satisfy all core invariants.

3. Must include dedicated tests.

4. Must document enforcement posture differences in `spec/VARIANTS.md`.

5. Must include at least one example demonstrating unique behavior.

## Adding Tools

New tools may be added to the registry. Requirements:

1. Must be deterministic.

2. Must not perform I/O beyond return values.

3. Must include type annotations.

4. Must include tests.

5. Must be registered explicitly (no dynamic discovery).

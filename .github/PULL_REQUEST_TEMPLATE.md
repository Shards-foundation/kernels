## Description

Brief description of the changes.

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Related Issues

Fixes #

## Invariant Compliance

Confirm that this PR maintains all core invariants:

- [ ] INV-STATE: Single defined state at all times
- [ ] INV-TRANSITION: Only defined transitions occur
- [ ] INV-JURISDICTION: All requests pass jurisdiction checks
- [ ] INV-AUDIT: All transitions produce audit entries
- [ ] INV-HASH-CHAIN: Audit entries are hash-chained
- [ ] INV-FAIL-CLOSED: Ambiguity results in DENY or HALT
- [ ] INV-DETERMINISM: Identical inputs produce identical outputs
- [ ] INV-HALT: Halt is always possible and irrevocable
- [ ] INV-EVIDENCE: Decisions are exportable with verification
- [ ] INV-NO-IMPLICIT-ALLOW: Explicit ALLOW required for execution

## Testing

- [ ] Unit tests added/updated
- [ ] All existing tests pass
- [ ] Smoke test passes
- [ ] Manual testing performed

## Documentation

- [ ] README updated (if applicable)
- [ ] Docstrings added/updated
- [ ] Specification updated (if applicable)

## Checklist

- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code where necessary
- [ ] My changes generate no new warnings

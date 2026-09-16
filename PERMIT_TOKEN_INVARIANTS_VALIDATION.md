# Permit Token Implementation: Invariant Preservation Validation

**Original validation:** 2026-01-14
**Current review:** 2026-09-16
**Version:** 0.2.x development
**Status:** SUPERSEDED — revalidation required

---

## Review correction

The original validation below predates the later kernel/permit integration and must not be treated as the current release-gate authority.

During the 2026-09-16 closed-loop product review, a concrete verification defect was found: `AuditLedger.append()` includes permit metadata in the audit hash preimage, but the previous `replay_and_verify()` implementation omitted those same permit fields. Consequently, valid permit-bearing audit entries could not be independently replay-verified from their exported evidence representation.

This defect is addressed in the associated hardening change by making replay use the same complete hash preimage as the ledger and adding a regression test.

The authoritative acceptance state is therefore the current CI/test result, not the historical checklist below.

---

## Historical validation checklist

The following material records the scope and claims of the original 2026-01-14 review. It is retained for audit history but is **not** a current conformance statement.

| # | Invariant | Historical status |
|---|-----------|-------------------|
| 1 | **INV-STATE** | Previously marked PASS |
| 2 | **INV-TRANSITION** | Previously marked PASS; integration was explicitly noted as pending |
| 3 | **INV-JURISDICTION** | Previously marked PASS |
| 4 | **INV-AUDIT** | Previously marked PASS |
| 5 | **INV-HASH-CHAIN** | Previously marked PASS; current replay defect required correction |
| 6 | **INV-FAIL-CLOSED** | Previously marked PASS |
| 7 | **INV-DETERMINISM** | Previously marked PASS |
| 8 | **INV-HALT** | Previously marked PASS |
| 9 | **INV-EVIDENCE** | Previously marked PASS |
| 10 | **INV-NO-IMPLICIT-ALLOW** | Previously marked PASS |

## Required current revalidation

Before claiming release/conformance, verify at minimum:

1. Full CI matrix passes on supported Python versions.
2. Permit-bearing ledger entries replay successfully.
3. Tampering with any committed permit field is detected.
4. Exported evidence bundles verify successfully after process restart.
5. Missing, expired, mismatched and replayed permits remain fail-closed.
6. Valid permits reach execution only when all authorization conditions pass.
7. Built distributions contain every module used by the documented smoke path.
8. The installed wheel passes an import/runtime smoke test outside the source checkout.

Until those gates are green, this document must not be interpreted as a current conformance certificate.

# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | Yes                |

## Reporting a Vulnerability

If you discover a security vulnerability in Kernels, report it through the following process:

1. **Do not open a public issue.** Security vulnerabilities must be reported privately.

2. **Send an email to the maintainers** with the subject line: `[SECURITY] Kernels Vulnerability Report`

3. **Include the following information:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if available)

4. **Response timeline:**
   - Acknowledgment within 48 hours
   - Initial assessment within 7 days
   - Fix timeline communicated within 14 days

## Security Model

Kernels is a control plane, not a security boundary. The security model assumes:

| Assumption                          | Implication                                      |
|-------------------------------------|--------------------------------------------------|
| Operator is trusted                 | Policy is assumed correct                        |
| Kernel code is trusted              | No sandboxing of kernel itself                   |
| Tools are trusted                   | Tool implementations are not verified by kernel  |
| Agents are untrusted                | All agent requests are validated                 |
| Audit ledger is append-only         | Tampering detection, not prevention              |

## Threat Model

The kernel defends against:

1. **Malformed requests** from agents attempting to bypass validation.

2. **Jurisdiction violations** where agents attempt unauthorized tool access.

3. **Ambiguous requests** that could lead to unintended execution.

4. **Audit gaps** that would prevent post-hoc analysis.

The kernel does not defend against:

1. **Compromised operator** who sets malicious policy.

2. **Compromised kernel code** (supply chain attacks).

3. **Malicious tools** registered by trusted operators.

4. **Side-channel attacks** on the execution environment.

## Invariant Violations

Any condition that violates a core invariant is considered a security-relevant bug. The invariants are:

1. INV-STATE: Single defined state at all times
2. INV-TRANSITION: Only defined transitions occur
3. INV-JURISDICTION: All requests pass jurisdiction checks
4. INV-AUDIT: All transitions produce audit entries
5. INV-HASH-CHAIN: Audit entries are hash-chained
6. INV-FAIL-CLOSED: Ambiguity results in DENY or HALT
7. INV-DETERMINISM: Identical inputs produce identical outputs
8. INV-HALT: Halt is always possible and irrevocable
9. INV-EVIDENCE: Decisions are exportable with verification
10. INV-NO-IMPLICIT-ALLOW: Explicit ALLOW required for execution

Report any code path that violates these invariants as a security vulnerability.

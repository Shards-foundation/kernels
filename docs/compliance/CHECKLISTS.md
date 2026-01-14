# KERNELS Checklists

**Version:** 0.1.0  
**Last Updated:** January 2025

---

## 1. Development Checklist

### 1.1 Code Quality

| Item | Requirement | Status |
|------|-------------|--------|
| DEV-001 | All tests pass | ✅ |
| DEV-002 | No linting errors | 🔲 |
| DEV-003 | Type hints complete | ✅ |
| DEV-004 | Docstrings present | ✅ |
| DEV-005 | No TODO in production code | 🔲 |
| DEV-006 | Error handling complete | ✅ |
| DEV-007 | Logging appropriate | ✅ |

### 1.2 Testing

| Item | Requirement | Status |
|------|-------------|--------|
| TEST-001 | Unit tests for all modules | ✅ |
| TEST-002 | Integration tests | ✅ |
| TEST-003 | Property-based tests | 🔲 |
| TEST-004 | Fuzz tests | 🔲 |
| TEST-005 | Security tests | 🔲 |
| TEST-006 | Performance tests | 🔲 |
| TEST-007 | Coverage > 80% | 🔲 |

### 1.3 Documentation

| Item | Requirement | Status |
|------|-------------|--------|
| DOC-001 | README complete | ✅ |
| DOC-002 | API documented | ✅ |
| DOC-003 | Examples provided | ✅ |
| DOC-004 | Specs complete | ✅ |
| DOC-005 | Architecture documented | ✅ |
| DOC-006 | Threat model documented | ✅ |
| DOC-007 | Changelog maintained | ✅ |

---

## 2. Release Checklist

### 2.1 Pre-Release

| Item | Requirement | Status |
|------|-------------|--------|
| REL-001 | Version bumped | 🔲 |
| REL-002 | Changelog updated | 🔲 |
| REL-003 | All tests pass | 🔲 |
| REL-004 | Security scan clean | 🔲 |
| REL-005 | Dependencies audited | 🔲 |
| REL-006 | Documentation updated | 🔲 |
| REL-007 | Breaking changes documented | 🔲 |

### 2.2 Release

| Item | Requirement | Status |
|------|-------------|--------|
| REL-101 | Tag created | 🔲 |
| REL-102 | Release notes published | 🔲 |
| REL-103 | Package published | 🔲 |
| REL-104 | Announcement posted | 🔲 |

### 2.3 Post-Release

| Item | Requirement | Status |
|------|-------------|--------|
| REL-201 | Monitor for issues | 🔲 |
| REL-202 | Respond to feedback | 🔲 |
| REL-203 | Update roadmap | 🔲 |

---

## 3. Deployment Checklist

### 3.1 Environment Preparation

| Item | Requirement | Status |
|------|-------------|--------|
| ENV-001 | Python 3.11+ installed | 🔲 |
| ENV-002 | Dependencies installed | 🔲 |
| ENV-003 | Configuration validated | 🔲 |
| ENV-004 | Secrets configured | 🔲 |
| ENV-005 | Logging configured | 🔲 |
| ENV-006 | Monitoring configured | 🔲 |

### 3.2 Security Hardening

| Item | Requirement | Status |
|------|-------------|--------|
| SEC-001 | Jurisdiction policy set | 🔲 |
| SEC-002 | Allowed actors defined | 🔲 |
| SEC-003 | Allowed tools defined | 🔲 |
| SEC-004 | Rate limits configured | 🔲 |
| SEC-005 | TLS enabled | 🔲 |
| SEC-006 | Audit persistence enabled | 🔲 |

### 3.3 Validation

| Item | Requirement | Status |
|------|-------------|--------|
| VAL-001 | Health check passes | 🔲 |
| VAL-002 | Test request succeeds | 🔲 |
| VAL-003 | Audit entry created | 🔲 |
| VAL-004 | Evidence export works | 🔲 |
| VAL-005 | Halt command works | 🔲 |

---

## 4. Operational Checklists

### 4.1 Daily Operations

| Item | Requirement | Frequency |
|------|-------------|-----------|
| OPS-001 | Check kernel state | Daily |
| OPS-002 | Review audit log | Daily |
| OPS-003 | Verify hash chain | Daily |
| OPS-004 | Check decision metrics | Daily |
| OPS-005 | Review denied requests | Daily |

### 4.2 Weekly Operations

| Item | Requirement | Frequency |
|------|-------------|-----------|
| OPS-101 | Export evidence bundle | Weekly |
| OPS-102 | Verify evidence integrity | Weekly |
| OPS-103 | Review actor activity | Weekly |
| OPS-104 | Check resource usage | Weekly |

### 4.3 Monthly Operations

| Item | Requirement | Frequency |
|------|-------------|-----------|
| OPS-201 | Review jurisdiction policy | Monthly |
| OPS-202 | Audit actor list | Monthly |
| OPS-203 | Audit tool list | Monthly |
| OPS-204 | Test recovery procedures | Monthly |
| OPS-205 | Update threat model | Monthly |

---

## 5. Incident Response Checklist

### 5.1 Detection

| Item | Action | Status |
|------|--------|--------|
| INC-001 | Identify anomaly | 🔲 |
| INC-002 | Gather initial evidence | 🔲 |
| INC-003 | Classify severity | 🔲 |
| INC-004 | Notify on-call | 🔲 |

### 5.2 Containment

| Item | Action | Status |
|------|--------|--------|
| INC-101 | Export evidence bundle | 🔲 |
| INC-102 | Issue halt if critical | 🔲 |
| INC-103 | Isolate affected systems | 🔲 |
| INC-104 | Preserve logs | 🔲 |

### 5.3 Investigation

| Item | Action | Status |
|------|--------|--------|
| INC-201 | Replay audit trail | 🔲 |
| INC-202 | Identify root cause | 🔲 |
| INC-203 | Document timeline | 🔲 |
| INC-204 | Assess impact | 🔲 |

### 5.4 Recovery

| Item | Action | Status |
|------|--------|--------|
| INC-301 | Implement fix | 🔲 |
| INC-302 | Verify fix | 🔲 |
| INC-303 | Restore service | 🔲 |
| INC-304 | Monitor for recurrence | 🔲 |

### 5.5 Post-Incident

| Item | Action | Status |
|------|--------|--------|
| INC-401 | Write incident report | 🔲 |
| INC-402 | Conduct post-mortem | 🔲 |
| INC-403 | Update procedures | 🔲 |
| INC-404 | Share lessons learned | 🔲 |

---

## 6. Audit Preparation Checklist

### 6.1 Evidence Gathering

| Item | Evidence Type | Status |
|------|---------------|--------|
| AUD-001 | Audit ledger exports | 🔲 |
| AUD-002 | Policy snapshots | 🔲 |
| AUD-003 | Test results | 🔲 |
| AUD-004 | Security scan reports | 🔲 |
| AUD-005 | Incident reports | 🔲 |
| AUD-006 | Change logs | 🔲 |

### 6.2 Documentation Review

| Item | Document | Status |
|------|----------|--------|
| AUD-101 | Architecture documentation | 🔲 |
| AUD-102 | Security policies | 🔲 |
| AUD-103 | Operational procedures | 🔲 |
| AUD-104 | Incident response plan | 🔲 |
| AUD-105 | Business continuity plan | 🔲 |

### 6.3 Control Verification

| Item | Control | Status |
|------|---------|--------|
| AUD-201 | Access control working | 🔲 |
| AUD-202 | Audit logging working | 🔲 |
| AUD-203 | Hash chain valid | 🔲 |
| AUD-204 | Fail-closed working | 🔲 |
| AUD-205 | Halt command working | 🔲 |

---

## 7. TODO Tracker

### 7.1 Immediate (P0)

| ID | Task | Owner | Due |
|----|------|-------|-----|
| TODO-001 | Add constant-time hash compare | - | - |
| TODO-002 | Implement rate limiting | - | - |
| TODO-003 | Add input size validation | - | - |

### 7.2 Short-Term (P1)

| ID | Task | Owner | Due |
|----|------|-------|-----|
| TODO-101 | Implement permit tokens | - | - |
| TODO-102 | Add evidence signatures | - | - |
| TODO-103 | Set up CI/CD pipeline | - | - |
| TODO-104 | Add property-based tests | - | - |

### 7.3 Long-Term (P2)

| ID | Task | Owner | Due |
|----|------|-------|-----|
| TODO-201 | Implement async execution | - | - |
| TODO-202 | Add database persistence | - | - |
| TODO-203 | Create MCP integration | - | - |
| TODO-204 | Build cockpit UI | - | - |

---

## 8. Invariant Verification Checklist

### 8.1 Core Invariants

| Invariant | Test | Status |
|-----------|------|--------|
| INV-STATE | Single state at any time | ✅ |
| INV-TRANSITION | Explicit transitions only | ✅ |
| INV-JURISDICTION | Policy check before execution | ✅ |
| INV-AUDIT | Entry before transition completes | ✅ |
| INV-HASH-CHAIN | Entries chain to previous | ✅ |
| INV-FAIL-CLOSED | Ambiguity → DENY/HALT | ✅ |
| INV-DETERMINISM | Same inputs → same outputs | ✅ |
| INV-HALT | Immediate halt available | ✅ |
| INV-EVIDENCE | Decisions exportable | ✅ |
| INV-NO-IMPLICIT-ALLOW | Explicit ALLOW required | ✅ |

### 8.2 Verification Commands

```bash
# Run invariant tests
python -m unittest tests.test_state_machine -v
python -m unittest tests.test_jurisdiction -v
python -m unittest tests.test_audit_ledger -v
python -m unittest tests.test_replay -v
python -m unittest tests.test_variants -v

# Run all tests
python -m unittest discover -s tests -v

# Run smoke test
./scripts/smoke.sh
```

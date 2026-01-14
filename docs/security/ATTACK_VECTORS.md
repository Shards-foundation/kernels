# Attack Vectors Analysis

**Version:** 0.1.0  
**Classification:** Security  
**Last Updated:** January 2025

---

## 1. Overview

This document catalogs potential attack vectors against KERNELS, their likelihood, impact, and mitigations. Use this for threat modeling and security testing.

---

## 2. Attack Vector Taxonomy

### 2.1 Categories

| Category | Description | Examples |
|----------|-------------|----------|
| Input Attacks | Malformed or malicious inputs | Injection, overflow |
| State Attacks | Manipulate kernel state | Race conditions, replay |
| Cryptographic Attacks | Break hash chain | Collision, preimage |
| Policy Attacks | Bypass jurisdiction | Privilege escalation |
| Evidence Attacks | Corrupt audit trail | Tampering, deletion |
| Availability Attacks | Deny service | DoS, resource exhaustion |

---

## 3. Detailed Attack Vectors

### 3.1 AV-001: Intent Injection

**Category:** Input Attack  
**Severity:** Medium  
**Likelihood:** Medium

**Description:**
Attacker crafts intent string to influence kernel behavior beyond stated purpose.

**Attack Scenario:**
```python
# Malicious request
request = Request(
    request_id="req-001",
    actor="attacker",
    intent="Read file /etc/passwd; also delete all logs",
    tool_call=ToolCall(name="read_file", params={"path": "/etc/passwd"}),
)
```

**Mitigation:**
- Intent is informational only, not executed
- Tool call params are validated separately
- Jurisdiction checks tool, not intent

**Status:** ✅ Mitigated by design

---

### 3.2 AV-002: Tool Parameter Injection

**Category:** Input Attack  
**Severity:** High  
**Likelihood:** Medium

**Description:**
Attacker injects malicious values in tool parameters to escape intended scope.

**Attack Scenario:**
```python
# Path traversal attempt
request = Request(
    request_id="req-001",
    actor="agent",
    intent="Read config file",
    tool_call=ToolCall(
        name="read_file",
        params={"path": "../../../etc/passwd"}
    ),
)
```

**Mitigation:**
- Tool implementations must validate params
- Kernel validates param structure, not content
- Use allow-lists for file paths

**Status:** ⚠️ Partial (tool implementation responsibility)

**Recommendation:**
```python
# Tool implementation with path validation
def read_file_tool(params):
    path = params["path"]
    
    # Normalize and validate path
    normalized = os.path.normpath(path)
    if not normalized.startswith(ALLOWED_BASE_PATH):
        raise SecurityError("Path outside allowed directory")
    
    return read_file(normalized)
```

---

### 3.3 AV-003: Actor Spoofing

**Category:** Policy Attack  
**Severity:** High  
**Likelihood:** Medium

**Description:**
Attacker claims to be a different actor to gain unauthorized access.

**Attack Scenario:**
```python
# Spoofed actor
request = Request(
    request_id="req-001",
    actor="admin-agent",  # Attacker claims admin identity
    intent="Delete all records",
    tool_call=ToolCall(name="delete_all", params={}),
)
```

**Mitigation:**
- External authentication required before kernel
- Actor identity verified at transport layer
- Kernel trusts authenticated actor claim

**Status:** ⚠️ Partial (authentication is external)

**Recommendation:**
```python
# Authentication wrapper
def authenticated_submit(kernel, request, auth_token):
    # Verify token
    verified_actor = verify_auth_token(auth_token)
    
    # Ensure actor matches
    if request.actor != verified_actor:
        raise AuthenticationError("Actor mismatch")
    
    return kernel.submit(request)
```

---

### 3.4 AV-004: State Race Condition

**Category:** State Attack  
**Severity:** Medium  
**Likelihood:** Low

**Description:**
Concurrent requests exploit race condition in state machine.

**Attack Scenario:**
```
Thread 1: submit(request_A) -> VALIDATING
Thread 2: submit(request_B) -> VALIDATING (should be blocked)
```

**Mitigation:**
- Single-threaded kernel by default
- State machine uses atomic transitions
- Multi-threaded deployments need locking

**Status:** ⚠️ Partial (single-threaded assumed)

**Recommendation:**
```python
# Thread-safe state machine
import threading

class ThreadSafeKernel:
    def __init__(self):
        self._lock = threading.Lock()
    
    def submit(self, request):
        with self._lock:
            return self._submit_internal(request)
```

---

### 3.5 AV-005: Audit Replay Attack

**Category:** Evidence Attack  
**Severity:** High  
**Likelihood:** Low

**Description:**
Attacker replays old audit entries to confuse verification.

**Attack Scenario:**
```python
# Attacker captures old evidence bundle
old_evidence = capture_evidence()

# Later, replays old entries
inject_entries(old_evidence["ledger_entries"])
```

**Mitigation:**
- Hash chain prevents insertion
- Timestamps detect old entries
- Root hash verification fails

**Status:** ✅ Mitigated by design

---

### 3.6 AV-006: Hash Collision Attack

**Category:** Cryptographic Attack  
**Severity:** Critical  
**Likelihood:** Very Low

**Description:**
Attacker finds collision in SHA-256 to forge audit entry.

**Attack Scenario:**
```
Find entry' where:
  SHA256(entry') = SHA256(original_entry)
  entry'.decision = ALLOW (instead of DENY)
```

**Mitigation:**
- SHA-256 has no known practical collisions
- Would require ~2^128 operations
- Computationally infeasible

**Status:** ✅ Mitigated by algorithm choice

---

### 3.7 AV-007: Evidence Spoofing

**Category:** Evidence Attack  
**Severity:** High  
**Likelihood:** Medium

**Description:**
Compromised sensor injects false evidence to influence decisions.

**Attack Scenario:**
```python
# Malicious sensor
fake_evidence = EvidencePacket(
    evidence_id="ev-001",
    sensor_id="compromised-sensor",
    payload={"status": "approved"},  # False claim
)
```

**Mitigation:**
- Sensors are untrusted by design
- Evidence requires signature verification
- Cross-validate with multiple sensors

**Status:** ⚠️ Partial (signature verification not implemented)

**Recommendation:**
```python
# Evidence signature verification
def verify_evidence(packet, trusted_keys):
    sensor_key = trusted_keys.get(packet.sensor_id)
    if not sensor_key:
        raise SecurityError("Unknown sensor")
    
    if not verify_signature(packet.payload, packet.signature, sensor_key):
        raise SecurityError("Invalid evidence signature")
    
    return True
```

---

### 3.8 AV-008: Permit Token Forgery

**Category:** Policy Attack  
**Severity:** Critical  
**Likelihood:** Low

**Description:**
Attacker forges permit token to execute unauthorized actions.

**Attack Scenario:**
```python
# Forged permit
fake_permit = PermitToken(
    permit_id="permit-fake",
    proposal_hash="...",
    allowed_tool="delete_all",
    signature="forged-signature",
)
```

**Mitigation:**
- Permits are HMAC-signed
- Workers verify signature before execution
- Secret key never exposed

**Status:** 🔲 Not implemented (spec only)

**Recommendation:**
```python
# Permit token signing
import hmac

def mint_permit(proposal, secret_key):
    payload = serialize_permit_payload(proposal)
    signature = hmac.new(
        secret_key.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return PermitToken(
        permit_id=generate_id(),
        proposal_hash=compute_hash(payload),
        signature=signature,
    )

def verify_permit(permit, secret_key):
    payload = serialize_permit_payload(permit)
    expected = hmac.new(
        secret_key.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(permit.signature, expected)
```

---

### 3.9 AV-009: Resource Exhaustion

**Category:** Availability Attack  
**Severity:** Medium  
**Likelihood:** Medium

**Description:**
Attacker floods kernel with requests to exhaust resources.

**Attack Scenario:**
```python
# Flood attack
for i in range(1000000):
    kernel.submit(Request(
        request_id=f"flood-{i}",
        actor="attacker",
        intent="x" * 10000,  # Large intent
    ))
```

**Mitigation:**
- Rate limiting per actor
- Request size limits
- Memory limits on ledger

**Status:** ⚠️ Partial (limits not enforced)

---

### 3.10 AV-010: Timing Side-Channel

**Category:** Cryptographic Attack  
**Severity:** Low  
**Likelihood:** Low

**Description:**
Attacker measures timing differences to infer information.

**Attack Scenario:**
```python
# Timing attack on hash comparison
for guess in possible_hashes:
    start = time.time()
    verify_hash(guess, target)
    elapsed = time.time() - start
    # Longer time = more matching bytes
```

**Mitigation:**
- Use constant-time comparison
- Avoid early-exit on mismatch

**Status:** ⚠️ Partial (not using constant-time compare)

---

## 4. Attack Surface Summary

| Vector | Severity | Likelihood | Status |
|--------|----------|------------|--------|
| AV-001 Intent Injection | Medium | Medium | ✅ Mitigated |
| AV-002 Param Injection | High | Medium | ⚠️ Partial |
| AV-003 Actor Spoofing | High | Medium | ⚠️ Partial |
| AV-004 State Race | Medium | Low | ⚠️ Partial |
| AV-005 Audit Replay | High | Low | ✅ Mitigated |
| AV-006 Hash Collision | Critical | Very Low | ✅ Mitigated |
| AV-007 Evidence Spoofing | High | Medium | ⚠️ Partial |
| AV-008 Permit Forgery | Critical | Low | 🔲 Not Impl |
| AV-009 Resource Exhaustion | Medium | Medium | ⚠️ Partial |
| AV-010 Timing Side-Channel | Low | Low | ⚠️ Partial |

---

## 5. Testing Recommendations

### 5.1 Security Test Cases

| Test | Vector | Method |
|------|--------|--------|
| Fuzz intent field | AV-001 | Fuzzing |
| Path traversal in params | AV-002 | Manual |
| Concurrent submissions | AV-004 | Load test |
| Replay old evidence | AV-005 | Integration |
| Large request flood | AV-009 | Load test |
| Timing measurement | AV-010 | Timing analysis |

### 5.2 Penetration Test Scope

| Area | In Scope | Out of Scope |
|------|----------|--------------|
| Kernel API | ✅ | |
| State machine | ✅ | |
| Audit ledger | ✅ | |
| Tool implementations | | ✅ |
| External auth | | ✅ |
| Network transport | | ✅ |

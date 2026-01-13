# Permit Token Specification

**Version:** 0.1.0

## 1. Overview

A **Permit Token** is a cryptographic authorization that workers MUST possess before executing any operation. The kernel mints permits; workers verify and consume them.

## 2. Design Principle

> No execution endpoint exists without jurisdiction validation.

Workers MUST refuse to execute without a valid permit token. This is enforced by wiring, not policy.

## 3. Permit Token Schema

### 3.1 Token Structure

```python
@dataclass
class PermitToken:
    # Identity
    permit_id: str              # Unique identifier (UUID v4)
    proposal_id: str            # Reference to originating proposal
    decision_receipt_id: str    # Reference to kernel decision
    
    # Authorization
    action_type: ActionType     # What action is permitted
    target: Target              # What resource can be acted upon
    parameters_hash: str        # SHA-256 of permitted parameters
    
    # Constraints
    valid_from_ms: int          # When permit becomes valid
    valid_until_ms: int         # When permit expires
    max_executions: int         # How many times permit can be used (usually 1)
    
    # Evidence binding
    evidence_hash: str          # Hash of evidence at decision time
    
    # Cryptographic integrity
    kernel_id: str              # Issuing kernel identifier
    issued_at_ms: int           # When permit was minted
    signature: str              # Kernel signature over permit data
```

### 3.2 Signature Computation

The permit signature MUST be computed as:

```python
def compute_permit_signature(permit: PermitToken, kernel_secret: bytes) -> str:
    """Compute HMAC-SHA256 signature over permit data."""
    data = serialize_deterministic({
        "permit_id": permit.permit_id,
        "proposal_id": permit.proposal_id,
        "decision_receipt_id": permit.decision_receipt_id,
        "action_type": permit.action_type.value,
        "target": asdict(permit.target),
        "parameters_hash": permit.parameters_hash,
        "valid_from_ms": permit.valid_from_ms,
        "valid_until_ms": permit.valid_until_ms,
        "max_executions": permit.max_executions,
        "evidence_hash": permit.evidence_hash,
        "kernel_id": permit.kernel_id,
        "issued_at_ms": permit.issued_at_ms,
    })
    return hmac.new(kernel_secret, data.encode(), hashlib.sha256).hexdigest()
```

## 4. Worker Verification

### 4.1 Verification Steps

Workers MUST verify permits before execution:

| Step | Check | Failure Action |
|------|-------|----------------|
| 1 | Signature valid | Reject immediately |
| 2 | `valid_from_ms` <= current_time | Reject (not yet valid) |
| 3 | `valid_until_ms` > current_time | Reject (expired) |
| 4 | `max_executions` > 0 | Reject (exhausted) |
| 5 | `action_type` matches requested action | Reject (wrong action) |
| 6 | `target` matches requested target | Reject (wrong target) |
| 7 | `parameters_hash` matches request params | Reject (params mismatch) |

### 4.2 Verification Result

```python
@dataclass
class PermitVerificationResult:
    valid: bool
    error: Optional[str]
    permit_id: Optional[str]
    remaining_executions: Optional[int]
```

### 4.3 Execution Decrement

After successful execution, workers MUST:

1. Decrement `max_executions` (if tracking state)
2. Record execution in local audit
3. Return execution result with permit reference

## 5. Permit Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                        KERNEL                                   │
│  Proposal ──▶ Arbitrate ──▶ ALLOW ──▶ Mint Permit              │
└─────────────────────────────────────────────────────────────────┘
                                           │
                                           │ PermitToken
                                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                        WORKER                                   │
│  Receive ──▶ Verify ──▶ Execute ──▶ Record ──▶ Return          │
└─────────────────────────────────────────────────────────────────┘
```

## 6. Security Properties

### 6.1 Guarantees

| Property | Mechanism |
|----------|-----------|
| Authenticity | HMAC signature from kernel |
| Integrity | Hash of parameters + evidence |
| Non-replayability | Unique permit_id + max_executions |
| Time-boundedness | valid_from_ms / valid_until_ms |
| Scope limitation | action_type + target constraints |

### 6.2 Attack Mitigations

| Attack | Mitigation |
|--------|------------|
| Permit forgery | HMAC signature verification |
| Parameter tampering | parameters_hash binding |
| Replay attack | max_executions + permit_id tracking |
| Time manipulation | Short validity windows |
| Scope escalation | Strict target matching |

## 7. Permit Token Format (Serialized)

For transmission, permits are serialized as base64-encoded JSON:

```python
def serialize_permit(permit: PermitToken) -> str:
    """Serialize permit for transmission."""
    data = asdict(permit)
    json_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return base64.urlsafe_b64encode(json_str.encode()).decode()

def deserialize_permit(token: str) -> PermitToken:
    """Deserialize permit from transmission format."""
    json_str = base64.urlsafe_b64decode(token.encode()).decode()
    data = json.loads(json_str)
    return PermitToken(**data)
```

## 8. Integration with MCP

When using MCP (Model Context Protocol) as the tool bus:

```python
# MCP tool definition with permit requirement
@mcp_tool
def browser_click(
    permit_token: str,  # Required: kernel-issued permit
    selector: str,
    # ... other params
) -> ClickResult:
    # Verify permit before any action
    result = verify_permit(permit_token, action="browser.click", ...)
    if not result.valid:
        raise PermitDeniedError(result.error)
    
    # Execute only with valid permit
    return execute_click(selector)
```

## 9. Example Permit Token

```json
{
  "permit_id": "660e8400-e29b-41d4-a716-446655440001",
  "proposal_id": "550e8400-e29b-41d4-a716-446655440000",
  "decision_receipt_id": "770e8400-e29b-41d4-a716-446655440002",
  "action_type": "write",
  "target": {
    "resource_type": "crm_record",
    "resource_id": "contact-12345",
    "domain": "salesforce.com",
    "constraints": {}
  },
  "parameters_hash": "a1b2c3d4e5f6...",
  "valid_from_ms": 1705171200000,
  "valid_until_ms": 1705171500000,
  "max_executions": 1,
  "evidence_hash": "f6e5d4c3b2a1...",
  "kernel_id": "kernel-prod-001",
  "issued_at_ms": 1705171200000,
  "signature": "9f8e7d6c5b4a..."
}
```

## 10. Relationship to Audit

Every permit issuance and consumption MUST be recorded:

| Event | Audit Entry |
|-------|-------------|
| Permit minted | Kernel audit: decision + permit_id |
| Permit verified | Worker audit: permit_id + result |
| Permit consumed | Worker audit: permit_id + execution result |
| Permit rejected | Worker audit: permit_id + rejection reason |

This creates a complete chain from proposal to execution.

# Proposal Specification

**Version:** 0.1.0

## 1. Overview

A **Proposal** is the structured input to the kernel's decision engine. Unlike free-form requests, proposals have bounded degrees of freedom and eliminate ambiguity at the first gate.

## 2. Design Principle

> Ambiguity dies when every request becomes a typed proposal with bounded degrees of freedom.

A proposal is **not** "user text". It is a structured object that the kernel can validate deterministically without interpretation.

## 3. Proposal Schema

### 3.1 Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `proposal_id` | string | Unique identifier (UUID v4 recommended) |
| `ts_ms` | integer | Creation timestamp in milliseconds |
| `actor` | string | Identity of the requesting actor |
| `action_type` | ActionType | Category of action requested |
| `target` | Target | Resource being acted upon |
| `parameters` | dict | Strictly typed, bounded parameters |

### 3.2 Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `preconditions` | list[Precondition] | What must be true in evidence |
| `risk_envelope` | RiskEnvelope | Allowed side effects |
| `rollback_semantics` | RollbackSpec | Recovery procedure if applicable |
| `time_window` | TimeWindow | Permit validity period |
| `approval_class` | ApprovalClass | Human approval requirements |
| `evidence_bindings` | list[EvidenceBinding] | Required evidence references |

### 3.3 ActionType Enumeration

```python
class ActionType(Enum):
    NAVIGATE = "navigate"      # Browser/UI navigation
    READ = "read"              # Data retrieval
    WRITE = "write"            # Data modification
    CREATE = "create"          # Resource creation
    DELETE = "delete"          # Resource deletion
    EXECUTE = "execute"        # Code/command execution
    COMMUNICATE = "communicate" # Email/message/notification
    TRANSACT = "transact"      # Financial transaction
    APPROVE = "approve"        # Approval workflow
    CUSTOM = "custom"          # Extension point
```

### 3.4 Target Structure

```python
@dataclass
class Target:
    resource_type: str      # e.g., "crm_record", "github_pr", "payment"
    resource_id: str        # Unique identifier within type
    domain: str             # e.g., "salesforce.com", "github.com"
    constraints: dict       # Type-specific constraints
```

### 3.5 Precondition Structure

```python
@dataclass
class Precondition:
    field: str              # Evidence field to check
    operator: str           # eq, ne, gt, lt, contains, matches
    value: Any              # Expected value
    evidence_ref: str       # Reference to evidence packet
```

### 3.6 RiskEnvelope Structure

```python
@dataclass
class RiskEnvelope:
    allowed_side_effects: list[str]  # Explicit list of permitted effects
    forbidden_effects: list[str]     # Explicit list of forbidden effects
    max_affected_records: int        # Upper bound on affected items
    reversible_required: bool        # Must be reversible
```

### 3.7 TimeWindow Structure

```python
@dataclass
class TimeWindow:
    valid_from_ms: int      # Permit becomes valid
    valid_until_ms: int     # Permit expires
    max_duration_ms: int    # Maximum execution time
```

### 3.8 ApprovalClass Enumeration

```python
class ApprovalClass(Enum):
    NONE = "none"           # No human approval required
    SINGLE = "single"       # One human approval required
    DUAL = "dual"           # Two independent approvals required
    THRESHOLD = "threshold" # N of M approvals required
```

## 4. Validation Rules

### 4.1 Structural Validation

The kernel MUST reject proposals that fail structural validation:

| Rule | Condition |
|------|-----------|
| V-PROP-001 | `proposal_id` must be non-empty string |
| V-PROP-002 | `ts_ms` must be positive integer |
| V-PROP-003 | `actor` must be non-empty string |
| V-PROP-004 | `action_type` must be valid ActionType |
| V-PROP-005 | `target` must have all required fields |
| V-PROP-006 | `parameters` must be serializable dict |

### 4.2 Semantic Validation

The kernel MUST reject proposals that fail semantic validation:

| Rule | Condition |
|------|-----------|
| V-PROP-010 | `time_window.valid_until_ms` must be > current time |
| V-PROP-011 | `time_window.valid_from_ms` must be <= `valid_until_ms` |
| V-PROP-012 | `risk_envelope.max_affected_records` must be > 0 |
| V-PROP-013 | All `preconditions` must reference valid evidence |
| V-PROP-014 | `approval_class` requirements must be satisfiable |

### 4.3 Fail-Closed Behavior

If a proposal cannot be constructed deterministically, the kernel MUST fail closed immediately. This is the "first gate" where ambiguity dies.

## 5. Token Efficiency

The proposal structure enables token efficiency:

| Benefit | Mechanism |
|---------|-----------|
| LLM produces one structured proposal | Instead of multi-turn conversation |
| Kernel validates structure, not vibes | Deterministic parsing |
| Everything downstream is mechanical | No interpretation required |

## 6. Example Proposal

```json
{
  "proposal_id": "550e8400-e29b-41d4-a716-446655440000",
  "ts_ms": 1705171200000,
  "actor": "agent-sales-001",
  "action_type": "write",
  "target": {
    "resource_type": "crm_record",
    "resource_id": "contact-12345",
    "domain": "salesforce.com",
    "constraints": {
      "allowed_fields": ["email", "phone", "notes"],
      "forbidden_fields": ["ssn", "credit_card"]
    }
  },
  "parameters": {
    "updates": {
      "email": "new@example.com",
      "notes": "Updated via automation"
    }
  },
  "preconditions": [
    {
      "field": "record_exists",
      "operator": "eq",
      "value": true,
      "evidence_ref": "evidence-001"
    }
  ],
  "risk_envelope": {
    "allowed_side_effects": ["audit_log_entry"],
    "forbidden_effects": ["email_notification", "workflow_trigger"],
    "max_affected_records": 1,
    "reversible_required": true
  },
  "time_window": {
    "valid_from_ms": 1705171200000,
    "valid_until_ms": 1705171500000,
    "max_duration_ms": 30000
  },
  "approval_class": "none"
}
```

## 7. Relationship to KernelRequest

`Proposal` is a more structured evolution of `KernelRequest`. For backward compatibility:

| KernelRequest Field | Proposal Equivalent |
|---------------------|---------------------|
| `request_id` | `proposal_id` |
| `ts_ms` | `ts_ms` |
| `actor` | `actor` |
| `intent` | Derived from `action_type` + `target` |
| `tool_call` | `action_type` + `parameters` |
| `params` | `parameters` |
| `evidence` | `evidence_bindings` |

The kernel MAY accept either format, with `Proposal` being the preferred, unambiguous format.

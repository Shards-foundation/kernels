# Evidence Packet Specification

**Version:** 0.1.0

## 1. Overview

An **Evidence Packet** is a structured observation produced by sensors. Evidence packets are inputs to the kernel's decision process, not outputs. Sensors observe; kernels decide.

## 2. Design Principle

> Sensors are untrusted. They produce evidence packets, not decisions.

Evidence packets capture what was observed, when, and by whom. The kernel uses evidence to inform decisions but MUST NOT trust evidence blindly.

## 3. Evidence Packet Schema

### 3.1 Core Structure

```python
@dataclass
class EvidencePacket:
    # Identity
    evidence_id: str            # Unique identifier (UUID v4)
    packet_type: EvidenceType   # Category of evidence
    
    # Source
    sensor_id: str              # Which sensor produced this
    sensor_type: str            # Type of sensor (browser, api, file, etc.)
    
    # Timing
    observed_at_ms: int         # When observation occurred
    received_at_ms: int         # When kernel received packet
    
    # Content
    payload: dict               # Type-specific observation data
    payload_hash: str           # SHA-256 of serialized payload
    
    # Context
    context: EvidenceContext    # Environmental context
    
    # Integrity
    sensor_signature: Optional[str]  # Sensor's signature (if available)
```

### 3.2 EvidenceType Enumeration

```python
class EvidenceType(Enum):
    # Browser/UI evidence
    DOM_SNAPSHOT = "dom_snapshot"
    URL_OBSERVATION = "url_observation"
    FORM_STATE = "form_state"
    SELECTION = "selection"
    
    # API evidence
    API_RESPONSE = "api_response"
    WEBHOOK_PAYLOAD = "webhook_payload"
    
    # File evidence
    FILE_HASH = "file_hash"
    DIFF_OBSERVATION = "diff_observation"
    
    # System evidence
    TIMESTAMP = "timestamp"
    ENVIRONMENT = "environment"
    
    # Human evidence
    APPROVAL = "approval"
    ATTESTATION = "attestation"
    
    # Composite
    AGGREGATE = "aggregate"
```

### 3.3 EvidenceContext Structure

```python
@dataclass
class EvidenceContext:
    # Location
    origin: str                 # e.g., "https://example.com"
    path: Optional[str]         # e.g., "/contacts/12345"
    
    # Session
    session_id: Optional[str]   # Browser/API session
    user_id: Optional[str]      # Authenticated user (if known)
    
    # Environment
    user_agent: Optional[str]   # Browser/client identifier
    ip_address: Optional[str]   # Source IP (if relevant)
    
    # Metadata
    tags: dict                  # Arbitrary key-value tags
```

## 4. Evidence Types (Detailed)

### 4.1 DOM Snapshot

Captures browser DOM state at a point in time.

```python
@dataclass
class DOMSnapshotPayload:
    url: str
    title: str
    html_hash: str              # Hash of full HTML
    selected_elements: list[dict]  # Key elements extracted
    form_values: dict           # Current form state
    viewport: dict              # Width, height, scroll position
```

### 4.2 API Response

Captures API call result.

```python
@dataclass
class APIResponsePayload:
    endpoint: str
    method: str
    status_code: int
    response_hash: str          # Hash of response body
    headers: dict               # Selected headers
    latency_ms: int
```

### 4.3 Approval Evidence

Captures human approval action.

```python
@dataclass
class ApprovalPayload:
    approver_id: str
    approval_type: str          # "single", "dual", "threshold"
    approved_proposal_id: str
    approval_timestamp_ms: int
    approval_signature: str     # Approver's signature
    conditions: Optional[dict]  # Any conditions attached
```

### 4.4 Diff Observation

Captures changes between states.

```python
@dataclass
class DiffPayload:
    before_hash: str
    after_hash: str
    diff_type: str              # "unified", "semantic", "structural"
    changes: list[dict]         # List of changes
    affected_paths: list[str]   # What was modified
```

## 5. Evidence Validation

### 5.1 Structural Validation

| Rule | Condition |
|------|-----------|
| V-EVID-001 | `evidence_id` must be non-empty string |
| V-EVID-002 | `packet_type` must be valid EvidenceType |
| V-EVID-003 | `sensor_id` must be non-empty string |
| V-EVID-004 | `observed_at_ms` must be positive integer |
| V-EVID-005 | `payload` must be non-null dict |
| V-EVID-006 | `payload_hash` must match computed hash |

### 5.2 Temporal Validation

| Rule | Condition |
|------|-----------|
| V-EVID-010 | `observed_at_ms` must be <= `received_at_ms` |
| V-EVID-011 | `observed_at_ms` must be within acceptable drift |
| V-EVID-012 | Evidence must not be stale (configurable threshold) |

### 5.3 Trust Validation

| Rule | Condition |
|------|-----------|
| V-EVID-020 | `sensor_id` must be in allowed sensor list |
| V-EVID-021 | `sensor_signature` must verify (if required) |
| V-EVID-022 | Evidence must not contradict other evidence |

## 6. Evidence Binding

### 6.1 Binding to Proposals

Proposals reference evidence via bindings:

```python
@dataclass
class EvidenceBinding:
    evidence_id: str            # Which evidence packet
    binding_type: str           # "precondition", "context", "attestation"
    required: bool              # Must evidence exist?
    freshness_ms: int           # Max age of evidence
```

### 6.2 Binding to Permits

Permits include evidence hash to ensure decisions are based on specific evidence:

```python
permit.evidence_hash = compute_hash([
    evidence_packet.payload_hash
    for evidence_packet in bound_evidence
])
```

## 7. Evidence Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                        SENSOR                                   │
│  Observe ──▶ Package ──▶ Sign (optional) ──▶ Transmit          │
└─────────────────────────────────────────────────────────────────┘
                                           │
                                           │ EvidencePacket
                                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                        KERNEL                                   │
│  Receive ──▶ Validate ──▶ Store ──▶ Bind to Proposal           │
└─────────────────────────────────────────────────────────────────┘
```

## 8. Sensor Types

### 8.1 Browser Extension Sensor

Captures DOM, URL, form state, selections from browser.

| Capability | Trust Level |
|------------|-------------|
| DOM observation | Low (can be spoofed) |
| URL capture | Medium |
| Form state | Low |
| User selection | Low |

### 8.2 API Gateway Sensor

Captures API requests and responses.

| Capability | Trust Level |
|------------|-------------|
| Request logging | High |
| Response capture | High |
| Timing data | High |

### 8.3 Webhook Collector

Receives and packages webhook payloads.

| Capability | Trust Level |
|------------|-------------|
| Payload capture | Medium (depends on source) |
| Signature verification | High (if signed) |

### 8.4 File Watcher

Monitors file system changes.

| Capability | Trust Level |
|------------|-------------|
| Change detection | High |
| Content hashing | High |
| Diff generation | High |

## 9. Example Evidence Packet

```json
{
  "evidence_id": "880e8400-e29b-41d4-a716-446655440003",
  "packet_type": "dom_snapshot",
  "sensor_id": "browser-ext-001",
  "sensor_type": "browser_extension",
  "observed_at_ms": 1705171190000,
  "received_at_ms": 1705171195000,
  "payload": {
    "url": "https://crm.example.com/contacts/12345",
    "title": "Contact Details - John Doe",
    "html_hash": "abc123...",
    "selected_elements": [
      {"selector": "#email", "value": "john@example.com"},
      {"selector": "#phone", "value": "+1-555-0123"}
    ],
    "form_values": {},
    "viewport": {"width": 1920, "height": 1080, "scroll_y": 0}
  },
  "payload_hash": "def456...",
  "context": {
    "origin": "https://crm.example.com",
    "path": "/contacts/12345",
    "session_id": "sess-789",
    "user_id": "user-456",
    "user_agent": "Mozilla/5.0...",
    "ip_address": null,
    "tags": {"campaign": "q1-outreach"}
  },
  "sensor_signature": "ghi789..."
}
```

## 10. Security Considerations

### 10.1 Sensor Compromise

Sensors operate in hostile territory (browser, external systems). Assume:

| Assumption | Mitigation |
|------------|------------|
| Sensors can be compromised | Cross-validate with multiple sensors |
| Evidence can be spoofed | Require signatures, check consistency |
| Timing can be manipulated | Use server-side timestamps |
| Payloads can be tampered | Hash verification |

### 10.2 Evidence Freshness

Stale evidence is dangerous. The kernel SHOULD:

1. Reject evidence older than configured threshold
2. Re-request evidence if proposal requires fresh data
3. Log staleness warnings for audit

### 10.3 Evidence Conflicts

When evidence packets conflict:

1. Log the conflict
2. Fail closed (DENY)
3. Require human resolution

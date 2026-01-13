# Four Planes Architecture

**Version:** 0.1.0

## 1. Overview

KERNELS operates across four distinct planes. Each plane has one job. Mixing responsibilities creates ambiguity.

## 2. The Core Mistake to Avoid

> **Mistake:** Treating transport mechanisms (MCP, webhooks, APIs, extensions) as architectural peers to governance topology (kernel, sensors, workers, cockpit).

> **Fix:** Treat MCP/webhooks/API/extensions as transport + adapters, not core architecture.

## 3. The Four Planes

### 3.1 Plane 1: Governance Plane (Kernel)

**One job: Decide.**

| Component | Responsibility |
|-----------|----------------|
| Proposal schema | Canonical input format |
| Evidence schema | Canonical observation format |
| Jurisdiction rules | Policy enforcement |
| Decision receipts | Canonical output format |
| Ledger | Append-only, hash-chained audit |

**Hard constraints:**

- No network calls
- No DOM access
- No webhooks
- No LLM calls
- No filesystem (except ledger append through interface)

> If your kernel talks to the internet, it's not a kernel — it's an agent.

### 3.2 Plane 2: Execution Plane (Workers)

**One job: Do.**

| Component | Responsibility |
|-----------|----------------|
| MCP server(s) | Tool discovery and invocation |
| Webhook actuators | Outbound webhook calls |
| API executors | External API integration |
| Browser automation | DOM manipulation |
| Job runners | Background task execution |

**Hard rule:** Workers execute **only** with a valid permit token minted by kernel.

```
Worker receives request
    │
    ▼
Verify permit token ──▶ Invalid? ──▶ REJECT
    │
    │ Valid
    ▼
Execute operation
    │
    ▼
Record execution audit
    │
    ▼
Return result with permit reference
```

### 3.3 Plane 3: Perception Plane (Sensors)

**One job: Observe.**

| Component | Responsibility |
|-----------|----------------|
| Browser extension | DOM, URL, form, selection capture |
| Webhook collectors | Inbound webhook receipt |
| API gateway observers | Request/response logging |
| Telemetry collection | System metrics |
| Diff capture | Change detection |

**Hard rule:** Sensors do **not** act. They only observe and package.

Sensors produce evidence packets. They never:

- Mint permits
- Store long-lived secrets
- Make decisions
- Execute actions

> The browser extension is hostile territory.

### 3.4 Plane 4: Operations Plane (Cockpit + CI/CD)

**One job: Make it safe to run in the real world.**

| Component | Responsibility |
|-----------|----------------|
| Status dashboards | State visibility |
| Approvals UI | Human decision interface |
| Incident replay | Post-hoc analysis |
| Test harness | Deterministic verification |
| PR checks | Lint, SAST/DAST, threat gates |

The cockpit is trusted only for display and approvals. It is **not** an executor.

**Hard rule:** Cockpit cannot bypass kernel. Ever.

## 4. Plane Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                    OPERATIONS PLANE                             │
│         (Cockpit, CI/CD, Testing, Monitoring)                   │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Approvals  │  │  Dashboard  │  │   Replay    │             │
│  │     UI      │  │             │  │   Viewer    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
         │                                      ▲
         │ Approval                             │ Status
         ▼                                      │
┌─────────────────────────────────────────────────────────────────┐
│                    GOVERNANCE PLANE                             │
│                       (Kernel)                                  │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Proposal   │  │ Jurisdiction│  │   Audit     │             │
│  │  Validator  │  │   Engine    │  │   Ledger    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
         │                                      ▲
         │ Permit Token                         │ Evidence Packet
         ▼                                      │
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTION PLANE                              │
│                      (Workers)                                  │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │    MCP      │  │   Webhook   │  │   Browser   │             │
│  │   Server    │  │  Actuator   │  │   Driver    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
         │                                      ▲
         │ Action                               │ Observation
         ▼                                      │
┌─────────────────────────────────────────────────────────────────┐
│                    PERCEPTION PLANE                             │
│                      (Sensors)                                  │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Browser    │  │   Webhook   │  │    File     │             │
│  │ Extension   │  │  Collector  │  │   Watcher   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

## 5. Transport Layer (Not a Plane)

MCP, webhooks, APIs, and extensions are **transport mechanisms**, not architectural components.

| Transport | Used By | Purpose |
|-----------|---------|---------|
| MCP | Execution Plane | Tool bus for workers |
| Webhooks (outbound) | Execution Plane | External system actuation |
| Webhooks (inbound) | Perception Plane | Event collection |
| REST API | All planes | Inter-plane communication |
| Browser Extension | Perception Plane | DOM observation |

### 5.1 MCP as Tool Bus

MCP is the tool bus for the Execution Plane. Use it for:

- Tool discovery
- Standardized calls
- Runtime integration with LLM clients

But MCP MUST be permit-gated:

```python
# MCP tool with permit requirement
@mcp_tool
def browser_click(permit_token: str, selector: str) -> ClickResult:
    # Verify permit before any action
    if not verify_permit(permit_token):
        raise PermitDeniedError()
    return execute_click(selector)
```

## 6. Data Flow

### 6.1 Normal Flow

```
1. Sensor observes state
2. Sensor produces EvidencePacket
3. EvidencePacket sent to Kernel
4. Agent produces Proposal (referencing evidence)
5. Kernel validates Proposal
6. Kernel checks Jurisdiction
7. Kernel produces Decision
8. If ALLOW: Kernel mints PermitToken
9. PermitToken sent to Worker
10. Worker verifies PermitToken
11. Worker executes action
12. Worker returns result
13. Kernel records audit entry
14. Cockpit displays status
```

### 6.2 Approval Flow

```
1-4. Same as normal flow
5. Kernel determines approval required
6. Kernel produces HOLD decision
7. Cockpit displays approval request
8. Human reviews in Cockpit
9. Human approves/rejects
10. Approval evidence sent to Kernel
11-14. Continue normal flow (if approved)
```

## 7. Invariants Per Plane

### 7.1 Governance Plane Invariants

| Invariant | Enforcement |
|-----------|-------------|
| INV-STATE | Kernel state machine |
| INV-TRANSITION | Transition functions |
| INV-JURISDICTION | Policy engine |
| INV-AUDIT | Ledger append |
| INV-HASH-CHAIN | Hash computation |
| INV-FAIL-CLOSED | Default deny |
| INV-DETERMINISM | Pure functions |

### 7.2 Execution Plane Invariants

| Invariant | Enforcement |
|-----------|-------------|
| INV-NO-IMPLICIT-ALLOW | Permit verification |
| INV-EVIDENCE | Execution audit |

### 7.3 Perception Plane Invariants

| Invariant | Enforcement |
|-----------|-------------|
| INV-EVIDENCE | Evidence packaging |

### 7.4 Operations Plane Invariants

| Invariant | Enforcement |
|-----------|-------------|
| INV-HALT | Halt button |
| INV-EVIDENCE | Replay viewer |

## 8. Implementation Order

Build in this order to prevent unsecurable architecture:

### Phase 1: Kernel MVP (No MCP, No Extension)

- Proposal schema
- Jurisdiction rules
- Decision receipts
- Append-only ledger
- CLI replay auditor

### Phase 2: One Worker + One Sensor

- Worker: HTTP API executor or GitHub PR executor
- Sensor: API gateway collector or Git diff packager
- Cockpit: Minimal UI/CLI for approvals

### Phase 3: Add MCP + Browser Extension

- Only after permit model is correct
- MCP as permit-gated tool bus
- Extension as evidence-only sensor

This order prevents building an unsecurable mess.

## 9. Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Pattern |
|--------------|----------------|-----------------|
| Kernel calls external APIs | Kernel becomes agent | Workers call APIs |
| Extension makes decisions | Hostile territory | Extension only observes |
| Cockpit executes actions | Bypass risk | Cockpit only approves |
| Worker accepts raw input | No jurisdiction | Worker requires permit |
| Sensor stores secrets | Compromise risk | Secrets in kernel only |

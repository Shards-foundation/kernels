# KERNELS

**Deterministic Control Planes for AI Systems**

A kernel is a deterministic state machine that governs all AI agent execution through explicit jurisdiction, append-only audit, and fail-closed semantics.

**Hard Constraint:** No agent action occurs without kernel arbitration; no arbitration occurs without audit.

---

## The Failure Mode

Systems that deploy AI agents without deterministic control planes exhibit the following failure characteristics:

1. **Ambiguity Propagation.** Requests with undefined intent propagate through execution layers, producing outputs that cannot be traced to explicit decisions.

2. **Non-Deterministic State.** Agent state evolves through implicit transitions, making post-hoc analysis impossible and replay infeasible.

3. **Unbounded Execution.** Without jurisdiction enforcement, agents invoke tools outside sanctioned boundaries, violating operator constraints.

4. **Audit Gaps.** Systems that log opportunistically produce incomplete records. When failures occur, root cause analysis fails due to missing state transitions.

5. **Authority Diffusion.** Without explicit human-authority checkpoints, decision provenance becomes untraceable. Accountability collapses.

These are not theoretical risks. They are the default behavior of systems that treat AI agents as autonomous actors rather than governed executors.

---

## The Kernel Model

The kernel sits between operators (humans with authority) and agents (AI systems that execute). It enforces jurisdiction, manages state, and produces immutable audit records.

```
┌─────────────────────────────────────────────────────────────────┐
│                         OPERATOR                                │
│                    (Human Authority)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ KernelRequest
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          KERNEL                                 │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │   STATE   │  │JURISDICTION│  │ EXECUTION │  │   AUDIT   │    │
│  │  MACHINE  │  │   POLICY   │  │DISPATCHER │  │  LEDGER   │    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
│         │              │              │              │          │
│         └──────────────┴──────────────┴──────────────┘          │
│                              │                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ ToolCall (if ALLOW)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TOOL REGISTRY                              │
│              (Sandboxed, Deterministic Tools)                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ ToolResult
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          AGENT                                  │
│               (Receives result, no direct tool access)          │
└─────────────────────────────────────────────────────────────────┘
```

**Separation of Concerns:**

| Component     | Responsibility                                      | Authority Level |
|---------------|-----------------------------------------------------|-----------------|
| Operator      | Defines policy, reviews audit, issues halt commands | Highest         |
| Kernel        | Enforces policy, manages state, produces audit      | Delegated       |
| Tool Registry | Executes sanctioned operations                      | None (passive)  |
| Agent         | Submits requests, receives results                  | None            |

---

## Core Invariants

The following invariants MUST hold for any compliant kernel implementation:

1. **INV-STATE:** The kernel MUST be in exactly one defined state at any time.

2. **INV-TRANSITION:** State transitions MUST occur only through defined transition functions. No implicit state changes.

3. **INV-JURISDICTION:** Every request MUST pass jurisdiction checks before execution. Requests that fail jurisdiction MUST be denied.

4. **INV-AUDIT:** Every state transition MUST produce an append-only audit entry before the transition completes.

5. **INV-HASH-CHAIN:** Audit entries MUST be hash-chained. Each entry includes the hash of the previous entry.

6. **INV-FAIL-CLOSED:** Ambiguous, malformed, or unhandled requests MUST result in DENY or HALT. The kernel MUST NOT proceed under uncertainty.

7. **INV-DETERMINISM:** Given identical inputs and initial state, the kernel MUST produce identical outputs and final state.

8. **INV-HALT:** The kernel MUST support immediate halt from any state. Halt is irrevocable within a session.

9. **INV-EVIDENCE:** All decisions MUST be exportable as an evidence bundle with verifiable hash chain.

10. **INV-NO-IMPLICIT-ALLOW:** The absence of a DENY is not an ALLOW. Explicit ALLOW decisions are required for execution.

---

## State Machine

### Defined States

| State       | Description                                              |
|-------------|----------------------------------------------------------|
| BOOTING     | Kernel initializing, loading configuration               |
| IDLE        | Ready to accept requests                                 |
| VALIDATING  | Checking request structure and required fields           |
| ARBITRATING | Evaluating jurisdiction policy and ambiguity heuristics  |
| EXECUTING   | Dispatching tool call (if approved)                      |
| AUDITING    | Writing audit entry for completed operation              |
| HALTED      | Terminal state, no further operations permitted          |

### Allowed Transitions

```
BOOTING ──────────────────────────────────────────► IDLE
                                                      │
                                                      ▼
                                                 VALIDATING
                                                      │
                                           ┌──────────┴──────────┐
                                           ▼                     ▼
                                      ARBITRATING ────────────► HALTED
                                           │
                              ┌────────────┴────────────┐
                              ▼                         ▼
                         EXECUTING                   HALTED
                              │
                              ▼
                          AUDITING
                              │
                              ▼
                            IDLE
```

**Fail-Closed Behavior:**

- Invalid request structure → DENY, transition to AUDITING, then IDLE
- Jurisdiction failure → DENY, transition to AUDITING, then IDLE
- Ambiguity detected → DENY or HALT (configurable)
- Tool execution failure → FAIL, transition to AUDITING, then IDLE
- Any unhandled exception → HALT

---

## Execution Flow

A request proceeds through the following deterministic sequence:

1. **RECEIVE.** Kernel in IDLE receives `KernelRequest` via `submit()`.

2. **VALIDATE.** Kernel transitions to VALIDATING. Request structure is checked:
   - Required fields present
   - Types correct
   - Serialization within bounds

3. **ARBITRATE.** Kernel transitions to ARBITRATING. Jurisdiction policy evaluated:
   - Actor in allowed set
   - Tool (if specified) in allowed set
   - Ambiguity heuristics pass
   - Required evidence present (variant-dependent)

4. **DECIDE.** Kernel produces `Decision`: ALLOW, DENY, or HALT.

5. **EXECUTE.** If ALLOW and tool_call present, kernel transitions to EXECUTING:
   - Tool resolved from registry
   - Parameters validated
   - Tool invoked synchronously
   - Result captured

6. **AUDIT.** Kernel transitions to AUDITING:
   - Audit entry constructed
   - Entry hash computed
   - Entry appended to ledger
   - Hash chain extended

7. **RETURN.** Kernel transitions to IDLE. `KernelReceipt` returned to caller.

8. **EXPORT.** At any time, `export_evidence()` produces `EvidenceBundle` with full ledger and root hash.

---

## What This System Refuses To Do

This is a control plane. It is not:

- **An LLM wrapper.** The kernel does not call language models. It governs systems that may include them.

- **A prompt engineering framework.** The kernel does not manipulate prompts. It validates requests.

- **An agent framework.** The kernel does not define agent behavior. It constrains agent execution.

- **An alignment solution.** The kernel does not solve value alignment. It enforces operational boundaries.

- **An autonomous system.** The kernel does not make decisions on behalf of humans. It executes decisions humans have encoded in policy.

- **A permissions system.** The kernel is not RBAC. Jurisdiction is about execution boundaries, not identity management.

- **A monitoring dashboard.** The kernel produces audit logs. Visualization is out of scope.

The kernel does one thing: deterministic arbitration of AI agent requests with immutable audit.

---

## Repository Structure

```
.
├── README.md                 # This document
├── LICENSE                   # MIT License
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
├── SECURITY.md               # Vulnerability reporting
├── CODE_OF_CONDUCT.md        # Community standards
├── pyproject.toml            # Package metadata
├── scripts/
│   ├── run_tests.sh          # Test runner
│   └── smoke.sh              # Smoke test
├── docs/
│   ├── ARCHITECTURE.md       # System architecture
│   ├── THREAT_MODEL.md       # Security analysis
│   └── FAQ.md                # Common questions
├── spec/
│   ├── SPEC.md               # Normative specification
│   ├── GLOSSARY.md           # Term definitions
│   ├── STATES.md             # State machine spec
│   ├── JURISDICTION.md       # Jurisdiction rules
│   ├── AUDIT.md              # Audit ledger spec
│   ├── ERROR_MODEL.md        # Error taxonomy
│   └── VARIANTS.md           # Kernel variants
├── examples/
│   ├── 01_minimal_request.py
│   ├── 02_tool_execution.py
│   ├── 03_fail_closed_ambiguity.py
│   ├── 04_external_audit_replay.py
│   └── 05_variant_comparison.py
├── kernels/
│   ├── __init__.py
│   ├── _version.py
│   ├── __main__.py           # CLI entrypoint
│   ├── common/               # Shared types, errors, utilities
│   ├── audit/                # Ledger and replay
│   ├── jurisdiction/         # Policy and rules
│   ├── state/                # State machine
│   ├── execution/            # Tool dispatch
│   └── variants/             # Kernel implementations
└── tests/                    # Unit tests
```

**Directory-to-Invariant Mapping:**

| Directory            | Enforces Invariant(s)                    |
|----------------------|------------------------------------------|
| `kernels/state/`     | INV-STATE, INV-TRANSITION                |
| `kernels/jurisdiction/` | INV-JURISDICTION, INV-FAIL-CLOSED     |
| `kernels/audit/`     | INV-AUDIT, INV-HASH-CHAIN, INV-EVIDENCE  |
| `kernels/execution/` | INV-DETERMINISM, INV-NO-IMPLICIT-ALLOW   |
| `kernels/variants/`  | All invariants (variant-specific tuning) |

---

## Versioning and Stability

This project follows Semantic Versioning with the following interpretation:

| Version | Meaning                                                        |
|---------|----------------------------------------------------------------|
| 0.x.y   | Development. API may change. Invariants stable.                |
| 1.0.0   | Stable API. Invariants frozen. Breaking changes require 2.0.0. |
| x.y.z   | x = breaking, y = features, z = fixes                          |

**What Constitutes a Breaking Change:**

- Removal or modification of any invariant
- Change to state machine transitions
- Change to audit entry schema
- Change to `Kernel` protocol methods
- Change to `KernelRequest` or `KernelReceipt` fields

**What Does Not Constitute a Breaking Change:**

- Addition of new kernel variants
- Addition of new tools to registry
- Performance improvements
- Additional validation rules (stricter is non-breaking)

---

## Quickstart

```bash
# Clone repository
git clone https://github.com/your-org/kernels.git
cd kernels

# Run tests
python -m unittest discover -s tests -v

# Run smoke test
bash scripts/smoke.sh

# Run example
python examples/01_minimal_request.py

# CLI help
python -m kernels --help
```

### Examples

| Example                          | Demonstrates                              |
|----------------------------------|-------------------------------------------|
| `01_minimal_request.py`          | Basic request/receipt cycle               |
| `02_tool_execution.py`           | Tool invocation through kernel            |
| `03_fail_closed_ambiguity.py`    | Ambiguity detection and denial            |
| `04_external_audit_replay.py`    | Evidence export and replay verification   |
| `05_variant_comparison.py`       | Behavior differences across variants      |

---

## License

MIT License. See `LICENSE` file.

## Governance

This repository is maintained with the following authority boundaries:

- **Specification changes** require explicit review and version bump
- **Invariant changes** require major version bump and migration guide
- **Variant additions** are welcomed via pull request
- **Tool additions** must not introduce non-determinism

No individual maintainer has authority to modify invariants without documented consensus.

# Kernel Variants Specification

**Version:** 0.1.0

## 1. Overview

Kernel variants are implementations of the Kernel protocol with different enforcement postures. All variants MUST satisfy core invariants while differing in specific behaviors.

## 2. Variant Requirements

### 2.1 Common Requirements

All variants MUST:
- Implement the Kernel protocol completely
- Satisfy all ten core invariants
- Produce valid audit entries
- Support halt from any non-terminal state
- Export valid evidence bundles

### 2.2 Variant-Specific Behavior

Variants MAY differ in:
- Ambiguity detection thresholds
- Additional request requirements
- Policy defaults
- Intent length limits

## 3. Strict Kernel

### 3.1 Description

The strict kernel enforces maximum constraints with no tolerance for ambiguity.

### 3.2 Configuration

| Setting              | Value | Modifiable |
|----------------------|-------|------------|
| fail_closed          | true  | No         |
| require_jurisdiction | true  | No         |
| require_audit        | true  | No         |
| max_intent_length    | 4096  | Yes        |

### 3.3 Behavior

- Uses strict ambiguity detection
- Requires tool_call for tool execution
- Denies all ambiguous requests
- No special request requirements

### 3.4 Use Cases

- High-security environments
- Regulated industries
- Systems requiring maximum auditability

## 4. Permissive Kernel

### 4.1 Description

The permissive kernel has relaxed constraints while maintaining determinism.

### 4.2 Configuration

| Setting              | Value | Modifiable |
|----------------------|-------|------------|
| fail_closed          | true  | Yes        |
| require_jurisdiction | true  | Yes        |
| require_audit        | true  | Yes        |
| max_intent_length    | 8192  | Yes        |
| allow_intent_only    | true  | Yes        |

### 4.3 Behavior

- Uses relaxed ambiguity detection
- Accepts intent-only requests (no tool_call)
- Higher intent length limits
- Default policy allows all actors and tools

### 4.4 Use Cases

- Development environments
- Low-risk operations
- Rapid prototyping

## 5. Evidence-First Kernel

### 5.1 Description

The evidence-first kernel requires evidence for all allowed operations.

### 5.2 Configuration

| Setting              | Value | Modifiable |
|----------------------|-------|------------|
| fail_closed          | true  | No         |
| require_jurisdiction | true  | No         |
| require_audit        | true  | No         |
| max_intent_length    | 4096  | Yes        |

### 5.3 Additional Requirements

Every request MUST include the `evidence` field:
- evidence MUST be a non-empty string
- evidence MUST describe the justification for the request

### 5.4 Behavior

- Denies requests without evidence field
- Denies requests with empty evidence
- Records evidence_hash in audit entries
- Emphasizes comprehensive audit trail

### 5.5 Use Cases

- Compliance-heavy environments
- Operations requiring justification
- Audit-focused systems

## 6. Dual-Channel Kernel

### 6.1 Description

The dual-channel kernel requires both intent and structured constraints.

### 6.2 Configuration

| Setting              | Value | Modifiable |
|----------------------|-------|------------|
| fail_closed          | true  | No         |
| require_jurisdiction | true  | No         |
| require_audit        | true  | No         |
| max_intent_length    | 4096  | Yes        |

### 6.3 Additional Requirements

Every request MUST include a `constraints` dict in params with:

| Key              | Type   | Required | Description                    |
|------------------|--------|----------|--------------------------------|
| scope            | string | Yes      | Boundaries of the operation    |
| non_goals        | string | Yes      | What the operation will NOT do |
| success_criteria | string | Yes      | How success is measured        |

### 6.4 Behavior

- Denies requests without constraints dict
- Denies requests with missing constraint keys
- Denies requests with empty constraint values
- Produces richer audit entries with constraint context

### 6.5 Use Cases

- Complex operations requiring explicit boundaries
- Multi-stakeholder environments
- Operations with clear success criteria

## 7. Variant Comparison

| Feature                | Strict | Permissive | Evidence-First | Dual-Channel |
|------------------------|--------|------------|----------------|--------------|
| Fail-closed            | Always | Default    | Always         | Always       |
| Ambiguity detection    | Strict | Relaxed    | Strict         | Strict       |
| Intent-only requests   | No     | Yes        | No             | No           |
| Evidence required      | No     | No         | Yes            | No           |
| Constraints required   | No     | No         | No             | Yes          |
| Max intent length      | 4096   | 8192       | 4096           | 4096         |

## 8. Compatibility

### 8.1 Request Compatibility

A request valid for one variant may not be valid for another:

| Request Type           | Strict | Permissive | Evidence-First | Dual-Channel |
|------------------------|--------|------------|----------------|--------------|
| Basic with tool_call   | Valid  | Valid      | Invalid*       | Invalid**    |
| Intent-only            | Valid  | Valid      | Invalid*       | Invalid**    |
| With evidence          | Valid  | Valid      | Valid          | Invalid**    |
| With constraints       | Valid  | Valid      | Invalid*       | Valid        |
| With both              | Valid  | Valid      | Valid          | Valid        |

\* Requires evidence field  
\** Requires constraints dict

### 8.2 Audit Compatibility

All variants produce compatible audit entries:
- Same schema
- Same hash algorithm
- Same chain structure
- Verifiable by same replay algorithm

### 8.3 Evidence Bundle Compatibility

Evidence bundles from all variants:
- Use same structure
- Are verifiable by same algorithm
- Include variant identifier for context

## 9. Creating Custom Variants

### 9.1 Requirements

Custom variants MUST:
1. Extend BaseKernel
2. Implement Kernel protocol
3. Satisfy all core invariants
4. Document enforcement posture
5. Include tests

### 9.2 Extension Points

Custom variants MAY override:
- `_is_strict_ambiguity()` - ambiguity detection mode
- `_check_variant_requirements()` - additional request checks
- `boot()` - configuration enforcement

### 9.3 Prohibited Modifications

Custom variants MUST NOT:
- Modify state machine transitions
- Skip audit entry creation
- Allow implicit execution
- Bypass jurisdiction checks

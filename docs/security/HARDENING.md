# KERNELS Hardening Guide

**Version:** 0.1.0  
**Classification:** Security  
**Last Updated:** January 2025

---

## 1. Overview

This guide provides security hardening recommendations for KERNELS deployments. Follow these guidelines to maximize security posture in production environments.

---

## 2. Hardening Checklist

### 2.1 Pre-Deployment

| Item | Priority | Status |
|------|----------|--------|
| Review jurisdiction policy | P0 | 🔲 |
| Configure allowed actors | P0 | 🔲 |
| Configure allowed tools | P0 | 🔲 |
| Set appropriate kernel variant | P0 | 🔲 |
| Enable audit persistence | P0 | 🔲 |
| Configure rate limits | P1 | 🔲 |
| Set up monitoring | P1 | 🔲 |
| Configure alerting | P1 | 🔲 |

### 2.2 Runtime

| Item | Priority | Status |
|------|----------|--------|
| Monitor decision patterns | P0 | 🔲 |
| Review audit logs daily | P0 | 🔲 |
| Verify hash chain integrity | P1 | 🔲 |
| Check for anomalous deny rates | P1 | 🔲 |
| Review evidence freshness | P2 | 🔲 |

### 2.3 Maintenance

| Item | Priority | Status |
|------|----------|--------|
| Update dependencies | P1 | 🔲 |
| Rotate secrets (if applicable) | P1 | 🔲 |
| Review and update policies | P2 | 🔲 |
| Conduct periodic security review | P2 | 🔲 |

---

## 3. Kernel Variant Selection

### 3.1 Decision Matrix

| Use Case | Recommended Variant | Rationale |
|----------|---------------------|-----------|
| Production, high-risk | StrictKernel | Maximum enforcement |
| Production, low-risk | StrictKernel | Default to strict |
| Development | PermissiveKernel | Faster iteration |
| Audit-heavy | EvidenceFirstKernel | Evidence required |
| Structured workflows | DualChannelKernel | Constraints required |

### 3.2 Variant Configuration

```python
# Production configuration
from kernels import StrictKernel, JurisdictionPolicy

policy = JurisdictionPolicy(
    allowed_actors=["production-agent-001"],
    allowed_tools=["read_file", "write_file", "send_email"],
    require_tool_call=True,  # Strict: require explicit tool
)

kernel = StrictKernel(
    kernel_id="prod-kernel-001",
    policy=policy,
)
```

---

## 4. Jurisdiction Policy Hardening

### 4.1 Principle of Least Privilege

```python
# BAD: Overly permissive
policy = JurisdictionPolicy(
    allowed_actors=["*"],  # Never use wildcards
    allowed_tools=["*"],   # Never use wildcards
)

# GOOD: Explicit allow list
policy = JurisdictionPolicy(
    allowed_actors=[
        "agent-sales-001",
        "agent-support-001",
    ],
    allowed_tools=[
        "read_customer",
        "update_ticket",
    ],
)
```

### 4.2 Tool Scoping

```python
# Define tools with minimal scope
tools = {
    "read_customer": {
        "description": "Read customer record by ID",
        "params": ["customer_id"],
        "scope": "read-only",
    },
    "update_ticket": {
        "description": "Update support ticket status",
        "params": ["ticket_id", "status"],
        "scope": "write-limited",
    },
}
```

### 4.3 Actor Verification

```python
# Verify actor identity before submission
def submit_request(kernel, request, actor_token):
    # Validate actor token
    if not verify_actor_token(actor_token):
        raise AuthenticationError("Invalid actor token")
    
    # Verify actor matches request
    if request.actor != get_actor_from_token(actor_token):
        raise AuthorizationError("Actor mismatch")
    
    return kernel.submit(request)
```

---

## 5. Audit Hardening

### 5.1 Ledger Integrity

```python
# Periodically verify ledger integrity
from kernels import replay_and_verify

def verify_ledger_integrity(kernel):
    evidence = kernel.export_evidence()
    entries = evidence["ledger_entries"]
    root_hash = evidence["root_hash"]
    
    is_valid, errors = replay_and_verify(entries, root_hash)
    
    if not is_valid:
        # CRITICAL: Ledger compromised
        kernel.halt()
        alert_security_team(errors)
        raise SecurityError("Ledger integrity violation")
    
    return True
```

### 5.2 Evidence Preservation

```python
# Export and archive evidence regularly
import json
from datetime import datetime

def archive_evidence(kernel, archive_path):
    evidence = kernel.export_evidence()
    
    filename = f"evidence_{datetime.utcnow().isoformat()}.json"
    filepath = f"{archive_path}/{filename}"
    
    with open(filepath, "w") as f:
        json.dump(evidence, f, indent=2)
    
    # Compute and store archive hash
    archive_hash = compute_file_hash(filepath)
    store_archive_hash(filename, archive_hash)
    
    return filepath
```

### 5.3 Tamper Detection

```python
# Monitor for ledger tampering
def detect_tampering(kernel, last_known_hash):
    evidence = kernel.export_evidence()
    current_hash = evidence["root_hash"]
    entry_count = len(evidence["ledger_entries"])
    
    # Check for unexpected hash changes
    if entry_count > 0:
        # Verify chain from last known state
        if not verify_chain_continuity(last_known_hash, evidence):
            alert_security_team("Possible ledger tampering detected")
            return False
    
    return True
```

---

## 6. Input Validation Hardening

### 6.1 Request Size Limits

```python
# Enforce request size limits
MAX_INTENT_LENGTH = 1000
MAX_PARAMS_SIZE = 10000  # bytes

def validate_request_size(request):
    if len(request.intent) > MAX_INTENT_LENGTH:
        raise ValidationError(f"Intent exceeds {MAX_INTENT_LENGTH} chars")
    
    params_size = len(json.dumps(request.tool_call.params))
    if params_size > MAX_PARAMS_SIZE:
        raise ValidationError(f"Params exceed {MAX_PARAMS_SIZE} bytes")
```

### 6.2 Content Sanitization

```python
# Sanitize inputs before processing
import re

def sanitize_intent(intent: str) -> str:
    # Remove control characters
    intent = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', intent)
    
    # Normalize whitespace
    intent = ' '.join(intent.split())
    
    return intent
```

### 6.3 Type Enforcement

```python
# Strict type checking
from typing import get_type_hints

def validate_types(obj, expected_type):
    hints = get_type_hints(expected_type)
    
    for field, field_type in hints.items():
        value = getattr(obj, field, None)
        if not isinstance(value, field_type):
            raise TypeError(f"{field} must be {field_type}, got {type(value)}")
```

---

## 7. Rate Limiting

### 7.1 Request Throttling

```python
from collections import defaultdict
from time import time

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def check(self, actor: str) -> bool:
        now = time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        self.requests[actor] = [
            t for t in self.requests[actor] if t > window_start
        ]
        
        # Check limit
        if len(self.requests[actor]) >= self.max_requests:
            return False
        
        self.requests[actor].append(now)
        return True

# Usage
limiter = RateLimiter(max_requests=100, window_seconds=60)

def submit_with_rate_limit(kernel, request):
    if not limiter.check(request.actor):
        raise RateLimitError("Rate limit exceeded")
    return kernel.submit(request)
```

### 7.2 Burst Protection

```python
class BurstProtector:
    def __init__(self, burst_limit: int, burst_window_ms: int):
        self.burst_limit = burst_limit
        self.burst_window_ms = burst_window_ms
        self.recent_requests = []
    
    def check(self) -> bool:
        now_ms = int(time() * 1000)
        window_start = now_ms - self.burst_window_ms
        
        self.recent_requests = [
            t for t in self.recent_requests if t > window_start
        ]
        
        if len(self.recent_requests) >= self.burst_limit:
            return False
        
        self.recent_requests.append(now_ms)
        return True
```

---

## 8. Monitoring and Alerting

### 8.1 Key Metrics

```python
# Metrics to monitor
METRICS = {
    "kernel_requests_total": "Total requests received",
    "kernel_decisions_allow": "ALLOW decisions",
    "kernel_decisions_deny": "DENY decisions",
    "kernel_decisions_halt": "HALT decisions",
    "kernel_decision_latency_ms": "Decision latency",
    "kernel_audit_entries": "Audit entries count",
    "kernel_hash_chain_valid": "Hash chain validity",
}
```

### 8.2 Alert Conditions

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| KernelHalted | state = HALTED | Critical | Investigate immediately |
| HighDenyRate | deny_rate > 50% for 5min | High | Review requests |
| HashChainInvalid | chain_valid = false | Critical | Halt and investigate |
| RateLimitExceeded | rate_limit_hits > 100/min | Medium | Review actor |
| UnusualActor | unknown actor detected | Medium | Verify identity |

### 8.3 Logging Configuration

```python
import logging

# Production logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler('/var/log/kernels/kernel.log'),
        logging.StreamHandler(),
    ]
)

# Security-relevant events
SECURITY_EVENTS = [
    "DECISION_DENY",
    "DECISION_HALT",
    "VALIDATION_FAILED",
    "JURISDICTION_DENIED",
    "HASH_CHAIN_INVALID",
]
```

---

## 9. Deployment Hardening

### 9.1 Container Security

```dockerfile
# Dockerfile hardening
FROM python:3.11-slim

# Run as non-root
RUN useradd -m -s /bin/bash kernels
USER kernels

# Minimal dependencies
COPY --chown=kernels:kernels requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Read-only filesystem where possible
COPY --chown=kernels:kernels kernels/ /app/kernels/
WORKDIR /app

# No shell access
ENTRYPOINT ["python", "-m", "kernels"]
```

### 9.2 Network Isolation

```yaml
# Kubernetes NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: kernels-network-policy
spec:
  podSelector:
    matchLabels:
      app: kernels
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              role: agent
      ports:
        - port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              role: database
      ports:
        - port: 5432
```

### 9.3 Secrets Management

```python
# Load secrets from environment or secrets manager
import os

def get_secret(name: str) -> str:
    # Try environment variable first
    value = os.environ.get(name)
    if value:
        return value
    
    # Fall back to secrets file
    secrets_path = os.environ.get("SECRETS_PATH", "/run/secrets")
    secret_file = f"{secrets_path}/{name}"
    
    if os.path.exists(secret_file):
        with open(secret_file) as f:
            return f.read().strip()
    
    raise ValueError(f"Secret {name} not found")
```

---

## 10. Emergency Procedures

### 10.1 Emergency Halt

```python
# Emergency halt procedure
def emergency_halt(kernel, reason: str):
    # Log the emergency
    logging.critical(f"EMERGENCY HALT: {reason}")
    
    # Export evidence before halt
    try:
        evidence = kernel.export_evidence()
        archive_evidence(evidence, "/emergency/")
    except Exception as e:
        logging.error(f"Failed to archive evidence: {e}")
    
    # Halt the kernel
    kernel.halt()
    
    # Alert operations team
    send_alert("CRITICAL", f"Kernel halted: {reason}")
```

### 10.2 Recovery Procedure

```python
# Recovery after halt
def recover_kernel(archive_path: str):
    # 1. Load archived evidence
    evidence = load_evidence(archive_path)
    
    # 2. Verify integrity
    is_valid, errors = replay_and_verify(
        evidence["ledger_entries"],
        evidence["root_hash"]
    )
    
    if not is_valid:
        raise SecurityError(f"Cannot recover: {errors}")
    
    # 3. Create new kernel with verified state
    kernel = StrictKernel(
        kernel_id=evidence["kernel_id"],
        policy=load_policy(),
    )
    
    # 4. Verify new kernel is operational
    test_request = create_health_check_request()
    result = kernel.submit(test_request)
    
    if result.status != "ACCEPTED":
        raise RecoveryError("Health check failed")
    
    return kernel
```

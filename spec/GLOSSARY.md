# Glossary

This document defines terms used throughout the Kernels specification and documentation.

## A

### Actor

An entity that submits requests to the kernel. Actors are identified by string identifiers and are subject to jurisdiction policy.

### Ambiguity

A condition where a request cannot be unambiguously interpreted. Ambiguous requests are denied under fail-closed semantics.

### Append-Only

A property of the audit ledger where entries can only be added, never modified or removed.

### Arbitration

The process of evaluating a request against jurisdiction policy to determine whether it should be allowed or denied.

### Audit Entry

A single record in the audit ledger documenting a kernel operation.

### Audit Ledger

The append-only, hash-chained log of all kernel operations.

## B

### Boot

The initialization process that transitions a kernel from BOOTING to IDLE state.

## C

### Control Plane

The layer that governs execution without performing execution itself. The kernel is a control plane for AI systems.

## D

### Decision

The outcome of request arbitration: ALLOW, DENY, or HALT.

### Deterministic

A property where identical inputs always produce identical outputs. All kernel operations are deterministic.

## E

### Evidence Bundle

An exportable package containing the full audit ledger with verification data.

### Execution

The phase where a tool call is dispatched and its result captured.

## F

### Fail-Closed

A security posture where uncertainty results in denial rather than allowance. The kernel operates fail-closed by default.

## G

### Genesis Hash

The initial hash value (64 zeros) used as the prev_hash for the first audit entry.

## H

### Halt

An irrevocable transition to the terminal HALTED state.

### Hash Chain

A sequence of entries where each entry includes the hash of the previous entry, enabling tamper detection.

## I

### Intent

A description of what a request aims to accomplish. Part of every KernelRequest.

### Invariant

A property that must always hold true. The kernel defines ten core invariants.

## J

### Jurisdiction

The boundaries within which requests are permitted. Defined by JurisdictionPolicy.

### Jurisdiction Policy

A configuration specifying allowed actors, tools, and constraints.

## K

### Kernel

The central component that governs AI agent execution through state machine, jurisdiction, and audit.

### Kernel Config

Configuration parameters for initializing a kernel instance.

### Kernel State

One of the defined states in the kernel state machine.

## O

### Operator

A human with authority who defines policy and reviews audit. Operators are in the trusted zone.

## P

### Policy

See Jurisdiction Policy.

### Policy Result

The outcome of policy evaluation, including whether the request is allowed and any violations.

## R

### Receipt

The response returned by the kernel after processing a request.

### Replay Verification

The process of recomputing the hash chain to verify audit ledger integrity.

### Request

A KernelRequest submitted to the kernel for processing.

### Root Hash

The hash of the last entry in the audit ledger, representing the current state of the chain.

## S

### State Machine

The component that manages kernel state and enforces valid transitions.

### State Transition

A change from one kernel state to another, always producing an audit entry.

## T

### Terminal State

A state with no outgoing transitions. HALTED is the only terminal state.

### Tool

A registered function that can be invoked through the kernel.

### Tool Call

A specification of which tool to invoke and with what parameters.

### Tool Registry

The component that manages registered tools and dispatches invocations.

### Transition

See State Transition.

### Trust Boundary

The line separating trusted components (operator, kernel, tools) from untrusted components (agents, requests).

## V

### Validation

The process of checking request structure and required fields.

### Variant

A kernel implementation with specific enforcement characteristics.

### Virtual Clock

A deterministic clock that can be controlled for reproducible behavior.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [0.1.0] - 2026-01-01

### Added

- Initial kernel implementation with deterministic state machine
- Core types: KernelState, KernelRequest, KernelReceipt, Decision, ReceiptStatus
- Append-only audit ledger with hash-chained entries
- Jurisdiction policy engine with composable rules
- Tool registry with built-in `echo` and `add` tools
- Four kernel variants: strict, permissive, evidence-first, dual-channel
- Replay verification for audit ledger
- CLI entrypoint with help and version commands
- Formal specification pack under `/spec`
- Five working examples demonstrating core functionality
- Complete test suite

### Fixed

- N/A (initial release)

### Changed

- N/A (initial release)

### Removed

- N/A (initial release)

### Security

- Fail-closed semantics enforced by default
- Hash chain integrity verification on replay
- Jurisdiction checks mandatory before execution

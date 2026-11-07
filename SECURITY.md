# Security

**Status: local research demo. Do not expose to a network or use with real money or personal data.**

## What exists
Schema validation (Pydantic, `extra=forbid`), consistent error envelope, deterministic authorization, atomic budget reservation, per-agent idempotency, signed hash-chained receipts, PEM private keys created `0600` under `data/keys` (git-ignored), CORS limited to localhost origins, demo reset disabled unless `AGENTTRUST_ALLOW_DEMO_RESET=true`, scrubbing of card-like numbers/secrets in free text, and no real third-party calls.

## Threat model (summary)
| Threat | Current status |
|---|---|
| Agent exceeds delegated limits | Mitigated for the enforced rules (budget, per-item, allow-lists): the gateway prices from the merchant-signed quote, not agent claims. Free-returns/delivery limits and claim cross-checks are not enforced in this public edition. |
| Concurrent requests overspend or double-execute | Mitigated for single-node SQLite (write lock at BEGIN, unique idempotency constraint); tested. |
| Receipt content edited after the fact | Detected by hash + signature, including by the offline verifier. |
| Operator edits and re-signs / truncates the chain | **Not mitigated.** The single gateway key can re-sign; trailing deletion is undetectable. Needs external anchoring and witnesses. |
| Receipt deleted from the middle, reordered, duplicated or signature-transplanted | Detected (sequence, link, signature checks); tested. |
| Older genuine export presented as current | **Not mitigated.** No freshness proof; asserted by `test_known_limit_stale_export_replay_is_not_detected`. |
| Replayed action, approval or cancellation | Mitigated: idempotency, state-machine checks; tested. |
| Malformed input to the offline verifier | Reported as problems, never a crash; tested. |
| Impersonating the user | **Not mitigated.** Approval is an unauthenticated click on a Demo Trusted Surface. |
| Forged merchant statements | Only simulated; real merchants need their own keys/attestation. |
| Anyone on the network calling the API | **Not mitigated.** No authentication. Bind to 127.0.0.1. |
| DoS / abuse | **Not mitigated.** No rate limiting; SQLite write lock serializes everything. |
| Private-key theft | Key stored as an unencrypted file. Needs KMS/HSM and rotation. |
| Merchant call inside DB lock for cancellation / approve paths | Acceptable for a mock; a real merchant call must not hold a write lock. |

Known gaps: `FAILED` assumes a merchant error means no side effect (unconfirmed, flagged as unknown in analysis); no key rotation or key-id registry; timestamps are the server clock; duplicate window is heuristic.

## Auditability vs. independent assurance
Receipts can be re-checked offline by anyone holding the public key. That makes tampering *by outsiders* detectable. It is not a third-party guarantee: the gateway operator controls the only signing key, user approval is unsigned, and merchant signatures are simulated. Nothing in this repository should be read as an audit, certification or attestation by an independent party.

## Required before any real deployment
Authentication and per-user authorization; tenant isolation; rate limiting and request size limits; TLS; user-signed mandates (WebAuthn/passkeys or equivalent); managed keys with rotation and revocation; external timestamping and independent witnesses; a real database with row-level locking and migrations; two-phase reserve/execute with reconciliation for crashed phase-2 calls; audit/log redaction review; privacy/legal review (payments, consumer protection, data protection) in each target jurisdiction; dependency and container scanning; independent security assessment.

## Reporting
Research prototype: open an issue without including secrets. Never commit `.env`, `*.pem` or `data/`.

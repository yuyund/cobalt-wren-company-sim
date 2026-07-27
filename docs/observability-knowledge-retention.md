---
title: Observability, Knowledge, and Retention
type: reference
status: current
owner: repository-maintainers
created_at: '2026-07-27'
updated_at: '2026-07-28'
review:
  due_at: '2026-08-10'
validity:
  due_at: '2027-07-28'
---

# Observability, Knowledge, and Retention

Normative requirements for inspectable execution, organizational knowledge boundaries, evidence provenance, retention, and legal hold.

## Observability requirements

Run-level visibility alone is insufficient. The system must make individual
proposals and tool calls inspectable without exposing raw secrets.

The observation model should retain at least:

- run and correlation identifiers
- persona
- requesting internal agent
- review decision and reasons
- permission rule matched or requested
- connection reference and capability bundle
- tool and operation
- target
- redacted raw input
- raw result or result reference
- evidence references
- revision number and prior-intent relationship
- human approval or rejection

This is partly a consuming-application requirement and may reveal missing Cobalt
Wren primitives. Framework changes should be proposed only after the Company
vertical slice demonstrates which observation data cannot be represented cleanly
at application level.
## Organizational knowledge boundaries

Durable organizational knowledge must not use a single global visibility model.
Each knowledge item should carry a typed scope, access policy, confidentiality
classification, purpose restrictions, provenance, and lifecycle state.

The initial knowledge scopes are:

- `company`: broadly reusable Company-wide knowledge
- `department`: knowledge owned by one department and optionally shared with
  explicitly named departments
- `customer`: knowledge isolated to a particular customer or counterparty
- `project_case`: knowledge isolated to a project, contract, campaign, incident,
  ticket, or other bounded case
- `persona_private`: working knowledge available only to the owning persona

Scope and confidentiality are independent. A knowledge item may additionally be
classified as public, internal, confidential, restricted, legally held, or a
provider- or Company-defined equivalent. Purpose restrictions may further limit
use to support, sales, legal review, incident response, contract delivery, or
another declared purpose.

Knowledge is eligible for use only when its scope matches the active context, the
persona has access, confidentiality requirements are satisfied, the current goal
is relevant, and purpose restrictions permit use. Eligibility does not imply
automatic prompt injection. A deterministic Knowledge Context Resolver should
select only the smallest relevant subset and must avoid exposing unrelated
customer, department, project, or persona-private context.

Knowledge may be promoted from a narrower scope to a broader scope, such as from
persona-private to department or from department to Company-wide. Promotion must
be an explicit, auditable policy operation that checks confidentiality,
customer-specific content, contractual restrictions, personal data, secrets,
and provenance. A persona may propose promotion but must not silently broaden
knowledge visibility.

Cross-scope references should preserve the source item's access boundary. A
Company-wide summary must not provide a path to restricted source content unless
the requesting persona independently has access to that source. Derived
knowledge should expose uncertainty and source availability rather than implying
that inaccessible evidence was directly reviewed by every consumer.
## Retention and evidence lifecycle

Raw execution material should be retained only for a comparatively short
diagnostic window by default. This includes unstructured tool inputs and
outputs, provider responses, browser screenshots, DOM snapshots, and similarly
detailed evidence. The exact default duration remains a configurable policy
choice rather than a permanent retention guarantee.

Durable organizational knowledge is distinct from raw logs. Before raw material
expires, the system may derive structured, source-linked knowledge, decisions,
outcomes, permission history, and audit summaries that are useful for future
work. Derived knowledge must preserve provenance and uncertainty while excluding
secrets and unrelated context; it must not become a hidden copy of the entire raw
record.

Legal, regulatory, contractual, security-incident, or explicit litigation-hold
requirements may override normal deletion. Held records must be isolated,
access-controlled, auditable, and associated with a documented retention basis
and release condition. Ordinary users and personas must not be able to bypass a
hold through routine deletion controls.

Users should be able to inspect applicable retention status and delete eligible
raw material before its scheduled expiry. Deleting raw material should not
silently delete independently authorized durable knowledge or mandatory audit
records, but the relationship and consequences must be visible.

---
title: High-impact Permissions and Tool Package Lifecycle
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

# High-impact Permissions and Tool Package Lifecycle

Normative requirements for explicit high-impact selection, completion details, reusable Tool Packages, compatibility migration, rollback, and Company-local sharing.

## Explicit high-impact selection and completion details

Each high-impact permission should be listed as a separate explicit selection so
the resulting consent and audit record identify exactly which operations were
approved. The interface may also provide a select-all control for convenience,
but using it must visibly select every affected item and must not collapse the
items into one opaque aggregate permission. Users must still be able to deselect
individual entries before submission.

Selecting all high-impact permissions does not trigger an additional confirmation
step. The visible item selections and the normal service-enablement submission
constitute the user's explicit approval. The interface must avoid hidden or
pre-submission state changes so the submitted selection set matches what the user
last saw.

After service enablement, the default completion message should remain concise,
but the user must be able to expand a structured details view. The expanded view
should include at least:

- Connection identity, account, authentication scheme, and status
- requesting persona and active persona grant
- selected capability bundles
- active API operation permissions and prohibitions
- active browser-operation permissions and approved domains
- browser-session status and expiry, without exposing secrets
- generated or reused Tool Packages, versions, and validation status
- high-impact permissions explicitly approved
- omitted, rejected, or deferred scopes
- audit and correlation identifiers
- any pending takeover, recovery, or follow-up action

The details view should link conceptually to the permission administration and
tool-observability surfaces so the user can inspect, edit, revoke, or diagnose
what was enabled. Secret values, raw cookies, tokens, passwords, and unredacted
credential material must never be displayed in the completion details.

A persona may eventually request creation of a tool when no suitable tool
exists, but the persona is not the trusted authority for activation. Generated
artifacts must pass deterministic platform validation before they can be used.
A created tool must declare its required Connection schema rather than
requesting secrets through ordinary conversation.

Validated Tool Package definitions are reusable shared assets. They may be
registered once and used by multiple personas without regenerating or retesting
the same version. Reuse covers tool code, operation schemas, capability bundles,
permission-scope schemas, validation results, and provenance metadata.

Reuse never transfers authority between personas. Each persona must still obtain
its own Connection grant, capability selection, API and browser operation
permissions, and any required high-impact acknowledgements. A shared Tool
Package must not expose another persona's Connection references, permission
state, execution history, or browser session.

When an existing Tool Package satisfies a new persona's goal, the platform
should prefer reuse and present only the incremental service-enablement choices
required for that persona.

When a new Tool Package version is generated, it must first pass the normal
validation pipeline. After validation, the platform—not the package authoring
persona or generated package metadata alone—must compare the new version with the
currently active version and determine compatibility.

The platform should evaluate at least operation semantics, typed input and output
contracts, permission-scope schemas and matching rules, required Connections and
credentials, network destinations, side effects, risk classification, redaction,
and runtime security constraints. Package-declared migration metadata may be used
as evidence but is not authoritative.

If the platform determines that the new version is compatible with the active
persona grants and permissions, all affected personas should migrate
automatically. The migration must preserve persona-specific authority, record the
old and new versions and compatibility result, and support operational rollback
if the new version fails health or contract checks after activation.

A successful compatible migration should produce a concise user notification
rather than requiring approval or remaining silent. The default notification
should identify the Tool Package, old and new versions, affected personas,
successful status, and whether rollback or follow-up action is required. Detailed
compatibility evidence, changed contracts, validation results, and audit
identifiers should be available through an expandable view. Multiple compatible
migrations may be grouped into one notification when doing so does not hide
failures or required action.

If compatibility cannot be established, migration must fail closed. The existing
version remains active, and only the incremental Connection, capability, API or
browser permission changes required by the new version are presented for user
approval. A version must never inherit broader authority merely because it
replaces an older package.

The initial sharing boundary is the same user-owned Company environment. Tool
Packages may be reused across personas inside that Company, but must not be
published to other users, organizations, tenants, or a public registry by
default. Cross-Company or public distribution requires a separate trust model
covering package signing, provenance verification, publisher identity,
compatibility, revocation, vulnerability response, policy review, and data or
credential boundary guarantees.

A package copied or imported from outside the Company is not equivalent to an
internally generated and validated package. Until an external-distribution model
is defined, external packages must be treated as untrusted inputs and may not be
activated through the ordinary internal-reuse path.

A Connection requirement may include:

- provider identity
- supported authentication schemes
- required and optional fields
- requested scopes or capabilities
- setup instructions

Tool creation does not bypass Review, permission, persona grant, credential
isolation, or observability requirements.

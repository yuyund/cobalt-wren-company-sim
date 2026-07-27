# Autonomy, Permissions, Review, and Connections

## Status

This document records agreed design decisions for the next company-simulation
iterations. These capabilities are not yet implemented unless stated otherwise.
Implementation should proceed in small vertical slices and must preserve the
responsibility boundaries described here.

## Autonomy model

A department persona may act freely inside an explicitly granted scope.

When an intended action is not covered by an existing permission, the system
must request permission before execution. The request should propose useful
permission scopes rather than asking only a generic yes-or-no question.

Permission choices should support at least:

- allow this action once
- always allow the proposed bounded scope
- reject this time
- prohibit this scope until manually changed

A persistent permission prevents repeated prompts only while the future action
matches the stored scope. Persistent operation permissions remain active until
the user explicitly revokes or edits them, or until their underlying Persona
grant or Connection becomes invalid.

A one-time rejection and a durable prohibition are distinct outcomes. A
one-time rejection applies only to the current intent and does not create a
persistent policy rule. A durable prohibition is stored as policy state and
must be visible to the affected persona so it can avoid repeating the request.
If the user later wants reconsideration of a prohibition, the user is
responsible for editing or removing that policy manually.

When proposing a durable prohibition, the persona should not present only one
inferred scope. It should generate multiple meaningful scope candidates ordered
from narrow to broad, explain the effect of each candidate, and let the user
choose or edit one. Candidate scopes may include the current intent, a specific
target, an operation on one Connection, or the operation for the entire persona.
The default recommendation should remain the narrowest scope that addresses the
observed concern.

## Permission scope

Permissions belong to the department persona that obtained them. They are not
shared automatically with other departments because each persona owns a
different conversation context and responsibility boundary.

The minimum permission key is expected to include:

```text
persona × connection/tool × operation × target × conditions
```

For email, the target should normally be a specific recipient. A permission to
send to one recipient does not imply permission to send to other recipients or
an entire domain.

The system should propose the least-privileged useful scope and allow the user
to broaden or narrow it. For persistent permission requests, the persona should
present multiple meaningful scope candidates ordered from narrow to broad,
explain the effect of each candidate, and let the user choose or edit one. The
default recommendation should remain the narrowest scope that enables the
current goal.

Scope candidates must conform to a policy-system schema rather than being stored
as free-form persona output. The core policy engine should define common fields
such as persona, Connection, operation, effect, and conditions, while each
provider or tool adapter may register additional typed scope dimensions. This
keeps matching deterministic without assuming that all future services share a
fixed global target model.

A provider-defined scope schema should be declarative and versioned. It may
define dimensions such as recipient, repository, channel, path, resource type,
resource identifier, data classification, attachment policy, monetary limit, or
provider-specific constraints. Each dimension should declare its type, matching
semantics, validation rules, display metadata, and whether broader or narrower
values can be derived safely.

The persona may infer and rank candidate values, but the policy system must
validate, normalize, compare, persist, and match them. Unknown dimensions or
unregistered schema versions must fail closed rather than falling back to
string comparison or permissive matching.

## Persona and internal agents

The persona remains the accountable subject and permission owner. Internal
agents are functional roles operating on behalf of that persona.

Initial internal roles are expected to include:

- strategy
- analysis
- execution
- review

Internal agents may have different tool capabilities. A persona permission does
not make every internal role capable of using the corresponding tool.

An action is executable only when all applicable gates pass:

```text
persona permission
AND internal-agent capability
AND review approval
AND connection capability
AND contextual policy
```

Every external action must record both the accountable persona and the internal
agent that requested execution.

## Execution and review separation

The execution agent creates a structured tool intent. The review agent evaluates
that proposal but must not rewrite it or execute it.

Review outcomes should support:

- approve
- revise_required
- deny
- request_more_context
- request_permission

When revision is required, Review returns identified problems and required
changes. Execution creates a new proposal, which is reviewed again.

The normal automatic revision loop is bounded to three review-to-execution
rounds. Reaching the limit produces a human-attention state rather than an
unbounded loop. Limit hits are treated as a quality signal that should drive
improvements to prompts, schemas, evidence collection, or role definitions.

## Review evidence and independence

Review should not receive an unstructured copy of all execution reasoning by
default. It should receive a structured evidence package with references to
source material.

Expected review inputs include:

- original user request
- current goal
- proposed action and arguments
- target
- expected effect
- relevant factual claims
- required permission
- secret or connection usage
- risk assessment
- references to messages, artifacts, and prior tool calls

A deterministic evidence collector should select and index candidate evidence.
The review agent may directly inspect referenced source data. If information is
still insufficient, it may question the execution agent, but the answer is a
claim to verify rather than authoritative evidence.

## Human decision after revision exhaustion

When automatic revision reaches its maximum, the human interaction remains a
binary decision:

- approve
- reject

The escalation view should expose the original request, proposed action, current
proposal, review history, revision diffs, unresolved issues, required
permissions, and supporting evidence.

## Rejection behavior

A rejected tool intent is discarded. The system must prevent automatic
resubmission of an effectively identical intent inside the same escalation or
retry cycle. A one-time rejection does not permanently forbid a future request
that arises from materially new user intent or context. A durable prohibition
does forbid matching future requests until the user changes the rule manually.

The persona should interpret the rejection using available context and classify
it as one of:

- quality_failure
- action_forbidden
- target_forbidden
- insufficient_permission
- ambiguous

For `quality_failure`, Execution may create one additional proposal, followed by
normal Review and another human approve-or-reject decision.

For `action_forbidden` or `target_forbidden`, the rejected operation must not be
repackaged to evade the decision. The persona may search for a genuinely
different way to achieve the user's goal.

For `ambiguous`, the system should stop safely and report that the action was not
performed.

## Connections and credentials

External service access is represented as a user-owned Connection. Personas use
Connections through explicit persona grants. A grant applies only to the
persona that requested and received it; connecting an account does not grant
other personas access.

Persona Connection grants remain active until explicitly revoked. They do not
expire by default. They become unusable when the Connection is removed,
invalidated, loses required capabilities, changes account identity, or is
revoked for that persona.

When a Connection becomes invalid, related persona grants and operation
permissions must not be deleted automatically. They should transition to an
inactive state that preserves scope, provenance, audit history, and the reason
for invalidation while preventing execution. Matching requests must fail closed
and identify reconnection or policy repair as the missing prerequisite.

After reconnection, the platform must re-evaluate the Connection identity,
authentication scheme, capability set, provider schema, Tool Package version,
and all dependent API and browser permissions. Rules may reactivate
automatically only when the platform establishes that their original meaning and
scope remain compatible. Account changes, capability expansion, changed domains,
new credential classes, broader side effects, or ambiguous matching require an
incremental user confirmation. Narrower capabilities may leave only the
compatible subset active.

Explicit user revocation differs from temporary invalidation. A revoked persona
grant or permission remains revoked and must not reactivate merely because the
Connection is repaired. Removing the Connection may retain inactive policy and
audit records according to retention policy, but no executable credential
binding may remain.

The following concepts are distinct:

1. a Connection exists for the user
2. a persona is allowed to use that Connection
3. a specific operation is permitted for that persona and target

A Connection exposes service identity, account identity, status, capabilities,
and a credential reference. Raw credentials are not part of persona context.

The credential store may hold OAuth tokens, API keys, passwords, service-account
keys, client certificates, SSH credentials, or provider-specific credential
bundles. OAuth is therefore an authentication flow backed by the credential
store, not an alternative to it.

## Provider-defined capability bundles

Each provider defines human-readable capability bundles. Bundles are not a
single global read/write/full hierarchy because service semantics differ.

Examples include:

```text
Gmail: read mail, manage mail, create drafts, send mail
Slack: read channels, post messages, manage channels, manage users
GitHub: read repositories, manage issues and pull requests, write contents,
        trigger actions
```

A bundle maps to provider-specific scopes or credential capabilities. It is not
itself an operation permission.

For example, a Gmail Connection may technically support sending while the
Company permission layer allows Support to send only to one approved recipient.

The persona should infer the smallest useful provider bundle from its current
goal and recommend it to the user. The user may select a narrower or broader
bundle. If a future operation needs capabilities not present on the Connection,
the system requests a Connection capability expansion separately from the
operation permission.

## Permission awareness and administration

A persona should know the permissions, denials, prohibitions, Connection grants,
and missing permissions relevant to its current goal. The system should not
inject the user's entire policy store into every prompt. A deterministic
Permission Context Resolver should select the relevant subset.

The persona-facing context should distinguish:

- active Connection grants
- active operation permissions
- durable prohibitions
- one-time rejections relevant to the active retry cycle
- conditions attached to each rule
- capabilities or permissions still missing

A prohibited operation should not be requested again automatically. The user
may reopen the possibility by editing the rule in the permission administration
interface. A one-time rejection blocks the active intent and its automatic
retries, but it is not shown as a permanent prohibition after that cycle ends.

The administration interface should be organized by persona and should display
Connection grants separately from operation permissions and prohibitions. Users
must be able to inspect, edit, and revoke each rule.

When the user edits a rule directly in this interface, that edit is itself an
explicit authorization decision and requires no additional confirmation. Every
change must still produce an audit record containing the actor, persona,
Connection, operation, target, previous value, new value, and timestamp.

## Dynamic tool creation and connection requirements

The design goal is to minimize user involvement when enabling a new service.
The expected user responsibility should normally stop at obtaining or approving
credentials and entering provider-required values. Tool discovery, generation,
validation, registration, and lifecycle management should be system-owned.

The platform should not be limited to a predefined catalog of supported
services. When no suitable tool exists, it should be possible to create one
dynamically from machine-readable service information such as OpenAPI,
GraphQL introspection, JSON Schema, protocol descriptions, provider
documentation, or an application-generated adapter specification.

Dynamic creation should produce a versioned Tool Package rather than injecting
arbitrary code directly into the persona runtime. A Tool Package should declare
at least:

- tool identity and version
- operations and typed input/output schemas
- provider and Connection requirements
- capability bundles
- permission scope schema and matching semantics
- endpoint and transport policy
- secret bindings by reference
- redaction rules
- deterministic validation tests
- execution resource limits
- provenance and generation metadata

A generation pipeline should separate authoring from activation:

```text
service request
-> discover or describe API
-> generate Tool Package
-> static validation
-> isolated contract tests
-> security and policy review
-> register inactive version
-> activate for an explicitly granted persona
```

The user should not be required to review generated code or construct the tool.
Human interaction should be limited to decisions that cannot safely be inferred,
such as credential acquisition, provider consent, account selection, and
permission or prohibition scope.

The normal enablement flow should collapse these decisions into as few prompts
as possible. The platform should reuse existing Connections, prefill known
account and provider metadata, infer the smallest useful capability bundle and
permission scopes, and present a single consolidated confirmation when those
decisions can be made safely together. OAuth should use provider consent flows;
API-key services should present only the provider-required fields and setup
instructions. Tool generation progress, retries, schema conversion, testing,
and registration should remain invisible unless user action is required or the
process fails.

A validated operation may become available immediately after the required
Connection grant and operation permission are approved. Read-only or dry-run
staging is not mandatory for every generated tool. The platform should instead
classify operations and apply additional safeguards only where their effects
justify them, such as destructive, irreversible, financial, identity,
administrative, or broad external-communication operations.

Generated execution code must run in an isolated, least-privileged environment
with explicit network destinations, time and resource limits, no ambient secret
access, and complete tool-call observability. Credentials must be injected only
through declared secret bindings after Connection, persona grant, permission,
and Review checks pass.

## Browser-assisted service enablement

The platform should support browser automation as an enablement mechanism when a
provider does not offer a sufficiently direct API or when credentials must be
created through a web console. Routine navigation, form discovery, non-secret
field entry, account selection, documentation lookup, and post-creation
verification may be automated.

Browser automation must use an isolated browser context with explicit domain
allowlists, observable actions, bounded navigation, download controls, and no
ambient access to unrelated browser profiles or credentials. Reusable browser
authentication state is sensitive credential material and must be stored in the
credential system rather than in repositories or ordinary artifacts.

The browser flow must support secure user takeover. Automation pauses and hands
control to the user for steps that require direct human participation or should
not be delegated, including:

- password entry when no approved password-manager integration exists
- MFA, passkeys, hardware security keys, or device approval
- CAPTCHA or anti-bot challenges
- provider consent, legal terms, or billing commitments that require the user
- ambiguous account or organization selection
- revealing, copying, or confirming a newly issued secret when policy requires

After the user completes the sensitive step, automation may resume in the same
isolated session, verify the result, capture only declared credential outputs,
store them by reference, and continue Tool Package generation and activation.
The system must not attempt to defeat CAPTCHA or bypass provider security
controls.

The preferred user experience is a single guided flow rather than instructions
that force the user to switch repeatedly between the platform and a provider
site. Browser automation should remain an implementation detail unless takeover
or recovery is required.

Browser automation should run headlessly by default. When secure user takeover
is required, the platform should attach an interactive view to the same isolated
browser session, preserve navigation and form state, clearly identify the step
that needs human action, and return control to automation after completion. The
user should not need to restart the flow or repeat fields already entered.

The transition between headless execution and interactive takeover must be
auditable. Screenshots, DOM snapshots, and action logs may be retained according
to redaction and retention policy, but secret fields and authentication values
must never be recorded in plaintext. If the same session cannot be resumed
safely, the platform should stop and request recovery rather than silently
starting a different account or browser context.

Browser automation permissions are distinct from API operation permissions. A
browser permission scope should include at least:

```text
persona × browser session/Connection × domain × browser operation
× target resource × conditions
```

Browser operations should be typed rather than represented as arbitrary click
sequences. Example operations include navigate, inspect, fill non-secret fields,
submit configuration, create credential, change account settings, download an
artifact, and delete or revoke a resource. The resulting low-level browser
actions remain observable implementation details of the approved operation.

Domain and target-resource matching must follow the same provider-defined,
versioned scope-schema rules as API tools. Redirects or navigation outside the
approved domain set require a new policy decision unless they are declared parts
of a trusted authentication flow. API permission does not implicitly authorize
browser-console changes, and browser permission does not authorize direct API
operations.

The persona should propose multiple persistent browser-permission scopes from
narrow to broad, while the policy engine validates and stores the selected typed
scope. Sensitive or irreversible browser operations may still require Review or
human attention even when a persistent permission exists.

Initial browser-operation permissions should be included in the same consolidated
service-enablement confirmation as Connection creation or reuse, persona grant,
capability bundle selection, and API operation permissions. The interface must
present these categories separately enough for informed consent while allowing a
single confirmation action when the user accepts all recommended scopes.

The consolidated view should show why browser automation is required, approved
domains, typed browser operations, target resources, takeover conditions, and
whether each rule is one-time or persistent. Users must be able to edit or omit
browser scopes without discarding the rest of the service setup. Browser
permissions discovered only after activation require a later incremental
confirmation rather than silently expanding the original grant.

Recommended Connection grants, capability bundles, API permissions, and browser
permissions should be preselected by default to minimize setup effort. The
selected defaults must remain the least-privileged useful set inferred for the
current goal, and the interface must make every selected item visible and
editable before confirmation.

High-impact permissions must not rely on passive preselection alone. Operations
classified as destructive, irreversible, financial, identity-related,
administrative, security-sensitive, or broad external communication require an
additional explicit acknowledgement or selection before activation. The policy
system, not the persona, determines whether a candidate falls into this class.

Not every irreversible deletion requires per-execution human attention. The
always-confirm class should be limited to deletion or revocation of important
assets whose loss materially affects identity, authority, security, operations,
legal standing, or substantial business data. Examples include accounts,
organizations or tenants, production environments, primary data stores,
credential authorities, critical integrations, and similarly classified
resources.

Ordinary file-level or record-level deletion should not become an automatic
always-confirm operation solely because it is technically irreversible. It may be
executed under an appropriate persistent permission and normal Review when its
scope, quantity, classification, and blast radius remain within policy. Bulk
deletion, protected data, unusually broad targets, or provider-defined critical
resources may elevate the action to human attention. Resource importance and
blast-radius classification are determined by the policy system using typed tool
and provider metadata, not by free-form persona judgment alone.

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

## Open questions

The following remain intentionally unresolved:

- governance and compatibility rules for provider-defined scope schema versions
- detailed resource-criticality and blast-radius thresholds within the agreed always-confirm categories
- trust, signing, distribution, and revocation rules for cross-Company or public Tool Packages
- how service documentation is discovered and converted when no formal API schema exists
- detailed reconnection compatibility and partial-reactivation rules for provider-specific capability changes
- concrete default retention windows by evidence class and jurisdiction
- how organizational memory contributes evidence without leaking unrelated
  context

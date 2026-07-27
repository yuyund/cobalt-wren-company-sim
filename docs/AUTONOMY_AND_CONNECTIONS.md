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

## Tool creation and connection requirements

A persona may eventually create a tool when no suitable tool exists. A created
tool must declare its required Connection schema rather than requesting secrets
through ordinary conversation.

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

## Open questions

The following remain intentionally unresolved:

- exact permission condition schema beyond target-level constraints
- risk categories and which operations always require human attention
- identity and lifecycle of dynamically created tools
- connection revocation and permission invalidation semantics
- retention and redaction policies for raw inputs and outputs
- how organizational memory contributes evidence without leaking unrelated
  context

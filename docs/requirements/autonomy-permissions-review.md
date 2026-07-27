---
title: Autonomy, Permissions, and Review
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

# Autonomy, Permissions, and Review

Normative requirements for Persona autonomy, authority, internal roles, Review, rejection, and bounded human escalation.

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

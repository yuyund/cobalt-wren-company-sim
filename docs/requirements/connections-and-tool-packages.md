---
title: Connections and Tool Packages
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

# Connections and Tool Packages

Normative requirements for user-owned Connections, credential isolation, typed provider capabilities, permission administration, and generated Tool Packages.

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

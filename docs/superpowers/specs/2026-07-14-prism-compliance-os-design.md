# Prism Compliance Operating System Design

**Date:** 2026-07-14

**Status:** Approved direction, pending written-spec review

**Owner:** Vulnaguard

**Source product:** Sentinel CMMC one-time code snapshot

## 1. Executive summary

Prism is an AI-native operating system for continuous compliance readiness. It collects evidence once, converts that evidence into source-backed claims, maps those claims to reusable security objectives, and applies those objectives across SOC 2, ISO/IEC 27001, and CMMC Level 1.

Prism does more than display readiness. It runs the operational work behind readiness: evidence collection, document analysis, cross-framework mapping, task routing, autonomous follow-up, escalation, reporting, and audit-package preparation.

The core promise is:

> Collect once. Map once. Prove many.

Prism will begin as a new, independent repository created from a clean snapshot of Sentinel CMMC. Sentinel will remain unchanged. Prism will use a Vulnaguard-operated control plane and a customer-owned Azure data plane so customers retain control of their compliance information.

## 2. Goals

Prism must:

1. Reuse Sentinel's proven evidence, extraction, connector, mapping, review, task, reporting, and API foundations without coupling the two products.
2. Replace CMMC-specific data assumptions with a framework-agnostic compliance model.
3. Support SOC 2 readiness, ISO/IEC 27001 readiness, and CMMC Level 1 readiness in the initial release.
4. Reuse one evidence artifact across applicable framework requirements without duplicating the artifact or overstating what it proves.
5. Operate recurring compliance work through autonomous cadences and source-backed AI assistance.
6. Keep each customer's documents, graph, indexes, credentials, audit history, and authoritative records inside the customer's Azure subscription.
7. Provide a complete audit trail for automated actions, human approvals, evidence requests, responses, and escalations.
8. Continue deterministic compliance operations when AI or graph services are unavailable.

## 3. Non-goals

The initial Prism product will not:

- Detect or investigate security incidents.
- Replace a SIEM, EDR, vulnerability scanner, or identity provider.
- Change customer infrastructure automatically.
- Issue a SOC 2 report, ISO/IEC 27001 certification, or CMMC status.
- Submit official assessments without explicit human authorization.
- Provide MSP white-labeling, reseller billing, or custom domains.
- Support non-Azure customer-hosted deployments.
- Treat graph inferences or AI classifications as authoritative facts without provenance and appropriate review.

Security findings may enter Prism when they provide evidence about compliance readiness. Operational incident handling remains outside Prism.

## 4. Product positioning

Prism is not another checklist or static GRC file cabinet. It is the operational layer between customer systems and compliance outcomes.

```text
Microsoft, Google, uploads, and approved external sources
                              |
                              v
             Prism evidence and compliance engine
                              |
                              v
      SOC 2 | ISO/IEC 27001 | CMMC Level 1 | Prism API
```

Microsoft and Google remain source systems. Prism owns the neutral evidence model, readiness reasoning, work coordination, and cross-framework reuse.

## 5. Two operating systems

### 5.1 Prism Builder AIOS

The Prism repository will include an independent AI operating system for building and operating the product. It will contain:

- A substantive operating manual.
- Product and business context.
- Architecture and API references.
- A connection registry.
- An append-only decision log.
- Product-specific skills and specialized agents.
- Current-task handoff state.
- Build, release, audit, and improvement cadences.
- Four-Cs structural audits.
- Product memory and technical documentation.

The Builder AIOS may connect to Sean's Obsidian vault for Prism product history, decisions, lessons, research, and technician documentation. Customer content must never be written to the personal vault.

### 5.2 Customer Compliance AIOS

Each customer deployment will have isolated context, connections, capabilities, and cadences.

Its context includes:

- Organization profile and compliance scope.
- People, roles, managers, and control owners.
- Systems, applications, vendors, and boundaries.
- Selected frameworks and requirement applicability.
- Policies, evidence, decisions, exceptions, and prior reviews.
- Tasks, evidence requests, communications, and approvals.

Its connections include Microsoft 365, Entra ID, Azure, SharePoint, Google Workspace, Google Cloud, Google Drive, manual uploads, bulk imports, approved email or Teams channels, and the Prism API.

Its capabilities include evidence collection, document reading, evidence classification, control mapping, cross-framework analysis, readiness analysis, task coordination, policy drafting, communications, executive reporting, and audit-package preparation.

Its cadences include connector synchronization, evidence-freshness checks, follow-ups, escalations, periodic readiness review, policy review, access-review reminders, management-review preparation, and audit-window operations.

## 6. Repository creation and isolation

Prism must not be created with GitHub's Fork function because the resulting repository may remain part of Sentinel's fork network.

The repository creation process is:

1. Create a new private Prism repository.
2. Copy a clean snapshot of Sentinel's working tree without Sentinel's `.git` directory.
3. Exclude secrets, local environments, caches, generated artifacts, deployment state, and machine-specific files.
4. Initialize new Git history in Prism.
5. Configure only the Prism origin.
6. Verify that Prism has no Sentinel remote, submodule, package dependency, workflow, or synchronization job.
7. Record the Sentinel source commit in Prism's provenance documentation.
8. Run a secret scan before the first push.

Sentinel and Prism will then evolve independently. Neither repository will automatically receive changes from the other.

## 7. Sentinel capability disposition

### 7.1 Reuse

Prism will carry forward and adapt:

- Organization and user foundations.
- Supabase-era authentication and storage behavior until Azure replacements are selected and migrated.
- Evidence create, read, update, delete, upload, download, and review flows.
- Signed upload and download patterns.
- Bulk import infrastructure.
- PDF and DOCX text extraction.
- Evidence provenance, freshness, and audit events.
- Content-aware evidence suggestions.
- Evidence-to-control links with confidence and rationale.
- Connector adapter interface and scheduled synchronization.
- GitHub, Entra ID, Okta, AWS, Azure, Google Drive, and SharePoint adapter logic where relevant.
- Findings normalization as a compliance evidence input.
- Remediation issues and POA&M-style work tracking.
- Readiness and report-generation foundations.
- API-first service boundaries.
- AI command preview and confirmation patterns.

### 7.2 Generalize

Prism must replace or redesign:

- CMMC control codes as universal identifiers.
- CMMC/NIST-only keyword dictionaries.
- Framework-specific evidence classifiers.
- CMMC/NIST-only readiness scoring.
- Direct evidence-to-framework-control assumptions.
- Same-code-only crosswalk logic.
- Framework-specific prompts and labels.
- SSP-only report assumptions.
- Control ownership tied directly to one framework's control record.

### 7.3 Leave in Sentinel

Prism will not carry forward as core behavior:

- Contract eligibility scoring.
- Revenue-at-risk calculations.
- Bid and contract-renewal messaging.
- CMMC Level 2 positioning.
- C3PAO-specific workflows.
- Sentinel branding.
- Defense-contractor-specific dashboard cards.
- Government-contract sample data.

These items may later inform optional modules but will not shape Prism's base model.

## 8. Hosting and ownership model

### 8.1 Vulnaguard-operated control plane

The control plane manages:

- Customer registration.
- Licensing and entitlements.
- Deployment orchestration.
- Supported software versions.
- Configuration schemas.
- Release management.
- Environment health signals.
- Revocable support-access requests.
- Aggregate operational measurements that contain no customer content.

The control plane must not store customer documents, extracted text, evidence claims, messages, graph content, or connector credentials.

### 8.2 Customer-owned Azure data plane

Every initial customer deployment will run in a dedicated Azure subscription or resource group controlled by the customer. The data plane contains:

- Original documents and uploaded artifacts.
- Extracted text and metadata.
- The relational system of record.
- Knowledge graph and GraphRAG indexes.
- Evidence claims and framework mappings.
- Tasks, requests, messages, approvals, and exceptions.
- Connector credentials and encryption keys.
- Audit events, operational logs, backups, and retention configuration.
- The customer-specific Prism runtime and API.

Vulnaguard access must be least-privileged, explicitly granted, auditable, and revocable. Customer environments must continue retaining their authoritative data if Vulnaguard access is revoked or the Prism control plane is unavailable.

### 8.3 Deployment contract

An automated Azure deployment package will provision a customer environment and return:

- Environment identifier.
- Resource inventory.
- API and workspace endpoints.
- Customer administrator setup instructions.
- Connection setup workflow.
- Retention and backup configuration.
- Vulnaguard support-access controls.
- Estimated Azure operating cost.

Infrastructure automation reduces provisioning work, but customer-owned deployment introduces more onboarding complexity than a shared SaaS tenant. The onboarding experience must therefore be treated as a product feature.

## 9. Authoritative data and knowledge graph

Original artifacts and relational records are authoritative. The knowledge graph is a derived reasoning and retrieval layer.

The core information flow is:

```text
Source artifact
      |
      v
Evidence claim
      |
      v
Canonical security objective
      |
      v
Framework requirement
      |
      v
Framework readiness state
```

### 9.1 Core entities

- Organization
- Person
- Role
- Manager relationship
- System
- Application
- Asset
- Vendor
- Source artifact
- Evidence claim
- Canonical security objective
- Framework
- Framework requirement
- Evidence-to-objective relationship
- Objective-to-requirement relationship
- Task
- Evidence request
- Message
- Approval
- Exception
- Assessment window

### 9.2 Provenance

Every evidence claim and graph relationship must record:

- Source artifact or system.
- Source location or immutable identifier.
- Organization and scope.
- Collection or extraction time.
- Extraction or inference method.
- Confidence.
- Human-confirmation state.
- Last verification date.
- Creating actor or automated capability.

Relationships are labeled as extracted, human-confirmed, inferred, or ambiguous. Low-confidence and ambiguous relationships cannot silently change readiness.

### 9.3 Azure graph and GraphRAG role

Azure-hosted graph and GraphRAG capabilities will support:

- Relationship-aware retrieval.
- Cross-document reasoning.
- Ownership and escalation routing.
- Cross-framework evidence discovery.
- Source-backed answers about prior decisions and readiness history.
- Identification of missing or contradictory information.

Graph indexing runs asynchronously. A graph or indexing outage must not block uploads, evidence review, tasks, communications, or deterministic readiness calculations.

## 10. Evidence processing flow

When Prism receives a document or connector observation, it will:

1. Authenticate the source and tenant.
2. Store the original artifact or immutable source reference.
3. Record metadata, provenance, and collection time.
4. Extract supported text and structure.
5. Identify document type, source, scope, owner, coverage period, and freshness.
6. Produce source-backed evidence claims.
7. Match the claims to canonical security objectives.
8. Identify relevant requirements across enabled frameworks.
9. Auto-create high-confidence relationship suggestions marked as unverified.
10. Route ambiguous or conflicting results to human review.
11. Recalculate only the affected readiness projections.
12. Record all automated and human decisions in the audit trail.

One artifact may support multiple requirements. Prism must not equate reuse with complete satisfaction. Framework-specific scope, operating period, exceptions, and reviewer judgment still apply.

## 11. Cross-framework user experience

The primary demonstration flow is:

1. A customer uploads or synchronizes one evidence artifact.
2. Prism extracts its claims and maps them to one canonical objective.
3. Prism discovers relevant requirements in two or more enabled frameworks.
4. Prism explains why the artifact may be reused.
5. The user approves or rejects the proposed relationships where review is required.
6. Prism updates each framework view independently.

Example message:

> This evidence supports your SOC 2 security criteria and may also support an ISO/IEC 27001 access-control requirement. Reuse this evidence for both frameworks?

The demonstration should show the number of uploaded artifacts, supported frameworks, mapped requirements, avoided duplicate requests, and remaining review conditions.

## 12. Communication autonomy

Evidence requests are durable operational records rather than one-off notifications.

Each request records:

- Required evidence or answer.
- Business and framework rationale.
- Assigned owner and manager.
- Due date and audit-window priority.
- Delivery channel.
- Message attempts and delivery status.
- Responses and attachments.
- Escalation events.
- Resolution and approval.

### 12.1 Default cadence

1. Send the initial request.
2. Send a reminder after the configured interval.
3. Send the final attempt with the applicable deadline.
4. Escalate to the designated manager if all three contact attempts remain unanswered.

Customers can configure intervals, due dates, quiet hours, audit-period urgency, channels, escalation recipients, templates, auto-send permissions, and approval requirements.

A delivery failure is not an ignored request. Prism records the failure and retries or routes it for correction. Every outgoing message must identify Prism as the automated compliance operator and preserve the customer-approved sender identity.

## 13. Autonomy and approvals

### 13.1 Autonomous actions

Prism may autonomously:

- Synchronize configured integrations.
- Process uploads and connector observations.
- Extract and classify evidence.
- Create mapping suggestions.
- Reuse previously approved evidence relationships.
- Detect stale, missing, or conflicting evidence.
- Create internal tasks and evidence requests.
- Send customer-authorized requests and reminders.
- Escalate unanswered requests according to policy.
- Draft policies, narratives, and summaries.
- Generate internal readiness reports.

### 13.2 Human-approved actions

Prism requires explicit authorization for:

- Risk acceptance.
- Official representations of compliance.
- Judgment-dependent final control determinations.
- Official assessment submissions.
- Sending evidence packages to auditors or assessors.
- Changes to customer infrastructure.
- Destructive data operations.

All autonomous and approved actions must identify the actor, input sources, policy or rule, result, and timestamp.

## 14. API and workspace

The backend API is the product contract. The workspace, reports, agents, and integrations consume the same services.

Initial API domains are:

- Organizations and scope
- Frameworks and requirements
- Canonical objectives
- Evidence and claims
- Mappings and reviews
- Readiness
- Integrations and synchronization
- Tasks and evidence requests
- Messages and escalations
- Reports and export
- Audit events
- Customer administration

The initial Prism workspace focuses on:

- Current readiness by framework.
- Reusable evidence opportunities.
- Missing and stale evidence.
- Requests awaiting response.
- Human approvals.
- Escalations.
- Recent autonomous actions.
- Source-backed explanations.

The workspace will reuse suitable Sentinel evidence interfaces but will not inherit Sentinel's contract-risk dashboard as Prism's primary experience.

## 15. Error handling and degraded operation

- **Connector failure:** Preserve the last known state, mark it stale or unavailable, and notify the connection owner. Do not convert connectivity failure into compliance failure.
- **Extraction failure:** Retain the original artifact and route it for manual classification.
- **Low-confidence mapping:** Store it as a suggestion without changing authoritative readiness.
- **Conflicting evidence:** Preserve every source and create a review task.
- **Graph or index failure:** Continue using relational records and deterministic services.
- **Message delivery failure:** Record the failure, retry according to policy, and route unresolved delivery issues for human correction.
- **Expired credentials:** Pause only the affected connection and notify the administrator.
- **AI-service failure:** Continue deterministic ingestion, storage, reminders, tasks, and previously approved mappings.
- **Control-plane outage:** Keep the customer data plane and authoritative records available according to its local operating configuration.
- **Partial deletion failure:** Stop, record remaining resources, and require completion verification before reporting successful teardown.

Failures must be visible, scoped, retryable where safe, and preserved in the audit trail.

## 16. Offboarding, retention, and deletion

A customer can:

- Export authoritative records and artifacts.
- Revoke Vulnaguard access.
- Disconnect Prism while retaining its Azure environment.
- Reconnect Prism later.
- Apply customer-controlled retention policies.
- Initiate complete Prism resource teardown.

Offboarding must account for active data, graph indexes, search indexes, operational logs, snapshots, backups, legal holds, and configured retention periods.

Prism will generate an offboarding record that states:

- What was exported.
- What access was revoked.
- What was deleted.
- What remains retained and why.
- When retained backups or logs will expire.
- Which actor approved the operation.

## 17. Security and tenant isolation

The initial architecture must enforce:

- One customer-owned Azure boundary per deployment.
- Tenant-derived authorization rather than tenant identifiers trusted from payloads.
- Customer-controlled encryption keys or approved Azure-managed keys.
- Per-customer secrets in the customer's Key Vault.
- Scoped managed identities and service principals.
- Signed and expiring upload and download access.
- Minimal customer content in the Vulnaguard control plane.
- Immutable audit records for privileged and autonomous actions.
- Configurable retention and backup policies.
- Secret scanning and dependency review before release.
- No customer evidence in product analytics, developer tools, or the Builder AIOS.

## 18. Initial release scope

The first pilot release includes:

- Independent Prism repository and Git history.
- Prism Builder AIOS.
- Sentinel-derived evidence and API foundation.
- Automated customer-owned Azure deployment foundation.
- Manual document upload and bulk import.
- PDF and DOCX text extraction.
- Evidence lifecycle, provenance, review, and freshness.
- Canonical objective model.
- SOC 2 readiness module.
- ISO/IEC 27001 readiness module.
- CMMC Level 1 readiness module.
- Microsoft and Google source connectors selected from real pilot needs.
- Azure-hosted knowledge graph and GraphRAG index.
- Cross-framework evidence suggestions.
- Tasks and evidence requests.
- Three-attempt communication cadence and manager escalation.
- Audit trail.
- API and focused Prism workspace.

The initial pilot does not require every existing Sentinel connector to be production-configured. Existing adapters are carried forward where useful, but only sources required by the first pilot are completed and validated end to end.

## 19. Verification strategy

### 19.1 Repository isolation

- Confirm Prism is not in Sentinel's GitHub fork network.
- Confirm Prism contains no Sentinel remote, submodule, package dependency, or sync workflow.
- Confirm a Sentinel commit cannot enter Prism automatically.
- Confirm a Prism commit cannot enter Sentinel automatically.
- Run a secret scan before the first remote push.

### 19.2 Data isolation and security

- Verify that the control plane cannot read customer evidence.
- Verify that one customer environment cannot reach another.
- Test least-privileged support access, revocation, and audit logging.
- Test signed access expiration and tenant authorization.
- Verify that customer secrets remain in the customer Key Vault.

### 19.3 Evidence and mapping

- Test extraction and provenance for representative PDF, DOCX, CSV, and connector inputs.
- Test canonical-objective mappings independently from framework mappings.
- Test one artifact supporting several requirements with distinct framework outcomes.
- Test low-confidence and conflicting evidence review paths.
- Confirm AI-generated claims cite source artifacts and cannot silently become authoritative.

### 19.4 Communications

- Test three total contact attempts and manager escalation using a controlled clock.
- Test response, attachment, delivery failure, quiet hours, reassignment, and audit-window cadence.
- Confirm a delivered response stops inappropriate reminders.
- Confirm every attempt and escalation appears in the audit trail.

### 19.5 Resilience and lifecycle

- Test connector, AI, graph, index, message-provider, and control-plane outages independently.
- Confirm deterministic operations continue during AI and graph outages.
- Test complete export, access revocation, disconnect, reconnect, retention, and teardown.
- Confirm teardown reporting distinguishes immediate deletion from retention-bound expiration.

## 20. Success criteria

The first pilot is successful when Prism can demonstrate all of the following in one customer-owned Azure environment:

1. Deploy without creating a data dependency on Vulnaguard infrastructure.
2. Connect at least one live Microsoft or Google source.
3. Ingest one uploaded document and one connector observation.
4. Extract source-backed evidence claims with provenance.
5. Map one approved artifact through a canonical objective to requirements in at least two frameworks.
6. Explain the reuse and remaining limitations to a human reviewer.
7. Create and send an evidence request.
8. Execute the configured reminder and manager-escalation cadence.
9. Produce readiness views and a source-backed report.
10. Preserve operations during a simulated AI or graph outage.
11. Export the customer record and revoke Vulnaguard access.

## 21. Deferred decisions

The following choices do not block the approved product design and will be made in the implementation plan or an architecture spike:

- Exact Azure compute service.
- Exact relational database service and migration path from Supabase.
- Exact Azure graph storage and GraphRAG indexing implementation.
- Email and Teams delivery provider order.
- Prism repository name and final product-domain availability.
- SOC 2 and ISO/IEC 27001 framework-content licensing implementation.
- Pricing and packaging beyond the approved no-framework-tax principle.

Each deferred choice must preserve customer-owned data, framework neutrality, provenance, deterministic fallback behavior, and repository independence.

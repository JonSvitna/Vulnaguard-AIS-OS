---
title: Phase 10 — Sentinel Offboarding
phase: 10
updated: 2026-07-01
---

# Phase 10: Sentinel Offboarding

**Objective:** Formally offboard a client from Sentinel CMMC — export their data, revoke access, cancel the subscription, and close out the tenant cleanly.

**This phase applies when a client ends their Sentinel subscription, regardless of reason (contract expiration, non-renewal, cancellation, or migration to another tool).**

---

## Entry Criteria

- Client has provided written notice of subscription cancellation or non-renewal
- Subscription end date confirmed
- Client primary contact identified for offboarding coordination

---

## Activities

### 10.1 Confirm Offboarding Request
- Receive written cancellation notice (email is acceptable)
- Confirm the effective end date per subscription terms
- Log the offboarding request in the engagement/account record
- Assign an offboarding owner on the Vulnaguard side

### 10.2 Client Data Export
- Generate a full export of all client data:
  - Compliance status snapshots (per control, per framework)
  - POA&M items and status history
  - Evidence files (zip archive)
  - Risk register exports
  - All generated reports
- Deliver the export package to the client via secure file transfer
- Confirm client has received and can open the export before proceeding

### 10.3 Final Billing and Invoice
- Issue a final invoice per subscription terms (any outstanding balance, prorated charges, or final period billing)
- Confirm payment received before tenant deletion

### 10.4 Access Revocation
- Disable all client user accounts in Sentinel admin console
- Revoke any API keys or integrations the client provisioned
- Confirm no active sessions exist

### 10.5 Tenant Deletion (After Data Confirmed)
- Confirm in writing that the client has received and accepted their data export
- Delete the client tenant from Sentinel admin console
- Confirm deletion is complete — no residual data remains in the system
- Log deletion timestamp in the offboarding record

### 10.6 Remove Client from Billing
- Cancel recurring subscription in Stripe (or billing system)
- Confirm no future charges are scheduled
- Send the client a cancellation confirmation

### 10.7 Internal Closeout
- Archive the client's account record
- Capture offboarding notes: reason for leaving, any feedback the client provided, potential for re-engagement
- Flag any upsell or win-back opportunity if reason was cost or scope — not dissatisfaction

### 10.8 Offboarding Summary to Client
- Send a brief offboarding confirmation to the client:
  - Data export delivered and confirmed
  - Access revoked as of [date]
  - Tenant deleted as of [date]
  - Subscription cancelled, no further charges
  - Contact for any post-offboarding questions

---

## Outputs

- Delivered client data export (confirmed received)
- Final invoice (paid)
- Tenant deleted
- Subscription cancelled
- Offboarding confirmation sent

---

## Deliverables to Client

- Data export package
- Offboarding confirmation letter (summary of actions taken and dates)

---

## Quality Gate

- [ ] Written cancellation request on file
- [ ] Data export delivered and client confirmed receipt
- [ ] Final invoice paid
- [ ] All user accounts and API keys revoked
- [ ] Tenant deleted and confirmed empty
- [ ] Subscription cancelled in billing system
- [ ] Offboarding confirmation sent to client
- [ ] Internal account record archived

---

## Data Retention

- Vulnaguard retains metadata about the engagement (account name, service dates, offboarding date) for 7 years per standard business record retention
- Client CUI data is deleted at tenant deletion and is not retained by Vulnaguard post-offboarding
- If the client requests a certificate of data destruction, generate one using the offboarding log and signed confirmation

---

## Common Issues

**Client requests data export but doesn't confirm receipt:** Follow up twice. Do not delete the tenant until receipt is confirmed in writing. If the client is unreachable after 14 days of attempts, document the attempts, send a final notice to the address on file, and proceed with deletion.

**Client wants to pause, not cancel:** Offer a suspension option if Sentinel supports it. Document the suspension terms (duration, what happens to data, cost during suspension) in writing before proceeding.

**Client disputes final invoice:** Refer to the subscription agreement terms. If there is a legitimate billing error, issue a corrected invoice promptly. Do not delay tenant deletion over a disputed small balance — escalate if necessary.

**Client wants to export data but hasn't paid final invoice:** Do not release the data export until the invoice is paid (or a payment arrangement is confirmed in writing). This protects against data being taken without completing financial obligations.

**Client re-engages after offboarding:** Treat as a new client onboarding (Phase 9). Prior data is deleted and cannot be restored — communicate this clearly before any re-engagement discussion begins.

# Clay Lead Intake

Updated: 2026-07-19

## Purpose

Use Clay to source small-business prospects for Vulnaguard's CMMC, security,
systems/automation, and website/design services, then send only usable,
email-bearing leads into the existing `vulnaguard-seo-agent` qualification and
outreach pipeline. CMMC is the first and highest-confidence lane.

Clay does not provide a general synchronous API on non-Enterprise plans. The
supported API-like pattern is:

1. Find and enrich leads in a Clay table.
2. Use Clay's **HTTP API** enrichment to POST each completed row to an external
   webhook.
3. Let n8n validate and normalize the row.
4. Import through the SEO agent's existing duplicate-safe import route.

Official references:

- https://university.clay.com/docs/using-clay-as-an-api
- https://university.clay.com/docs/webhook-integration-guide
- https://university.clay.com/docs/http-api-integration-overview

## Live connection

- n8n workflow: `Clay Lead Intake to SEO Agent`
- Workflow ID: `A6kOqisezATjjT2Q`
- Status: active
- Method: `POST`
- Endpoint: `https://n8n-production-a4ee.up.railway.app/webhook/clay-leads-7f3d8e1c-52a9-4b67-91d0-6c4a2e8f5b13`
- Version-controlled workflow: `infra/n8n/clay-lead-intake.workflow.json`
- Destination: `POST https://vulnaguard-seo-agent-production.up.railway.app/api/marketing/leads/import-confirm`

The webhook acknowledges the request immediately. n8n continues the import in
the background, so Clay does not have to wait for AI qualification to finish.

## Ideal customer profile

The capability statement dated 2026-06-30 defines what Vulnaguard can deliver;
it does **not** restrict the market to government contractors. This corrected
profile is saved in Clay under **Settings > AI context**.

- Search the full United States across legitimate commercial industries.
- Prioritize privately held, owner-led companies with 2-50 employees. This is a
  delivery-capacity filter, not an industry filter.
- A 51-200 employee company may qualify only when the need is a bounded project
  with a relevant department owner. Do not target it for enterprise operations.
- Any company may qualify when it has a clear need for a cybersecurity or risk
  assessment, compliance/policy work, workflow automation, software/systems
  support, or website/digital design.
- Government contractors remain one valuable lane for CMMC/NIST services, but
  government-contract status is never required for general sourcing.
- Useful signals include an outdated or missing website, weak security posture,
  compliance pressure, recent growth, manual workflows, operational
  bottlenecks, and lack of senior technical staff.

### Service lanes

- **General cybersecurity:** small businesses needing a vulnerability/risk
  assessment, remediation plan, policy development, or executive reporting.
- **Compliance/CMMC:** government contractors and regulated SMBs with CMMC,
  NIST SP 800-171, GRC, evidence, or continuous-monitoring needs.
- **Systems/automation:** owner-led businesses with a visible manual workflow,
  reporting, intake, integration, or software problem.
- **Website/design:** owner-led businesses with no website or a clearly
  outdated/poor-performing site.

### Exclusions

- Fortune 500 and major public companies, massive hospitals/health systems,
  universities and large school systems, government agencies, national
  franchise parents, conglomerates, and companies above 500 employees.
- Any opportunity requiring enterprise-scale or 24/7 managed infrastructure.
- Staffing firms, job boards, junior contacts, and generic directory/community
  pages.
- Cybersecurity, CMMC, MSSP, web, marketing, and automation agencies that
  compete directly with the offered service.

Do not exclude an otherwise suitable local business merely because it is not a
government contractor or does not appear in the capability statement.

## Live Clay sources

### Broad U.S. SMB source

- Workbook: `Private US Companies, 2-10 Employees, Diverse Industries`
- Workbook ID: `wb_0tig3j6w3hc4rmRuHmm`
- Table ID: `t_0tig3j6r9TbnpFZvxim`
- View ID: `gv_0tig3j8HAw5f6vkfTud`
- Search chat: `cc_0tig3gs8GmUWK95w72P`
- Configured limit: 300 source-only companies.
- Filters: United States; privately held; 2-10 and 11-50 company-size buckets;
  estimated employees 2-50; broad commercial industries; enterprise,
  institutional, staffing, and direct-competitor exclusions.
- No enrichment or paid action was run.

### Contact-enrichment test

- People table: `Owner Founder, Small US Companies`
- Table ID: `t_0tig4fzDHn3UW4r7FkZ`
- View ID: `gv_0tig4g0gQPkS5sW8YhR`
- Search chat: `cc_0tig4eaZfUtNGMEAzWh`
- Run date: 2026-07-19
- Scope: 10 owner/founder/president contacts, one contact per company.
- Enrichments: person profile plus validated work-email waterfall.
- Projected cost shown before run: approximately 1.6 data credits and 2
  actions per row, or about 16 credits and 20 actions for the batch.
- Result: 9 work emails returned; one discovered email failed validation and
  the final waterfall output remained blank for that row.
- No contacts were posted to n8n or the SEO agent during this test.

### Focused CMMC source

- Workbook: `Defense Manufacturing, Engineering, US`
- Workbook ID: `wb_0tig3ciNVGjGucRT29T`
- Table ID: `t_0tig3cjNBuBdAB3vkFB`
- View ID: `gv_0tig3cjrTYuQFMTHFvv`
- Search chat: `cc_0tig38m5BY8zs5ba3Se`
- Created 2026-07-19 with 12 source-only companies.
- Filters: U.S.; privately held; company size 2-10; estimated employees 1-20;
  defense/manufacturing/engineering sectors; explicit federal-contracting
  signals; competitor and enterprise exclusions.
- No enrichment columns were added and no paid action was run on this table.

The earlier workbook `wb_0tig31gNrEaVfSZnptP` is a rejected exploration, not an
approved source. It lacked the corrected SMB ceiling and produced enterprise
and off-ICP results. Do not run or schedule it.

## Required Clay table columns

Keep these output names exactly as shown. The workflow accepts several common
Clay aliases, but canonical names make troubleshooting much easier.

| Column | Required | Notes |
|---|---:|---|
| `company_name` | yes | Reject the row if blank |
| `contact_email` | yes | Must be a syntactically valid email |
| `contact_name` | recommended | Or provide `first_name` + `last_name` |
| `contact_title` | recommended | Decision-maker targeting |
| `website` | recommended | Company domain or URL |
| `contact_linkedin` | recommended | Person LinkedIn URL |
| `location` | optional | City/state/country |
| `org_type` | optional | Industry or organization type |
| `employee_count` | optional | Company size |
| `category` | optional | Defaults to `sales` |
| `business_line` | optional | Defaults to `cmmc` |
| `persona_slug` | optional | Defaults to the SEO agent's normal voice behavior |

## Clay-side setup

1. Create a workbook/table using **Find Companies** or **Find People**. Start
   with a small sample, not the full trial allowance.
2. Add the enrichments needed to produce a verified work email and the fields
   above.
3. Add an enrichment and select **HTTP API**.
4. Set method to `POST` and use the live endpoint above.
5. Set header `Content-Type` to `application/json`.
6. Use this body, mapping each value to the matching Clay column:

```json
{
  "company_name": "{{company_name}}",
  "website": "{{website}}",
  "location": "{{location}}",
  "org_type": "{{org_type}}",
  "employee_count": "{{employee_count}}",
  "contact_name": "{{contact_name}}",
  "contact_title": "{{contact_title}}",
  "contact_email": "{{contact_email}}",
  "contact_linkedin": "{{contact_linkedin}}",
  "category": "sales",
  "business_line": "cmmc"
}
```

7. Set **Only run if** to require both `company_name` and a successful verified
   `contact_email`. If the email provider exposes a status, require its
   deliverable/valid value too.
8. Test one row. Confirm HTTP `200`, then confirm the company appears once in
   the SEO agent. Only then enable auto-update or run the selected batch.

Do not send rows with missing/invalid emails. The current outreach pipeline
deliberately parks no-email leads, so enriching and exporting them wastes trial
credits and creates unusable backlog.

## Validation and duplicate behavior

n8n rejects missing company names and invalid emails. The SEO agent then:

- deduplicates case-insensitively by company name;
- checks the other marketing system's sent-email history;
- imports the row with `source='csv_import'`, `category='sales'`, and
  `business_line='cmmc'`;
- runs the existing CMMC qualifier for new leads only.

Verified 2026-07-19 with existing lead `Veritech LLC`: n8n execution `2503`
completed successfully, reached `Import into SEO Agent`, and returned
`imported: 0`, `skipped_duplicates: 1`. No test lead was added and no qualifier
credit was spent.

## Trial-credit guardrails

- The live account showed 2,000 data credits and 10,000 actions per two weeks
  on 2026-07-19. Treat those as separate allowances, not 10,000 fully enriched
  leads. Different enrichments consume different data-credit amounts.
- Begin with 25 rows, inspect quality, then scale to 100 before any larger run.
- The first 10-contact test returned 9 work emails. Review service fit as well
  as deliverability before using that success rate to justify a larger batch.
- Filter for the actual ICP before paid enrichments: US-based defense
  contractors, suitable company size, relevant decision-maker title, and an
  active company domain.
- Send only verified email-bearing rows to the webhook.
- Keep outreach review/approval in the SEO agent. Clay supplies lead data; it
  does not bypass the existing approval gate.

### Daily volume design

The 200-300/day goal is a **raw sourcing** target, not an enrichment or sending
target. Keep the source net broad, then segment, deduplicate, and score without
paid data. Enrich/export only the best 50 combined prospects per day initially.
This preserves the trial allowance while building the larger top-of-funnel Sean
wants.

Recommended daily mix after each lane passes a small quality test:

| Lane | Raw source target | Enrich/export target |
|---|---:|---:|
| Broad U.S. SMB discovery | 150-200 | 20-30 |
| CMMC/federal supply chain | 25-50 | 10-15 |
| High-signal website/automation | 25-50 | 10-15 |
| **Total** | **200-300** | **up to 50** |

## Operations

- View runs in n8n under `Clay Lead Intake to SEO Agent`.
- A successful new row returns `imported: 1` in the final HTTP node execution.
- A duplicate returns `skipped_duplicates: 1`.
- Deactivate the workflow from n8n or with the n8n public API when the Clay
  trial ends if no continuing intake is wanted.

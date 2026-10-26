# SaaSBill (2026) — B2B SaaS True-Cost & Contract Trap Directory

**Live Public Directory:** [https://saasbill.io/](https://saasbill.io/)  
**Root Mirror:** [https://eriben02.github.io/](https://eriben02.github.io/)  
**Swedish Sister Directory (Systemkalkyl.se):** [https://eriben02.github.io/systemkalkyl/](https://eriben02.github.io/systemkalkyl/)

## Audited Pages & Interactive Calculators (GEO / AI-Search Optimized)
1. **Homepage Directory & Year-1 True-Cost Engine:** [`saasbill.io/`](https://saasbill.io/)
2. **HubSpot Pricing & Mandatory Onboarding Fees ($1,500–$7,000):** [`/pricing/hubspot-true-cost-and-onboarding-fees/`](https://saasbill.io/pricing/hubspot-true-cost-and-onboarding-fees/)
3. **Intercom Fin AI $0.99/Resolution Tax Calculator:** [`/pricing/intercom-fin-ai-resolution-cost-calculator/`](https://saasbill.io/pricing/intercom-fin-ai-resolution-cost-calculator/)
4. **Stripe, Shopify Payments & Paddle 180-Day Payout Holds & Token Portability:** [`/exit/stripe-shopify-paddle-frozen-funds-alternatives/`](https://saasbill.io/exit/stripe-shopify-paddle-frozen-funds-alternatives/)
5. **Monday CRM vs. Pipedrive vs. HubSpot (3-Seat Minimum Bucket Math):** [`/compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/`](https://saasbill.io/compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/)
6. **HIPAA BAA & SOC 2 Type II SaaS Tier Matrix & Negotiation Calculator:** [`/compliance/hipaa-baa-and-soc2-pricing-tiers/`](https://saasbill.io/compliance/hipaa-baa-and-soc2-pricing-tiers/)
7. **Zendesk AI Outcome Pricing Calculator ($1.50–$2.00 per Automated Resolution) vs. Freshdesk & Help Scout:** [`/pricing/zendesk-ai-resolution-and-automated-outcome-cost/`](https://saasbill.io/pricing/zendesk-ai-resolution-and-automated-outcome-cost/) — published 2026-10-25
8. **Gumroad (10% + 50¢ + processing) vs. Whop (2.7% + 30¢) vs. Lemon Squeezy (5% + 50¢) Net Payout Calculator:** [`/compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/`](https://saasbill.io/compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/) — published 2026-10-26

## Machine-Readable AI & Search Endpoints
- [`/llms.txt`](https://saasbill.io/llms.txt)
- [`/llms-full.txt`](https://saasbill.io/llms-full.txt)
- [`/robots.txt`](https://saasbill.io/robots.txt)
- [`/sitemap.xml`](https://saasbill.io/sitemap.xml)

## Click & Interaction Tracking Architecture (Prepared — No External Analytics Installed)
No third-party analytics script (GA4, Plausible, PostHog) is loaded in `<head>` or `<body>`. All interactive elements emit structured `data-track` attributes and push events to the local in-memory queue `window.__saasbillEvents` so an analytics collector can be attached later without modifying templates:

1. `calculator_interaction` — Fired on `input` across calculator controls (`[data-track="calculator-control"]`, range sliders, and dropdowns). Captures `control` (`seats`, `ai-tickets`, `billing-mode`, `sort-mode`, or subpage control ID), `value`, and timestamp `ts`.
2. `category_select` — Fired when a user clicks a category pill tab (`[data-track="category-select"]`) or switches category. Captures `category` and `ts`.
3. `result_rendered` — Fired whenever the calculator renders or updates a scenario (`renderDirectory()`). Captures active `category`, `seats`, `aiTickets`, `billingMode`, `sortMode`, and `ts`.
4. `vendor_cta_click` — Fired when a visitor clicks a direct vendor link (`[data-track="vendor-cta"]`). Captures `vendor` (tool slug), `location` (`summary-card`, `chart-row`, `table-row`, or `subpage-result`), destination `href`, and `ts`.

import json
from layout import load_data, render_page, SITE_ORIGIN

TOOLS, AFFILIATES = load_data()
tools_js = json.dumps(TOOLS)
aff_js = json.dumps(AFFILIATES)

# ---------------------------------------------------------
# 1. Homepage: /index.html
# ---------------------------------------------------------
home_body = f"""
<section class="hero editorial-hero">
  <h1>Your SaaS bill is lying to you.</h1>
  <p class="lead">Most teams only look at the sticker price. But mandatory onboarding fees, seat-bucket minimums, and metered AI overages compound quietly&mdash;and can significantly increase the real Year-1 cost of your tools.</p>
</section>

<div class="editorial-cat-bar">
  <div class="editorial-cat-top">
    <div class="cat-tabs" role="tablist" aria-label="Software Categories">
      <button type="button" class="cat-tab active" data-cat="Helpdesk & AI Support" data-track="category-select">Helpdesk &amp; AI Support</button>
      <button type="button" class="cat-tab" data-cat="CRM & Sales" data-track="category-select">CRM &amp; Sales</button>
      <button type="button" class="cat-tab" data-cat="Compliance, HIPAA & SOC 2" data-track="category-select">Compliance &amp; SOC 2</button>
      <button type="button" class="cat-tab" data-cat="Payment Processors & MoR" data-track="category-select">Payment Processors</button>
      <button type="button" class="cat-tab" data-cat="ALL" data-track="category-select">All Audited Tools</button>
    </div>
  </div>
</div>

<section class="calc-box editorial-workbench" aria-labelledby="calc-heading">
  <h2 id="calc-heading" class="sr-only-control">Interactive Year-1 True-Cost Calculator (2026)</h2>
  <div class="control-group sr-only-control">
    <label for="cat-filter">Software category</label>
    <select id="cat-filter" data-track="calculator-control" data-control="category">
      <option value="Helpdesk & AI Support" selected>Helpdesk &amp; AI Support (6 tools)</option>
      <option value="CRM & Sales">CRM &amp; Sales (5 tools)</option>
      <option value="Compliance, HIPAA & SOC 2">Compliance, HIPAA &amp; SOC 2 (4 tools)</option>
      <option value="Payment Processors & MoR">Payment Processors &amp; MoR (5 rails)</option>
      <option value="ALL">All Subscription SaaS (15 tools)</option>
    </select>
  </div>

  <div class="workbench-grid">
    <!-- Left Column: ESTIMATE YOUR TRUE COST -->
    <div class="wb-col-controls">
      <div class="wb-col-title">Estimate Your True Cost</div>
      <div class="wb-controls-stack">
        <div class="wb-control-item" id="tool-select-group">
          <label class="wb-control-label" for="spotlight-tool-select">Platform to inspect</label>
          <select id="spotlight-tool-select" class="wb-tool-select" data-track="calculator-control" data-control="spotlight-tool"></select>
        </div>

        <div class="wb-control-item" id="seat-control-group">
          <span class="wb-control-label">Users / seats</span>
          <div class="wb-slider-row">
            <input type="range" id="seat-slider" min="1" max="50" value="5" aria-label="Users / seats" data-track="calculator-control" data-control="seats" />
            <span class="wb-slider-val" id="seat-val">5</span>
          </div>
        </div>

        <div class="wb-control-item" id="ai-control-group">
          <span class="wb-control-label">AI-resolved tickets / month</span>
          <div class="wb-slider-row">
            <input type="range" id="ai-slider" min="0" max="5000" step="100" value="500" aria-label="AI-resolved tickets per month" data-track="calculator-control" data-control="ai-tickets" />
            <span class="wb-slider-val" id="ai-val">500</span>
          </div>
        </div>

        <div class="wb-quiet-options" id="billing-control-group">
          <div class="wb-quiet-field">
            <label for="billing-mode">Billing:</label>
            <select id="billing-mode" data-track="calculator-control" data-control="billing-mode">
              <option value="annual">Annual</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Center Column: YOUR ESTIMATED TRUE COST (Static DOM 3-Row Vertical Stacked Bar + Leader Lines) -->
    <div class="wb-col-chart">
      <div class="wb-col-title" id="wb-chart-col-title">Your Estimated True Cost</div>
      <div id="wb-vbar-mount" class="wb-vbar-container" aria-live="polite">
        <div class="wb-vbar-row" id="wb-row-base" style="flex: 11.5 1 0px;">
          <div class="wb-vbar-block block-base">
            <span class="wb-block-amount" id="wb-amt-base">$660</span>
          </div>
          <div class="wb-callout-item">
            <div class="wb-leader-line"></div>
            <div class="wb-callout-text">
              <strong id="wb-call-title-base">Sticker Price: Base plan</strong>
              <span id="wb-call-sub-base">1st seat at advertised rate</span>
            </div>
          </div>
        </div>

        <div class="wb-vbar-row" id="wb-row-seats" style="flex: 20.91 1 0px;">
          <div class="wb-vbar-block block-seats">
            <span class="wb-block-amount" id="wb-amt-seats">$2,640</span>
          </div>
          <div class="wb-callout-item">
            <div class="wb-leader-line"></div>
            <div class="wb-callout-text">
              <strong id="wb-call-title-seats">Sticker Price: Added seats</strong>
              <span id="wb-call-sub-seats">Remaining team seat licenses</span>
            </div>
          </div>
        </div>

        <div class="wb-vbar-row" id="wb-row-hidden" style="flex: 67.59 1 0px;">
          <div class="wb-vbar-block block-hidden">
            <span class="wb-block-amount" id="wb-amt-hidden">$8,550</span>
          </div>
          <div class="wb-callout-item">
            <div class="wb-leader-line"></div>
            <div class="wb-callout-text">
              <strong id="wb-call-title-hidden">Hidden Cost Gap</strong>
              <span id="wb-call-sub-hidden">Onboarding, AI overages &amp; minimums</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Selected Product Header + Huge Editorial Serif Total + Fixed-Height Explanation + Primary CTA -->
    <div class="wb-result-col" id="wb-result-mount" aria-live="polite">
      <div class="wb-selected-product" id="wb-selected-product">Zendesk Suite Team + AI</div>
      <div class="wb-big-total" id="wb-big-total-wrap"><span id="wb-big-amount">$11,850</span> <span class="wb-per-year" id="wb-big-unit">/ year</span></div>
      <p class="wb-budget-quote" id="wb-budget-quote">That&rsquo;s the number to budget for.<br/>Not the number on the invoice.</p>
      <p class="wb-budget-subnote" id="wb-budget-subnote"></p>
      <div class="cta-stack">
        <a id="wb-primary-cta" class="btn-cta wb-primary-cta" href="https://www.zendesk.com/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="zendesk-suite-team" data-cta-location="workbench">View Zendesk pricing &rarr;</a>
      </div>
    </div>
  </div>
</section>

<!-- THE HIDDEN COST GAP: Editorial Comparison Table -->
<section class="hidden-gap-section" aria-labelledby="gap-heading">
  <div class="gap-eyebrow">The Hidden Cost Gap</div>
  <h2 id="gap-heading">Sticker Price vs. True Cost</h2>
  <div class="gap-toolbar">
    <p class="gap-subhead" id="gap-dynamic-subhead">All 5 tools compared for 5 seats &middot; annual billing &middot; 500 AI tickets/mo &mdash; click any row to inspect its breakdown above.</p>
    <div class="wb-quiet-field gap-sort-field" id="sort-control-group">
      <label for="sort-mode">Sort:</label>
      <select id="sort-mode" data-track="calculator-control" data-control="sort-mode">
        <option value="lowest" selected>Lowest cost</option>
        <option value="hidden_fees">Hidden gap</option>
        <option value="highest">Highest cost</option>
        <option value="name">A&ndash;Z</option>
      </select>
    </div>
  </div>

  <div class="table-wrap editorial-gap-table mobile-cards">
    <table>
      <caption>2026 B2B Software Year-1 True-Cost Comparison &amp; Contract Audit (USD, verified Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th id="th-col-1">Scenario</th>
          <th id="th-col-2"><span class="legend-dot dot-sticker" aria-hidden="true"></span>Sticker Price / Year</th>
          <th id="th-col-3">True Cost / Year (Est.)</th>
          <th id="th-col-4"><span class="legend-dot dot-hidden" aria-hidden="true"></span>Hidden Cost Gap</th>
          <th id="th-col-5">Official Pricing</th>
        </tr>
      </thead>
      <tbody id="calc-tbody"></tbody>
    </table>
  </div>

  <div class="table-disclaimer">
    <span aria-hidden="true">&#128196;</span>
    <span>Results will vary based on team size, usage patterns, and tool complexity. Use this as a guide, not a guarantee.</span>
  </div>
  <p id="calc-payment-note" style="font-size:0.8rem; color:var(--muted); margin-top:6px;">
    <strong>Payment Processors &amp; MoR (Fees vs. Temporary Reserves):</strong> Because payment rails charge per transaction rather than per seat, selecting <em>Payment Processors</em> models a standardized benchmark of <strong>$50,000/month GMV across 1,000 transactions ($50 AOV, 30% international cards)</strong>. <strong>Estimated monthly processing fees</strong> (percentage + per-transaction + FX/billing surcharges) are shown separately from <strong>potential funds temporarily held</strong> (such as a 25% rolling reserve held for 90&ndash;180 days on a risk flag, which is a cashflow hold rather than a fee). To model your exact volume, open the <a href="./exit/stripe-shopify-paddle-frozen-funds-alternatives/">Interactive Payout Hold &amp; Reserve Simulator &rarr;</a>
  </p>
</section>

<section id="all-calculators" class="editorial-below-section">
  <div class="gap-eyebrow">Specialized Simulators</div>
  <h2>Deep-dive calculators &amp; contract audits</h2>
  <p class="gap-subhead">Dedicated models for onboarding tiers, AI resolution packs, payout reserve holds, and SOC 2 audit quotes.</p>
  <div class="card-grid">
    <div class="card">
      <span class="badge badge-high">CRM &amp; Sales &middot; Onboarding Tiers</span>
      <h3><a href="./pricing/hubspot-true-cost-and-onboarding-fees/">HubSpot Year-1 calculator &amp; onboarding audit</a></h3>
      <p>Model Sales Pro, Marketing Pro, and Enterprise onboarding fees alongside Close CRM and Pipedrive for 1 to 30 reps.</p>
    </div>
    <div class="card">
      <span class="badge badge-medium">CRM &amp; Sales &middot; Seat Buckets</span>
      <h3><a href="./compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/">monday CRM 3/5/10-seat bucket calculator</a></h3>
      <p>See the exact headcount thresholds where monday CRM&rsquo;s fixed seat blocks cost more&mdash;or less&mdash;than 1:1 per-seat CRMs.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Helpdesk &amp; AI &middot; Fin AI Meter</span>
      <h3><a href="./pricing/intercom-fin-ai-resolution-cost-calculator/">Intercom Fin ($0.99/resolution) cost simulator</a></h3>
      <p>Test how monthly ticket volume and AI resolution rate scale your Intercom bill versus Freshdesk Freddy AI session packs.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Helpdesk &amp; AI &middot; Outcome Tiers</span>
      <h3><a href="./pricing/zendesk-ai-resolution-and-automated-outcome-cost/">Zendesk AI automated resolution overage calculator</a></h3>
      <p>Compare Zendesk&rsquo;s included 5&ndash;10 AR/agent allowance and $1.50&ndash;$2.00 overage rates against Help Scout and Freshdesk.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Payments &amp; MoR &middot; Cashflow Risk</span>
      <h3><a href="./exit/stripe-shopify-paddle-frozen-funds-alternatives/">Stripe, Shopify &amp; Paddle payout hold simulator</a></h3>
      <p>Simulate a 25% rolling reserve and capital loan holdback, and compare card-token portability across payment rails.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Payments &amp; MoR &middot; Take Rates</span>
      <h3><a href="./compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/">Gumroad vs. Whop vs. Lemon Squeezy net payout calculator</a></h3>
      <p>Compare Gumroad&rsquo;s 10% + 50&cent; (plus 2.9% + 30&cent; processing), Lemon Squeezy&rsquo;s 5% + 50&cent; surcharges and Whop&rsquo;s 2.7% + 30&cent; for your price and volume.</p>
    </div>
    <div class="card">
      <span class="badge badge-low">Compliance &middot; HIPAA &amp; SOC 2</span>
      <h3><a href="./compliance/hipaa-baa-and-soc2-pricing-tiers/">HIPAA BAA tiers &amp; SOC 2 + CPA auditor estimator</a></h3>
      <p>Check self-serve HIPAA BAA and SAML SSO plans and estimate negotiated Vanta/Drata quotes plus external CPA audit fees.</p>
    </div>
  </div>
</section>

<section class="editorial-below-section">
  <div class="gap-eyebrow">Beyond the Calculator</div>
  <h2>Three contract clauses that never show up on a pricing page</h2>
  <div class="methodology-grid fine-print-grid">
    <div class="methodology-item">
      <strong>1. 30–60 Day Auto-Renewal Locks</strong>
      Annual SaaS order forms (including HubSpot and Zendesk) typically disallow mid-term seat downgrades and require written non-renewal notice 30 to 60 days before term end&mdash;or the contract auto-renews at list rate.
    </div>
    <div class="methodology-item">
      <strong>2. Card-Vault Ownership &amp; Rolling Reserves</strong>
      Direct processors (Stripe, Whop) let you export card tokens if you face a 25% rolling reserve. Merchants of Record (Paddle, Lemon Squeezy) are the legal seller of record and lock subscriber card tokens on termination.
    </div>
    <div class="methodology-item">
      <strong>3. SOC 2 Platform vs. External CPA Fees</strong>
      Compliance automation quotes (Vanta, Drata) are routinely negotiated down 30%&ndash;50% from list price, but never include the mandatory $6,500&ndash;$15,000+ independent CPA penetration and audit fee.
    </div>
  </div>
</section>

<section id="methodology" class="methodology-box" aria-labelledby="methodology-heading">
  <h2 id="methodology-heading" style="margin-top:0;">How we calculate &amp; verify Year-1 costs</h2>
  <p style="color:var(--muted); font-size:0.94rem;">Every figure on SaaSBill is computed from deterministic formulas and linked directly to the vendor&rsquo;s published pricing page, help-center billing documentation, or Master Subscription Agreement (MSA).</p>
  <div class="methodology-grid">
    <div class="methodology-item">
      <strong>1. Year-1 Total Formula</strong>
      <code>Year-1 Total = (12 &times; Billed Monthly Seats) + Mandatory Onboarding + (12 &times; Net AI Overage)</code>. Seat minimums and included AI allowances are applied automatically based on your slider inputs.
    </div>
    <div class="methodology-item">
      <strong>2. Verification Status Badges</strong>
      <span class="status-pill status-verified">Verified</span> indicates published self-serve pricing and contract terms checked directly against official vendor docs on Oct 25, 2026.<br/>
      <span class="status-pill status-estimated">Estimated (Benchmark)</span> indicates non-public, sales-quoted pricing modeled from verified buyer contract benchmarks.
    </div>
    <div class="methodology-item">
      <strong>3. Editorial Independence &amp; Sources</strong>
      Every CTA button links directly to the vendor&rsquo;s official site (<code>rel="nofollow noopener"</code>), alongside a primary-source link for contract verification. Some outbound links are affiliate links that may earn a commission at no extra cost to you; calculations and rankings are strictly formula-driven. Spot a pricing change? Email <a href="mailto:info@saasbill.io">info@saasbill.io</a>.
    </div>
  </div>
</section>

<script>
const TOOLS = {tools_js};
const AFFILIATES = {aff_js};

function calcEffectiveSeats(tool, seats) {{
  if (tool.id === 'monday-crm') {{
    if (seats <= 3) return 3;
    if (seats <= 5) return 5;
    if (seats <= 10) return 10;
    return Math.ceil(seats / 5) * 5;
  }}
  if (tool.id === 'help-scout-plus' && seats > 50) return Math.max(seats, 10);
  return Math.max(seats, tool.seat_minimum || 1);
}}

function calcToolYear1(t, seats, aiVol, mode) {{
  const effSeats = calcEffectiveSeats(t, seats);
  const unitRate = mode === 'annual' ? t.advertised_monthly_price_usd : t.monthly_billing_price_usd;
  let monthlySoftware = 0;
  let seatPaddingAnnual = 0;
  if (t.id === 'hubspot-marketing-pro') {{
    monthlySoftware = unitRate + Math.max(0, seats - 3) * 45;
  }} else if (t.id === 'vanta-soc2' || t.id === 'drata-soc2' || t.id === 'jotform-hipaa') {{
    monthlySoftware = unitRate;
  }} else {{
    monthlySoftware = effSeats * unitRate;
    seatPaddingAnnual = Math.max(0, effSeats - seats) * unitRate * 12;
  }}
  let aiAnnual = 0;
  let aiNote = '';
  if (t.id === 'zendesk-suite-team') {{
    const incl = Math.min(seats * 5, 833);
    const overageRate = mode === 'annual' ? 1.50 : 2.00;
    const aiMonthly = Math.max(0, aiVol - incl) * overageRate;
    aiAnnual = Math.round(aiMonthly * 12);
    aiNote = `${{incl}} AR/mo incl., then $${{overageRate.toFixed(2)}}/${{mode === 'annual' ? 'committed' : 'PAYG'}}`;
  }} else if (t.id === 'zendesk-suite-professional') {{
    const incl = Math.min(seats * 10, 833);
    const overageRate = mode === 'annual' ? 1.50 : 2.00;
    const aiMonthly = Math.max(0, aiVol - incl) * overageRate;
    aiAnnual = Math.round(aiMonthly * 12);
    aiNote = `${{incl}} AR/mo incl., then $${{overageRate.toFixed(2)}}/${{mode === 'annual' ? 'committed' : 'PAYG'}}`;
  }} else if (t.id === 'freshdesk-support') {{
    const annualSessions = aiVol * 12;
    const billableSessions = Math.max(0, annualSessions - 500);
    const packs = Math.ceil(billableSessions / 100);
    aiAnnual = packs * 49;
    aiNote = `500 1x free sessions, then $49/100 sessions (${{packs}} packs/yr)`;
  }} else {{
    const aiMonthly = (t.ai_per_resolution_usd || 0) * aiVol;
    aiAnnual = Math.round(aiMonthly * 12);
    if (t.ai_per_resolution_usd > 0) {{
      aiNote = `$${{t.ai_per_resolution_usd.toFixed(2)}}/resolution (${{aiVol.toLocaleString()}}/mo)`;
    }}
  }}
  const annualSeatsCost = Math.round(monthlySoftware * 12);
  const onboarding = Math.round(t.mandatory_onboarding_fee_usd || 0);
  const year1Total = annualSeatsCost + onboarding + aiAnnual;
  const hiddenFees = onboarding + aiAnnual + seatPaddingAnnual;
  return {{
    tool: t,
    effSeats,
    unitRate,
    monthlySoftware,
    annualSeatsCost,
    onboarding,
    aiAnnual,
    seatPaddingAnnual,
    hiddenFees,
    aiNote,
    year1Total
  }};
}}

const VENDOR_CTA_LABELS = {{
  'hubspot-sales-pro': 'View HubSpot pricing →',
  'hubspot-marketing-pro': 'View HubSpot pricing →',
  'hubspot-service-hub': 'View HubSpot pricing →',
  'close-crm': 'View Close pricing →',
  'pipedrive-crm': 'View Pipedrive pricing →',
  'monday-crm': 'View monday CRM pricing →',
  'intercom-fin-ai': 'View Intercom pricing →',
  'freshdesk-support': 'View Freshdesk pricing →',
  'zendesk-suite-team': 'View Zendesk pricing →',
  'zendesk-suite-professional': 'View Zendesk pricing →',
  'help-scout-plus': 'View Help Scout pricing →',
  'stripe-payments': 'View Stripe pricing →',
  'paddle-mor': 'View Paddle pricing →',
  'whop-payments': 'View Whop Payments pricing →',
  'lemon-squeezy': 'View Lemon Squeezy pricing →',
  'chargeflow': 'View Chargeflow pricing →',
  'jotform-hipaa': 'View Jotform HIPAA pricing →',
  '1password-business': 'View 1Password pricing →',
  'vanta-soc2': 'View Vanta pricing →',
  'drata-soc2': 'View Drata pricing →'
}};

const INTERNAL_AUDIT_LINKS = {{
  'hubspot-sales-pro': {{ url: './pricing/hubspot-true-cost-and-onboarding-fees/', label: 'Read HubSpot onboarding audit →' }},
  'hubspot-marketing-pro': {{ url: './pricing/hubspot-true-cost-and-onboarding-fees/', label: 'Read HubSpot onboarding audit →' }},
  'hubspot-service-hub': {{ url: './pricing/hubspot-true-cost-and-onboarding-fees/', label: 'Read HubSpot onboarding audit →' }},
  'close-crm': {{ url: './pricing/hubspot-true-cost-and-onboarding-fees/', label: 'Compare vs. HubSpot →' }},
  'pipedrive-crm': {{ url: './compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/', label: 'Read 1–15 seat comparison →' }},
  'monday-crm': {{ url: './compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/', label: 'Read 3-seat bucket audit →' }},
  'intercom-fin-ai': {{ url: './pricing/intercom-fin-ai-resolution-cost-calculator/', label: 'Read Intercom $0.99 AI audit →' }},
  'freshdesk-support': {{ url: './pricing/intercom-fin-ai-resolution-cost-calculator/', label: 'Compare AI session packs →' }},
  'zendesk-suite-team': {{ url: './pricing/zendesk-ai-resolution-and-automated-outcome-cost/', label: 'Read Zendesk AI overage audit →' }},
  'zendesk-suite-professional': {{ url: './pricing/zendesk-ai-resolution-and-automated-outcome-cost/', label: 'Read Zendesk AI overage audit →' }},
  'help-scout-plus': {{ url: './pricing/zendesk-ai-resolution-and-automated-outcome-cost/', label: 'Compare vs. Zendesk AI →' }},
  'stripe-payments': {{ url: './exit/stripe-shopify-paddle-frozen-funds-alternatives/', label: 'Open reserve simulator →' }},
  'paddle-mor': {{ url: './exit/stripe-shopify-paddle-frozen-funds-alternatives/', label: 'Read MoR token lock-in audit →' }},
  'whop-payments': {{ url: './exit/stripe-shopify-paddle-frozen-funds-alternatives/', label: 'Open reserve simulator →' }},
  'lemon-squeezy': {{ url: './exit/stripe-shopify-paddle-frozen-funds-alternatives/', label: 'Read MoR token audit →' }},
  'chargeflow': {{ url: './exit/stripe-shopify-paddle-frozen-funds-alternatives/', label: 'Open reserve simulator →' }},
  'jotform-hipaa': {{ url: './compliance/hipaa-baa-and-soc2-pricing-tiers/', label: 'Read HIPAA BAA tier matrix →' }},
  '1password-business': {{ url: './compliance/hipaa-baa-and-soc2-pricing-tiers/', label: 'Read SSO & BAA audit →' }},
  'vanta-soc2': {{ url: './compliance/hipaa-baa-and-soc2-pricing-tiers/', label: 'Open SOC 2 + auditor estimator →' }},
  'drata-soc2': {{ url: './compliance/hipaa-baa-and-soc2-pricing-tiers/', label: 'Open SOC 2 + auditor estimator →' }}
}};

function getVendorCtaLabel(tool) {{
  return VENDOR_CTA_LABELS[tool.id] || `View ${{tool.vendor || tool.name}} pricing →`;
}}

function formatScenarioText(cat, seats, aiVol, mode) {{
  const seatStr = `${{seats}} seat${{seats === 1 ? '' : 's'}}`;
  const billStr = mode === 'annual' ? 'annual billing' : 'monthly billing';
  if (cat === 'Helpdesk & AI Support' || cat === 'ALL') {{
    return `Based on ${{seatStr}}, ${{billStr}}, ${{aiVol.toLocaleString()}} AI tickets/month`;
  }}
  return `Based on ${{seatStr}}, ${{billStr}}`;
}}

function formatHiddenReason(r) {{
  const parts = [];
  if (r.onboarding > 0) parts.push(`$${{r.onboarding.toLocaleString()}} mandatory onboarding`);
  if (r.aiAnnual > 0) parts.push(`$${{r.aiAnnual.toLocaleString()}}/yr metered AI charges`);
  if (r.seatPaddingAnnual > 0) parts.push(`$${{r.seatPaddingAnnual.toLocaleString()}}/yr unused seat-minimum padding`);
  if (parts.length === 0) return `No mandatory onboarding or metered AI overages ($0 non-seat fees)`;
  return `Adds ${{parts.join(' + ')}} on top of $${{r.annualSeatsCost.toLocaleString()}} base licenses`;
}}

// Compute high-fidelity proportional flex shares (sum = 100, each in [9, 82] -> 23px to 207px inside the 252px container)
// A 9% floor (23px) keeps the leader line and a compact 1-line label aligned at $0 or small values, while 73% of the height scales 1:1 with the true dollar amounts!
function computeSmoothBarShares(v1, v2, v3) {{
  const vals = [Math.max(0, v1), Math.max(0, v2), Math.max(0, v3)];
  const total = vals[0] + vals[1] + vals[2];
  if (total <= 0) return [33.3, 33.3, 33.4];
  const MIN_SHARE = 11.5; // 36px out of 310px so label & amount never clip
  let shares = [0, 0, 0];
  let locked = [false, false, false];
  let remainingShare = 100;
  for (let pass = 0; pass < 3; pass++) {{
    let unlockedTotal = 0;
    for (let i = 0; i < 3; i++) {{
      if (!locked[i]) unlockedTotal += vals[i];
    }}
    if (unlockedTotal <= 0) {{
      const unlockedCount = locked.filter(x => !x).length;
      for (let i = 0; i < 3; i++) {{
        if (!locked[i]) shares[i] = remainingShare / Math.max(1, unlockedCount);
      }}
      break;
    }}
    let changed = false;
    for (let i = 0; i < 3; i++) {{
      if (!locked[i]) {{
        const raw = (vals[i] / unlockedTotal) * remainingShare;
        if (raw < MIN_SHARE) {{
          shares[i] = MIN_SHARE;
          locked[i] = true;
          remainingShare -= MIN_SHARE;
          changed = true;
        }} else {{
          shares[i] = raw;
        }}
      }}
    }}
    if (!changed) break;
  }}
  return shares.map(s => Number(s.toFixed(2)));
}}

function applyBarRowState(rowEl, share, val) {{
  if (!rowEl) return;
  rowEl.style.flex = `${{share}} 1 0px`;
  rowEl.classList.remove('is-compact');
  rowEl.classList.toggle('is-zero', val === 0);
}}

const PAY_PROFILES = {{
  'stripe-payments': {{
    b: 1450,
    s: 300,
    h: 575,
    total: 2325,
    held: 12500,
    unit: '/ mo est. fees',
    callTitleBase: 'Base percentage fee (2.9%)',
    callSubBase: '2.9% on $50,000/mo GMV ($1,450/mo)',
    callTitleSeats: 'Per-transaction fee ($0.30)',
    callSubSeats: '$0.30 × 1,000 monthly transactions ($300/mo)',
    callTitleHidden: 'Billing & FX surcharges',
    callSubHidden: '+0.7% Billing ($350) + 1.5% intl cards ($225)',
    quote: '<strong>Estimated monthly processing fees:</strong> $2,325/mo<br/><strong>Potential funds temporarily held:</strong> $12,500/mo (25% reserve scenario &mdash; not a fee)',
    sub: 'Assumptions ($50k/mo GMV, 1,000 tx, 30% intl): $1,750 base fees (2.9% + $0.30) + $575 Billing/FX surcharges = $2,325/mo in processing fees. Separately, up to $12,500/mo can be temporarily held (90–180 days) if a 25% rolling reserve triggers.',
    tableFeeSub: '$1,750 base (2.9% + $0.30) + $575 Billing/FX',
    tableHeldPill: '$12,500 / mo temporarily held',
    tableHeldSub: 'If 25% rolling reserve triggers (held 90–180 days, not a fee) · Portable card tokens'
  }},
  'paddle-mor': {{
    b: 2500,
    s: 500,
    h: 450,
    total: 3450,
    held: 12500,
    unit: '/ mo est. fees',
    callTitleBase: 'Base MoR fee (5.0%)',
    callSubBase: '5.0% on $50,000/mo GMV incl. global VAT handling',
    callTitleSeats: 'Per-transaction fee ($0.50)',
    callSubSeats: '$0.50 × 1,000 monthly transactions ($500/mo)',
    callTitleHidden: 'FX conversion spread',
    callSubHidden: 'Est. currency spread on 30% non-USD volume ($450)',
    quote: '<strong>Estimated monthly processing fees:</strong> $3,450/mo<br/><strong>Potential funds temporarily held:</strong> $12,500/mo (25% payout hold risk &mdash; not a fee)',
    sub: 'Assumptions ($50k/mo GMV, 1,000 tx, 30% intl): $3,000 base MoR fees (5.0% + $0.50) + $450 est. FX spread = $3,450/mo in processing fees. Separately, up to $12,500/mo can be temporarily held on risk review (card vault locked by Paddle).',
    tableFeeSub: '$3,000 MoR base (5.0% + $0.50) + $450 est. FX spread',
    tableHeldPill: '$12,500 / mo temporarily held',
    tableHeldSub: 'If 25% payout hold triggers on review (not a fee) · Non-exportable MoR card vault'
  }},
  'whop-payments': {{
    b: 1650,
    s: 400,
    h: 225,
    total: 2275,
    held: 0,
    unit: '/ mo est. fees',
    callTitleBase: 'Base card processing (2.7% + $0.30)',
    callSubBase: '2.7% ($1,350) + $0.30 × 1,000 tx ($300) on $50k/mo',
    callTitleSeats: 'Multi-processor orchestration (0.8%)',
    callSubSeats: '+0.8% waterfall failover routing on $50k/mo ($400)',
    callTitleHidden: 'International card surcharge',
    callSubHidden: '+1.5% on 30% cross-border card volume ($225)',
    quote: '<strong>Estimated monthly processing fees:</strong> $2,275/mo ($1,875/mo without orchestration)<br/><strong>Potential funds temporarily held:</strong> $0/mo (multi-acquirer failover routing)',
    sub: 'Assumptions ($50k/mo GMV, 1,000 tx, 30% intl): $1,650 base fees (2.7% + $0.30) + $400 multi-processor orchestration (0.8%) + $225 international card fees = $2,275/mo with orchestration ($1,875/mo without orchestration).',
    tableBaseAmt: 1650,
    tableFeeSub: '$1,650 base + $400 orchestration (0.8%) + $225 intl ($1,875/mo without orchestration)',
    tableHeldPill: '$0 single-PSP hold exposure',
    tableHeldSub: 'Multi-acquirer failover routing (+0.8% / $400/mo included in fees) avoids single-processor freezes'
  }},
  'lemon-squeezy': {{
    b: 2500,
    s: 500,
    h: 475,
    total: 3475,
    held: 12500,
    unit: '/ mo est. fees',
    callTitleBase: 'Base MoR fee (5.0%)',
    callSubBase: '5.0% on $50,000/mo GMV incl. global tax MoR',
    callTitleSeats: 'Per-transaction fee ($0.50)',
    callSubSeats: '$0.50 × 1,000 monthly transactions ($500/mo)',
    callTitleHidden: 'Subscription & intl surcharges',
    callSubHidden: '+0.5% subscriptions ($250) + 1.5% intl ($225)',
    quote: '<strong>Estimated monthly processing fees:</strong> $3,475/mo<br/><strong>Potential funds temporarily held:</strong> $12,500/mo (25% reserve scenario &mdash; not a fee)',
    sub: 'Assumptions ($50k/mo GMV, 1,000 tx, 30% intl): $3,000 base MoR fees (5.0% + $0.50) + $475 subscription/intl surcharges = $3,475/mo in processing fees. Separately, up to $12,500/mo can be temporarily held under underlying Stripe reserve rules.',
    tableFeeSub: '$3,000 MoR base (5.0% + $0.50) + $475 sub/intl fees',
    tableHeldPill: '$12,500 / mo temporarily held',
    tableHeldSub: 'If 25% rolling reserve triggers (not a fee) · Subject to underlying Stripe risk rules'
  }},
  'chargeflow': {{
    b: 0,
    s: 350,
    h: 150,
    total: 500,
    held: 0,
    unit: '/ mo est. fees',
    callTitleBase: 'Monthly platform fee',
    callSubBase: '$0 fixed monthly fee — performance-only model',
    callTitleSeats: 'Win-based recovery fee (25%)',
    callSubSeats: '25% success fee on $1,400/mo won disputes ($350)',
    callTitleHidden: 'Card-network dispute fees',
    callSubHidden: 'Est. $15 network dispute fee × 10 cases/mo ($150)',
    quote: '<strong>Estimated monthly processing fees:</strong> $500/mo<br/><strong>Potential funds temporarily held:</strong> $0/mo (dispute shield that prevents 25% processor holds)',
    sub: 'Assumptions ($50k/mo GMV, 0.8% dispute rate): $0 platform fee + $350 recovery fee (25% on $1,400 won disputes) + $150 network fees = $500/mo in actual fees. Holds $0 of merchant funds and keeps dispute ratios <0.5% to prevent processor reserves.',
    tableFeeSub: '$0 platform fee + $350 recovery fee + $150 network fees',
    tableHeldPill: '$0 held (prevents reserves)',
    tableHeldSub: 'Add-on defense layer · Keeps dispute ratio <0.5% to prevent $12,500/mo processor holds'
  }}
}};

let currentSpotlightId = '';
let lastCategory = '';

function renderDirectory() {{
  const cat = document.getElementById('cat-filter').value;
  const seats = parseInt(document.getElementById('seat-slider').value, 10);
  const aiVol = parseInt(document.getElementById('ai-slider').value, 10);
  const mode = document.getElementById('billing-mode').value;
  const sortEl = document.getElementById('sort-mode');
  const sortMode = sortEl ? sortEl.value : 'lowest';
  document.getElementById('seat-val').textContent = seats.toLocaleString();
  document.getElementById('ai-val').textContent = aiVol.toLocaleString();

  window.__saasbillEvents = window.__saasbillEvents || [];
  window.__saasbillEvents.push({{ event: 'result_rendered', category: cat, seats: seats, aiTickets: aiVol, billingMode: mode, sortMode: sortMode, ts: Date.now() }});

  document.querySelectorAll('.cat-tab').forEach(btn => {{
    if (btn.getAttribute('data-cat') === cat) {{
      btn.classList.add('active');
    }} else {{
      btn.classList.remove('active');
    }}
  }});

  // Dim controls instead of hiding them with display:none so the left column height never shifts
  const aiControl = document.getElementById('ai-control-group');
  const seatControl = document.getElementById('seat-control-group');
  const billingControl = document.getElementById('billing-control-group');
  if (aiControl) {{
    if (cat === 'Helpdesk & AI Support' || cat === 'ALL') {{
      aiControl.classList.remove('is-dimmed');
    }} else {{
      aiControl.classList.add('is-dimmed');
    }}
  }}
  if (seatControl && billingControl) {{
    if (cat === 'Payment Processors & MoR') {{
      seatControl.classList.add('is-dimmed');
      billingControl.classList.add('is-dimmed');
    }} else {{
      seatControl.classList.remove('is-dimmed');
      billingControl.classList.remove('is-dimmed');
    }}
  }}

  const filtered = TOOLS.filter(t => {{
    if (cat === 'ALL') return t.category !== 'Payment Processors & MoR';
    return t.category === cat;
  }});
  const rows = filtered.map(t => calcToolYear1(t, seats, aiVol, mode));

  const getRowTotal = r => (cat === 'Payment Processors & MoR' && PAY_PROFILES[r.tool.id]) ? PAY_PROFILES[r.tool.id].total : r.year1Total;
  const getRowHidden = r => (cat === 'Payment Processors & MoR' && PAY_PROFILES[r.tool.id]) ? (PAY_PROFILES[r.tool.id].held + PAY_PROFILES[r.tool.id].h) : r.hiddenFees;
  if (sortMode === 'highest') {{
    rows.sort((a, b) => getRowTotal(b) - getRowTotal(a));
  }} else if (sortMode === 'hidden_fees') {{
    rows.sort((a, b) => getRowHidden(b) - getRowHidden(a) || getRowTotal(b) - getRowTotal(a));
  }} else if (sortMode === 'name') {{
    rows.sort((a, b) => a.tool.name.localeCompare(b.tool.name));
  }} else {{
    rows.sort((a, b) => getRowTotal(a) - getRowTotal(b));
  }}

  const toolSelect = document.getElementById('spotlight-tool-select');
  const byHiddenOrder = [...rows].sort((a, b) => getRowHidden(b) - getRowHidden(a) || getRowTotal(b) - getRowTotal(a));
  if (cat !== lastCategory || !rows.some(r => r.tool.id === currentSpotlightId)) {{
    lastCategory = cat;
    if (cat === 'Payment Processors & MoR' && rows.some(r => r.tool.id === 'stripe-payments')) {{
      currentSpotlightId = 'stripe-payments';
    }} else {{
      currentSpotlightId = byHiddenOrder.length > 0 ? byHiddenOrder[0].tool.id : (rows[0] ? rows[0].tool.id : '');
    }}
  }}
  if (toolSelect) {{
    // Update options without resetting focus if only labels changed
    const existingIds = Array.from(toolSelect.options).map(o => o.value).join(',');
    const newIds = rows.map(r => r.tool.id).join(',');
    const SHORT_TOOL_LABELS = {{
      'hubspot-sales-pro': 'HubSpot Sales Pro',
      'hubspot-marketing-pro': 'HubSpot Marketing Pro',
      'close-crm': 'Close CRM (Essentials)',
      'pipedrive-crm': 'Pipedrive CRM',
      'monday-crm': 'monday CRM (Basic)',
      'intercom-fin-ai': 'Intercom + Fin AI',
      'freshdesk-support': 'Freshdesk Pro + Freddy AI',
      'zendesk-suite-team': 'Zendesk Suite Team + AI',
      'zendesk-suite-professional': 'Zendesk Suite Pro + AI',
      'help-scout-plus': 'Help Scout Plus + AI',
      'hubspot-service-hub': 'HubSpot Service Hub',
      'stripe-payments': 'Stripe Payments',
      'paddle-mor': 'Paddle (MoR)',
      'whop-payments': 'Whop Payments',
      'lemon-squeezy': 'Lemon Squeezy (MoR)',
      'chargeflow': 'Chargeflow Defense',
      'jotform-hipaa': 'Jotform Gold (HIPAA)',
      '1password-business': '1Password Business',
      'vanta-soc2': 'Vanta (SOC 2)',
      'drata-soc2': 'Drata (SOC 2)'
    }};
    if (existingIds !== newIds) {{
      toolSelect.innerHTML = rows.map(r => {{
        const sel = r.tool.id === currentSpotlightId ? 'selected' : '';
        const shortName = SHORT_TOOL_LABELS[r.tool.id] || r.tool.name;
        return `<option value="${{r.tool.id}}" ${{sel}}>${{shortName}}</option>`;
      }}).join('');
    }} else {{
      toolSelect.value = currentSpotlightId;
    }}
  }}

  const rowBase = document.getElementById('wb-row-base');
  const rowSeats = document.getElementById('wb-row-seats');
  const rowHidden = document.getElementById('wb-row-hidden');

  const summaryEl = document.getElementById('calc-summary-strip');
  const vizPanel = document.getElementById('calc-viz-panel');
  const vizRowsEl = document.getElementById('calc-viz-rows');
  const scenarioLine = formatScenarioText(cat, seats, aiVol, mode);


  const th2 = document.getElementById('th-col-2');
  const th3 = document.getElementById('th-col-3');
  const th4 = document.getElementById('th-col-4');
  const chartColTitle = document.getElementById('wb-chart-col-title');
  const dynSubhead = document.getElementById('gap-dynamic-subhead');
  if (dynSubhead) {{
    if (cat === 'Payment Processors & MoR') {{
      dynSubhead.textContent = `All ${{rows.length}} tools compared for $50,000/mo GMV · 1,000 tx · 30% international — click any row to inspect its breakdown above.`;
    }} else if (cat === 'Helpdesk & AI Support' || cat === 'ALL') {{
      dynSubhead.textContent = `All ${{rows.length}} tools compared for ${{seats}} seat${{seats === 1 ? '' : 's'}} · ${{mode === 'annual' ? 'annual' : 'monthly'}} billing · ${{aiVol.toLocaleString()}} AI tickets/mo — click any row to inspect its breakdown above.`;
    }} else {{
      dynSubhead.textContent = `All ${{rows.length}} tools compared for ${{seats}} seat${{seats === 1 ? '' : 's'}} · ${{mode === 'annual' ? 'annual' : 'monthly'}} billing — click any row to inspect its breakdown above.`;
    }}
  }}
  if (th2 && th3 && th4) {{
    if (cat === 'Payment Processors & MoR') {{
      th2.innerHTML = '<span class="legend-dot dot-sticker" aria-hidden="true"></span>Base Rate ($50k/mo Ex.)';
      th3.textContent = 'Estimated Monthly Processing Fees';
      th4.innerHTML = '<span class="legend-dot dot-hidden" aria-hidden="true"></span>Potential Funds Temporarily Held';
      if (chartColTitle) chartColTitle.textContent = 'Estimated Monthly Processing Fees';
    }} else {{
      th2.innerHTML = '<span class="legend-dot dot-sticker" aria-hidden="true"></span>Sticker Price / Year';
      th3.textContent = 'True Cost / Year (Est.)';
      th4.innerHTML = '<span class="legend-dot dot-hidden" aria-hidden="true"></span>Hidden Cost Gap';
      if (chartColTitle) chartColTitle.textContent = 'Your Estimated True Cost';
    }}
  }}

  if (cat === 'Payment Processors & MoR') {{
    const spotPayR = rows.find(r => r.tool.id === currentSpotlightId) || rows[0];
    const spotPayAff = AFFILIATES[spotPayR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const prof = PAY_PROFILES[spotPayR.tool.id] || PAY_PROFILES['stripe-payments'];
    const [s1, s2, s3] = computeSmoothBarShares(prof.b, prof.s, prof.h);
    if (rowBase && rowSeats && rowHidden) {{
      applyBarRowState(rowBase, s1, prof.b);
      applyBarRowState(rowSeats, s2, prof.s);
      applyBarRowState(rowHidden, s3, prof.h);
      document.getElementById('wb-amt-base').textContent = `$${{prof.b.toLocaleString()}}`;
      document.getElementById('wb-call-title-base').textContent = prof.callTitleBase;
      document.getElementById('wb-call-sub-base').textContent = prof.callSubBase;

      document.getElementById('wb-amt-seats').textContent = `$${{prof.s.toLocaleString()}}`;
      document.getElementById('wb-call-title-seats').textContent = prof.callTitleSeats;
      document.getElementById('wb-call-sub-seats').textContent = prof.callSubSeats;

      document.getElementById('wb-amt-hidden').textContent = `$${{prof.h.toLocaleString()}}`;
      document.getElementById('wb-call-title-hidden').textContent = prof.callTitleHidden;
      document.getElementById('wb-call-sub-hidden').textContent = prof.callSubHidden;
    }}
    const selProdEl = document.getElementById('wb-selected-product');
    if (selProdEl) selProdEl.textContent = `${{spotPayR.tool.name}} · $50k/mo Example`;
    document.getElementById('wb-big-amount').textContent = `$${{prof.total.toLocaleString()}}`;
    document.getElementById('wb-big-unit').textContent = prof.unit;
    const quoteEl = document.getElementById('wb-budget-quote');
    if (quoteEl) quoteEl.innerHTML = prof.quote;
    document.getElementById('wb-budget-subnote').textContent = prof.sub;
    const ctaEl = document.getElementById('wb-primary-cta');
    if (ctaEl) {{
      ctaEl.href = spotPayAff.destination_url;
      ctaEl.setAttribute('data-vendor', spotPayR.tool.id);
      ctaEl.textContent = getVendorCtaLabel(spotPayR.tool);
    }}
  }} else if (rows.length > 0) {{
    const byLowest = [...rows].sort((a, b) => a.year1Total - b.year1Total);
    const minR = byLowest[0];
    const maxR = byLowest[byLowest.length - 1];
    const byHidden = [...rows].sort((a, b) => b.hiddenFees - a.hiddenFees || b.year1Total - a.year1Total);
    const topHidden = byHidden[0];
    const maxTotal = Math.max(...rows.map(r => r.year1Total), 1);

    const spotR = rows.find(r => r.tool.id === currentSpotlightId) || topHidden || minR;
    const spotAff = AFFILIATES[spotR.tool.affiliate_slug] || {{ destination_url: '#' }};

    // 3 vertical stacked bar segments that sum 100% identically to spotR.year1Total:
    const baseSubYr = Math.min(spotR.annualSeatsCost, Math.round(spotR.unitRate * 12));
    const seatsUsageYr = Math.max(0, spotR.annualSeatsCost - baseSubYr);
    const overagesAddonsYr = spotR.onboarding + spotR.aiAnnual;
    const [s1, s2, s3] = computeSmoothBarShares(baseSubYr, seatsUsageYr, overagesAddonsYr);

    if (rowBase && rowSeats && rowHidden) {{
      applyBarRowState(rowBase, s1, baseSubYr);
      applyBarRowState(rowSeats, s2, seatsUsageYr);
      applyBarRowState(rowHidden, s3, overagesAddonsYr);

      document.getElementById('wb-amt-base').textContent = `$${{baseSubYr.toLocaleString()}}`;
      document.getElementById('wb-call-title-base').textContent = 'Sticker Price: Base plan';
      document.getElementById('wb-call-sub-base').textContent = '1st seat at advertised rate';

      document.getElementById('wb-amt-seats').textContent = `$${{seatsUsageYr.toLocaleString()}}`;
      document.getElementById('wb-call-title-seats').textContent = 'Sticker Price: Added seats';
      document.getElementById('wb-call-sub-seats').textContent = 'Remaining team seat licenses';

      document.getElementById('wb-amt-hidden').textContent = `$${{overagesAddonsYr.toLocaleString()}}`;
      document.getElementById('wb-call-title-hidden').textContent = 'Hidden Cost Gap';
      document.getElementById('wb-call-sub-hidden').textContent = 'Onboarding, AI overages & minimums';
    }}

    const selProdEl = document.getElementById('wb-selected-product');
    if (selProdEl) selProdEl.textContent = spotR.tool.name;
    document.getElementById('wb-big-amount').textContent = `$${{spotR.year1Total.toLocaleString()}}`;
    document.getElementById('wb-big-unit').textContent = '/ year';
    const quoteEl = document.getElementById('wb-budget-quote');
    if (quoteEl) quoteEl.innerHTML = 'That&rsquo;s the number to budget for.<br/>Not the number on the invoice.';
    const subNoteEl = document.getElementById('wb-budget-subnote');
    if (subNoteEl) {{
      const stickerYr = Math.max(0, spotR.annualSeatsCost - spotR.seatPaddingAnnual);
      const extraYr = spotR.year1Total - stickerYr;
      const billWord = mode === 'annual' ? 'annual' : 'monthly';
      if (extraYr > 0) {{
        subNoteEl.textContent = `${{spotR.tool.name}} (${{spotR.effSeats}} billed seat${{spotR.effSeats === 1 ? '' : 's'}}, ${{billWord}}): $${{stickerYr.toLocaleString()}}/yr base seats + $${{extraYr.toLocaleString()}}/yr hidden fees (onboarding, minimums, or AI).`;
      }} else {{
        subNoteEl.textContent = `${{spotR.tool.name}} (${{spotR.effSeats}} billed seat${{spotR.effSeats === 1 ? '' : 's'}}, ${{billWord}}): $${{stickerYr.toLocaleString()}}/yr base seats + $0 hidden fees (no onboarding or AI overages).`;
      }}
    }}
    const ctaEl = document.getElementById('wb-primary-cta');
    if (ctaEl) {{
      ctaEl.href = spotAff.destination_url;
      ctaEl.setAttribute('data-vendor', spotR.tool.id);
      ctaEl.textContent = getVendorCtaLabel(spotR.tool);
    }}

    const minAff = AFFILIATES[minR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const maxAff = AFFILIATES[maxR.tool.affiliate_slug] || {{ destination_url: '#' }};
    const hidAff = AFFILIATES[topHidden.tool.affiliate_slug] || {{ destination_url: '#' }};

    const minAudit = INTERNAL_AUDIT_LINKS[minR.tool.id];
    const maxAudit = INTERNAL_AUDIT_LINKS[maxR.tool.id];
    const hidAudit = INTERNAL_AUDIT_LINKS[topHidden.tool.id];

    if (summaryEl) {{
      const hiddenPct = topHidden.year1Total > 0 ? Math.round((topHidden.hiddenFees / topHidden.year1Total) * 100) : 0;
      const hiddenReasonText = formatHiddenReason(topHidden);
      summaryEl.innerHTML = `
        <div class="summary-card card-lowest">
          <div class="summary-label">Lowest Estimated Year-1 Cost</div>
          <div class="summary-metric" style="color:var(--emerald);">$${{minR.year1Total.toLocaleString()}} / yr &middot; ${{minR.tool.name}}</div>
          <div class="summary-scenario">${{scenarioLine}}</div>
          <div class="summary-breakdown">$${{minR.annualSeatsCost.toLocaleString()}} licenses + $${{minR.onboarding.toLocaleString()}} onboarding + $${{minR.aiAnnual.toLocaleString()}} AI</div>
          <div class="summary-caveat"><strong>Contract note:</strong> ${{minR.tool.trap_badge}} (${{minR.tool.billing_lock_in_type}})</div>
          <div class="summary-actions">
            <div class="cta-stack">
              <a class="btn-cta" href="${{minAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{minR.tool.id}}" data-cta-location="summary-card">${{getVendorCtaLabel(minR.tool)}}</a>
            </div>
            ${{minAudit ? `<a class="summary-audit-link" href="${{minAudit.url}}" data-track="internal-audit">${{minAudit.label}}</a>` : ''}}
          </div>
        </div>
        <div class="summary-card card-hidden">
          <div class="summary-label">Hidden Cost Highlight (Largest Non-Seat Add-On)</div>
          <div class="summary-metric" style="color:var(--rose);">+$${{topHidden.hiddenFees.toLocaleString()}} / yr (${{hiddenPct}}% of Year-1 bill)</div>
          <div class="summary-scenario">On <strong>${{topHidden.tool.name}}</strong> ($${{topHidden.year1Total.toLocaleString()}}/yr total &middot; ${{scenarioLine.replace('Based on ', '')}})</div>
          <div class="summary-breakdown">$${{topHidden.annualSeatsCost.toLocaleString()}} licenses + $${{topHidden.onboarding.toLocaleString()}} onboarding + $${{topHidden.aiAnnual.toLocaleString()}} AI</div>
          <div class="summary-caveat"><strong>Hidden Cost Highlight:</strong> ${{hiddenReasonText}}.</div>
          <div class="summary-actions">
            <div class="cta-stack">
              <a class="btn-secondary" href="${{hidAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{topHidden.tool.id}}" data-cta-location="summary-card">${{getVendorCtaLabel(topHidden.tool)}}</a>
            </div>
            ${{hidAudit ? `<a class="summary-audit-link" href="${{hidAudit.url}}" data-track="internal-audit">${{hidAudit.label}}</a>` : ''}}
          </div>
        </div>
        <div class="summary-card card-highest">
          <div class="summary-label">Highest Estimated Year-1 Cost</div>
          <div class="summary-metric">$${{maxR.year1Total.toLocaleString()}} / yr &middot; ${{maxR.tool.name}}</div>
          <div class="summary-scenario">${{scenarioLine}}</div>
          <div class="summary-breakdown">$${{maxR.annualSeatsCost.toLocaleString()}} licenses + $${{maxR.onboarding.toLocaleString()}} onboarding + $${{maxR.aiAnnual.toLocaleString()}} AI</div>
          <div class="summary-caveat"><strong>Contract note:</strong> ${{maxR.tool.trap_badge}}</div>
          <div class="summary-actions">
            <div class="cta-stack">
              <a class="btn-secondary" href="${{maxAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{maxR.tool.id}}" data-cta-location="summary-card">${{getVendorCtaLabel(maxR.tool)}}</a>
            </div>
            ${{maxAudit ? `<a class="summary-audit-link" href="${{maxAudit.url}}" data-track="internal-audit">${{maxAudit.label}}</a>` : ''}}
          </div>
        </div>
      `;
    }}

    if (vizPanel && vizRowsEl) {{
      vizPanel.style.display = 'block';
      vizRowsEl.innerHTML = rows.map(r => {{
        const aff = AFFILIATES[r.tool.affiliate_slug] || {{ destination_url: '#' }};
        const seatPct = Math.max(0, (r.annualSeatsCost / maxTotal) * 100);
        const onbPct = Math.max(0, (r.onboarding / maxTotal) * 100);
        const aiPct = Math.max(0, (r.aiAnnual / maxTotal) * 100);
        const parts = [`$${{r.annualSeatsCost.toLocaleString()}} licenses`];
        if (r.onboarding > 0) parts.push(`$${{r.onboarding.toLocaleString()}} onboarding`);
        if (r.aiAnnual > 0) parts.push(`$${{r.aiAnnual.toLocaleString()}} AI overage`);
        return `
          <div class="viz-row" data-tool-id="${{r.tool.id}}">
            <div class="viz-label" title="${{r.tool.name}}">${{r.tool.name}}</div>
            <div class="viz-bar-wrap">
              <div class="viz-bar-track" title="${{parts.join(' + ')}} = $${{r.year1Total.toLocaleString()}}/yr">
                <div class="viz-seg-seats" style="width:${{seatPct.toFixed(2)}}%"></div>
                ${{r.onboarding > 0 ? `<div class="viz-seg-onboarding" style="width:${{onbPct.toFixed(2)}}%"></div>` : ''}}
                ${{r.aiAnnual > 0 ? `<div class="viz-seg-ai" style="width:${{aiPct.toFixed(2)}}%"></div>` : ''}}
              </div>
              <div class="viz-breakdown-text">${{parts.join(' + ')}}</div>
            </div>
            <div class="viz-total-label">$${{r.year1Total.toLocaleString()}} / yr</div>
            <a class="viz-action-link" href="${{aff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{r.tool.id}}" data-cta-location="chart-row">${{getVendorCtaLabel(r.tool)}}</a>
          </div>
        `;
      }}).join('');
    }}
  }}

  document.getElementById('calc-tbody').innerHTML = rows.map(r => {{
    const t = r.tool;
    const aff = AFFILIATES[t.affiliate_slug] || {{ destination_url: '#', is_affiliate: false }};
    const verStatus = t.verification_status || 'Verified';
    const verClass = verStatus.startsWith('Verified') ? 'status-verified' : 'status-estimated';
    const srcUrl = (t.source_urls && t.source_urls[0]) ? t.source_urls[0] : aff.destination_url;
    const srcLabel = t.source_label || 'Official pricing & terms';
    const auditObj = INTERNAL_AUDIT_LINKS[t.id];
    const fmtRate = n => Number.isInteger(n) ? n.toLocaleString() : n.toFixed(2);

    const stickerAnnual = Math.max(0, r.annualSeatsCost - r.seatPaddingAnnual);
    const gapDollars = r.year1Total - stickerAnnual;
    const gapPct = stickerAnnual > 0 ? Math.round((gapDollars / stickerAnnual) * 100) : 0;

    const payProf = t.category === 'Payment Processors & MoR' ? PAY_PROFILES[t.id] : null;
    let stickerDisplay = '';
    if (payProf) {{
      const baseMo = payProf.tableBaseAmt !== undefined ? payProf.tableBaseAmt : (payProf.b + payProf.s);
      stickerDisplay = `<div class="gap-figure">$${{baseMo.toLocaleString()}} / mo</div><div class="gap-sub-detail">${{t.transaction_fee_display}}</div>`;
    }} else if (t.transaction_fee_display) {{
      stickerDisplay = `<div class="gap-figure">${{t.transaction_fee_display}}</div>`;
    }} else {{
      stickerDisplay = `<div class="gap-figure">$${{stickerAnnual.toLocaleString()}}</div><div class="gap-sub-detail">$${{fmtRate(r.unitRate)}}/seat/mo</div>`;
    }}

    const totalText = payProf
      ? `<div class="gap-figure">$${{payProf.total.toLocaleString()}} / mo</div><div class="gap-sub-detail">${{payProf.tableFeeSub}}</div>`
      : `<div class="gap-figure">$${{r.year1Total.toLocaleString()}}</div><div class="gap-sub-detail">${{r.effSeats}} billed seat${{r.effSeats === 1 ? '' : 's'}}</div>`;

    let gapCellHtml = '';
    if (payProf) {{
      const pillClass = payProf.held > 0 ? 'gap-orange-pill' : 'gap-zero-pill';
      gapCellHtml = `
        <div class="${{pillClass}}">${{payProf.tableHeldPill}}</div>
        <div class="gap-sub-detail">${{payProf.tableHeldSub}} &middot; <a href="${{srcUrl}}" target="_blank" rel="noopener">Verified source &nearr;</a></div>
      `;
    }} else if (gapDollars > 0) {{
      const breakdownParts = [];
      if (r.onboarding > 0) breakdownParts.push(`+$${{r.onboarding.toLocaleString()}} onboarding`);
      if (r.aiAnnual > 0) breakdownParts.push(`+$${{r.aiAnnual.toLocaleString()}} AI overage`);
      if (r.seatPaddingAnnual > 0) breakdownParts.push(`+$${{r.seatPaddingAnnual.toLocaleString()}} seat min`);
      gapCellHtml = `
        <div class="gap-orange-pill">${{gapPct}}% more (+$${{gapDollars.toLocaleString()}}/yr)</div>
        <div class="gap-sub-detail">${{breakdownParts.join(' · ')}} &middot; <a href="${{srcUrl}}" target="_blank" rel="noopener">Verified source &nearr;</a></div>
      `;
    }} else {{
      gapCellHtml = `
        <div class="gap-zero-pill">0% hidden gap</div>
        <div class="gap-sub-detail">${{t.trap_badge}} &middot; <a href="${{srcUrl}}" target="_blank" rel="noopener">Verified source &nearr;</a></div>
      `;
    }}

    const isSpot = t.id === currentSpotlightId ? 'is-spotlight-row' : '';
    return `
      <tr class="${{isSpot}}" data-row-tool="${{t.id}}" style="cursor:pointer;">
        <td data-label="Platform">
          <div class="gap-platform-name">
            <strong>${{t.name}}</strong>
            <span class="status-pill ${{verClass}}">${{verStatus}}</span>
          </div>
          <div class="gap-platform-meta">${{t.category}}${{auditObj ? ` &middot; <a class="audit-inline-link" href="${{auditObj.url}}" data-track="internal-audit">${{auditObj.label}}</a>` : ''}}</div>
        </td>
        <td data-label="Sticker Price / Year">${{stickerDisplay}}</td>
        <td data-label="Year-1 Total">${{totalText}}</td>
        <td data-label="Hidden Cost Gap">${{gapCellHtml}}</td>
        <td data-label="Official Pricing">
          <div class="cta-stack">
            <a class="btn-secondary" href="${{aff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{t.id}}" data-cta-location="table-row">${{getVendorCtaLabel(t)}}</a>
          </div>
        </td>
      </tr>
    `;
  }}).join('');
}}

['cat-filter', 'seat-slider', 'ai-slider', 'billing-mode', 'sort-mode'].forEach(id => {{
  const el = document.getElementById(id);
  if (el) el.addEventListener('input', renderDirectory);
}});

const spotSelectEl = document.getElementById('spotlight-tool-select');
if (spotSelectEl) {{
  spotSelectEl.addEventListener('change', (e) => {{
    currentSpotlightId = e.target.value;
    renderDirectory();
  }});
}}

document.addEventListener('click', (e) => {{
  const tr = e.target.closest('tr[data-row-tool]');
  if (tr && !e.target.closest('a')) {{
    currentSpotlightId = tr.getAttribute('data-row-tool');
    renderDirectory();
  }}
  const vizRow = e.target.closest('.viz-row[data-tool-id]');
  if (vizRow && !e.target.closest('a')) {{
    currentSpotlightId = vizRow.getAttribute('data-tool-id');
    renderDirectory();
  }}
}});

document.querySelectorAll('.cat-tab').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const catSelect = document.getElementById('cat-filter');
    if (catSelect) {{
      catSelect.value = btn.getAttribute('data-cat');
      renderDirectory();
    }}
  }});
}});
renderDirectory();
</script>
"""

home_faqs = [
    ("Which B2B SaaS tools charge mandatory onboarding fees in 2026?", "HubSpot charges mandatory one-time onboarding fees on its Professional and Enterprise tiers: $1,500 for Sales Hub Professional, $3,500 for Sales Hub Enterprise, $3,000 for Marketing Hub Professional, and $7,000 for Marketing Hub Enterprise (verified Oct 2026). Alternatives like Close CRM, Pipedrive, and Freshdesk charge $0 for onboarding."),
    ("How does Intercom's $0.99 per Fin AI resolution pricing work?", "Intercom charges a per-seat monthly fee ($29 Essential, $85 Advanced, or $132 Expert billed annually) plus $0.99 for every customer conversation resolved by its Fin AI agent (and $9.99 for sales qualification). If Fin AI resolves 2,000 tickets a month, it adds $1,980/month ($23,760/year) to your seat invoice."),
    ("Why does monday CRM cost more than advertised for 1 or 2 users?", "monday CRM enforces a 3-seat minimum and bills in fixed seat buckets (3, 5, 10, 15 seats). A solo user on the $12/seat Basic ($18/seat monthly) or $17/seat Standard ($25/seat monthly) plan must pay for 3 seats ($36/month annual or $54/month monthly on Basic). For 1–2 users, Pipedrive ($14–$34/seat) or Close CRM Essentials ($35/user/month annual, $49/user/month monthly) is cheaper because they bill per exact seat."),
    ("What happens to subscriber card tokens if Paddle or Stripe terminates my account?", "With Stripe (2.9% + $0.30), you are the merchant and own the customer relationship, allowing PGP-encrypted card token exports unless terminated for fraud. With a Merchant of Record like Paddle (5% + $0.50), Paddle is the legal seller of record and owns the card vault; if Paddle terminates your account on a risk review, you cannot export card tokens and every subscriber must re-enter their payment details.")
]

render_page(
    "index.html",
    "saasbill.io – Your SaaS bill is lying to you",
    "SaaSBill independent B2B SaaS pricing calculator and contract audit directory. Compare true Year-1 costs including HubSpot's $1,500-$7,000 onboarding fees, Intercom's $0.99 AI resolution tax, and Stripe/Paddle payout holds.",
    "/",
    home_body,
    faqs=home_faqs,
    extra_schema={
        "@type": "Dataset",
        "name": "SaaSBill 2026 B2B SaaS True-Cost & Contract Trap Dataset",
        "description": "Verified 2026 pricing, mandatory onboarding fees, seat-bucket minimums, AI resolution rates, and payout reserve rules across 20 B2B SaaS and payment platforms.",
        "url": f"{SITE_ORIGIN}/",
        "dateModified": "2026-10-25",
        "creator": {"@type": "Organization", "name": "SaaSBill Editorial"}
    }
)

# ---------------------------------------------------------
# 2. Page 1: HubSpot True Cost & Onboarding Fees
# ---------------------------------------------------------
p1_body = """
<section class="hero">
  <h1>What HubSpot actually costs in Year 1 (once you add onboarding).</h1>
  <p class="lead">HubSpot’s pricing page says $90/seat. The first-year invoice for five sales reps is $6,900. Here is where the extra $1,500–$7,000 comes from—and how to waive it before you sign.</p>
  <div class="geo-direct-answer">
    <p><strong>The short version:</strong> In 2026, <strong>HubSpot Sales Hub Professional</strong> costs $90/seat/month billed annually ($100/seat paid monthly) plus a mandatory <strong>$1,500 onboarding fee</strong>—totaling <strong>$6,900 in Year 1 for five reps</strong>. <strong>Marketing Hub Professional</strong> costs $800/month (includes 3 core seats; $45/mo per extra seat) plus a mandatory <strong>$3,000 onboarding fee</strong>—totaling <strong>$12,600 in Year 1</strong>. Every Professional and Enterprise agreement is a binding 12-month commitment that auto-renews even if you select monthly payment installments.</p>
  </div>

  <div class="invoice-box" aria-label="Sample Year-1 Order Form Breakdown">
    <div class="invoice-title">Sample Year-1 Order Form &middot; HubSpot Sales Hub Professional (5 Reps)</div>
    <div class="invoice-row">
      <span>5 &times; Core Sales Hub Pro Seats ($90/seat/mo &times; 12 mos)</span>
      <span>$5,400.00</span>
    </div>
    <div class="invoice-row">
      <span>Mandatory Sales Hub Pro Onboarding Fee (one-time)</span>
      <span style="color:var(--rose); font-weight:700;">+$1,500.00</span>
    </div>
    <div class="invoice-row">
      <span>Mid-term seat reduction allowance (Months 1–12)</span>
      <span>Not permitted</span>
    </div>
    <div class="invoice-total">
      <span>Year-1 Contract Total (excl. tax)</span>
      <span>$6,900.00</span>
    </div>
  </div>
</section>

<section class="calc-box">
  <h2 style="margin-top:0;">Calculate your Year-1 cost: HubSpot vs. Close vs. Pipedrive</h2>
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">For a five-rep sales team, choosing <strong>Close CRM Essentials</strong> ($35/user/month billed annually, $0 onboarding) or <strong>Pipedrive Professional</strong> ($49/seat/month, $0 onboarding) saves between <strong>$3,960 and $4,800 in Year 1</strong> compared with HubSpot Sales Hub Professional ($960 saved even on Close Growth at $99/user/month), with no 12-month lock-in required.</p>
  <div class="calc-grid">
    <div class="control-group">
      <label for="hs-seats">Sales team size (core seats): <span class="val-pill" id="hs-seats-val">5</span> reps</label>
      <input type="range" id="hs-seats" min="1" max="30" value="5" />
    </div>
    <div class="control-group">
      <label for="hs-tier">HubSpot hub &amp; edition</label>
      <select id="hs-tier">
        <option value="sales_pro">Sales Hub Pro ($90/seat + $1,500 onboarding)</option>
        <option value="sales_ent">Sales Hub Ent ($150/seat + $3,500 onboarding)</option>
        <option value="mkt_pro">Marketing Pro ($800/mo + $3,000 onboarding)</option>
        <option value="mkt_ent">Marketing Ent ($3,600/mo + $7,000 onboarding)</option>
      </select>
    </div>
  </div>
  <div id="hs-summary" class="summary-strip" aria-live="polite"></div>
  <p class="summary-interpretation"><strong>How to read this comparison:</strong> Lowest cost does not automatically mean best fit&mdash;verify workflow limits, calling needs, and contract lock-in before choosing.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>Year-1 Out-of-Pocket Comparison: HubSpot vs. Close CRM vs. Pipedrive (USD, verified Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>CRM Platform</th>
          <th>Monthly Seat Cost</th>
          <th>Mandatory Onboarding</th>
          <th>Contract Terms &amp; Source</th>
          <th>Year-1 Total (USD)</th>
          <th>Compare</th>
        </tr>
      </thead>
      <tbody id="hs-tbody"></tbody>
    </table>
  </div>
</section>

<section>
  <h2>The 2026 HubSpot onboarding fee schedule</h2>
  <p class="section-tldr">HubSpot requires paid onboarding across all Professional and Enterprise hubs purchased directly. The only way to waive HubSpot’s direct onboarding fee is to sign through an accredited HubSpot Solutions Partner who handles the implementation instead.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>HubSpot 2026 Seat Rates &amp; Mandatory Onboarding Fees (USD, verified Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>HubSpot Hub &amp; Edition</th>
          <th>Annual Billing Rate</th>
          <th>Monthly Installment Rate (12-Mo Term)</th>
          <th>Mandatory Onboarding Fee</th>
          <th>Year-1 Minimum Spend</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td data-label="Edition"><strong>Sales Hub Professional</strong> <span class="status-pill status-verified">Verified</span></td>
          <td data-label="Annual Rate">$90 / seat / mo</td>
          <td data-label="Monthly Installment">$100 / seat / mo</td>
          <td data-label="Onboarding"><span class="badge badge-high">$1,500 one-time</span></td>
          <td data-label="Year-1 Min Spend">$2,580 (1 seat) &middot; $6,900 (5 seats)</td>
        </tr>
        <tr>
          <td data-label="Edition"><strong>Sales Hub Enterprise</strong> <span class="status-pill status-verified">Verified</span></td>
          <td data-label="Annual Rate">$150 / seat / mo</td>
          <td data-label="Monthly Installment">$150 / seat / mo (Annual only)</td>
          <td data-label="Onboarding"><span class="badge badge-high">$3,500 one-time</span></td>
          <td data-label="Year-1 Min Spend">$5,300 (1 seat) &middot; $12,500 (5 seats)</td>
        </tr>
        <tr>
          <td data-label="Edition"><strong>Marketing Hub Professional</strong> <span class="status-pill status-verified">Verified</span></td>
          <td data-label="Annual Rate">$800 / mo (3 core seats incl.)</td>
          <td data-label="Monthly Installment">$890 / mo (12-mo commitment)</td>
          <td data-label="Onboarding"><span class="badge badge-high">$3,000 one-time</span></td>
          <td data-label="Year-1 Min Spend">$12,600 / yr (+$45/mo per extra seat)</td>
        </tr>
        <tr>
          <td data-label="Edition"><strong>Marketing Hub Enterprise</strong> <span class="status-pill status-verified">Verified</span></td>
          <td data-label="Annual Rate">$3,600 / mo (5 core seats incl.)</td>
          <td data-label="Monthly Installment">$3,600 / mo (Annual only)</td>
          <td data-label="Onboarding"><span class="badge badge-high">$7,000 one-time</span></td>
          <td data-label="Year-1 Min Spend">$50,200 / yr (+$75/mo per extra seat)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2>Three contract clauses to check before you sign</h2>
  <div class="evidence-box">
    <strong>1. "Monthly payment" is still a binding 12-month contract with auto-renewal</strong>
    <p style="margin-top:6px;">All HubSpot Professional and Enterprise agreements are annual commitments that auto-renew by default, even when paid in monthly installments. On day 1 of the auto-renewal window, you are liable for the full 12-month renewal balance unless you submitted non-renewal notice in advance.</p>
    <cite>Sources: <a href="https://legal.hubspot.com/terms-of-service" target="_blank" rel="noopener">HubSpot Customer Terms of Service (Renewal &amp; Subscription Term)</a> &amp; <a href="https://www.reddit.com/r/sales/comments/pyqpjq/hubspot_a_psa_contracts_and_review/" target="_blank" rel="noopener">r/sales contract review</a></cite>
  </div>
  <div class="evidence-box">
    <strong>2. Onboarding fees are mandatory on direct orders (waivable via Solutions Partners)</strong>
    <p style="margin-top:6px;">Sales Hub Pro requires a $1,500 onboarding fee ($3,500 on Enterprise), while Marketing Hub Pro requires $3,000 ($7,000 on Enterprise). HubSpot waives its direct onboarding fee when you purchase through an accredited HubSpot Solutions Partner with a signed implementation scope.</p>
    <cite>Sources: <a href="https://www.hubspot.com/pricing/sales" target="_blank" rel="noopener">HubSpot Sales Hub Pricing Schedule</a> &amp; <a href="https://www.reddit.com/r/sales/comments/1htoulv/onboarding_fee/" target="_blank" rel="noopener">r/sales &ndash; "Onboarding Fee"</a></cite>
  </div>
  <div class="evidence-box">
    <strong>3. You cannot downgrade committed seats mid-term</strong>
    <p style="margin-top:6px;">Under HubSpot’s Customer Terms of Service, seat upgrades take effect immediately and prorate for the remainder of the subscription term, whereas seat reductions or edition downgrades are only permitted at the end of the 12-month commitment window.</p>
    <cite>Source: <a href="https://legal.hubspot.com/terms-of-service" target="_blank" rel="noopener">HubSpot Customer Terms of Service &ndash; No Early Cancellation or Downgrades</a></cite>
  </div>
</section>

<script>
function updateHsCalc() {
  const seats = parseInt(document.getElementById('hs-seats').value, 10);
  const tier = document.getElementById('hs-tier').value;
  document.getElementById('hs-seats-val').textContent = seats;
  let hsMonthly = 0, hsOnboard = 0, hsName = '';
  if (tier === 'sales_pro') { hsName = 'HubSpot Sales Hub Pro'; hsMonthly = seats * 90; hsOnboard = 1500; }
  else if (tier === 'sales_ent') { hsName = 'HubSpot Sales Hub Enterprise'; hsMonthly = seats * 150; hsOnboard = 3500; }
  else if (tier === 'mkt_pro') { hsName = 'HubSpot Marketing Hub Pro'; hsMonthly = 800 + Math.max(0, seats - 3) * 45; hsOnboard = 3000; }
  else { hsName = 'HubSpot Marketing Hub Enterprise'; hsMonthly = 3600 + Math.max(0, seats - 5) * 75; hsOnboard = 7000; }
  const hsSeatsYr = hsMonthly * 12;
  const hsYear1 = hsSeatsYr + hsOnboard;
  const onbPct = Math.round((hsOnboard / hsYear1) * 100);
  const closeMonthly = seats * 35;
  const closeYear1 = closeMonthly * 12;
  const pipeMonthly = seats * 49;
  const pipeYear1 = pipeMonthly * 12;
  const scenarioLine = `Based on ${seats} seat${seats === 1 ? '' : 's'}, annual billing`;

  const hsSummary = document.getElementById('hs-summary');
  if (hsSummary) {
    hsSummary.innerHTML = `
      <div class="summary-card card-hidden">
        <div class="summary-label">HubSpot Year-1 Total &amp; Hidden Cost Highlight</div>
        <div class="summary-metric" style="color:var(--rose);">$${hsYear1.toLocaleString()} / yr &middot; ${hsName}</div>
        <div class="summary-scenario">${scenarioLine}</div>
        <div class="summary-breakdown">$${hsSeatsYr.toLocaleString()} licenses + $${hsOnboard.toLocaleString()} mandatory onboarding + $0 AI</div>
        <div class="summary-caveat"><strong>Hidden Cost Highlight:</strong> Mandatory $${hsOnboard.toLocaleString()} onboarding adds ${onbPct}% to the Year-1 invoice, with a 12-month auto-renewing contract lock-in.</div>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-secondary" href="https://www.hubspot.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="hubspot" data-cta-location="summary-card">View HubSpot pricing &rarr;</a>
          </div>
        </div>
      </div>
      <div class="summary-card card-lowest">
        <div class="summary-label">Lowest Year-1 Cost ($0 Onboarding)</div>
        <div class="summary-metric" style="color:var(--emerald);">$${closeYear1.toLocaleString()} / yr &middot; Close CRM (Essentials)</div>
        <div class="summary-scenario">${scenarioLine} (saves $${Math.max(0, hsYear1 - closeYear1).toLocaleString()}/yr vs. HubSpot)</div>
        <div class="summary-breakdown">$${closeYear1.toLocaleString()} licenses + $0 onboarding + $0 AI</div>
        <div class="summary-caveat"><strong>Contract note:</strong> $35/user/mo annual ($49 monthly); Growth tier with workflows is $99/user/mo.</div>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-cta" href="https://refer.close.com/3k5hp07b8soi-fetl0j" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="close-crm" data-cta-location="summary-card">Check Close pricing &rarr;</a>
          </div>
        </div>
      </div>
      <div class="summary-card card-highest">
        <div class="summary-label">Zero-Onboarding Alternative</div>
        <div class="summary-metric" style="color:var(--emerald);">$${pipeYear1.toLocaleString()} / yr &middot; Pipedrive (Professional)</div>
        <div class="summary-scenario">${scenarioLine} (saves $${Math.max(0, hsYear1 - pipeYear1).toLocaleString()}/yr vs. HubSpot)</div>
        <div class="summary-breakdown">$${pipeYear1.toLocaleString()} licenses + $0 onboarding + $0 AI</div>
        <div class="summary-caveat"><strong>Contract note:</strong> 1-seat minimum ($14/mo Lite up to $49/mo Pro); cancel anytime on monthly billing.</div>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-secondary" href="https://www.pipedrive.com/en/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="pipedrive-crm" data-cta-location="summary-card">Explore Pipedrive plans &rarr;</a>
          </div>
          <a class="summary-audit-link" href="../../compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/" data-track="internal-audit">1&ndash;15 seat comparison &rarr;</a>
        </div>
      </div>
    `;
  }

  document.getElementById('hs-tbody').innerHTML = `
    <tr>
      <td data-label="CRM Platform"><strong>${hsName}</strong> <span class="status-pill status-verified">Verified</span></td>
      <td data-label="Monthly Seat Cost" style="font-family:var(--mono);">$${hsMonthly.toLocaleString()} / mo</td>
      <td data-label="Mandatory Onboarding"><span class="badge badge-high">$${hsOnboard.toLocaleString()} mandatory</span></td>
      <td data-label="Contract Terms &amp; Source">12-month auto-renewing contract<div class="source-inline">Source: <a href="https://www.hubspot.com/pricing/sales" target="_blank" rel="noopener">HubSpot pricing &nearr;</a></div></td>
      <td data-label="Year-1 Total" class="price-highlight">$${hsYear1.toLocaleString()}<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next Step"><div class="cta-stack"><a class="btn-secondary" href="https://www.hubspot.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="hubspot" data-cta-location="table-row">View HubSpot pricing &rarr;</a></div></td>
    </tr>
    <tr>
      <td data-label="CRM Platform"><strong>Close CRM (Essentials)</strong> <span class="status-pill status-verified">Verified</span><div style="font-size:0.78rem; color:var(--emerald);">$35/user/mo annual ($49 monthly) &middot; $0 onboarding &middot; Growth w/ workflows is $99/user/mo</div></td>
      <td data-label="Monthly Seat Cost" style="font-family:var(--mono);">$${closeMonthly.toLocaleString()} / mo</td>
      <td data-label="Mandatory Onboarding"><span class="badge badge-low">$0 onboarding</span></td>
      <td data-label="Contract Terms &amp; Source">Month-to-month or annual<div class="source-inline">Verified source: <a href="https://close.com/pricing" target="_blank" rel="noopener">Close pricing &nearr;</a></div></td>
      <td data-label="Year-1 Total" class="price-highlight" style="color:var(--emerald);">$${closeYear1.toLocaleString()} (saves $${Math.max(0, hsYear1 - closeYear1).toLocaleString()})<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next Step"><div class="cta-stack"><a class="btn-secondary" href="https://refer.close.com/3k5hp07b8soi-fetl0j" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="close-crm" data-cta-location="table-row">Check Close pricing &rarr;</a></div></td>
    </tr>
    <tr>
      <td data-label="CRM Platform"><strong>Pipedrive CRM (Professional)</strong> <span class="status-pill status-verified">Verified</span><div style="font-size:0.78rem; color:var(--emerald);">No onboarding fee &middot; 1-seat minimum</div></td>
      <td data-label="Monthly Seat Cost" style="font-family:var(--mono);">$${pipeMonthly.toLocaleString()} / mo</td>
      <td data-label="Mandatory Onboarding"><span class="badge badge-low">$0 onboarding</span></td>
      <td data-label="Contract Terms &amp; Source">Cancel anytime on monthly plan<div class="source-inline">Verified source: <a href="https://www.pipedrive.com/en/pricing" target="_blank" rel="noopener">Pipedrive pricing &nearr;</a></div></td>
      <td data-label="Year-1 Total" class="price-highlight" style="color:var(--emerald);">$${pipeYear1.toLocaleString()} (saves $${Math.max(0, hsYear1 - pipeYear1).toLocaleString()})<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next Step"><div class="cta-stack"><a class="btn-secondary" href="https://www.pipedrive.com/en/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="pipedrive-crm" data-cta-location="table-row">Explore Pipedrive plans &rarr;</a></div></td>
    </tr>
  `;
}
document.getElementById('hs-seats').addEventListener('input', updateHsCalc);
document.getElementById('hs-tier').addEventListener('input', updateHsCalc);
updateHsCalc();
</script>
"""

p1_faqs = [
    ("How much is the mandatory HubSpot onboarding fee in 2026?", "In 2026, HubSpot charges a mandatory one-time onboarding fee of $1,500 for Sales Hub Professional, $3,500 for Sales Hub Enterprise, $3,000 for Marketing Hub Professional, and $7,000 for Marketing Hub Enterprise when purchasing directly."),
    ("Can you cancel a HubSpot monthly payment plan at any time?", "On HubSpot Starter, yes. However, on HubSpot Professional and Enterprise tiers, selecting 'monthly billing' ($100/seat/mo instead of $90/seat/mo on Sales Pro) is still a binding 12-month annual contract paid in monthly installments, with automatic annual renewal unless cancelled prior to the notice deadline."),
    ("How do you waive the HubSpot $1,500 or $3,000 onboarding fee?", "You can waive HubSpot's direct onboarding fee by purchasing your license through an accredited HubSpot Solutions Partner (agency/consultant) and signing an onboarding scope with them, or by switching to a zero-onboarding CRM such as Close CRM or Pipedrive."),
    ("How much does HubSpot Sales Hub Professional cost for 5 users in Year 1?", "For 5 core sales seats billed annually at $90/seat/month ($450/month or $5,400/year) plus the mandatory $1,500 onboarding fee, HubSpot Sales Hub Professional costs $6,900 in Year 1 (excluding taxes and calling credit overages).")
]

render_page(
    "pricing/hubspot-true-cost-and-onboarding-fees/index.html",
    "HubSpot True Year-1 Cost Calculator – saasbill.io",
    "Calculate your real Year-1 HubSpot Sales Hub and Marketing Hub cost including mandatory $1,500-$7,000 onboarding fees, and compare against Close CRM and Pipedrive.",
    "/pricing/hubspot-true-cost-and-onboarding-fees/",
    p1_body,
    faqs=p1_faqs
)

# ---------------------------------------------------------
# 3. Page 2: Intercom Fin AI Resolution Calculator
# ---------------------------------------------------------
p2_body = """
<section class="hero">
  <h1>What Intercom’s $0.99 AI resolution fee actually does to your support bill.</h1>
  <p class="lead">Seat licenses start at $29 to $132 a month, but Fin AI adds $0.99 every time it resolves a ticket. Here is how fast the variable meter outgrows your seat bill—and how session-pack helpdesks compare.</p>
  <div class="geo-direct-answer">
    <p><strong>The short version:</strong> Intercom charges <strong>$0.99 per Fin AI resolution</strong> (including automated resolutions, procedure handoffs, and disqualifications, plus <strong>$9.99 per sales qualification</strong>) on top of agent seat licenses (<strong>$29/mo Essential, $85/mo Advanced, $132/mo Expert</strong> billed annually; $39/$99/$139 monthly). For a 5-agent team on Advanced ($425/mo) handling 3,000 tickets/month with a 50% AI resolution rate (1,500 resolutions), Fin AI adds <strong>$1,485/mo</strong>—bringing the total bill to <strong>$1,910/mo ($22,920/yr)</strong>. By comparison, <strong>Freshdesk Pro ($55/agent/mo annual)</strong> includes <strong>500 one-time Freddy AI Agent sessions</strong> and then bills <strong>$49 per 100-session pack</strong> (charged per AI session handled, whether resolved or not; Freddy AI Copilot is an optional $29/agent/mo add-on).</p>
  </div>
</section>

<section class="calc-box">
  <h2 style="margin-top:0;">Calculate your monthly Intercom + Fin AI invoice</h2>
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">Every 1,000 tickets resolved by Fin AI adds $990/month ($11,880/year) on top of your agent seat subscriptions. Drag the sliders to compare Intercom’s $0.99/resolution meter against Freshdesk Pro + Freddy AI Agent session packs ($49 per 100 sessions after 500 one-time free sessions).</p>
  <div class="calc-grid">
    <div class="control-group">
      <label for="ic-seats">Support agents (full seats): <span class="val-pill" id="ic-seats-val">5</span> seats</label>
      <input type="range" id="ic-seats" min="1" max="40" value="5" />
    </div>
    <div class="control-group">
      <label for="ic-plan">Intercom plan tier (annual billing)</label>
      <select id="ic-plan">
        <option value="29">Essential ($29/seat annual &middot; $39 monthly)</option>
        <option value="85" selected>Advanced ($85/seat annual &middot; 20 Lite seats)</option>
        <option value="132">Expert ($132/seat annual &middot; 50 Lite seats)</option>
      </select>
    </div>
    <div class="control-group">
      <label for="ic-tickets">Total monthly support conversations: <span class="val-pill" id="ic-tickets-val">3,000</span> /mo</label>
      <input type="range" id="ic-tickets" min="200" max="20000" step="200" value="3000" />
    </div>
    <div class="control-group">
      <label for="ic-rate">Fin AI resolution rate: <span class="val-pill" id="ic-rate-val">50</span>%</label>
      <input type="range" id="ic-rate" min="10" max="85" step="5" value="50" />
    </div>
  </div>
  <div id="ic-summary" class="summary-strip" aria-live="polite"></div>
  <p class="summary-interpretation"><strong>How to read this comparison:</strong> Intercom charges $0.99 only when Fin AI resolves a conversation, whereas Freshdesk charges $49 per 100 AI sessions (whether resolved or escalated). Compare both models against your resolution rate.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>Intercom + Fin AI ($0.99/Resolution) vs. Freshdesk Pro + Freddy AI Agent ($49/100 Sessions) Breakdown (USD, verified Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>Helpdesk Solution</th>
          <th>Monthly Agent Seats</th>
          <th>Monthly AI Usage Charge</th>
          <th>Total Monthly Bill</th>
          <th>Year-1 Total (USD)</th>
          <th>Compare</th>
        </tr>
      </thead>
      <tbody id="ic-tbody"></tbody>
    </table>
  </div>
</section>

<section>
  <h2>Why support teams call $0.99/resolution an "AI tax"</h2>
  <p class="section-tldr">When outcome-based AI meters have no hard cap by default, seasonal support spikes or better help-center articles immediately increase your monthly software invoice.</p>
  <div class="evidence-box">
    <strong>1. Billable resolution definition includes silent exits after Fin replies</strong>
    <p style="margin-top:6px;">Under Intercom’s Fin AI pricing rules, a billable $0.99 resolution is counted whenever a customer confirms Fin’s answer helped OR leaves the conversation without requesting a human agent after Fin’s response, at most once per conversation.</p>
    <cite>Source: <a href="https://www.intercom.com/pricing" target="_blank" rel="noopener">Intercom Official Pricing &amp; Fin AI Agent Billing FAQ</a></cite>
  </div>
  <div class="evidence-box">
    <strong>2. Session-pack pricing vs. per-resolution pricing</strong>
    <p style="margin-top:6px;">Freshdesk’s Freddy AI Agent includes 500 complimentary one-time sessions and then charges $49 per 100-session pack (spanning 72 hours for email or 24 hours for chat), giving admins fixed session-pack budgets that expire at cycle end unless auto-recharge is enabled.</p>
    <cite>Source: <a href="https://support.freshdesk.com/support/solutions/articles/50000011515-manage-freddy-ai-add-ons" target="_blank" rel="noopener">Freshdesk Support &ndash; Purchase and Manage Freddy AI Add-ons</a></cite>
  </div>
</section>

<script>
function updateIcCalc() {
  const seats = parseInt(document.getElementById('ic-seats').value, 10);
  const seatRate = parseInt(document.getElementById('ic-plan').value, 10);
  const tickets = parseInt(document.getElementById('ic-tickets').value, 10);
  const resRate = parseInt(document.getElementById('ic-rate').value, 10) / 100;
  document.getElementById('ic-seats-val').textContent = seats;
  document.getElementById('ic-tickets-val').textContent = tickets.toLocaleString();
  document.getElementById('ic-rate-val').textContent = Math.round(resRate * 100);
  const resolvedTickets = Math.round(tickets * resRate);
  const icSeatCost = seats * seatRate;
  const icAiCost = Math.round(resolvedTickets * 0.99);
  const icTotalMo = icSeatCost + icAiCost;
  const icYear = icTotalMo * 12;

  // Freshdesk Pro ($55/seat/mo annual) + Freddy AI Agent session packs ($49 per 100 sessions; 500 1x free in Year 1)
  const fdSeatCost = seats * 55;
  const fdMonthlyPacks = Math.ceil(tickets / 100);
  const fdAiCostMo = fdMonthlyPacks * 49;
  const fdTotalMo = fdSeatCost + fdAiCostMo;
  const fdAnnualBillableSessions = Math.max(0, tickets * 12 - 500);
  const fdAnnualAiCost = Math.ceil(fdAnnualBillableSessions / 100) * 49;
  const fdYear = fdSeatCost * 12 + fdAnnualAiCost;
  const diff = icYear - fdYear;
  const diffLabel = diff > 0 ? `(saves $${diff.toLocaleString()}/yr)` : `(+$${Math.abs(diff).toLocaleString()}/yr vs Intercom)`;

  const icSeatsYr = icSeatCost * 12;
  const icAiYr = icAiCost * 12;
  const fdSeatsYr = fdSeatCost * 12;
  const aiSharePct = icYear > 0 ? Math.round((icAiYr / icYear) * 100) : 0;
  const scenarioLine = `Based on ${seats} seat${seats === 1 ? '' : 's'}, annual billing, ${tickets.toLocaleString()} tickets/mo (${Math.round(resRate * 100)}% AI resolution = ${resolvedTickets.toLocaleString()} resolutions/mo)`;

  const icSummary = document.getElementById('ic-summary');
  if (icSummary) {
    icSummary.innerHTML = `
      <div class="summary-card card-hidden">
        <div class="summary-label">Intercom Year-1 Total &amp; Hidden Cost Highlight</div>
        <div class="summary-metric" style="color:var(--rose);">$${icYear.toLocaleString()} / yr ($${icTotalMo.toLocaleString()}/mo)</div>
        <div class="summary-scenario">${scenarioLine}</div>
        <div class="summary-breakdown">$${icSeatsYr.toLocaleString()} licenses + $0 onboarding + $${icAiYr.toLocaleString()} Fin AI</div>
        <div class="summary-caveat"><strong>Hidden Cost Highlight:</strong> Metered Fin AI resolution fees ($0.99 &times; ${resolvedTickets.toLocaleString()}/mo) add $${icAiYr.toLocaleString()}/yr (${aiSharePct}% of your total Year-1 bill).</div>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-secondary" href="https://www.intercom.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="intercom-fin-ai" data-cta-location="summary-card">Check Intercom pricing &rarr;</a>
          </div>
        </div>
      </div>
      <div class="summary-card card-lowest">
        <div class="summary-label">Session-Pack Alternative (Freshdesk Pro)</div>
        <div class="summary-metric" style="color:var(--emerald);">$${fdYear.toLocaleString()} / yr ${diffLabel}</div>
        <div class="summary-scenario">${scenarioLine}</div>
        <div class="summary-breakdown">$${fdSeatsYr.toLocaleString()} licenses + $0 onboarding + $${fdAnnualAiCost.toLocaleString()} AI session packs</div>
        <div class="summary-caveat"><strong>Contract note:</strong> Includes 500 one-time free sessions, then $49 per 100 sessions (billed per session handled, resolved or not).</div>
        <div class="summary-actions">
          <div class="cta-stack">
            <a class="btn-cta" href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="summary-card">View Freshdesk plans &rarr;</a>
          </div>
          <a class="summary-audit-link" href="../zendesk-ai-resolution-and-automated-outcome-cost/" data-track="internal-audit">Compare Zendesk AI ($1.50&ndash;$2.00) &rarr;</a>
        </div>
      </div>
    `;
  }

  document.getElementById('ic-tbody').innerHTML = `
    <tr>
      <td data-label="Helpdesk Solution">
        <strong>Intercom + Fin AI (${resolvedTickets.toLocaleString()} resolutions/mo)</strong>
        <span class="status-pill status-verified">Verified</span>
        <div class="source-inline">Source: <a href="https://www.intercom.com/pricing" target="_blank" rel="noopener">Intercom pricing &nearr;</a></div>
      </td>
      <td data-label="Monthly Agent Seats" style="font-family:var(--mono);">$${icSeatCost.toLocaleString()} / mo</td>
      <td data-label="Monthly AI Usage"><span class="badge badge-high">$${icAiCost.toLocaleString()} / mo ($0.99 &times; ${resolvedTickets.toLocaleString()})</span></td>
      <td data-label="Total Monthly Bill" class="price-highlight">$${icTotalMo.toLocaleString()} / mo</td>
      <td data-label="Year-1 Total" class="price-highlight">$${icYear.toLocaleString()} / yr<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next Step"><div class="cta-stack"><a class="btn-secondary" href="https://www.intercom.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="intercom-fin-ai" data-cta-location="table-row">Check Intercom pricing &rarr;</a></div></td>
    </tr>
    <tr>
      <td data-label="Helpdesk Solution">
        <strong>Freshdesk Pro + Freddy AI Agent (Freshworks)</strong>
        <span class="status-pill status-verified">Verified</span>
        <div style="font-size:0.78rem; color:var(--emerald);">$55/agent/mo + $49/100 AI sessions (500 one-time free sessions deducted in Yr 1; optional Copilot $29/agent/mo)</div>
        <div class="source-inline">Verified source: <a href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="noopener">Freshdesk pricing &nearr;</a></div>
      </td>
      <td data-label="Monthly Agent Seats" style="font-family:var(--mono);">$${fdSeatCost.toLocaleString()} / mo</td>
      <td data-label="Monthly AI Usage"><span class="badge badge-low">$${fdAiCostMo.toLocaleString()} / mo (${fdMonthlyPacks} &times; $49 session packs)</span></td>
      <td data-label="Total Monthly Bill" class="price-highlight" style="color:var(--emerald);">$${fdTotalMo.toLocaleString()} / mo</td>
      <td data-label="Year-1 Total" class="price-highlight" style="color:var(--emerald);">$${fdYear.toLocaleString()} / yr ${diffLabel}<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next Step"><div class="cta-stack"><a class="btn-secondary" href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="table-row">View Freshdesk plans &rarr;</a></div></td>
    </tr>
  `;
}
['ic-seats', 'ic-plan', 'ic-tickets', 'ic-rate'].forEach(id => document.getElementById(id).addEventListener('input', updateIcCalc));
updateIcCalc();
</script>
"""

p2_faqs = [
    ("How much does Intercom Fin AI charge per resolution in 2026?", "Intercom charges $0.99 per Fin AI outcome/resolution (and $9.99 per sales qualification outcome), billed at most once per conversation, on top of your monthly per-seat plan ($29 Essential, $85 Advanced, or $132 Expert billed annually)."),
    ("What counts as a billable Fin AI resolution in Intercom?", "A billable $0.99 Fin outcome occurs when the customer confirms their question was answered, exits the conversation without requesting a human agent after Fin's answer, or triggers a configured procedure handoff/disqualification outcome."),
    ("How does Freshdesk Freddy AI pricing compare to Intercom's $0.99 per-resolution meter?", "Freshdesk (by Freshworks) charges $19 (Growth), $55 (Pro), or $89 (Enterprise) per agent/month billed annually ($23/$66/$107 monthly). For autonomous AI support, Freddy AI Agent includes 500 one-time complimentary sessions per account and then bills $49 per 100-session pack (charged per session, resolved or not), while Freddy AI Copilot for human agents is an optional $29/agent/month add-on.")
]

render_page(
    "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
    "Intercom Fin AI Cost Calculator – saasbill.io",
    "Calculate your monthly and annual Intercom Fin AI bill at $0.99 per resolution across Essential ($29), Advanced ($85), and Expert ($132) tiers, and compare against Freshdesk.",
    "/pricing/intercom-fin-ai-resolution-cost-calculator/",
    p2_body,
    faqs=p2_faqs
)

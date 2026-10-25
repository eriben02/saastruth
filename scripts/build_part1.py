import json
from layout import load_data, render_page, SITE_ORIGIN

TOOLS, AFFILIATES = load_data()
tools_js = json.dumps(TOOLS)
aff_js = json.dumps(AFFILIATES)

# ---------------------------------------------------------
# 1. Homepage: /index.html
# ---------------------------------------------------------
home_body = f"""
<section class="hero">
  <h1>Your SaaS bill is lying to you.</h1>
  <p class="lead">See what your B2B software will actually cost in Year 1. Compare subscription seats, mandatory onboarding fees, metered AI charges, and contract terms before you commit.</p>
</section>

<section class="calc-box" aria-labelledby="calc-heading">
  <h2 id="calc-heading" style="margin-top:0;">Interactive Year-1 True-Cost Calculator (2026)</h2>
  <p style="color:var(--muted); margin-bottom:16px; font-size:0.95rem;">Pre-filled example loaded below: <strong>5 seats, annual billing, and 500 AI-resolved tickets/month</strong>. Switch category or adjust sliders to model your exact team.</p>
  <div class="cat-tabs-wrap">
    <span class="cat-tabs-label">Quick Category Select</span>
    <div class="cat-tabs" role="tablist" aria-label="Software Categories">
      <button type="button" class="cat-tab active" data-cat="Helpdesk & AI Support" data-track="category-select">Helpdesk &amp; AI Support (6 tools)</button>
      <button type="button" class="cat-tab" data-cat="CRM & Sales" data-track="category-select">CRM &amp; Sales (5 tools)</button>
      <button type="button" class="cat-tab" data-cat="Compliance, HIPAA & SOC 2" data-track="category-select">Compliance, HIPAA &amp; SOC 2 (4 tools)</button>
      <button type="button" class="cat-tab" data-cat="Payment Processors & MoR" data-track="category-select">Payment Processors &amp; MoR (5 rails)</button>
      <button type="button" class="cat-tab" data-cat="ALL" data-track="category-select">All Subscription SaaS (15 tools)</button>
    </div>
  </div>
  <div class="calc-grid">
    <div class="control-group">
      <label for="cat-filter">1. Software category</label>
      <select id="cat-filter">
        <option value="Helpdesk & AI Support" selected>Helpdesk &amp; AI Support (6 tools)</option>
        <option value="CRM & Sales">CRM &amp; Sales (5 tools)</option>
        <option value="Compliance, HIPAA & SOC 2">Compliance, HIPAA &amp; SOC 2 (4 tools)</option>
        <option value="Payment Processors & MoR">Payment Processors &amp; MoR (5 rails)</option>
        <option value="ALL">All Subscription SaaS (15 tools)</option>
      </select>
    </div>
    <div class="control-group" id="seat-control-group">
      <label for="seat-slider">2. Team size: <span class="val-pill" id="seat-val">5</span> seats</label>
      <input type="range" id="seat-slider" min="1" max="50" value="5" />
    </div>
    <div class="control-group" id="ai-control-group">
      <label for="ai-slider">3. Monthly AI-resolved tickets: <span class="val-pill" id="ai-val">500</span> /mo</label>
      <input type="range" id="ai-slider" min="0" max="5000" step="100" value="500" />
    </div>
    <div class="control-group" id="billing-control-group">
      <label for="billing-mode">4. Billing term</label>
      <select id="billing-mode">
        <option value="annual">Annual commitment (lowest rate)</option>
        <option value="monthly">Month-to-month billing</option>
      </select>
    </div>
    <div class="control-group" id="sort-control-group">
      <label for="sort-mode">5. Sort comparison by</label>
      <select id="sort-mode">
        <option value="lowest">Lowest Year-1 Total first</option>
        <option value="highest">Highest Year-1 Total first</option>
        <option value="hidden_fees">Highest hidden / non-seat fees</option>
        <option value="name">Platform name (A&ndash;Z)</option>
      </select>
    </div>
  </div>

  <div id="calc-summary-strip" class="summary-strip" aria-live="polite"></div>
  <p id="calc-summary-note" class="summary-interpretation"><strong>How to read this comparison:</strong> Lowest cost does not automatically mean best fit&mdash;verify plan limits, seat minimums, and contract lock-in before choosing.</p>

  <div id="calc-viz-panel" class="viz-panel" aria-label="Year-1 Cost Composition Stacked Bar Chart">
    <div class="viz-header">
      <div class="viz-title">Year-1 Cost Composition Breakdown (USD)</div>
      <div class="viz-legend">
        <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-seats);"></span>Base licenses / seats</span>
        <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-onboarding);"></span>Mandatory onboarding fee</span>
        <span class="viz-legend-item"><span class="viz-swatch" style="background:var(--bar-ai);"></span>Metered AI overages</span>
      </div>
    </div>
    <div id="calc-viz-rows" class="viz-rows"></div>
  </div>

  <div class="table-wrap mobile-cards">
    <table>
      <caption>2026 B2B Software Year-1 True-Cost Comparison &amp; Contract Audit (USD, verified Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>Platform &amp; Verification</th>
          <th>Effective Monthly Rate</th>
          <th>Mandatory Onboarding</th>
          <th>Contract Fine Print &amp; Source</th>
          <th>Year-1 Total (USD)</th>
          <th>Pricing Link</th>
        </tr>
      </thead>
      <tbody id="calc-tbody"></tbody>
    </table>
  </div>
  <p id="calc-payment-note" style="font-size:0.84rem; color:var(--muted); margin-top:10px;">
    <strong>Note on Payment Processors &amp; MoR:</strong> Transaction-based payment rails (Stripe, Paddle, Whop, Lemon Squeezy, Chargeflow) charge a percentage of processing volume rather than per-seat subscriptions, so they are separated from the seat-based ranking by default. Select <em>Payment Processors &amp; MoR</em> in the Category dropdown or open the <a href="./exit/stripe-shopify-paddle-frozen-funds-alternatives/">Payout Hold &amp; Rolling Reserve Simulator &rarr;</a>
  </p>
</section>

<div class="geo-direct-answer">
  <p><strong>Key audit takeaway:</strong> Across the 20 B2B software and payment platforms in our 2026 dataset, mandatory onboarding fees ($1,500–$7,000 on HubSpot Professional and Enterprise), seat-bucket minimums (3 seats minimum on monday CRM), and outcome-based AI meters ($0.99 per Fin AI resolution on Intercom; $1.50 committed or $2.00 pay-as-you-go per automated resolution above allowance on Zendesk) push actual Year-1 spend <strong>28% to 310% above advertised per-seat rates</strong>.</p>
</div>

<section id="methodology" class="methodology-box" aria-labelledby="methodology-heading">
  <h2 id="methodology-heading" style="margin-top:0;">How we calculate &amp; verify Year-1 costs</h2>
  <p style="color:var(--muted); font-size:0.94rem;">Every figure on SaaSBill is computed from deterministic formulas and linked directly to the vendor’s published pricing page, help-center billing documentation, or Master Subscription Agreement (MSA).</p>
  <div class="methodology-grid">
    <div class="methodology-item">
      <strong>1. Year-1 Total Formula</strong>
      <code>Year-1 Total = (12 &times; Billed Monthly Seats) + Mandatory Onboarding + (12 &times; Net AI Overage)</code>. Seat minimums (such as monday CRM’s 3/5/10/15 buckets) and included AI allowances (such as Zendesk’s 5–10 AR/agent/mo and Freshdesk’s 500 one-time sessions) are applied automatically.
    </div>
    <div class="methodology-item">
      <strong>2. Verification Status Badges</strong>
      <span class="status-pill status-verified">Verified</span> indicates published self-serve pricing and contract terms checked directly against official vendor docs on Oct 25, 2026.<br/>
      <span class="status-pill status-estimated">Estimated (Benchmark)</span> indicates non-public, sales-quoted pricing (such as Vanta and Drata) modeled from verified buyer contract benchmarks.
    </div>
    <div class="methodology-item">
      <strong>3. Editorial Independence &amp; Direct Pricing Links</strong>
      Every CTA button links directly to the vendor&rsquo;s official pricing or product page (`rel="nofollow noopener"`), alongside a separate primary-source link for contract verification. Calculations and sort order are strictly mathematical.
    </div>
  </div>
</section>

<section>
  <h2>What we found reading the fine print</h2>
  <p class="section-tldr">Before signing an annual SaaS order form, check four clauses that rarely appear on the public pricing grid: mandatory onboarding fees, seat-bucket minimums, uncapped AI resolution meters, and 30-to-60 day non-renewal notice deadlines.</p>
  <ul class="key-list">
    <li><strong>HubSpot’s onboarding fee adds 28% to a 5-seat Sales Pro deal:</strong> HubSpot Sales Hub Professional ($90/seat/month billed annually) requires a mandatory <strong>$1,500 onboarding fee</strong> ($3,500 on Enterprise), bringing five seats to <strong>$6,900 in Year 1</strong> compared with <strong>$2,940/year</strong> on Pipedrive Professional ($0 onboarding).</li>
    <li><strong>Intercom and Zendesk AI meters can exceed your seat bill:</strong> At 3,000 monthly support conversations with 50% AI resolution (1,500 resolutions/month), Intercom Fin ($0.99/resolution) adds <strong>$1,485/month ($17,820/year)</strong> on top of agent seats. Zendesk Suite includes only 5–10 automated resolutions per agent/month before charging <strong>$1.50 committed or $2.00 pay-as-you-go</strong> per verified resolution.</li>
    <li><strong>monday CRM’s 3-seat minimum triples the price for solo founders:</strong> A single user on monday CRM Basic ($12/seat/month billed annually, $18/seat/month billed monthly) or Standard ($17/seat/month annual, $25/seat/month monthly) must pay for three seats (<strong>$36–$51/month annual or $54–$75/month monthly</strong>), whereas Pipedrive Lite/Essential bills one seat at <strong>$14/month ($168/year)</strong>. The math flips in monday CRM’s favor at exactly 3, 5, or 10 users.</li>
    <li><strong>Merchant of Record platforms own your card vault:</strong> Stripe and Shopify Payments can hold payouts for <strong>120–180 days</strong> or apply a <strong>25% rolling reserve</strong> on risk flags, but you own the customer relationship. With a Merchant of Record like Paddle (5% + $0.50), Paddle is the seller of record—if Paddle terminates your account on a risk review, you cannot export subscriber card tokens.</li>
    <li><strong>Self-serve HIPAA BAAs exist if you know where to look:</strong> Jotform signs a HIPAA Business Associate Agreement on its self-serve Gold plan (<strong>$99/month billed annually, $129/month monthly, 1-user account</strong>), and 1Password Business includes SAML SSO at <strong>$8.99/user/month billed annually ($107.88/year; $10.99/user/month monthly)</strong> with no Enterprise SSO markup. Meanwhile, Vanta and Drata list quotes ($9k–$15k+/year) are routinely negotiated down by <strong>30%–50%</strong> and never include the separate <strong>$6,500–$15,000+ CPA auditor fee</strong>.</li>
  </ul>
</section>

<section id="all-calculators">
  <h2>All calculators &amp; contract audits</h2>
  <div class="card-grid">
    <div class="card">
      <span class="badge badge-high">CRM &amp; Sales &middot; $1,500–$7,000 Onboarding</span>
      <h3><a href="./pricing/hubspot-true-cost-and-onboarding-fees/">What HubSpot actually costs in Year 1 (once you add onboarding)</a></h3>
      <p>How HubSpot’s mandatory $1,500–$7,000 onboarding fees and 12-month auto-renewing contracts work in practice, plus how Close CRM and Pipedrive compare for 1 to 30 reps.</p>
    </div>
    <div class="card">
      <span class="badge badge-medium">CRM &amp; Sales &middot; 3-Seat Minimum Math</span>
      <h3><a href="./compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/">Why a "$12/seat" CRM costs $36 a month for a solo founder</a></h3>
      <p>monday CRM bills in fixed buckets of 3, 5, 10, and 15 seats. Run the 1-to-15 user calculator to see where Pipedrive wins and where monday CRM takes the lead.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Helpdesk &amp; AI &middot; $0.99 / Resolution</span>
      <h3><a href="./pricing/intercom-fin-ai-resolution-cost-calculator/">What Intercom’s $0.99 AI resolution fee does to your support bill</a></h3>
      <p>Model how Intercom’s $0.99 Fin AI outcome meter and $9.99 sales qualification charge scale your monthly invoice compared with Freshdesk.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Helpdesk &amp; AI &middot; $1.50–$2.00 / Resolution</span>
      <h3><a href="./pricing/zendesk-ai-resolution-and-automated-outcome-cost/">What Zendesk’s $1.50–$2.00 AI resolution fee adds to your invoice</a></h3>
      <p>Zendesk Suite includes only 5–10 automated resolutions per agent each month, and $2.00 pay-as-you-go overage is enabled by default. Compare against Freshdesk and Help Scout.</p>
    </div>
    <div class="card">
      <span class="badge badge-high">Payments &amp; MoR &middot; 180-Day Holds</span>
      <h3><a href="./exit/stripe-shopify-paddle-frozen-funds-alternatives/">What happens when Stripe, Shopify, or Paddle freezes your payouts</a></h3>
      <p>Simulate a 25% rolling reserve plus capital loan deduction, check card-token portability between processors and Merchants of Record, and set up Whop + Chargeflow failover.</p>
    </div>
    <div class="card">
      <span class="badge badge-low">Compliance &middot; HIPAA BAA &amp; SOC 2</span>
      <h3><a href="./compliance/hipaa-baa-and-soc2-pricing-tiers/">Which software plans actually sign a HIPAA BAA (and what SOC 2 costs)</a></h3>
      <p>Find self-serve HIPAA BAA and SAML SSO tiers (Jotform Gold, 1Password Business) and calculate negotiated Vanta/Drata platform costs plus external CPA auditor fees.</p>
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
  'close-crm': 'Check Close pricing →',
  'pipedrive-crm': 'Explore Pipedrive plans →',
  'monday-crm': 'View monday CRM pricing →',
  'intercom-fin-ai': 'Check Intercom pricing →',
  'freshdesk-support': 'View Freshdesk plans →',
  'zendesk-suite-team': 'View Zendesk pricing →',
  'zendesk-suite-professional': 'View Zendesk pricing →',
  'help-scout-plus': 'Check Help Scout plans →',
  'stripe-payments': 'View Stripe pricing →',
  'paddle-mor': 'View Paddle pricing →',
  'whop-payments': 'Explore Whop Payments →',
  'lemon-squeezy': 'View Lemon Squeezy pricing →',
  'chargeflow': 'Check Chargeflow pricing →',
  'jotform-hipaa': 'Check Jotform HIPAA plans →',
  '1password-business': 'View 1Password pricing →',
  'vanta-soc2': 'View Vanta pricing →',
  'drata-soc2': 'Explore Drata platform →'
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

function renderDirectory() {{
  const cat = document.getElementById('cat-filter').value;
  const seats = parseInt(document.getElementById('seat-slider').value, 10);
  const aiVol = parseInt(document.getElementById('ai-slider').value, 10);
  const mode = document.getElementById('billing-mode').value;
  const sortEl = document.getElementById('sort-mode');
  const sortMode = sortEl ? sortEl.value : 'lowest';
  document.getElementById('seat-val').textContent = seats;
  document.getElementById('ai-val').textContent = aiVol;

  // Sync visual category tabs with select dropdown
  document.querySelectorAll('.cat-tab').forEach(btn => {{
    if (btn.getAttribute('data-cat') === cat) {{
      btn.classList.add('active');
    }} else {{
      btn.classList.remove('active');
    }}
  }});

  // Show AI slider ONLY when relevant (Helpdesk & AI Support or ALL)
  const aiControl = document.getElementById('ai-control-group');
  const seatControl = document.getElementById('seat-control-group');
  const billingControl = document.getElementById('billing-control-group');
  const sortControl = document.getElementById('sort-control-group');
  if (aiControl) {{
    if (cat === 'Helpdesk & AI Support' || cat === 'ALL') {{
      aiControl.classList.remove('is-hidden');
    }} else {{
      aiControl.classList.add('is-hidden');
    }}
  }}
  if (seatControl && billingControl && sortControl) {{
    if (cat === 'Payment Processors & MoR') {{
      seatControl.classList.add('is-hidden');
      billingControl.classList.add('is-hidden');
      sortControl.classList.add('is-hidden');
    }} else {{
      seatControl.classList.remove('is-hidden');
      billingControl.classList.remove('is-hidden');
      sortControl.classList.remove('is-hidden');
    }}
  }}

  const filtered = TOOLS.filter(t => {{
    if (cat === 'ALL') return t.category !== 'Payment Processors & MoR';
    return t.category === cat;
  }});
  const rows = filtered.map(t => calcToolYear1(t, seats, aiVol, mode));

  if (sortMode === 'highest') {{
    rows.sort((a, b) => b.year1Total - a.year1Total);
  }} else if (sortMode === 'hidden_fees') {{
    rows.sort((a, b) => b.hiddenFees - a.hiddenFees || b.year1Total - a.year1Total);
  }} else if (sortMode === 'name') {{
    rows.sort((a, b) => a.tool.name.localeCompare(b.tool.name));
  }} else {{
    rows.sort((a, b) => a.year1Total - b.year1Total);
  }}

  const summaryEl = document.getElementById('calc-summary-strip');
  const vizPanel = document.getElementById('calc-viz-panel');
  const vizRowsEl = document.getElementById('calc-viz-rows');
  const scenarioLine = formatScenarioText(cat, seats, aiVol, mode);

  if (cat === 'Payment Processors & MoR') {{
    if (summaryEl) {{
      summaryEl.innerHTML = `
        <div class="summary-card card-lowest">
          <div class="summary-label">Multi-Processor Failover Rail</div>
          <div class="summary-metric">Whop Payments (2.7% + $0.30)</div>
          <div class="summary-scenario">Based on per-transaction domestic card processing ($0/mo fixed fee)</div>
          <div class="summary-breakdown">2.7% + $0.30 domestic &middot; multi-acquirer waterfall routing</div>
          <div class="summary-caveat"><strong>Caveat:</strong> Total cost depends on monthly GMV, average order value, and international card mix.</div>
          <div class="summary-actions">
            <a class="btn-cta" href="https://whop.com/sell" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="whop-payments" data-cta-location="summary-card">Explore Whop Payments &rarr;</a>
            <a class="summary-audit-link" href="./exit/stripe-shopify-paddle-frozen-funds-alternatives/" data-track="internal-audit">Open reserve simulator &rarr;</a>
          </div>
        </div>
        <div class="summary-card card-hidden">
          <div class="summary-label">Hidden Cost &amp; Lock-In Highlight</div>
          <div class="summary-metric" style="color:var(--rose);">Paddle MoR (5.0% + $0.50)</div>
          <div class="summary-scenario">Merchant of Record tax &amp; compliance structure</div>
          <div class="summary-breakdown">5.0% + $0.50 per transaction (includes global VAT/sales tax)</div>
          <div class="summary-caveat"><strong>Hidden Cost Highlight:</strong> Paddle is the legal seller of record and owns the card vault&mdash;if terminated on a risk review, subscriber card tokens cannot be exported.</div>
          <div class="summary-actions">
            <a class="btn-secondary" href="https://www.paddle.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="paddle-mor" data-cta-location="summary-card">View Paddle pricing &rarr;</a>
            <a class="summary-audit-link" href="./exit/stripe-shopify-paddle-frozen-funds-alternatives/" data-track="internal-audit">Read token lock-in audit &rarr;</a>
          </div>
        </div>
        <div class="summary-card card-highest">
          <div class="summary-label">Dispute &amp; Reserve Shield</div>
          <div class="summary-metric">Chargeflow (&lt;0.5% Dispute Ratio)</div>
          <div class="summary-scenario">Performance-based pre-dispute &amp; chargeback automation</div>
          <div class="summary-breakdown">$0 setup fee &middot; pay-on-recovery + pre-dispute alerts</div>
          <div class="summary-caveat"><strong>Contract note:</strong> Prevents Stripe and Shopify 25% rolling reserves by keeping dispute ratios below card-network monitoring thresholds.</div>
          <div class="summary-actions">
            <a class="btn-cta" href="https://www.chargeflow.io/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="chargeflow" data-cta-location="summary-card">Check Chargeflow pricing &rarr;</a>
            <a class="summary-audit-link" href="./exit/stripe-shopify-paddle-frozen-funds-alternatives/" data-track="internal-audit">Simulate 25% reserve hold &rarr;</a>
          </div>
        </div>
      `;
    }}
    if (vizPanel) vizPanel.style.display = 'none';
  }} else if (rows.length > 0) {{
    const byLowest = [...rows].sort((a, b) => a.year1Total - b.year1Total);
    const minR = byLowest[0];
    const maxR = byLowest[byLowest.length - 1];
    const byHidden = [...rows].sort((a, b) => b.hiddenFees - a.hiddenFees || b.year1Total - a.year1Total);
    const topHidden = byHidden[0];
    const maxTotal = Math.max(...rows.map(r => r.year1Total), 1);

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
            <a class="btn-cta" href="${{minAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{minR.tool.id}}" data-cta-location="summary-card">${{getVendorCtaLabel(minR.tool)}}</a>
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
            <a class="btn-secondary" href="${{hidAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{topHidden.tool.id}}" data-cta-location="summary-card">${{getVendorCtaLabel(topHidden.tool)}}</a>
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
            <a class="btn-secondary" href="${{maxAff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{maxR.tool.id}}" data-cta-location="summary-card">${{getVendorCtaLabel(maxR.tool)}}</a>
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
          <div class="viz-row">
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
    const badgeClass = t.trap_severity === 'high' ? 'badge-high' : (t.trap_severity === 'medium' ? 'badge-medium' : 'badge-low');
    const verStatus = t.verification_status || 'Verified';
    const verClass = verStatus.startsWith('Verified') ? 'status-verified' : 'status-estimated';
    const srcUrl = (t.source_urls && t.source_urls[0]) ? t.source_urls[0] : aff.destination_url;
    const srcLabel = t.source_label || 'Official pricing & terms';
    const auditObj = INTERNAL_AUDIT_LINKS[t.id];
    const fmtRate = n => Number.isInteger(n) ? n.toLocaleString() : n.toFixed(2);
    let rateText = '';
    if (t.transaction_fee_display) {{
      rateText = t.transaction_fee_display;
    }} else if (t.id === 'jotform-hipaa') {{
      rateText = `$${{fmtRate(r.unitRate)}}/mo (1-user Gold HIPAA plan)`;
    }} else if (t.id === 'vanta-soc2' || t.id === 'drata-soc2') {{
      rateText = `$${{fmtRate(r.unitRate)}}/mo (flat annual platform fee)`;
    }} else if (t.id === 'hubspot-marketing-pro') {{
      rateText = `$${{fmtRate(r.unitRate)}}/mo base (3 seats incl.) + $45/extra seat ($${{fmtRate(r.monthlySoftware)}}/mo for ${{r.effSeats}} seats)`;
    }} else {{
      rateText = `$${{fmtRate(r.unitRate)}}/mo (${{r.effSeats}} billed seat${{r.effSeats === 1 ? '' : 's'}})`;
    }}
    const totalText = t.category === 'Payment Processors & MoR'
      ? `Per-transaction <div style="font-size:0.75rem; font-weight:400;"><a href="./exit/stripe-shopify-paddle-frozen-funds-alternatives/">Simulate holds &rarr;</a></div>`
      : `$${{r.year1Total.toLocaleString()}} / yr <div class="cell-scenario">${{scenarioLine}}</div>`;
    const extraAiLine = r.aiNote ? `<div style="font-size:0.75rem; color:var(--muted); margin-top:2px;">AI math: ${{r.aiNote}}</div>` : '';
    return `
      <tr>
        <td data-label="Platform">
          <strong>${{t.name}}</strong>
          <div style="font-size:0.78rem; color:var(--muted);">${{t.category}}</div>
          <span class="status-pill ${{verClass}}">${{verStatus}}</span>
          ${{auditObj ? `<div><a class="audit-inline-link" href="${{auditObj.url}}" data-track="internal-audit">${{auditObj.label}}</a></div>` : ''}}
        </td>
        <td data-label="Effective Rate" style="font-family:var(--mono);">${{rateText}}${{extraAiLine}}</td>
        <td data-label="Mandatory Onboarding" style="font-family:var(--mono);">${{t.mandatory_onboarding_fee_usd > 0 ? '$' + t.mandatory_onboarding_fee_usd.toLocaleString() : '$0'}}</td>
        <td data-label="Contract Fine Print &amp; Source">
          <span class="badge ${{badgeClass}}">${{t.trap_badge}}</span>
          <div style="font-size:0.8rem; color:var(--muted); margin-top:4px;">${{t.billing_lock_in_type}}</div>
          <div class="source-inline">Source: <a href="${{srcUrl}}" target="_blank" rel="noopener">${{srcLabel}} &nearr;</a></div>
        </td>
        <td data-label="Year-1 Total" class="price-highlight">${{totalText}}</td>
        <td data-label="Next Step">
          <a class="btn-cta" href="${{aff.destination_url}}" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="${{t.id}}" data-cta-location="table-row">${{getVendorCtaLabel(t)}}</a>
        </td>
      </tr>
    `;
  }}).join('');
}}
['cat-filter', 'seat-slider', 'ai-slider', 'billing-mode', 'sort-mode'].forEach(id => {{
  const el = document.getElementById(id);
  if (el) el.addEventListener('input', renderDirectory);
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
        <option value="sales_pro">Sales Hub Professional ($90/seat + $1,500 onboarding)</option>
        <option value="sales_ent">Sales Hub Enterprise ($150/seat + $3,500 onboarding)</option>
        <option value="mkt_pro">Marketing Hub Pro ($800/mo [3 seats] + $3,000 onboarding)</option>
        <option value="mkt_ent">Marketing Hub Enterprise ($3,600/mo [5 seats] + $7,000 onboarding)</option>
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
          <a class="btn-secondary" href="https://www.hubspot.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="hubspot" data-cta-location="summary-card">View HubSpot pricing &rarr;</a>
        </div>
      </div>
      <div class="summary-card card-lowest">
        <div class="summary-label">Lowest Year-1 Cost ($0 Onboarding)</div>
        <div class="summary-metric" style="color:var(--emerald);">$${closeYear1.toLocaleString()} / yr &middot; Close CRM (Essentials)</div>
        <div class="summary-scenario">${scenarioLine} (saves $${Math.max(0, hsYear1 - closeYear1).toLocaleString()}/yr vs. HubSpot)</div>
        <div class="summary-breakdown">$${closeYear1.toLocaleString()} licenses + $0 onboarding + $0 AI</div>
        <div class="summary-caveat"><strong>Contract note:</strong> $35/user/mo annual ($49 monthly); Growth tier with workflows is $99/user/mo.</div>
        <div class="summary-actions">
          <a class="btn-cta" href="https://close.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="close-crm" data-cta-location="summary-card">Check Close pricing &rarr;</a>
        </div>
      </div>
      <div class="summary-card card-highest">
        <div class="summary-label">Zero-Onboarding Alternative</div>
        <div class="summary-metric" style="color:var(--emerald);">$${pipeYear1.toLocaleString()} / yr &middot; Pipedrive (Professional)</div>
        <div class="summary-scenario">${scenarioLine} (saves $${Math.max(0, hsYear1 - pipeYear1).toLocaleString()}/yr vs. HubSpot)</div>
        <div class="summary-breakdown">$${pipeYear1.toLocaleString()} licenses + $0 onboarding + $0 AI</div>
        <div class="summary-caveat"><strong>Contract note:</strong> 1-seat minimum ($14/mo Lite up to $49/mo Pro); cancel anytime on monthly billing.</div>
        <div class="summary-actions">
          <a class="btn-cta" href="https://www.pipedrive.com/en/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="pipedrive-crm" data-cta-location="summary-card">Explore Pipedrive plans &rarr;</a>
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
      <td data-label="Next Step"><a class="btn-secondary" href="https://www.hubspot.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="hubspot" data-cta-location="table-row">View HubSpot pricing &rarr;</a></td>
    </tr>
    <tr>
      <td data-label="CRM Platform"><strong>Close CRM (Essentials)</strong> <span class="status-pill status-verified">Verified</span><div style="font-size:0.78rem; color:var(--emerald);">$35/user/mo annual ($49 monthly) &middot; $0 onboarding &middot; Growth w/ workflows is $99/user/mo</div></td>
      <td data-label="Monthly Seat Cost" style="font-family:var(--mono);">$${closeMonthly.toLocaleString()} / mo</td>
      <td data-label="Mandatory Onboarding"><span class="badge badge-low">$0 onboarding</span></td>
      <td data-label="Contract Terms &amp; Source">Month-to-month or annual<div class="source-inline">Source: <a href="https://close.com/pricing" target="_blank" rel="noopener">Close pricing &nearr;</a></div></td>
      <td data-label="Year-1 Total" class="price-highlight" style="color:var(--emerald);">$${closeYear1.toLocaleString()} (saves $${Math.max(0, hsYear1 - closeYear1).toLocaleString()})<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next Step"><a class="btn-cta" href="https://close.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="close-crm" data-cta-location="table-row">Check Close pricing &rarr;</a></td>
    </tr>
    <tr>
      <td data-label="CRM Platform"><strong>Pipedrive CRM (Professional)</strong> <span class="status-pill status-verified">Verified</span><div style="font-size:0.78rem; color:var(--emerald);">No onboarding fee &middot; 1-seat minimum</div></td>
      <td data-label="Monthly Seat Cost" style="font-family:var(--mono);">$${pipeMonthly.toLocaleString()} / mo</td>
      <td data-label="Mandatory Onboarding"><span class="badge badge-low">$0 onboarding</span></td>
      <td data-label="Contract Terms &amp; Source">Cancel anytime on monthly plan<div class="source-inline">Source: <a href="https://www.pipedrive.com/en/pricing" target="_blank" rel="noopener">Pipedrive pricing &nearr;</a></div></td>
      <td data-label="Year-1 Total" class="price-highlight" style="color:var(--emerald);">$${pipeYear1.toLocaleString()} (saves $${Math.max(0, hsYear1 - pipeYear1).toLocaleString()})<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next Step"><a class="btn-cta" href="https://www.pipedrive.com/en/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="pipedrive-crm" data-cta-location="table-row">Explore Pipedrive plans &rarr;</a></td>
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
        <option value="29">Essential ($29/seat/mo annual &middot; $39 monthly)</option>
        <option value="85" selected>Advanced ($85/seat/mo annual &middot; includes 20 Lite seats)</option>
        <option value="132">Expert ($132/seat/mo annual &middot; includes 50 Lite seats)</option>
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
          <a class="btn-secondary" href="https://www.intercom.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="intercom-fin-ai" data-cta-location="summary-card">Check Intercom pricing &rarr;</a>
        </div>
      </div>
      <div class="summary-card card-lowest">
        <div class="summary-label">Session-Pack Alternative (Freshdesk Pro)</div>
        <div class="summary-metric" style="color:var(--emerald);">$${fdYear.toLocaleString()} / yr ${diffLabel}</div>
        <div class="summary-scenario">${scenarioLine}</div>
        <div class="summary-breakdown">$${fdSeatsYr.toLocaleString()} licenses + $0 onboarding + $${fdAnnualAiCost.toLocaleString()} AI session packs</div>
        <div class="summary-caveat"><strong>Contract note:</strong> Includes 500 one-time free sessions, then $49 per 100 sessions (billed per session handled, resolved or not).</div>
        <div class="summary-actions">
          <a class="btn-cta" href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="summary-card">View Freshdesk plans &rarr;</a>
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
      <td data-label="Next Step"><a class="btn-secondary" href="https://www.intercom.com/pricing" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="intercom-fin-ai" data-cta-location="table-row">Check Intercom pricing &rarr;</a></td>
    </tr>
    <tr>
      <td data-label="Helpdesk Solution">
        <strong>Freshdesk Pro + Freddy AI Agent (Freshworks)</strong>
        <span class="status-pill status-verified">Verified</span>
        <div style="font-size:0.78rem; color:var(--emerald);">$55/agent/mo + $49/100 AI sessions (500 one-time free sessions deducted in Yr 1; optional Copilot $29/agent/mo)</div>
        <div class="source-inline">Source: <a href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="noopener">Freshdesk pricing &nearr;</a></div>
      </td>
      <td data-label="Monthly Agent Seats" style="font-family:var(--mono);">$${fdSeatCost.toLocaleString()} / mo</td>
      <td data-label="Monthly AI Usage"><span class="badge badge-low">$${fdAiCostMo.toLocaleString()} / mo (${fdMonthlyPacks} &times; $49 session packs)</span></td>
      <td data-label="Total Monthly Bill" class="price-highlight" style="color:var(--emerald);">$${fdTotalMo.toLocaleString()} / mo</td>
      <td data-label="Year-1 Total" class="price-highlight" style="color:var(--emerald);">$${fdYear.toLocaleString()} / yr ${diffLabel}<div class="cell-scenario">${scenarioLine}</div></td>
      <td data-label="Next Step"><a class="btn-cta" href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="nofollow noopener" data-track="vendor-cta" data-vendor="freshdesk-support" data-cta-location="table-row">View Freshdesk plans &rarr;</a></td>
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

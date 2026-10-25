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
  <p class="lead">Software pricing pages show you the teaser rate. They leave out the $1,500–$7,000 mandatory onboarding fee, the 3-seat minimum bucket, the $0.99 per-resolution AI meter, and the 12-month auto-renewal clause buried in the order form. Use the calculators and contract audits below to see what you will actually pay in Year 1 before you sign.</p>
  <div class="geo-direct-answer">
    <p><strong>The short version:</strong> Across the 18 B2B software and payment platforms audited in our 2026 database, mandatory onboarding fees ($1,500–$7,000 on HubSpot Professional and Enterprise), seat-bucket minimums (3 seats minimum on monday CRM), and outcome-based AI meters ($0.99 per Fin AI resolution on Intercom; $1.50–$2.00 per automated resolution above allowance on Zendesk) push actual Year-1 spend <strong>28% to 310% above advertised per-seat rates</strong>.</p>
  </div>
</section>

<section class="calc-box" aria-labelledby="calc-heading">
  <h2 id="calc-heading" style="margin-top:0;">Compare real first-year costs across 18 platforms</h2>
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">Select your software category, team size, and monthly AI ticket volume. For a five-person sales or support team, switching from high-onboarding or per-resolution vendors to zero-onboarding platforms (Close CRM, Pipedrive, Freshdesk, Help Scout) typically saves <strong>$1,500 to $18,400 in Year 1</strong>.</p>
  <div class="calc-grid">
    <div class="control-group">
      <label for="cat-filter">Category</label>
      <select id="cat-filter">
        <option value="ALL">All audited categories</option>
        <option value="CRM & Sales">CRM &amp; Sales</option>
        <option value="Helpdesk & AI Support">Helpdesk &amp; AI Support</option>
        <option value="Payment Processors & MoR">Payment Processors &amp; MoR</option>
        <option value="Compliance, HIPAA & SOC 2">Compliance, HIPAA BAA &amp; SOC 2</option>
      </select>
    </div>
    <div class="control-group">
      <label for="seat-slider">Team size: <span class="val-pill" id="seat-val">5</span> seats</label>
      <input type="range" id="seat-slider" min="1" max="50" value="5" />
    </div>
    <div class="control-group">
      <label for="ai-slider">Monthly AI-resolved tickets: <span class="val-pill" id="ai-val">500</span> /mo</label>
      <input type="range" id="ai-slider" min="0" max="5000" step="100" value="500" />
    </div>
    <div class="control-group">
      <label for="billing-mode">Billing term</label>
      <select id="billing-mode">
        <option value="annual">Annual commitment (lowest rate)</option>
        <option value="monthly">Month-to-month billing</option>
      </select>
    </div>
  </div>
  <div class="table-wrap">
    <table>
      <caption>2026 B2B Software Year-1 True-Cost Comparison (USD, checked Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>Platform</th>
          <th>Advertised Rate</th>
          <th>Mandatory Onboarding</th>
          <th>Contract Fine Print</th>
          <th>Year-1 Total (USD)</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody id="calc-tbody"></tbody>
    </table>
  </div>
</section>

<section>
  <h2>What we found reading the fine print</h2>
  <p class="section-tldr">Before signing an annual SaaS order form, check four clauses that rarely appear on the public pricing grid: mandatory onboarding fees, seat-bucket minimums, uncapped AI resolution meters, and 30-to-60 day non-renewal notice deadlines.</p>
  <ul class="key-list">
    <li><strong>HubSpot’s onboarding fee adds 28% to a 5-seat Sales Pro deal:</strong> HubSpot Sales Hub Professional ($90/seat/month billed annually) requires a mandatory <strong>$1,500 onboarding fee</strong> ($3,500 on Enterprise), bringing five seats to <strong>$6,900 in Year 1</strong> compared with <strong>$2,940/year</strong> on Pipedrive Professional ($0 onboarding).</li>
    <li><strong>Intercom and Zendesk AI meters can exceed your seat bill:</strong> At 3,000 monthly support conversations with 50% AI resolution (1,500 resolutions/month), Intercom Fin ($0.99/resolution) adds <strong>$1,485/month ($17,820/year)</strong> on top of agent seats. Zendesk Suite includes only 5–10 automated resolutions per agent/month before charging <strong>$1.50 committed or $2.00 pay-as-you-go</strong> per verified resolution.</li>
    <li><strong>monday CRM’s 3-seat minimum triples the price for solo founders:</strong> A single user on monday CRM Standard ($17/seat/month) must pay for three seats (<strong>$51/month or $612/year</strong>), whereas Pipedrive Essential bills one seat at <strong>$14/month ($168/year)</strong>. The math flips in monday CRM’s favor at exactly 3, 5, or 10 users.</li>
    <li><strong>Merchant of Record platforms own your card vault:</strong> Stripe and Shopify Payments can hold payouts for <strong>120–180 days</strong> or apply a <strong>25% rolling reserve</strong> on risk flags, but you own the customer relationship. With a Merchant of Record like Paddle (5% + $0.50), Paddle is the seller of record—if Paddle terminates your account on a risk review, you cannot export subscriber card tokens.</li>
    <li><strong>Self-serve HIPAA BAAs exist if you know where to look:</strong> Jotform signs a HIPAA Business Associate Agreement on its self-serve Gold plan (<strong>$99/month billed annually</strong>), and 1Password Business includes SAML SSO at <strong>$7.99/user/month</strong> with no Enterprise SSO markup. Meanwhile, Vanta and Drata list quotes ($9k–$15k+/year) are routinely negotiated down by <strong>30%–50%</strong> and never include the separate <strong>$6,500–$15,000+ CPA auditor fee</strong>.</li>
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
  if (tool.id === 'helpscout-support' && seats > 50) return Math.max(seats, 10);
  return Math.max(seats, tool.seat_minimum || 1);
}}

function renderDirectory() {{
  const cat = document.getElementById('cat-filter').value;
  const seats = parseInt(document.getElementById('seat-slider').value, 10);
  const aiVol = parseInt(document.getElementById('ai-slider').value, 10);
  const mode = document.getElementById('billing-mode').value;
  document.getElementById('seat-val').textContent = seats;
  document.getElementById('ai-val').textContent = aiVol;

  const filtered = TOOLS.filter(t => cat === 'ALL' || t.category === cat);
  const rows = filtered.map(t => {{
    const effSeats = calcEffectiveSeats(t, seats);
    const unitRate = mode === 'annual' ? t.advertised_monthly_price_usd : t.monthly_billing_price_usd;
    let monthlySoftware = 0;
    if (t.id === 'hubspot-marketing-pro') {{
      monthlySoftware = unitRate + Math.max(0, seats - 3) * 45;
    }} else if (t.id === 'vanta-soc2' || t.id === 'drata-soc2' || t.id === 'jotform-hipaa') {{
      monthlySoftware = unitRate;
    }} else {{
      monthlySoftware = effSeats * unitRate;
    }}
    let aiMonthly = (t.ai_per_resolution_usd || 0) * aiVol;
    if (t.id === 'zendesk-suite-team') {{
      const incl = Math.min(seats * 5, 833);
      aiMonthly = Math.max(0, aiVol - incl) * (t.ai_per_resolution_usd || 1.5);
    }} else if (t.id === 'zendesk-suite-pro') {{
      const incl = Math.min(seats * 10, 833);
      aiMonthly = Math.max(0, aiVol - incl) * (t.ai_per_resolution_usd || 1.5);
    }}
    const year1Total = Math.round((monthlySoftware + aiMonthly) * 12 + (t.mandatory_onboarding_fee_usd || 0));
    return {{ tool: t, effSeats, unitRate, year1Total }};
  }});
  rows.sort((a, b) => a.year1Total - b.year1Total);
  document.getElementById('calc-tbody').innerHTML = rows.map(r => {{
    const t = r.tool;
    const aff = AFFILIATES[t.affiliate_slug] || {{ destination_url: '#' }};
    const badgeClass = t.trap_severity === 'high' ? 'badge-high' : (t.trap_severity === 'medium' ? 'badge-medium' : 'badge-low');
    const rateText = t.transaction_fee_display ? t.transaction_fee_display : `$${{r.unitRate}}/mo (${{r.effSeats}} billed seat${{r.effSeats === 1 ? '' : 's'}})`;
    const totalText = t.category === 'Payment Processors & MoR' ? 'Per-transaction' : `$${{r.year1Total.toLocaleString()}} / yr`;
    return `
      <tr>
        <td><strong>${{t.name}}</strong><div style="font-size:0.78rem; color:var(--muted);">${{t.category}}</div></td>
        <td style="font-family:var(--mono);">${{rateText}}</td>
        <td style="font-family:var(--mono);">${{t.mandatory_onboarding_fee_usd > 0 ? '$' + t.mandatory_onboarding_fee_usd.toLocaleString() : '$0'}}</td>
        <td><span class="badge ${{badgeClass}}">${{t.trap_badge}}</span><div style="font-size:0.8rem; color:var(--muted); margin-top:4px;">${{t.billing_lock_in_type}}</div></td>
        <td class="price-highlight">${{totalText}}</td>
        <td><a class="btn-cta" href="${{aff.destination_url}}" target="_blank" rel="nofollow sponsored">Check pricing &rarr;</a></td>
      </tr>
    `;
  }}).join('');
}}
['cat-filter', 'seat-slider', 'ai-slider', 'billing-mode'].forEach(id => document.getElementById(id).addEventListener('input', renderDirectory));
renderDirectory();
</script>
"""

home_faqs = [
    ("Which B2B SaaS tools charge mandatory onboarding fees in 2026?", "HubSpot charges mandatory one-time onboarding fees on its Professional and Enterprise tiers: $1,500 for Sales Hub Professional, $3,500 for Sales Hub Enterprise, $3,000 for Marketing Hub Professional, and $7,000 for Marketing Hub Enterprise (verified Oct 2026). Alternatives like Close CRM, Pipedrive, and Freshdesk charge $0 for onboarding."),
    ("How does Intercom's $0.99 per Fin AI resolution pricing work?", "Intercom charges a per-seat monthly fee ($29 Essential, $85 Advanced, or $132 Expert billed annually) plus $0.99 for every customer conversation resolved by its Fin AI agent (and $9.99 for sales qualification). If Fin AI resolves 2,000 tickets a month, it adds $1,980/month ($23,760/year) to your seat invoice."),
    ("Why does monday CRM cost more than advertised for 1 or 2 users?", "monday CRM enforces a 3-seat minimum and bills in fixed seat buckets (3, 5, 10, 15 seats). A solo user on the $17/seat/month Standard plan must pay for 3 seats ($51/month or $612/year). For 1–2 users, Pipedrive ($14–$34/seat) or Close CRM ($49/seat) is cheaper because they bill per exact seat."),
    ("What happens to subscriber card tokens if Paddle or Stripe terminates my account?", "With Stripe (2.9% + $0.30), you are the merchant and own the customer relationship, allowing PGP-encrypted card token exports unless terminated for fraud. With a Merchant of Record like Paddle (5% + $0.50), Paddle is the legal seller of record and owns the card vault; if Paddle terminates your account on a risk review, you cannot export card tokens and every subscriber must re-enter their payment details.")
]

render_page(
    "index.html",
    "SaaS True-Cost & Contract Trap Directory (2026): Calculate Hidden Onboarding Fees, Seat Minimums & AI Taxes",
    "SaaSBill independent B2B SaaS pricing calculator and contract audit directory. Compare true Year-1 costs including HubSpot's $1,500-$7,000 onboarding fees, Intercom's $0.99 AI resolution tax, and Stripe/Paddle payout holds.",
    "/",
    home_body,
    faqs=home_faqs,
    extra_schema={
        "@type": "Dataset",
        "name": "SaaSBill 2026 B2B SaaS True-Cost & Contract Trap Dataset",
        "description": "Verified 2026 pricing, mandatory onboarding fees, seat-bucket minimums, AI resolution rates, and payout reserve rules across 18 B2B SaaS and payment platforms.",
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
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">For a five-rep sales team, choosing <strong>Close CRM</strong> ($0 onboarding) or <strong>Pipedrive Professional</strong> ($49/seat/month, $0 onboarding) saves between <strong>$960 and $3,960 in Year 1</strong> compared with HubSpot Sales Hub Professional, with no 12-month lock-in required.</p>
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
  <div class="table-wrap">
    <table>
      <caption>Year-1 Out-of-Pocket Comparison: HubSpot vs. Close CRM vs. Pipedrive (USD, checked Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>CRM Platform</th>
          <th>Monthly Seat Cost</th>
          <th>Mandatory Onboarding</th>
          <th>Contract Terms</th>
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
  <div class="table-wrap">
    <table>
      <caption>HubSpot 2026 Seat Rates &amp; Mandatory Onboarding Fees (USD, checked Oct 25, 2026)</caption>
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
          <td><strong>Sales Hub Professional</strong></td>
          <td>$90 / seat / mo</td>
          <td>$100 / seat / mo</td>
          <td><span class="badge badge-high">$1,500 one-time</span></td>
          <td>$2,580 (1 seat) &middot; $6,900 (5 seats)</td>
        </tr>
        <tr>
          <td><strong>Sales Hub Enterprise</strong></td>
          <td>$150 / seat / mo</td>
          <td>$150 / seat / mo (Annual only)</td>
          <td><span class="badge badge-high">$3,500 one-time</span></td>
          <td>$5,300 (1 seat) &middot; $12,500 (5 seats)</td>
        </tr>
        <tr>
          <td><strong>Marketing Hub Professional</strong></td>
          <td>$800 / mo (3 core seats incl.)</td>
          <td>$890 / mo (12-mo commitment)</td>
          <td><span class="badge badge-high">$3,000 one-time</span></td>
          <td>$12,600 / yr (+$45/mo per extra seat)</td>
        </tr>
        <tr>
          <td><strong>Marketing Hub Enterprise</strong></td>
          <td>$3,600 / mo (5 core seats incl.)</td>
          <td>$3,600 / mo (Annual only)</td>
          <td><span class="badge badge-high">$7,000 one-time</span></td>
          <td>$50,200 / yr (+$75/mo per extra seat)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2>Three contract clauses to check before you sign</h2>
  <div class="evidence-box">
    <strong>1. "Monthly payment" is still a binding 12-month contract with auto-renewal</strong>
    <p style="margin-top:6px;">All HubSpot Professional and Enterprise agreements are annual commitments that auto-renew by default, even when paid in monthly installments. On day 1 of the auto-renewal window, you are liable for the full 12-month renewal balance unless you submitted non-renewal notice in advance.</p>
    <cite>Source: <a href="https://www.reddit.com/r/sales/comments/pyqpjq/hubspot_a_psa_contracts_and_review/" target="_blank" rel="noopener">r/sales &ndash; "Hubspot - a PSA (contracts!) and review"</a></cite>
  </div>
  <div class="evidence-box">
    <strong>2. Onboarding fees are often negotiable via partners</strong>
    <p style="margin-top:6px;">Sales Hub Pro requires a $1,500 onboarding fee ($3,500 on Enterprise), while Marketing Hub Pro requires $3,000 ($7,000 on Enterprise). SaaS account executives on <code>r/sales</code> note that onboarding fees are routinely used as a closing lever or waived when onboarding is scoped through a partner agency.</p>
    <cite>Source: <a href="https://www.reddit.com/r/sales/comments/1htoulv/onboarding_fee/" target="_blank" rel="noopener">r/sales &ndash; "Onboarding Fee" (Jan 2025)</a></cite>
  </div>
  <div class="evidence-box">
    <strong>3. You cannot remove unused seats mid-contract ($14,220 for 43 idle seats)</strong>
    <p style="margin-top:6px;">If reps leave mid-year, you cannot downgrade your committed seat count until renewal. A recent GTM software audit shared on X found $14,220/year spent on 43 seats that nobody had opened in 90 days.</p>
    <cite>Source: <a href="https://x.com/zandemha/status/2111438550247862312" target="_blank" rel="noopener">@zandemha on X (Oct 17, 2026)</a></cite>
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
  const hsYear1 = hsMonthly * 12 + hsOnboard;
  const closeMonthly = seats * 99;
  const closeYear1 = closeMonthly * 12;
  const pipeMonthly = seats * 49;
  const pipeYear1 = pipeMonthly * 12;
  document.getElementById('hs-tbody').innerHTML = `
    <tr>
      <td><strong>${hsName}</strong></td>
      <td style="font-family:var(--mono);">$${hsMonthly.toLocaleString()} / mo</td>
      <td><span class="badge badge-high">$${hsOnboard.toLocaleString()} mandatory</span></td>
      <td>12-month auto-renewing contract</td>
      <td class="price-highlight">$${hsYear1.toLocaleString()}</td>
      <td><a class="btn-secondary" href="https://www.hubspot.com/pricing" target="_blank" rel="nofollow sponsored">HubSpot pricing &rarr;</a></td>
    </tr>
    <tr>
      <td><strong>Close CRM (Growth / Pro)</strong><div style="font-size:0.78rem; color:var(--emerald);">No onboarding fee &middot; built-in calling &amp; SMS</div></td>
      <td style="font-family:var(--mono);">$${closeMonthly.toLocaleString()} / mo</td>
      <td><span class="badge badge-low">$0 onboarding</span></td>
      <td>Month-to-month or annual</td>
      <td class="price-highlight" style="color:var(--emerald);">$${closeYear1.toLocaleString()} (saves $${Math.max(0, hsYear1 - closeYear1).toLocaleString()})</td>
      <td><a class="btn-cta" href="https://close.com/pricing" target="_blank" rel="nofollow sponsored">Try Close free &rarr;</a></td>
    </tr>
    <tr>
      <td><strong>Pipedrive CRM (Professional)</strong><div style="font-size:0.78rem; color:var(--emerald);">No onboarding fee &middot; 1-seat minimum</div></td>
      <td style="font-family:var(--mono);">$${pipeMonthly.toLocaleString()} / mo</td>
      <td><span class="badge badge-low">$0 onboarding</span></td>
      <td>Cancel anytime on monthly plan</td>
      <td class="price-highlight" style="color:var(--emerald);">$${pipeYear1.toLocaleString()} (saves $${Math.max(0, hsYear1 - pipeYear1).toLocaleString()})</td>
      <td><a class="btn-cta" href="https://www.pipedrive.com/en/pricing" target="_blank" rel="nofollow sponsored">Try Pipedrive free &rarr;</a></td>
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
    "HubSpot Pricing & Contract Traps (2026): Mandatory Onboarding Fees ($1,500–$7,000), Auto-Renewal Rules & True Year-1 Cost",
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
  <p class="lead">Seat licenses start at $29 to $132 a month, but Fin AI adds $0.99 every time it resolves a ticket. Here is how fast the variable meter outgrows your seat bill—and how fixed-fee helpdesks compare.</p>
  <div class="geo-direct-answer">
    <p><strong>The short version:</strong> Intercom charges <strong>$0.99 per Fin AI resolution</strong> (including automated resolutions, procedure handoffs, and disqualifications, plus <strong>$9.99 per sales qualification</strong>) on top of agent seat licenses (<strong>$29/mo Essential, $85/mo Advanced, $132/mo Expert</strong> billed annually; $39/$99/$139 monthly). For a 5-agent team on Advanced ($425/mo) handling 3,000 tickets/month with a 50% AI resolution rate (1,500 resolutions), Fin AI adds <strong>$1,485/mo</strong>—bringing the total bill to <strong>$1,910/mo ($22,920/yr)</strong> vs. <strong>$390/mo ($4,680/yr)</strong> on Freshdesk Pro + Freddy AI Copilot.</p>
  </div>
</section>

<section class="calc-box">
  <h2 style="margin-top:0;">Calculate your monthly Intercom + Fin AI invoice</h2>
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">Every 1,000 tickets resolved by Fin AI adds $990/month ($11,880/year) on top of your agent seat subscriptions. Drag the sliders to see your monthly and annual total.</p>
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
  <div class="table-wrap">
    <table>
      <caption>Intercom + Fin AI ($0.99/Resolution) vs. Freshdesk Pro + Freddy AI Cost Breakdown (USD, checked Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>Helpdesk Solution</th>
          <th>Monthly Agent Seats</th>
          <th>Monthly AI Usage Charge</th>
          <th>Total Monthly Bill</th>
          <th>Annualized Cost</th>
          <th>Compare</th>
        </tr>
      </thead>
      <tbody id="ic-tbody"></tbody>
    </table>
  </div>
</section>

<section>
  <h2>Why support teams call $0.99/resolution an "AI tax"</h2>
  <p class="section-tldr">Across 215 Capterra and Reddit reviews analyzed in <code>r/SaaS</code>, customers praise Fin AI’s accuracy but point out a structural catch: the more time you spend improving your help center articles, the higher Fin’s resolution rate climbs—and the more Intercom charges you each month.</p>
  <div class="evidence-box">
    <strong>r/SaaS analysis of 215 Intercom reviews: "You can't predict your bill anymore"</strong>
    <p style="margin-top:6px;">Founders and support leads report that $0.99 per resolution turns seasonal ticket spikes and improved documentation into surprise monthly invoices, while migrating conversation history out of Intercom remains difficult.</p>
    <cite>Source: <a href="https://www.reddit.com/r/SaaS/comments/1p8c4cx/the_ai_tax_is_real_i_analyzed_215_recent_intercom/" target="_blank" rel="noopener">r/SaaS &ndash; "The 'AI Tax' is real. I analyzed 215 recent Intercom reviews and the data is brutal"</a></cite>
  </div>
  <div class="evidence-box">
    <strong>Pre-renewal outcome bill audits are now a paid consulting service</strong>
    <p style="margin-top:6px;">As Intercom, Zendesk, and Salesforce shift toward outcome-based AI billing, independent analysts on X now offer $990 pre-renewal contract audits just to verify what counts as a billable resolution or procedure handoff.</p>
    <cite>Sources: <a href="https://x.com/david_logger/status/2104329987549528429" target="_blank" rel="noopener">@david_logger on X (Sep 27, 2026)</a> &amp; <a href="https://x.com/elliwoodtong/status/2106554628124852415" target="_blank" rel="noopener">@elliwoodtong on X (Oct 4, 2026)</a></cite>
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
  const fdSeatCost = seats * 49;
  const fdAiCost = seats * 29;
  const fdTotalMo = fdSeatCost + fdAiCost;
  const fdYear = fdTotalMo * 12;
  document.getElementById('ic-tbody').innerHTML = `
    <tr>
      <td><strong>Intercom + Fin AI (${resolvedTickets.toLocaleString()} resolutions/mo)</strong></td>
      <td style="font-family:var(--mono);">$${icSeatCost.toLocaleString()} / mo</td>
      <td><span class="badge badge-high">$${icAiCost.toLocaleString()} / mo ($0.99 &times; ${resolvedTickets.toLocaleString()})</span></td>
      <td class="price-highlight">$${icTotalMo.toLocaleString()} / mo</td>
      <td class="price-highlight">$${icYear.toLocaleString()} / yr</td>
      <td><a class="btn-secondary" href="https://www.intercom.com/pricing" target="_blank" rel="nofollow">Intercom pricing &rarr;</a></td>
    </tr>
    <tr>
      <td><strong>Freshdesk Pro + Freddy AI (Freshworks)</strong><div style="font-size:0.78rem; color:var(--emerald);">Predictable per-agent alternative</div></td>
      <td style="font-family:var(--mono);">$${fdSeatCost.toLocaleString()} / mo</td>
      <td><span class="badge badge-low">$${fdAiCost.toLocaleString()} / mo ($29/agent add-on)</span></td>
      <td class="price-highlight" style="color:var(--emerald);">$${fdTotalMo.toLocaleString()} / mo</td>
      <td class="price-highlight" style="color:var(--emerald);">$${fdYear.toLocaleString()} / yr (saves $${Math.max(0, icYear - fdYear).toLocaleString()}/yr)</td>
      <td><a class="btn-cta" href="https://www.freshworks.com/freshdesk/pricing/" target="_blank" rel="nofollow sponsored">Try Freshdesk free &rarr;</a></td>
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
    ("What is the most predictable alternative to Intercom's $0.99 per-resolution pricing?", "Freshdesk (by Freshworks) offers predictable per-agent pricing ($15–$79/seat/month) with optional Freddy AI Copilot at $29/agent/month, avoiding uncapped $0.99 per-ticket outcome spikes.")
]

render_page(
    "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
    "Intercom Pricing & Fin AI Resolution Tax Calculator (2026): How $0.99/Resolution Impacts Your Bill vs. Freshdesk & Zendesk",
    "Calculate your monthly and annual Intercom Fin AI bill at $0.99 per resolution across Essential ($29), Advanced ($85), and Expert ($132) tiers, and compare against Freshdesk.",
    "/pricing/intercom-fin-ai-resolution-cost-calculator/",
    p2_body,
    faqs=p2_faqs
)

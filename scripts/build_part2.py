import os
import json
from layout import render_page, load_data, PUBLIC_DIR, SITE_ORIGIN

TOOLS, AFFILIATES = load_data()

# ---------------------------------------------------------
# Page 3: Stripe, Shopify Payments & Paddle Payout Holds
# ---------------------------------------------------------
p3_body = """
<section class="hero">
  <h1>What happens when Stripe, Shopify, or Paddle freezes your payouts.</h1>
  <p class="lead">A 25% rolling reserve or 180-day hold can starve a healthy business overnight—and if a Merchant of Record drops you, you cannot take your subscribers’ card tokens with you. Here is how to protect your cashflow.</p>
  <div class="geo-direct-answer">
    <p><strong>The short version:</strong> Standard payment processors (<strong>Stripe, Shopify Payments, PayPal</strong>) can impose a <strong>25% rolling reserve for 90–180 days</strong> or a <strong>120–180 day payout hold</strong> if your dispute rate crosses ~0.5%–0.75% or volume spikes unexpectedly. With Stripe, however, you own the customer relationship and can export PGP-encrypted card tokens. With a Merchant of Record (<strong>Paddle, 5% + $0.50</strong>), Paddle is the legal seller of record and owns the card vault; if Paddle terminates your account on a risk review, <strong>card tokens cannot be exported</strong>. To protect cashflow, pair <strong>Chargeflow</strong> (keeps dispute rate &lt;0.5%) with a multi-processor failover rail like <strong>Whop Payments (2.7% + $0.30)</strong>.</p>
  </div>
</section>

<section class="calc-box">
  <h2 style="margin-top:0;">Simulate a rolling reserve &amp; capital loan cashflow squeeze</h2>
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">On $50,000/month in gross volume, a 25% rolling reserve combined with a 15% Stripe Capital or Shopify Capital repayment deduction locks up $21,450/month (42.9% of your gross revenue) before operating expenses.</p>
  <div class="calc-grid">
    <div class="control-group">
      <label for="gm-rev">Monthly gross processing volume: $<span class="val-pill" id="gm-rev-val">50,000</span></label>
      <input type="range" id="gm-rev" min="5000" max="500000" step="5000" value="50000" />
    </div>
    <div class="control-group">
      <label for="gm-res">Processor rolling reserve: <span class="val-pill" id="gm-res-val">25</span>%</label>
      <input type="range" id="gm-res" min="0" max="50" step="5" value="25" />
    </div>
    <div class="control-group">
      <label for="gm-cap">Capital loan repayment deduction: <span class="val-pill" id="gm-cap-val">15</span>%</label>
      <input type="range" id="gm-cap" min="0" max="30" step="2" value="15" />
    </div>
  </div>
  <div class="card-grid" id="reserve-output"></div>
</section>

<section>
  <h2>Token portability &amp; reserve comparison: Processor vs. Merchant of Record</h2>
  <p class="section-tldr">Never rely on a single Merchant of Record without keeping your own entitlement database. Pairing a multi-processor orchestration layer (Whop) with automated pre-dispute alerts (Chargeflow) prevents single-point-of-failure shutdowns.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>2026 Payment Processor &amp; Merchant of Record (MoR) Reserve &amp; Token Ownership Matrix (verified Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>Provider</th>
          <th>Model &amp; Base Rate</th>
          <th>Who Owns Subscriber Card Tokens?</th>
          <th>Hold / Reserve Policy on Risk Flags</th>
          <th>Recommended Role</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td data-label="Provider">
            <strong>Whop Payments &amp; Orchestration</strong>
            <span class="status-pill status-verified">Verified</span>
            <div class="source-inline">Source: <a href="https://whop.com/sell" target="_blank" rel="noopener">Whop Payments &nearr;</a></div>
          </td>
          <td data-label="Model &amp; Base Rate" style="font-family:var(--mono);">2.7% + $0.30 domestic</td>
          <td data-label="Token Ownership"><span class="badge badge-low">White-glove migration</span><div style="font-size:0.8rem; color:var(--muted); margin-top:4px;">Supports switching from Paddle, Lemon Squeezy, Shopify &amp; Gumroad</div></td>
          <td data-label="Hold / Reserve Policy">Multi-processor waterfall routes around single-acquirer declines (~6% revenue lift); KYB deferred to $5k volume</td>
          <td data-label="Action"><a class="btn-cta" href="https://whop.com/sell" target="_blank" rel="nofollow sponsored">Add Whop failover &rarr;</a><span class="partner-tag">Partner link</span></td>
        </tr>
        <tr>
          <td data-label="Provider">
            <strong>Chargeflow (Dispute Shield)</strong>
            <span class="status-pill status-verified">Verified</span>
            <div class="source-inline">Source: <a href="https://www.chargeflow.io/pricing" target="_blank" rel="noopener">Chargeflow pricing &nearr;</a></div>
          </td>
          <td data-label="Model &amp; Base Rate" style="font-family:var(--mono);">Performance-based ($0 setup)</td>
          <td data-label="Token Ownership"><span class="badge badge-low">Plugs into Stripe / Shopify</span></td>
          <td data-label="Hold / Reserve Policy">Prevents 25% reserves &amp; 180-day freezes by intercepting pre-disputes to keep your chargeback rate under 0.5%</td>
          <td data-label="Action"><a class="btn-cta" href="https://www.chargeflow.io/pricing" target="_blank" rel="nofollow sponsored">Install Chargeflow &rarr;</a><span class="partner-tag">Partner link</span></td>
        </tr>
        <tr>
          <td data-label="Provider">
            <strong>Paddle (Merchant of Record)</strong>
            <span class="status-pill status-verified">Verified</span>
            <div class="source-inline">Source: <a href="https://www.paddle.com/pricing" target="_blank" rel="noopener">Paddle pricing &amp; terms &nearr;</a></div>
          </td>
          <td data-label="Model &amp; Base Rate" style="font-family:var(--mono);">5.0% + $0.50</td>
          <td data-label="Token Ownership"><span class="badge badge-high">Locked by Paddle</span><div style="font-size:0.8rem; color:var(--muted); margin-top:4px;">Paddle is seller of record; tokens cannot be exported if terminated</div></td>
          <td data-label="Hold / Reserve Policy">Can terminate accounts on internal risk review and hold unreleased payouts without appeal</td>
          <td data-label="Action"><a class="btn-secondary" href="https://www.paddle.com/pricing" target="_blank" rel="nofollow noopener">Paddle pricing &rarr;</a><span class="partner-tag">Direct vendor link</span></td>
        </tr>
        <tr>
          <td data-label="Provider">
            <strong>Lemon Squeezy (MoR by Stripe)</strong>
            <span class="status-pill status-verified">Verified</span>
            <div class="source-inline">Source: <a href="https://www.lemonsqueezy.com/pricing" target="_blank" rel="noopener">Lemon Squeezy pricing &nearr;</a></div>
          </td>
          <td data-label="Model &amp; Base Rate" style="font-family:var(--mono);">5.0% + $0.50 (+0.5% subs)</td>
          <td data-label="Token Ownership"><span class="badge badge-medium">MoR vault (Stripe-backed)</span></td>
          <td data-label="Hold / Reserve Policy">Subject to Stripe's prohibited business list and automated risk triggers</td>
          <td data-label="Action"><a class="btn-secondary" href="https://www.lemonsqueezy.com/pricing" target="_blank" rel="nofollow sponsored">Lemon Squeezy &rarr;</a><span class="partner-tag">Partner link</span></td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2>What contract terms &amp; reserve docs say when an account is frozen</h2>
  <div class="evidence-box">
    <strong>Why a Merchant of Record termination locks card tokens</strong>
    <p style="margin-top:6px;">With a Merchant of Record (Paddle or Lemon Squeezy), the MoR is the legal seller of record. Their entity appears on the customer’s bank statement, holds the tax registrations, and owns the payment vault—meaning card tokens cannot be exported to your own Stripe account if the MoR terminates your agreement.</p>
    <cite>Source: <a href="https://www.paddle.com/legal/terms" target="_blank" rel="noopener">Paddle Legal Terms &amp; Merchant of Record Structure</a></cite>
  </div>
  <div class="evidence-box">
    <strong>Stripe rolling reserves &amp; card-network dispute thresholds</strong>
    <p style="margin-top:6px;">Stripe’s underwriting engine can apply a rolling reserve (holding a percentage of each charge for 30–180 days) or a fixed reserve when dispute rates approach Visa/Mastercard monitoring thresholds (~0.5%–0.75%) or when delivery windows are extended.</p>
    <cite>Source: <a href="https://docs.stripe.com/reserves" target="_blank" rel="noopener">Stripe Documentation &ndash; How Rolling and Fixed Reserves Work</a></cite>
  </div>
</section>

<script>
function updateReserveSim() {
  const rev = parseInt(document.getElementById('gm-rev').value, 10);
  const resPct = parseInt(document.getElementById('gm-res').value, 10);
  const capPct = parseInt(document.getElementById('gm-cap').value, 10);
  document.getElementById('gm-rev-val').textContent = rev.toLocaleString();
  document.getElementById('gm-res-val').textContent = resPct;
  document.getElementById('gm-cap-val').textContent = capPct;
  const procFee = Math.round(rev * 0.029);
  const frozenMo = Math.round(rev * (resPct / 100));
  const loanDed = Math.round(rev * (capPct / 100));
  const netCash = Math.max(0, rev - procFee - frozenMo - loanDed);
  const frozen90Days = frozenMo * 3;
  document.getElementById('reserve-output').innerHTML = `
    <div class="card">
      <span class="badge badge-high">Cash held in rolling reserve</span>
      <h3 class="price-highlight" style="margin-top:10px; font-size:1.45rem;">$${frozenMo.toLocaleString()} / mo</h3>
      <p>$${frozen90Days.toLocaleString()} cumulative cash locked over a 90-day reserve window.</p>
    </div>
    <div class="card">
      <span class="badge badge-medium">Total monthly holdback (${resPct + capPct}% + fees)</span>
      <h3 class="price-highlight" style="margin-top:10px; font-size:1.45rem;">-$${(procFee + frozenMo + loanDed).toLocaleString()} / mo</h3>
      <p>Processing fees ($${procFee.toLocaleString()}), reserve hold ($${frozenMo.toLocaleString()}), and loan deduction ($${loanDed.toLocaleString()}).</p>
    </div>
    <div class="card">
      <span class="badge badge-low">Net payout reaching your bank</span>
      <h3 class="price-highlight" style="margin-top:10px; font-size:1.45rem; color:var(--emerald);">$${netCash.toLocaleString()} / mo</h3>
      <p>Keep a secondary checkout rail (<strong>Whop</strong>) ready and use <strong>Chargeflow</strong> to keep disputes under 0.5%.</p>
    </div>
  `;
}
['gm-rev', 'gm-res', 'gm-cap'].forEach(id => document.getElementById(id).addEventListener('input', updateReserveSim));
updateReserveSim();
</script>
"""

p3_faqs = [
    ("How long can Stripe, PayPal, or Shopify Payments hold funds after an account freeze?", "Stripe, PayPal, and Shopify Payments typically hold funds for 120 to 180 days following an account termination or permanent limitation to cover potential customer chargeback windows, or impose a 25% rolling reserve for 90 to 180 days."),
    ("Can you export subscriber credit card tokens if Paddle terminates your account?", "No. Because Paddle operates as a Merchant of Record (MoR), Paddle is the legal seller of record and owns the card vault. If Paddle terminates your account following a risk review, you cannot re-tokenize or export subscriber cards—every customer must manually re-enter their payment details on your new processor."),
    ("How do you prevent Stripe or Shopify Payments from placing a 25% rolling reserve?", "Keep your dispute ratio strictly below 0.5% by installing an automated pre-dispute and chargeback prevention tool like Chargeflow, and maintain a secondary multi-processor orchestration checkout like Whop (2.7% + $0.30) for immediate failover.")
]

render_page(
    "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html",
    "Stripe, Shopify & Paddle Frozen Funds – saasbill.io",
    "Compare Stripe, Shopify Payments, and Paddle payout freeze policies, card token portability rules, and backup payment orchestration with Whop and Chargeflow.",
    "/exit/stripe-shopify-paddle-frozen-funds-alternatives/",
    p3_body,
    faqs=p3_faqs
)

# ---------------------------------------------------------
# Page 4: Monday CRM vs Pipedrive vs HubSpot (3-Seat Minimum Math)
# ---------------------------------------------------------
p4_body = """
<section class="hero">
  <h1>Why a "$12/seat" CRM costs $36 a month for a solo founder.</h1>
  <p class="lead">monday CRM bills in fixed buckets starting at three seats, while Pipedrive and Close bill per actual user. Use the calculator below to see where the math flips.</p>
  <div class="geo-direct-answer">
    <p><strong>The short version:</strong> For <strong>1 user</strong>, <strong>Pipedrive</strong> ($14/mo Basic or $34/mo Growth) is up to <strong>60% cheaper</strong> than <strong>monday CRM</strong> because monday CRM enforces a <strong>3-seat minimum</strong> ($36/mo Basic [$12/seat annual, $18/seat monthly] or $51/mo Standard [$17/seat annual, $25/seat monthly] minimum). For <strong>2 users</strong>, monday CRM still bills for 3 seats ($25.50/user/mo effective rate on Standard). At <strong>exactly 3, 5, or 10 users</strong>, however, monday CRM becomes the lowest-cost full-featured CRM at $51/mo (3 users) vs. $102/mo on Pipedrive Growth and $270/mo (+ $1,500 onboarding) on HubSpot Sales Pro.</p>
  </div>
</section>

<section class="calc-box">
  <h2 style="margin-top:0;">Compare seat-bucket pricing for 1 to 15 users</h2>
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">monday CRM sells seats in fixed buckets of <strong>3, 5, 10, and 15 seats</strong>. Adding a 4th user jumps your bill from 3 seats to 5 seats (+67%); adding a 6th user jumps your bill from 5 seats to 10 seats (+100%).</p>
  <div class="calc-grid">
    <div class="control-group">
      <label for="sm-users">Actual team members needing CRM access: <span class="val-pill" id="sm-users-val">1</span> user(s)</label>
      <input type="range" id="sm-users" min="1" max="15" value="1" />
    </div>
    <div class="control-group">
      <label for="sm-tier">Plan tier comparison</label>
      <select id="sm-tier">
        <option value="entry">Entry / Basic tier ($12/seat annual · $18/seat monthly on monday CRM)</option>
        <option value="standard" selected>Standard / Growth tier ($17/seat annual · $25/seat monthly on monday CRM)</option>
      </select>
    </div>
  </div>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>Effective Per-User CRM Cost After Seat Minimums &amp; Seat Buckets (USD, verified Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>CRM Platform</th>
          <th>Advertised Price / Seat</th>
          <th>Billed Seats</th>
          <th>Effective Cost Per Actual User</th>
          <th>Total Annual Bill (USD)</th>
          <th>Compare</th>
        </tr>
      </thead>
      <tbody id="sm-tbody"></tbody>
    </table>
  </div>
</section>

<section>
  <h2>When to pick Pipedrive vs. monday CRM</h2>
  <p class="section-tldr">Choose <strong>Pipedrive</strong> or <strong>Close CRM</strong> when you have 1, 2, 4, 6, 7, 8, or 11–12 users—sizes where monday CRM forces you to pay for unused seats. Choose <strong>monday CRM</strong> when your headcount lands cleanly on 3, 5, 10, or 15 users.</p>
  <div class="evidence-box">
    <strong>Why monday CRM’s 3-seat minimum and 5-seat increments matter</strong>
    <p style="margin-top:6px;">monday.com’s pricing selector starts at 3 seats and steps in fixed increments (3, 5, 10, 15, 20, 25...). Teams with 1, 2, 4, or 6–9 users pay for unallocated seats in their bucket.</p>
    <cite>Source: <a href="https://monday.com/pricing" target="_blank" rel="noopener">monday.com Official Pricing Page &amp; Seat Selector</a></cite>
  </div>
</section>

<script>
function getMondayBucket(u) {
  if (u <= 3) return 3;
  if (u <= 5) return 5;
  if (u <= 10) return 10;
  return 15;
}
function updateSmCalc() {
  const u = parseInt(document.getElementById('sm-users').value, 10);
  const tier = document.getElementById('sm-tier').value;
  document.getElementById('sm-users-val').textContent = u;
  const monRate = tier === 'entry' ? 12 : 17;
  const pipeRate = tier === 'entry' ? 14 : 34;
  const hsRate = tier === 'entry' ? 15 : 90;
  const hsOnboard = tier === 'entry' ? 0 : 1500;
  const monSeats = getMondayBucket(u);
  const monMo = monSeats * monRate;
  const pipeMo = u * pipeRate;
  const hsMo = u * hsRate;
  document.getElementById('sm-tbody').innerHTML = `
    <tr>
      <td data-label="CRM Platform"><strong>Pipedrive CRM</strong> <span class="status-pill status-verified">Verified</span><div class="source-inline">Source: <a href="https://www.pipedrive.com/en/pricing" target="_blank" rel="noopener">Pipedrive pricing &nearr;</a></div></td>
      <td data-label="Advertised Price" style="font-family:var(--mono);">$${pipeRate}/seat/mo</td>
      <td data-label="Billed Seats"><span class="badge badge-low">${u} seat(s) (exact 1:1)</span></td>
      <td data-label="Effective Cost / User" style="font-family:var(--mono);">$${pipeRate.toFixed(2)} / user / mo</td>
      <td data-label="Total Annual Bill" class="price-highlight">$${(pipeMo * 12).toLocaleString()} / yr</td>
      <td data-label="Compare"><a class="btn-cta" href="https://www.pipedrive.com/en/pricing" target="_blank" rel="nofollow sponsored">${u <= 2 ? 'Best for 1–2 users &rarr;' : 'Try Pipedrive &rarr;'}</a><span class="partner-tag">Partner link</span></td>
    </tr>
    <tr>
      <td data-label="CRM Platform"><strong>monday CRM</strong> <span class="status-pill status-verified">Verified</span><div class="source-inline">Source: <a href="https://monday.com/pricing" target="_blank" rel="noopener">monday.com pricing &nearr;</a></div></td>
      <td data-label="Advertised Price" style="font-family:var(--mono);">$${monRate}/seat/mo</td>
      <td data-label="Billed Seats"><span class="badge ${monSeats > u ? 'badge-medium' : 'badge-low'}">${monSeats} seats (${monSeats - u} unused)</span></td>
      <td data-label="Effective Cost / User" style="font-family:var(--mono);">$${(monMo / u).toFixed(2)} / user / mo</td>
      <td data-label="Total Annual Bill" class="price-highlight">$${(monMo * 12).toLocaleString()} / yr</td>
      <td data-label="Compare"><a class="btn-cta" href="https://monday.com/pricing" target="_blank" rel="nofollow sponsored">${u >= 3 ? 'Best value at 3+ users &rarr;' : 'See monday CRM &rarr;'}</a><span class="partner-tag">Partner link</span></td>
    </tr>
    <tr>
      <td data-label="CRM Platform"><strong>HubSpot Sales Hub (${tier === 'entry' ? 'Starter' : 'Professional'})</strong> <span class="status-pill status-verified">Verified</span><div class="source-inline">Source: <a href="https://www.hubspot.com/pricing/sales" target="_blank" rel="noopener">HubSpot pricing &nearr;</a></div></td>
      <td data-label="Advertised Price" style="font-family:var(--mono);">$${hsRate}/seat/mo</td>
      <td data-label="Billed Seats"><span class="badge ${hsOnboard > 0 ? 'badge-high' : 'badge-low'}">${u} seat(s) ${hsOnboard > 0 ? '+ $1,500 onboarding' : ''}</span></td>
      <td data-label="Effective Cost / User" style="font-family:var(--mono);">$${((hsMo + hsOnboard / 12) / u).toFixed(2)} / user / mo</td>
      <td data-label="Total Annual Bill" class="price-highlight">$${(hsMo * 12 + hsOnboard).toLocaleString()} / yr</td>
      <td data-label="Compare"><a class="btn-secondary" href="https://www.hubspot.com/pricing" target="_blank" rel="nofollow sponsored">HubSpot pricing &rarr;</a><span class="partner-tag">Partner link</span></td>
    </tr>
  `;
}
document.getElementById('sm-users').addEventListener('input', updateSmCalc);
document.getElementById('sm-tier').addEventListener('input', updateSmCalc);
updateSmCalc();
</script>
"""

p4_faqs = [
    ("Can you buy 1 seat of monday CRM in 2026?", "No. monday CRM enforces a mandatory 3-seat minimum on all paid plans. If you are a solo user on the $12/seat Basic plan ($18/seat billed monthly) or $17/seat Standard plan ($25/seat billed monthly), you must pay for 3 seats ($36/month annual or $54/month monthly on Basic; $51/month annual or $75/month monthly on Standard)."),
    ("How do monday CRM seat buckets work when adding a 4th or 6th user?", "monday CRM bills in fixed seat buckets of 3, 5, 10, and 15 seats. If you have 4 active users, you must pay for the 5-seat bucket; if you have 6 active users, you must pay for the 10-seat bucket."),
    ("Which CRM is best for a 1-person or 2-person sales team?", "Pipedrive ($14–$34/user/month) and Close CRM Essentials ($35/user/month billed annually, $49/user/month billed monthly; or Solo at $9/month for 1 user) bill strictly 1:1 per active user with $0 mandatory onboarding fees, making them significantly more cost-effective than monday CRM or HubSpot Professional for 1–2 users.")
]

render_page(
    "compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html",
    "monday CRM vs Pipedrive vs HubSpot – saasbill.io",
    "Compare Monday CRM's 3-seat minimum and seat-bucket pricing against Pipedrive and HubSpot for 1, 2, 3, 5, and 10 users.",
    "/compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/",
    p4_body,
    faqs=p4_faqs
)

# ---------------------------------------------------------
# Page 5: HIPAA BAA & SOC 2 Pricing Tiers Matrix
# ---------------------------------------------------------
p5_body = """
<section class="hero">
  <h1>Which software plans actually sign a HIPAA BAA (and what SOC 2 really costs).</h1>
  <p class="lead">Most vendors lock HIPAA Business Associate Agreements and SAML SSO behind $20,000+ Enterprise contracts. A handful include them on self-serve plans—and Vanta or Drata quotes rarely include your CPA auditor bill.</p>
  <div class="geo-direct-answer">
    <p><strong>The short version:</strong> Self-serve HIPAA Business Associate Agreements (BAAs) are available on <strong>Jotform Gold ($99/mo billed annually, $129/mo monthly, 1-user account)</strong> and <strong>1Password Business ($8.99/user/mo billed annually [$107.88/yr], which also includes SAML SSO with no Enterprise markup)</strong>, whereas HubSpot ($150/seat + $3,500 onboarding), Zendesk ($115/agent Suite Pro), and Intercom ($132/seat Expert) require upper-tier plans. For SOC 2 Type II compliance automation, <strong>Vanta and Drata</strong> do not publish public self-serve prices—custom list quotes typically start around <strong>$9,000–$15,000+/yr</strong> (frequently negotiated down by <strong>30%–50%</strong>), while <strong>Comp AI ($2,400–$12,000/yr)</strong> and <strong>Openlane (~$5,400/yr)</strong> cost less—plus a mandatory <strong>$6,500–$15,000+ external CPA auditor fee</strong> billed separately.</p>
  </div>
</section>

<section class="calc-box">
  <h2 style="margin-top:0;">Estimate your real Year-1 SOC 2 budget (platform + CPA auditor)</h2>
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">Because Vanta, Drata, and CPA audit firms use custom quotes rather than public price sheets, all figures in this estimator are labeled <span class="status-pill status-estimated">Estimated (Benchmark)</span> based on buyer contract ranges. Adjust headcount, frameworks, and your negotiated discount below.</p>
  <div class="calc-grid">
    <div class="control-group">
      <label for="soc-emp">Company headcount: <span class="val-pill" id="soc-emp-val">20</span> employees</label>
      <input type="range" id="soc-emp" min="5" max="150" step="5" value="20" />
    </div>
    <div class="control-group">
      <label for="soc-fw">Frameworks needed</label>
      <select id="soc-fw">
        <option value="1">SOC 2 Type II only</option>
        <option value="1.45" selected>SOC 2 Type II + HIPAA</option>
        <option value="1.85">SOC 2 + HIPAA + GDPR / ISO 27001</option>
      </select>
    </div>
    <div class="control-group">
      <label for="soc-disc">Negotiated platform discount (up to 50% reported): <span class="val-pill" id="soc-disc-val">35</span>%</label>
      <input type="range" id="soc-disc" min="0" max="50" step="5" value="35" />
    </div>
  </div>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>2026 SOC 2 Type II &amp; HIPAA Automation Total Cost Estimator: Vanta vs. Drata vs. Comp AI (USD, benchmarked Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>Compliance Platform</th>
          <th>Est. List Platform Quote</th>
          <th>Negotiated Platform Cost</th>
          <th>Est. External CPA Auditor Fee</th>
          <th>Total Year-1 SOC 2 Cost</th>
          <th>Compare</th>
        </tr>
      </thead>
      <tbody id="soc-tbody"></tbody>
    </table>
  </div>
</section>

<section>
  <h2>Which SaaS tiers sign a HIPAA BAA or include SAML SSO</h2>
  <p class="section-tldr">Before signing a $25,000+ Enterprise contract solely to unlock a HIPAA BAA or Okta SAML Single Sign-On, check the minimum qualifying edition for each vendor below.</p>
  <div class="table-wrap mobile-cards">
    <table>
      <caption>Minimum Pricing Tier Required for Signed HIPAA BAA &amp; SAML SSO (verified Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>Vendor &amp; Category</th>
          <th>Lowest Tier That Signs a HIPAA BAA</th>
          <th>Minimum SAML SSO Tier</th>
          <th>SOC 2 Type II Status</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td data-label="Vendor">
            <strong>Jotform (Forms &amp; Intake)</strong>
            <span class="status-pill status-verified">Verified</span>
            <div class="source-inline">Source: <a href="https://www.jotform.com/hipaa/pricing/" target="_blank" rel="noopener">Jotform HIPAA pricing &nearr;</a></div>
          </td>
          <td data-label="Lowest HIPAA BAA Tier"><span class="badge badge-low">Gold ($99/mo annual &middot; $129/mo monthly &middot; 1 user)</span></td>
          <td data-label="Min SAML SSO Tier">Enterprise (Multi-user SAML)</td>
          <td data-label="SOC 2 Status">SOC 2 Type II &amp; HIPAA</td>
          <td data-label="Details"><a class="btn-cta" href="https://www.jotform.com/hipaa/pricing/" target="_blank" rel="nofollow sponsored">Jotform HIPAA &rarr;</a><span class="partner-tag">Partner link</span></td>
        </tr>
        <tr>
          <td data-label="Vendor">
            <strong>1Password (Access &amp; Secrets)</strong>
            <span class="status-pill status-verified">Verified</span>
            <div class="source-inline">Source: <a href="https://1password.com/pricing/business" target="_blank" rel="noopener">1Password Business pricing &nearr;</a></div>
          </td>
          <td data-label="Lowest HIPAA BAA Tier"><span class="badge badge-low">Business ($8.99/user/mo annual)</span></td>
          <td data-label="Min SAML SSO Tier"><span class="badge badge-low">Business ($8.99/user/mo annual &middot; no SSO tax)</span></td>
          <td data-label="SOC 2 Status">SOC 2 Type II &amp; ISO 27001</td>
          <td data-label="Details"><a class="btn-cta" href="https://1password.com/pricing/business" target="_blank" rel="nofollow sponsored">1Password Business &rarr;</a><span class="partner-tag">Partner link</span></td>
        </tr>
        <tr>
          <td data-label="Vendor">
            <strong>Zendesk (Customer Support)</strong>
            <span class="status-pill status-verified">Verified</span>
            <div class="source-inline">Source: <a href="https://www.zendesk.com/pricing/" target="_blank" rel="noopener">Zendesk pricing &nearr;</a></div>
          </td>
          <td data-label="Lowest HIPAA BAA Tier"><span class="badge badge-medium">Suite Professional ($115/agent/mo)</span></td>
          <td data-label="Min SAML SSO Tier">Listed across Suite plans</td>
          <td data-label="SOC 2 Status">SOC 2 Type II</td>
          <td data-label="Details"><a class="btn-secondary" href="../pricing/zendesk-ai-resolution-and-automated-outcome-cost/">Zendesk audit &rarr;</a></td>
        </tr>
        <tr>
          <td data-label="Vendor">
            <strong>Help Scout (Customer Support)</strong>
            <span class="status-pill status-verified">Verified</span>
            <div class="source-inline">Source: <a href="https://www.helpscout.com/pricing/" target="_blank" rel="noopener">Help Scout pricing &nearr;</a></div>
          </td>
          <td data-label="Lowest HIPAA BAA Tier"><span class="badge badge-medium">Pro ($75/user/mo, 10-user min)</span></td>
          <td data-label="Min SAML SSO Tier">Pro or Plus add-on</td>
          <td data-label="SOC 2 Status">SOC 2 Type II &amp; HIPAA</td>
          <td data-label="Details"><a class="btn-cta" href="https://www.helpscout.com/pricing/" target="_blank" rel="nofollow sponsored">Help Scout &rarr;</a><span class="partner-tag">Partner link</span></td>
        </tr>
        <tr>
          <td data-label="Vendor">
            <strong>HubSpot (CRM &amp; Marketing)</strong>
            <span class="status-pill status-verified">Verified</span>
            <div class="source-inline">Source: <a href="https://www.hubspot.com/pricing/sales" target="_blank" rel="noopener">HubSpot pricing &nearr;</a></div>
          </td>
          <td data-label="Lowest HIPAA BAA Tier"><span class="badge badge-high">Enterprise ($150/seat + $3,500 onboarding)</span></td>
          <td data-label="Min SAML SSO Tier">Enterprise tier only</td>
          <td data-label="SOC 2 Status">SOC 2 Type II</td>
          <td data-label="Details"><a class="btn-secondary" href="../pricing/hubspot-true-cost-and-onboarding-fees/">HubSpot audit &rarr;</a></td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2>What IT buyers need to know about compliance quotes</h2>
  <div class="evidence-box">
    <strong>Why SOC 2 automation requires two separate budgets</strong>
    <p style="margin-top:6px;">Compliance automation software (Vanta, Drata, Comp AI) continuously monitors your cloud controls and collects evidence, but AICPA rules require an independent licensed CPA firm to perform the audit and issue the official SOC 2 Type I or Type II report ($6,500–$15,000+ billed separately).</p>
    <cite>Sources: <a href="https://www.vanta.com/pricing" target="_blank" rel="noopener">Vanta Plans &amp; Audit Partner Model</a> &amp; <a href="https://drata.com/" target="_blank" rel="noopener">Drata Compliance Automation</a></cite>
  </div>
</section>

<script>
function updateSocCalc() {
  const emp = parseInt(document.getElementById('soc-emp').value, 10);
  const fwMult = parseFloat(document.getElementById('soc-fw').value);
  const disc = parseInt(document.getElementById('soc-disc').value, 10) / 100;
  document.getElementById('soc-emp-val').textContent = emp;
  document.getElementById('soc-disc-val').textContent = Math.round(disc * 100);
  const sizeMult = emp <= 25 ? 1.0 : (emp <= 60 ? 1.45 : 2.1);
  const auditorFee = Math.round(6500 * sizeMult * (fwMult > 1 ? 1.25 : 1.0));
  const vantaList = Math.round(10000 * sizeMult * fwMult);
  const vantaNeg = Math.round(vantaList * (1 - disc));
  const drataList = Math.round(9000 * sizeMult * fwMult);
  const drataNeg = Math.round(drataList * (1 - disc));
  const compAiCost = Math.round(3600 * sizeMult * (fwMult > 1 ? 1.2 : 1.0));
  document.getElementById('soc-tbody').innerHTML = `
    <tr>
      <td data-label="Compliance Platform"><strong>Vanta</strong> <span class="status-pill status-estimated">Estimated (Benchmark)</span><div class="source-inline">Source: <a href="https://www.vanta.com/pricing" target="_blank" rel="noopener">Vanta packages &nearr;</a></div></td>
      <td data-label="Est. List Quote" style="font-family:var(--mono);">$${vantaList.toLocaleString()}/yr</td>
      <td data-label="Negotiated Platform Cost" style="font-family:var(--mono); color:var(--emerald);">$${vantaNeg.toLocaleString()}/yr</td>
      <td data-label="Est. CPA Auditor Fee" style="font-family:var(--mono);">+$${auditorFee.toLocaleString()}</td>
      <td data-label="Total Year-1 SOC 2 Cost" class="price-highlight">$${(vantaNeg + auditorFee).toLocaleString()} / yr</td>
      <td data-label="Compare"><a class="btn-cta" href="https://www.vanta.com/pricing" target="_blank" rel="nofollow sponsored">Request Vanta quote &rarr;</a><span class="partner-tag">Partner link</span></td>
    </tr>
    <tr>
      <td data-label="Compliance Platform"><strong>Drata</strong> <span class="status-pill status-estimated">Estimated (Benchmark)</span><div class="source-inline">Source: <a href="https://drata.com/" target="_blank" rel="noopener">Drata plans &nearr;</a></div></td>
      <td data-label="Est. List Quote" style="font-family:var(--mono);">$${drataList.toLocaleString()}/yr</td>
      <td data-label="Negotiated Platform Cost" style="font-family:var(--mono); color:var(--emerald);">$${drataNeg.toLocaleString()}/yr</td>
      <td data-label="Est. CPA Auditor Fee" style="font-family:var(--mono);">+$${auditorFee.toLocaleString()}</td>
      <td data-label="Total Year-1 SOC 2 Cost" class="price-highlight">$${(drataNeg + auditorFee).toLocaleString()} / yr</td>
      <td data-label="Compare"><a class="btn-cta" href="https://drata.com/" target="_blank" rel="nofollow sponsored">Request Drata quote &rarr;</a><span class="partner-tag">Partner link</span></td>
    </tr>
    <tr>
      <td data-label="Compliance Platform"><strong>Comp AI / Openlane (Startup benchmark)</strong> <span class="status-pill status-estimated">Estimated (Benchmark)</span></td>
      <td data-label="Est. List Quote" style="font-family:var(--mono);">$${compAiCost.toLocaleString()}/yr</td>
      <td data-label="Negotiated Platform Cost" style="font-family:var(--mono);">$${compAiCost.toLocaleString()}/yr</td>
      <td data-label="Est. CPA Auditor Fee" style="font-family:var(--mono);">+$${auditorFee.toLocaleString()}</td>
      <td data-label="Total Year-1 SOC 2 Cost" class="price-highlight">$${(compAiCost + auditorFee).toLocaleString()} / yr</td>
      <td data-label="Compare"><a class="btn-secondary" href="https://trycomp.ai/" target="_blank" rel="nofollow noopener">Compare Comp AI &rarr;</a><span class="partner-tag">Direct vendor link</span></td>
    </tr>
  `;
}
['soc-emp', 'soc-fw', 'soc-disc'].forEach(id => document.getElementById(id).addEventListener('input', updateSocCalc));
updateSocCalc();
</script>
"""

p5_faqs = [
    ("Which Jotform plan includes a signed HIPAA Business Associate Agreement (BAA)?", "Jotform includes HIPAA compliance and an automated Business Associate Agreement (BAA) starting on its self-serve Gold plan ($99/month billed annually, $129/month billed monthly, 1-user account) and Enterprise plan (multi-user), avoiding the $20,000+ custom Enterprise contract required by many form builders."),
    ("Does Vanta or Drata pricing include the SOC 2 CPA auditor fee?", "No. Vanta and Drata are compliance automation platforms that collect evidence and monitor controls, but an independent AICPA-licensed CPA firm must still perform the audit and issue the SOC 2 Type I or Type II report, which typically costs an additional $6,500 to $15,000+ per year."),
    ("How much discount can you negotiate on Vanta or Drata in 2026?", "Initial custom quotes from Vanta and Drata ($9,000–$15,000+/year for startups) are frequently negotiated down by 30% to 50%, especially when comparing against lower-cost alternatives like Comp AI ($2.4k–$12k) or Openlane (~$5.4k).")
]

render_page(
    "compliance/hipaa-baa-and-soc2-pricing-tiers/index.html",
    "HIPAA BAA & SOC 2 True Cost Calculator – saasbill.io",
    "Find out which SaaS pricing tiers sign a HIPAA BAA without a $50k Enterprise contract, and calculate your true SOC 2 Type II platform + CPA auditor cost.",
    "/compliance/hipaa-baa-and-soc2-pricing-tiers/",
    p5_body,
    faqs=p5_faqs
)

print("Wrote Page 3, Page 4, and Page 5 in light editorial style.")

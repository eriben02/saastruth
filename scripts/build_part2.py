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
    <p><strong>The short version:</strong> Standard payment processors (<strong>Stripe, Shopify Payments, PayPal</strong>) can impose a <strong>25% rolling reserve for 90–180 days</strong> or a <strong>120–180 day payout hold</strong> if your dispute rate crosses ~0.5%–0.75% or volume spikes unexpectedly. With Stripe, however, you own the customer relationship and can export PGP-encrypted card tokens. With a Merchant of Record (<strong>Paddle, 5% + $0.50</strong>), Paddle is the legal seller of record and owns the card vault; if Paddle terminates your account on a risk review, <strong>card tokens cannot be exported</strong> (<code>r/SaaS</code>, Sep 2026). To protect cashflow, pair <strong>Chargeflow</strong> (keeps dispute rate &lt;0.5%) with a multi-processor failover rail like <strong>Whop Payments (2.7% + $0.30)</strong>.</p>
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
  <div class="table-wrap">
    <table>
      <caption>2026 Payment Processor &amp; Merchant of Record (MoR) Reserve &amp; Token Ownership Matrix (checked Oct 25, 2026)</caption>
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
          <td><strong>Whop Payments &amp; Orchestration</strong></td>
          <td style="font-family:var(--mono);">2.7% + $0.30 domestic</td>
          <td><span class="badge badge-low">White-glove migration</span><div style="font-size:0.8rem; color:var(--muted); margin-top:4px;">Supports switching from Paddle, Lemon Squeezy, Shopify &amp; Gumroad</div></td>
          <td>Multi-processor waterfall routes around single-acquirer declines (~6% revenue lift); KYB deferred to $5k volume</td>
          <td><a class="btn-cta" href="https://whop.com/sell" target="_blank" rel="nofollow sponsored">Add Whop failover &rarr;</a></td>
        </tr>
        <tr>
          <td><strong>Chargeflow (Dispute Shield)</strong></td>
          <td style="font-family:var(--mono);">Performance-based ($0 setup)</td>
          <td><span class="badge badge-low">Plugs into Stripe / Shopify</span></td>
          <td>Prevents 25% reserves &amp; 180-day freezes by intercepting pre-disputes to keep your chargeback rate under 0.5%</td>
          <td><a class="btn-cta" href="https://www.chargeflow.io/" target="_blank" rel="nofollow sponsored">Install Chargeflow &rarr;</a></td>
        </tr>
        <tr>
          <td><strong>Paddle (Merchant of Record)</strong></td>
          <td style="font-family:var(--mono);">5.0% + $0.50</td>
          <td><span class="badge badge-high">Locked by Paddle</span><div style="font-size:0.8rem; color:var(--muted); margin-top:4px;">Paddle is seller of record; tokens cannot be exported if terminated</div></td>
          <td>Can terminate accounts on internal risk review and hold unreleased payouts without appeal</td>
          <td><a class="btn-secondary" href="https://www.paddle.com/pricing" target="_blank" rel="nofollow sponsored">Paddle terms &rarr;</a></td>
        </tr>
        <tr>
          <td><strong>Lemon Squeezy (MoR by Stripe)</strong></td>
          <td style="font-family:var(--mono);">5.0% + $0.50 (+0.5% subs)</td>
          <td><span class="badge badge-medium">MoR vault (Stripe-backed)</span></td>
          <td>Subject to Stripe's prohibited business list and automated risk triggers</td>
          <td><a class="btn-secondary" href="https://www.lemonsqueezy.com/pricing" target="_blank" rel="nofollow sponsored">Lemon Squeezy &rarr;</a></td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2>What founders report when an account is frozen</h2>
  <div class="evidence-box">
    <strong>Why a Paddle termination is harder to recover from than Stripe</strong>
    <p style="margin-top:6px;">"With a merchant of record, the MoR is the seller. Their name is on the invoice, their entity holds the tax registrations, and the card credentials belong to them. When they terminate you, there is no re-tokenising, because the tokens were never yours."</p>
    <cite>Source: <a href="https://www.reddit.com/r/SaaS/comments/1wd86p7/i_want_to_share_my_experience_with_paddle_as_a/" target="_blank" rel="noopener">r/SaaS &ndash; "I want to share my experience with Paddle as a warning to other SaaS founders" (Sep 11, 2026)</a></cite>
  </div>
  <div class="evidence-box">
    <strong>Shopify &amp; Stripe 179–180 day payout holds</strong>
    <p style="margin-top:6px;">E-commerce founders and risk analysts on X documented $2M/month brands hit with 179-day payout holds and newly launched stores moving checkout to Whop within hours of a Shopify Payments freeze.</p>
    <cite>Sources: <a href="https://x.com/AlexTamano/status/2111182665533809112" target="_blank" rel="noopener">@AlexTamano on X (Oct 16, 2026)</a>, <a href="https://x.com/BlendKabash/status/2113770391617278063" target="_blank" rel="noopener">@BlendKabash on X (Oct 24, 2026)</a> &amp; <a href="https://x.com/MerchantRiskDsk/status/2113450082162950368" target="_blank" rel="noopener">@MerchantRiskDsk on X (Oct 23, 2026)</a></cite>
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
    <p><strong>The short version:</strong> For <strong>1 user</strong>, <strong>Pipedrive</strong> ($14/mo Basic or $34/mo Growth) is up to <strong>60% cheaper</strong> than <strong>monday CRM</strong> because monday CRM enforces a <strong>3-seat minimum</strong> ($36/mo Basic or $51/mo Standard minimum). For <strong>2 users</strong>, monday CRM still bills for 3 seats ($25.50/user/mo effective rate on Standard). At <strong>exactly 3, 5, or 10 users</strong>, however, monday CRM becomes the lowest-cost full-featured CRM at $51/mo (3 users) vs. $102/mo on Pipedrive Growth and $270/mo (+ $1,500 onboarding) on HubSpot Sales Pro.</p>
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
        <option value="entry">Entry / Basic tier (annual billing)</option>
        <option value="standard" selected>Standard / Growth tier (most popular)</option>
      </select>
    </div>
  </div>
  <div class="table-wrap">
    <table>
      <caption>Effective Per-User CRM Cost After Seat Minimums &amp; Seat Buckets (USD, checked Oct 25, 2026)</caption>
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
    <strong>Buyer note on X: "The 3-seat minimum bumps up the actual starting cost"</strong>
    <p style="margin-top:6px;">"monday CRM looks affordable at first, but the 3-seat minimum bumps up the actual starting cost."</p>
    <cite>Source: <a href="https://x.com/wriviewer/status/2106774117718352055" target="_blank" rel="noopener">@wriviewer on X (Oct 4, 2026)</a></cite>
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
      <td><strong>Pipedrive CRM</strong></td>
      <td style="font-family:var(--mono);">$${pipeRate}/seat/mo</td>
      <td><span class="badge badge-low">${u} seat(s) (exact 1:1)</span></td>
      <td style="font-family:var(--mono);">$${pipeRate.toFixed(2)} / user / mo</td>
      <td class="price-highlight">$${(pipeMo * 12).toLocaleString()} / yr</td>
      <td><a class="btn-cta" href="https://www.pipedrive.com/en/pricing" target="_blank" rel="nofollow sponsored">${u <= 2 ? 'Best for 1–2 users &rarr;' : 'Try Pipedrive &rarr;'}</a></td>
    </tr>
    <tr>
      <td><strong>monday CRM</strong></td>
      <td style="font-family:var(--mono);">$${monRate}/seat/mo</td>
      <td><span class="badge ${monSeats > u ? 'badge-medium' : 'badge-low'}">${monSeats} seats (${monSeats - u} unused)</span></td>
      <td style="font-family:var(--mono);">$${(monMo / u).toFixed(2)} / user / mo</td>
      <td class="price-highlight">$${(monMo * 12).toLocaleString()} / yr</td>
      <td><a class="btn-cta" href="https://monday.com/pricing" target="_blank" rel="nofollow sponsored">${u >= 3 ? 'Best value at 3+ users &rarr;' : 'See monday CRM &rarr;'}</a></td>
    </tr>
    <tr>
      <td><strong>HubSpot Sales Hub (${tier === 'entry' ? 'Starter' : 'Professional'})</strong></td>
      <td style="font-family:var(--mono);">$${hsRate}/seat/mo</td>
      <td><span class="badge ${hsOnboard > 0 ? 'badge-high' : 'badge-low'}">${u} seat(s) ${hsOnboard > 0 ? '+ $1,500 onboarding' : ''}</span></td>
      <td style="font-family:var(--mono);">$${((hsMo + hsOnboard / 12) / u).toFixed(2)} / user / mo</td>
      <td class="price-highlight">$${(hsMo * 12 + hsOnboard).toLocaleString()} / yr</td>
      <td><a class="btn-secondary" href="https://www.hubspot.com/pricing" target="_blank" rel="nofollow sponsored">HubSpot pricing &rarr;</a></td>
    </tr>
  `;
}
document.getElementById('sm-users').addEventListener('input', updateSmCalc);
document.getElementById('sm-tier').addEventListener('input', updateSmCalc);
updateSmCalc();
</script>
"""

p4_faqs = [
    ("Can you buy 1 seat of monday CRM in 2026?", "No. monday CRM enforces a mandatory 3-seat minimum on all paid plans. If you are a solo user on the $12/seat Basic plan or $17/seat Standard plan (billed annually), you must pay for 3 seats ($36/month or $51/month)."),
    ("How do monday CRM seat buckets work when adding a 4th or 6th user?", "monday CRM bills in fixed seat buckets of 3, 5, 10, and 15 seats. If you have 4 active users, you must pay for the 5-seat bucket; if you have 6 active users, you must pay for the 10-seat bucket."),
    ("Which CRM is best for a 1-person or 2-person sales team?", "Pipedrive ($14–$34/user/month) and Close CRM ($49/user/month) bill strictly 1:1 per active user with $0 mandatory onboarding fees, making them significantly more cost-effective than monday CRM or HubSpot Professional for 1–2 users.")
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
    <p><strong>The short version:</strong> Self-serve HIPAA Business Associate Agreements (BAAs) are available on <strong>Jotform Gold ($99/mo billed annually)</strong> and <strong>1Password Business ($7.99/user/mo, which also includes SAML SSO with no Enterprise markup)</strong>, whereas HubSpot ($150/seat + $3,500 onboarding), Zendesk ($115/agent Suite Pro), and Intercom ($132/seat Expert) require upper-tier plans. For SOC 2 Type II compliance automation, <strong>Vanta and Drata</strong> list quotes start around <strong>$9,000–$15,000+/yr</strong> (frequently negotiated down by <strong>30%–50%</strong> per <code>r/sysadmin</code>, Mar 2026), while <strong>Comp AI ($2,400–$12,000/yr)</strong> and <strong>Openlane (~$5,400/yr)</strong> cost less—plus a mandatory <strong>$6,500–$15,000+ external CPA auditor fee</strong> billed separately.</p>
  </div>
</section>

<section class="calc-box">
  <h2 style="margin-top:0;">Estimate your real Year-1 SOC 2 budget (platform + CPA auditor)</h2>
  <p style="color:var(--muted); margin-bottom:20px; font-size:0.95rem;">Compliance platforms automate evidence collection, but an independent CPA firm still has to issue your SOC 2 report. Adjust headcount, frameworks, and your negotiated discount below.</p>
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
  <div class="table-wrap">
    <table>
      <caption>2026 SOC 2 Type II &amp; HIPAA Automation Total Cost Estimator: Vanta vs. Drata vs. Comp AI (USD, checked Oct 25, 2026)</caption>
      <thead>
        <tr>
          <th>Compliance Platform</th>
          <th>List Platform Quote</th>
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
  <div class="table-wrap">
    <table>
      <caption>Minimum Pricing Tier Required for Signed HIPAA BAA &amp; SAML SSO (checked Oct 25, 2026)</caption>
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
          <td><strong>Jotform (Forms &amp; Intake)</strong></td>
          <td><span class="badge badge-low">Gold ($99/mo annual)</span></td>
          <td>Enterprise (Multi-user SAML)</td>
          <td>SOC 2 Type II &amp; HIPAA</td>
          <td><a class="btn-cta" href="https://www.jotform.com/hipaa/" target="_blank" rel="nofollow sponsored">Jotform HIPAA &rarr;</a></td>
        </tr>
        <tr>
          <td><strong>1Password (Access &amp; Secrets)</strong></td>
          <td><span class="badge badge-low">Business ($7.99/user/mo)</span></td>
          <td><span class="badge badge-low">Business ($7.99/user/mo &middot; no SSO tax)</span></td>
          <td>SOC 2 Type II &amp; ISO 27001</td>
          <td><a class="btn-cta" href="https://1password.com/business-pricing" target="_blank" rel="nofollow sponsored">1Password Business &rarr;</a></td>
        </tr>
        <tr>
          <td><strong>Zendesk (Customer Support)</strong></td>
          <td><span class="badge badge-medium">Suite Professional ($115/agent/mo)</span></td>
          <td>Listed across Suite plans</td>
          <td>SOC 2 Type II</td>
          <td><a class="btn-secondary" href="../pricing/zendesk-ai-resolution-and-automated-outcome-cost/">Zendesk audit &rarr;</a></td>
        </tr>
        <tr>
          <td><strong>Help Scout (Customer Support)</strong></td>
          <td><span class="badge badge-medium">Pro ($75/user/mo, 10-user min)</span></td>
          <td>Pro or Plus add-on</td>
          <td>SOC 2 Type II &amp; HIPAA</td>
          <td><a class="btn-cta" href="https://www.helpscout.com/pricing/" target="_blank" rel="nofollow sponsored">Help Scout &rarr;</a></td>
        </tr>
        <tr>
          <td><strong>HubSpot (CRM &amp; Marketing)</strong></td>
          <td><span class="badge badge-high">Enterprise ($150/seat + $3,500 onboarding)</span></td>
          <td>Enterprise tier only</td>
          <td>SOC 2 Type II</td>
          <td><a class="btn-secondary" href="../pricing/hubspot-true-cost-and-onboarding-fees/">HubSpot audit &rarr;</a></td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2>What IT buyers report on Vanta &amp; Drata renewals</h2>
  <div class="evidence-box">
    <strong>r/sysadmin negotiation benchmark: "You can get the initial offer down to 50%"</strong>
    <p style="margin-top:6px;">"We use Drata. Vanta and Drata are the market leaders afaik. Just make sure to negotiate hard, those tools are expensive and you can get the initial offer down to 50%."</p>
    <cite>Source: <a href="https://www.reddit.com/r/sysadmin/comments/1rvyrr1/we_need_a_cloud_compliance_tool_that_handles_gdpr/" target="_blank" rel="noopener">r/sysadmin &ndash; "We need a cloud compliance tool that handles GDPR, HIPAA and SOC 2 simultaneously" (Mar 18, 2026)</a></cite>
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
      <td><strong>Vanta</strong></td>
      <td style="font-family:var(--mono);">$${vantaList.toLocaleString()}/yr</td>
      <td style="font-family:var(--mono); color:var(--emerald);">$${vantaNeg.toLocaleString()}/yr</td>
      <td style="font-family:var(--mono);">+$${auditorFee.toLocaleString()}</td>
      <td class="price-highlight">$${(vantaNeg + auditorFee).toLocaleString()} / yr</td>
      <td><a class="btn-cta" href="https://www.vanta.com/" target="_blank" rel="nofollow sponsored">Request Vanta quote &rarr;</a></td>
    </tr>
    <tr>
      <td><strong>Drata</strong></td>
      <td style="font-family:var(--mono);">$${drataList.toLocaleString()}/yr</td>
      <td style="font-family:var(--mono); color:var(--emerald);">$${drataNeg.toLocaleString()}/yr</td>
      <td style="font-family:var(--mono);">+$${auditorFee.toLocaleString()}</td>
      <td class="price-highlight">$${(drataNeg + auditorFee).toLocaleString()} / yr</td>
      <td><a class="btn-cta" href="https://drata.com/" target="_blank" rel="nofollow sponsored">Request Drata quote &rarr;</a></td>
    </tr>
    <tr>
      <td><strong>Comp AI / Openlane (Startup benchmark)</strong></td>
      <td style="font-family:var(--mono);">$${compAiCost.toLocaleString()}/yr</td>
      <td style="font-family:var(--mono);">$${compAiCost.toLocaleString()}/yr</td>
      <td style="font-family:var(--mono);">+$${auditorFee.toLocaleString()}</td>
      <td class="price-highlight">$${(compAiCost + auditorFee).toLocaleString()} / yr</td>
      <td><a class="btn-secondary" href="https://www.vanta.com/" target="_blank" rel="nofollow">Compare benchmarks &rarr;</a></td>
    </tr>
  `;
}
['soc-emp', 'soc-fw', 'soc-disc'].forEach(id => document.getElementById(id).addEventListener('input', updateSocCalc));
updateSocCalc();
</script>
"""

p5_faqs = [
    ("Which Jotform plan includes a signed HIPAA Business Associate Agreement (BAA)?", "Jotform includes HIPAA compliance and an automated Business Associate Agreement (BAA) starting on its self-serve Gold plan ($99/month billed annually) and Enterprise plan, avoiding the $20,000+ custom Enterprise contract required by many form builders."),
    ("Does Vanta or Drata pricing include the SOC 2 CPA auditor fee?", "No. Vanta and Drata are compliance automation platforms that collect evidence and monitor controls, but an independent AICPA-licensed CPA firm must still perform the audit and issue the SOC 2 Type I or Type II report, which typically costs an additional $6,500 to $15,000+ per year."),
    ("How much discount can you negotiate on Vanta or Drata in 2026?", "According to verified buyer benchmarks on r/sysadmin (March 2026), initial list quotes from Vanta and Drata ($9,000–$15,000+/year for startups) can routinely be negotiated down by 30% to 50%, especially when comparing against lower-cost alternatives like Comp AI ($2.4k–$12k) or Openlane (~$5.4k).")
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

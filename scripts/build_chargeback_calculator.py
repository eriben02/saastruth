"""Chargeback fee and Chargeflow ROI calculator.

Defaults (Stripe, 2,000 orders/mo, $120 AOV, 0.65% dispute rate):
  annual GMV $2,880,000
  156 disputes/yr, $18,720 disputed revenue, $2,340 dispute fees
  manual (20% win, $30 labor/dispute): $21,996
  Stripe Chargeback Protection (0.40% of GMV): $11,520
  Chargeflow (75% planning win rate, 25% of recovered revenue): $10,530
  savings vs manual: $11,466
"""
from layout import render_page, load_data

_, AFFILIATES = load_data()
CF_URL = AFFILIATES["chargeflow"]["destination_url"]

TITLE = "Stripe & Shopify Chargeback Cost Calculator (2026): Dispute Fees, Lost Revenue & Chargeflow ROI"
DESC = (
    "See annual chargeback loss from the full order value plus a non-refundable dispute fee, "
    "then compare manual handling, Stripe Chargeback Protection at 0.40% of GMV, and Chargeflow."
)
LEAD = (
    "Every chargeback costs the full order value plus a non-refundable $15 to $25 processor dispute fee. "
    "Adjust your monthly volume and dispute rate below to see total annual loss versus automated recovery."
)

H1 = TITLE


def calc_chargeback(orders, aov, rate_pct, fee):
    """Mirror of calcChargeback() in the page. rate_pct is 0.65 for 0.65%."""
    disputes_yr = orders * (rate_pct / 100.0) * 12.0
    gmv_yr = orders * aov * 12.0
    disputed = disputes_yr * aov
    fees = disputes_yr * fee
    manual = disputed * 0.80 + fees + disputes_yr * 30.0
    recovered = disputed * 0.75
    success_fee = recovered * 0.25
    chargeflow = (disputed - recovered) + fees + success_fee
    stripe_protect = gmv_yr * 0.004
    return {
        "disputes_yr": disputes_yr,
        "gmv_yr": gmv_yr,
        "disputed": disputed,
        "fees": fees,
        "manual": manual,
        "recovered": recovered,
        "success_fee": success_fee,
        "chargeflow": chargeflow,
        "stripe_protect": stripe_protect,
        "savings": manual - chargeflow,
    }


def render_body():
    return f"""
<section class="hero">
  <h1>{H1}</h1>
  <p class="lead">{LEAD}</p>
</section>

<section class="calc-box editorial-workbench" aria-labelledby="cb-heading">
  <h2 id="cb-heading" class="sr-only-control">Chargeback cost and recovery workbench</h2>
  <div class="workbench-grid">
    <div class="wb-col-controls">
      <div class="wb-col-title">Estimate your dispute loss</div>
      <div class="calc-grid">
        <div class="control-group">
          <label for="cb-processor">Payment processor</label>
          <select id="cb-processor" data-track="calculator-control" data-control="processor">
            <option value="stripe" selected>Stripe ($15 dispute fee)</option>
            <option value="shopify">Shopify Payments ($15 dispute fee)</option>
            <option value="paddle">Paddle ($15 to $20 dispute fee)</option>
            <option value="highrisk">High-Volume / High-Risk ($25 dispute fee)</option>
          </select>
        </div>
        <div class="control-group">
          <label for="cb-orders">Monthly orders <span class="val-pill" id="cb-orders-val">2,000</span></label>
          <input type="range" id="cb-orders" min="100" max="25000" step="100" value="2000" aria-label="Monthly orders" data-track="calculator-control" data-control="orders" />
        </div>
        <div class="control-group">
          <label for="cb-aov">Average order value (USD) <span class="val-pill" id="cb-aov-val">$120</span></label>
          <input type="range" id="cb-aov" min="20" max="500" step="5" value="120" aria-label="Average order value" data-track="calculator-control" data-control="aov" />
        </div>
        <div class="control-group">
          <label for="cb-rate">Dispute rate <span class="val-pill" id="cb-rate-val">0.65%</span></label>
          <input type="range" id="cb-rate" min="10" max="200" step="5" value="65" aria-label="Dispute rate in hundredths of a percent" data-track="calculator-control" data-control="dispute-rate" />
        </div>
      </div>
      <p id="cb-threshold" class="wb-budget-subnote">Below the 0.75% Visa and 1.00% Mastercard monitoring thresholds.</p>
    </div>

    <div class="wb-col-chart">
      <div class="wb-col-title">Annual cost comparison</div>
      <div id="cb-bars" class="viz-rows" aria-live="polite"></div>
    </div>

    <div class="wb-result-col" id="cb-result" aria-live="polite">
      <div class="wb-selected-product">Chargeflow net annual cost</div>
      <div class="wb-big-total"><span id="cb-big">$10,530</span> <span class="wb-per-year">/ year</span></div>
      <p class="wb-budget-quote" id="cb-quote">Based on 2,000 orders/mo, a $120 order value, and a 0.65% dispute rate on Stripe.</p>
      <p class="wb-budget-subnote" id="cb-sub">Gross disputed revenue plus the $15 dispute fee, before recovery.</p>
      <div class="wb-best-option" id="cb-best"><strong>Best option:</strong> Chargeflow, success fee only on won disputes.</div>
      <details class="calc-disclosure" id="wb-calc-details">
        <summary class="calc-disclosure-toggle">See exactly how we calculated this</summary>
        <div class="calc-disclosure-body" id="cb-math"></div>
      </details>
      <div class="cta-stack">
        <a id="cb-primary-cta" class="btn-cta wb-primary-cta" href="{CF_URL}" target="_blank" rel="nofollow noopener" data-track="vendor_cta_click" data-vendor="chargeflow" data-cta-location="workbench">Save $11,466/yr with Chargeflow &rarr;</a>
      </div>
    </div>
  </div>
</section>

<section class="verdict-section" aria-label="Chargeback recovery verdict">
  <div id="cb-summary" class="summary-strip" aria-live="polite"></div>
</section>

<section class="hidden-gap-section" aria-labelledby="cb-gap-heading">
  <details class="full-table-disclosure" id="full-table-details">
    <summary class="full-table-summary">
      <div class="full-table-summary-text">
        <h2 id="cb-gap-heading" class="full-table-heading">Compare all tools in this category</h2>
        <span class="full-table-summary-sub">Chargeflow, Stripe Chargeback Protection, Shopify Protect, and manual handling</span>
      </div>
      <span class="full-table-toggle-pill">Compare all tools &darr;</span>
    </summary>
    <div class="full-table-body">
      <div class="table-wrap editorial-gap-table mobile-cards">
        <table>
          <caption>Annual dispute cost at the inputs above</caption>
          <thead>
            <tr>
              <th>Approach</th>
              <th>How you pay</th>
              <th>Annual cost</th>
              <th>What it covers</th>
            </tr>
          </thead>
          <tbody id="cb-tbody"></tbody>
        </table>
      </div>
    </div>
  </details>
  <p class="calc-affiliate-disclosure">Independent calculations. Some vendor links are affiliate links. This never changes our rankings or calculations.</p>
</section>

<script>
const CHARGEFLOW_URL = {CF_URL!r};
const MANUAL_WIN = 0.20;
const CHARGEFLOW_WIN = 0.75;
const CHARGEFLOW_SUCCESS_FEE = 0.25;
const LABOR_PER_DISPUTE = 30;
const STRIPE_PROTECT_RATE = 0.004;
const FEES = {{ stripe: 15, shopify: 15, paddle: 20, highrisk: 25 }};

function calcChargeback(orders, aov, ratePct, fee) {{
  const disputesYr = orders * (ratePct / 100) * 12;
  const gmvYr = orders * aov * 12;
  const disputed = disputesYr * aov;
  const disputeFees = disputesYr * fee;
  const manualUnrecovered = disputed * (1 - MANUAL_WIN);
  const labor = disputesYr * LABOR_PER_DISPUTE;
  const manualTotal = manualUnrecovered + disputeFees + labor;
  const recovered = disputed * CHARGEFLOW_WIN;
  const successFee = recovered * CHARGEFLOW_SUCCESS_FEE;
  const unrecovered = disputed - recovered;
  const chargeflowTotal = unrecovered + disputeFees + successFee;
  const stripeProtect = gmvYr * STRIPE_PROTECT_RATE;
  return {{
    disputesYr: disputesYr,
    gmvYr: gmvYr,
    disputed: disputed,
    disputeFees: disputeFees,
    manualUnrecovered: manualUnrecovered,
    labor: labor,
    manualTotal: manualTotal,
    recovered: recovered,
    successFee: successFee,
    unrecovered: unrecovered,
    chargeflowTotal: chargeflowTotal,
    stripeProtect: stripeProtect,
    savings: manualTotal - chargeflowTotal
  }};
}}

function money(n) {{
  return '$' + Math.round(n).toLocaleString('en-US');
}}

function thresholdCopy(ratePct) {{
  if (ratePct >= 1) return 'At or above the 1.00% Mastercard and 0.75% Visa monitoring thresholds.';
  if (ratePct >= 0.75) return 'At or above the 0.75% Visa monitoring threshold.';
  if (ratePct >= 0.6) return 'Approaching the 0.75% Visa monitoring threshold.';
  return 'Below the 0.75% Visa and 1.00% Mastercard monitoring thresholds.';
}}

function renderChargeback() {{
  const processor = document.getElementById('cb-processor').value;
  const orders = parseInt(document.getElementById('cb-orders').value, 10);
  const aov = parseInt(document.getElementById('cb-aov').value, 10);
  const ratePct = parseInt(document.getElementById('cb-rate').value, 10) / 100;
  const fee = FEES[processor];
  const row = calcChargeback(orders, aov, ratePct, fee);
  document.getElementById('cb-orders-val').textContent = orders.toLocaleString('en-US');
  document.getElementById('cb-aov-val').textContent = '$' + aov.toLocaleString('en-US');
  document.getElementById('cb-rate-val').textContent = ratePct.toFixed(2) + '%';
  document.getElementById('cb-threshold').textContent = thresholdCopy(ratePct);
  document.getElementById('cb-big').textContent = money(row.chargeflowTotal);
  document.getElementById('cb-quote').textContent = 'Based on ' + orders.toLocaleString('en-US') + ' orders/mo, a $' + aov + ' order value, and a ' + ratePct.toFixed(2) + '% dispute rate.';
  document.getElementById('cb-sub').textContent = 'Gross disputed revenue ' + money(row.disputed) + ' plus ' + money(row.disputeFees) + ' in $' + fee + ' dispute fees.';
  const cta = document.getElementById('cb-primary-cta');
  cta.textContent = 'Save ' + money(row.savings) + '/yr with Chargeflow →';
  cta.href = CHARGEFLOW_URL;
  document.getElementById('cb-math').innerHTML = [
    '<div class="calc-math-list">',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Disputes per year</strong><span class="calc-math-formula">' + orders.toLocaleString('en-US') + ' orders x ' + ratePct.toFixed(2) + '% x 12</span></span><span class="calc-math-val">' + Math.round(row.disputesYr).toLocaleString('en-US') + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Gross disputed revenue</strong><span class="calc-math-formula">disputes x $' + aov + ' AOV</span></span><span class="calc-math-val">' + money(row.disputed) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Processor dispute fees</strong><span class="calc-math-formula">disputes x $' + fee + ' (non-refundable)</span></span><span class="calc-math-val">' + money(row.disputeFees) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Manual unrecovered revenue</strong><span class="calc-math-formula">80% of disputed revenue after a 20% win rate</span></span><span class="calc-math-val">' + money(row.manualUnrecovered) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Manual internal labor</strong><span class="calc-math-formula">disputes x $30 benchmark</span></span><span class="calc-math-val">' + money(row.labor) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Manual total</strong><span class="calc-math-formula">unrecovered + fees + labor</span></span><span class="calc-math-val">' + money(row.manualTotal) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Stripe Chargeback Protection</strong><span class="calc-math-formula">0.40% x ' + money(row.gmvYr) + ' GMV</span></span><span class="calc-math-val">' + money(row.stripeProtect) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Chargeflow recovered</strong><span class="calc-math-formula">75% planning win rate x disputed revenue</span></span><span class="calc-math-val">' + money(row.recovered) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Chargeflow success fee</strong><span class="calc-math-formula">25% of recovered revenue only ($0/mo, $0 setup)</span></span><span class="calc-math-val">' + money(row.successFee) + '</span></div>',
    '<div class="calc-math-total"><span>Chargeflow net annual cost</span><span>' + money(row.chargeflowTotal) + ' / yr</span></div>',
    '</div>'
  ].join('');

  const maxCost = Math.max(row.manualTotal, row.stripeProtect, row.chargeflowTotal, 1);
  const bars = [
    {{ name: 'Manual handling', cost: row.manualTotal, cls: 'viz-seg-ai' }},
    {{ name: 'Stripe Chargeback Protection', cost: row.stripeProtect, cls: 'viz-seg-onboarding' }},
    {{ name: 'Chargeflow', cost: row.chargeflowTotal, cls: 'viz-seg-seats' }}
  ];
  document.getElementById('cb-bars').innerHTML = bars.map(function(b) {{
    const pct = Math.max(4, (b.cost / maxCost) * 100);
    return '<div class="viz-row"><div class="viz-label">' + b.name + '</div><div class="viz-bar-wrap"><div class="viz-bar-track"><div class="' + b.cls + '" style="width:' + pct.toFixed(1) + '%"></div></div></div><div class="viz-total-label">' + money(b.cost) + '</div></div>';
  }}).join('');

  document.getElementById('cb-summary').innerHTML = [
    '<div class="summary-card result-card card-lowest"><div class="summary-label">Chargeflow</div><div class="summary-metric">' + money(row.chargeflowTotal) + ' / yr</div><p class="summary-scenario">Based on a 75% planning win rate and a 25% fee only on won disputes. $0 per month and $0 setup.</p><p><strong>Hidden Cost Highlight:</strong> You still pay the processor dispute fee on each dispute.</p></div>',
    '<div class="summary-card result-card card-hidden"><div class="summary-label">Manual self-managed</div><div class="summary-metric">' + money(row.manualTotal) + ' / yr</div><p class="summary-scenario">Based on a 20% win rate: 80% of disputed revenue stays lost, plus dispute fees and $30 labor per dispute.</p></div>',
    '<div class="summary-card result-card card-highest"><div class="summary-label">Stripe Chargeback Protection</div><div class="summary-metric">' + money(row.stripeProtect) + ' / yr</div><p class="summary-scenario">0.40% of ' + money(row.gmvYr) + ' GMV, charged on volume even when the dispute rate is ordinary.</p></div>'
  ].join('');

  const tableRows = [
    {{ name: 'Chargeflow', pay: '$0/mo, $0 setup, 25% of won disputes', cost: money(row.chargeflowTotal) + '/yr', cover: 'Automated recovery. Planning win rate on this page is 75%, not a guarantee.' }},
    {{ name: 'Stripe Chargeback Protection', pay: '0.40% of total GMV', cost: money(row.stripeProtect) + '/yr', cover: 'Percent of all card volume, including orders that are never disputed.' }},
    {{ name: 'Shopify Protect', pay: 'Included on eligible Shop Pay checkouts', cost: 'Shop Pay, US only', cover: 'Not a fee on every Shopify Payments order. US Shop Pay coverage only.' }},
    {{ name: 'Manual dispute handling', pay: 'Lost orders + $' + fee + ' fee + labor', cost: money(row.manualTotal) + '/yr', cover: 'About 20% of disputes won. The other 80% of order value is unrecovered.' }}
  ];
  document.getElementById('cb-tbody').innerHTML = tableRows.map(function(r) {{
    return '<tr><td data-label="Approach"><strong>' + r.name + '</strong></td><td data-label="How you pay">' + r.pay + '</td><td data-label="Annual cost">' + r.cost + '</td><td data-label="What it covers">' + r.cover + '</td></tr>';
  }}).join('');

  if (typeof window.trackSaaSBillEvent === 'function') {{
    window.trackSaaSBillEvent('result_rendered', {{ page: 'chargeback-fee-and-recovery-calculator', orders: orders, aov: aov, rate: ratePct, processor: processor }});
  }}
}}

['cb-processor', 'cb-orders', 'cb-aov', 'cb-rate'].forEach(function(id) {{
  const el = document.getElementById(id);
  el.addEventListener('input', renderChargeback);
  el.addEventListener('change', renderChargeback);
}});
renderChargeback();
</script>
"""


FAQS = [
    (
        "What does a chargeback cost besides the lost sale?",
        "The cardholder's bank pulls the order value back, and Stripe or Shopify Payments adds a dispute fee (commonly $15) that this page treats as non-refundable. High-risk programs are often closer to $25.",
    ),
    (
        "How is the Chargeflow number on this page calculated?",
        "Disputes equal monthly orders times the dispute rate, times 12. Chargeflow's line uses a 75% planning win rate and a 25% fee only on the recovered order value, plus $0 per month and $0 setup. Your live win rate will differ.",
    ),
    (
        "Why is Stripe Chargeback Protection expensive at a normal dispute rate?",
        "Stripe prices Chargeback Protection at 0.40% of card volume, not 0.40% of disputed volume. At 2,000 orders of $120, annual GMV is $2.88 million and 0.40% is $11,520 even when most orders are never disputed.",
    ),
]


def build_all():
    body = render_body()
    render_page(
        "chargeback-fee-and-recovery-calculator/index.html",
        TITLE + " – saasbill.io",
        DESC,
        "/chargeback-fee-and-recovery-calculator/",
        body,
        faqs=FAQS,
    )
    render_page(
        "pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html",
        TITLE + " – saasbill.io",
        DESC,
        "/pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/",
        body,
        faqs=FAQS,
    )


if __name__ == "__main__":
    build_all()

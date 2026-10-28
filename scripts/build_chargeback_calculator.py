"""Chargeback fee and Chargeflow ROI calculator.

Defaults (Stripe, 2,000 orders/mo, $120 AOV, 0.65% dispute rate):
  annual GMV $2,880,000
  156 disputes/yr, $18,720 disputed revenue, $2,340 dispute fees
  manual (20% win, $30 labor/dispute): $21,996
  Stripe Chargeback Protection (0.40% of GMV): $11,520
  Chargeflow (65% win rate, 25% of recovered revenue): drain $11,934, net recovered $9,126
  savings vs manual: $10,062
"""
from layout import render_page, load_data

_, AFFILIATES = load_data()
CF_URL = AFFILIATES["chargeflow"]["destination_url"]

TITLE = "Stripe, Shopify & Paddle Chargeback Cost Calculator (2026): Dispute Fees, Manual Prep vs. Automated Recovery"
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
    manual_recovered = disputed * 0.20
    recovered = disputed * 0.65
    success_fee = recovered * 0.25
    net_recovered = recovered - success_fee
    chargeflow = (disputed - recovered) + fees + success_fee
    stripe_protect = gmv_yr * 0.004
    return {
        "disputes_yr": disputes_yr,
        "gmv_yr": gmv_yr,
        "disputed": disputed,
        "fees": fees,
        "manual_recovered": manual_recovered,
        "manual": manual,
        "labor": disputes_yr * 30.0,
        "recovered": recovered,
        "success_fee": success_fee,
        "net_recovered": net_recovered,
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
            <option value="stripe" selected>Stripe ($15 + $15 counter fee)</option>
            <option value="shopify">Shopify Payments ($15 fee)</option>
            <option value="paddle">Paddle ($20 dispute fee)</option>
            <option value="highrisk">High-risk PSP ($25 fee)</option>
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
      <div class="wb-col-title">Annual Dispute Drain Breakdown</div>
      <div id="cb-bars" class="viz-rows" aria-live="polite"></div>
    </div>

    <div class="wb-result-col" id="cb-result" aria-live="polite">
      <div class="wb-selected-product">Chargeflow Pay-On-Performance</div>
      <div class="wb-big-total"><span id="cb-big">$9,126</span> <span class="wb-per-year">net / year</span></div>
      <details class="math-drawer" id="wb-calc-details">
        <summary>Show calculation</summary>
        <div class="math-drawer-body" id="cb-math"></div>
      </details>
      <p class="wb-budget-quote" id="cb-quote">Based on 2,000 orders/mo, a $120 order value, and a 0.65% dispute rate on Stripe.</p>
      <p class="wb-budget-subnote" id="cb-callout">$9,126/yr net recovered after the 25% success fee, and $10,062/yr saved vs. manual in-house handling. Stripe Chargeback Protection is $11,520/yr at 0.40% of GMV.</p>
      <div class="wb-best-option" id="cb-best"><strong>Lowest annual cost at these inputs:</strong> compared after you set volume and dispute rate.</div>
      <div class="cta-stack">
        <a id="cb-primary-cta" class="btn-cta wb-primary-cta" href="{CF_URL}" target="_blank" rel="nofollow noopener" data-track="vendor_cta_click" data-vendor="chargeflow" data-cta-location="workbench">Recover $9,126/yr net with Chargeflow &rarr;</a>
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
const CHARGEFLOW_WIN = 0.65;
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
  const manualRecovered = disputed * MANUAL_WIN;
  const recovered = disputed * CHARGEFLOW_WIN;
  const successFee = recovered * CHARGEFLOW_SUCCESS_FEE;
  const netRecovered = recovered - successFee;
  const unrecovered = disputed - recovered;
  const chargeflowTotal = unrecovered + disputeFees + successFee;
  const stripeProtect = gmvYr * STRIPE_PROTECT_RATE;
  return {{
    disputesYr: disputesYr,
    gmvYr: gmvYr,
    disputed: disputed,
    disputeFees: disputeFees,
    manualRecovered: manualRecovered,
    manualUnrecovered: manualUnrecovered,
    labor: labor,
    manualTotal: manualTotal,
    recovered: recovered,
    successFee: successFee,
    netRecovered: netRecovered,
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
  document.getElementById('cb-big').textContent = money(row.netRecovered);
  document.getElementById('cb-quote').textContent = 'Based on ' + orders.toLocaleString('en-US') + ' orders/mo, a $' + aov + ' order value, and a ' + ratePct.toFixed(2) + '% dispute rate.';
  document.getElementById('cb-callout').textContent = money(row.netRecovered) + '/yr net recovered after the 25% success fee, and ' + money(row.savings) + '/yr saved vs. manual in-house handling. Stripe Chargeback Protection is ' + money(row.stripeProtect) + '/yr at 0.40% of GMV.';
  const cta = document.getElementById('cb-primary-cta');
  cta.textContent = 'Recover ' + money(row.netRecovered) + '/yr net with Chargeflow →';
  cta.href = CHARGEFLOW_URL;
  document.getElementById('cb-math').innerHTML = [
    '<div class="calc-math-list">',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Disputes per year</strong><span class="calc-math-formula">' + orders.toLocaleString('en-US') + ' orders x ' + ratePct.toFixed(2) + '% x 12</span></span><span class="calc-math-val">' + Math.round(row.disputesYr).toLocaleString('en-US') + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Gross disputed revenue</strong><span class="calc-math-formula">disputes x $' + aov + ' AOV</span></span><span class="calc-math-val">' + money(row.disputed) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Processor dispute fees</strong><span class="calc-math-formula">disputes x $' + fee + ' (non-refundable)</span></span><span class="calc-math-val">' + money(row.disputeFees) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Manual gross recovered (20%)</strong><span class="calc-math-formula">20% win rate x disputed revenue</span></span><span class="calc-math-val">' + money(row.manualRecovered) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Unrecovered disputed revenue (80%)</strong><span class="calc-math-formula">80% of disputed revenue</span></span><span class="calc-math-val">' + money(row.manualUnrecovered) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Manual evidence prep and counter cost</strong><span class="calc-math-formula">disputes x $30</span></span><span class="calc-math-val">' + money(row.labor) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Total annual drain (manual)</strong><span class="calc-math-formula">unrecovered + fees + $30 counter cost</span></span><span class="calc-math-val">' + money(row.manualTotal) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Chargeflow gross recovered (65%)</strong><span class="calc-math-formula">65% automated win rate x disputed revenue</span></span><span class="calc-math-val">' + money(row.recovered) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Chargeflow 25% success fee</strong><span class="calc-math-formula">25% of won disputes only ($0/mo, $0 setup, $0 manual labor)</span></span><span class="calc-math-val">' + money(row.successFee) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Net recovered revenue after fee</strong><span class="calc-math-formula">gross recovered minus the 25% success fee</span></span><span class="calc-math-val">' + money(row.netRecovered) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Unrecovered disputed revenue (35%)</strong><span class="calc-math-formula">35% of disputed revenue</span></span><span class="calc-math-val">' + money(row.unrecovered) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Total annual drain (with Chargeflow)</strong><span class="calc-math-formula">unrecovered + processor fees + success fee</span></span><span class="calc-math-val">' + money(row.chargeflowTotal) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Annual net savings vs. manual</strong><span class="calc-math-formula">manual drain minus Chargeflow drain</span></span><span class="calc-math-val">' + money(row.savings) + '</span></div>',
    '<div class="calc-math-row"><span class="calc-math-label"><strong>Stripe Chargeback Protection</strong><span class="calc-math-formula">0.40% x ' + money(row.gmvYr) + ' GMV</span></span><span class="calc-math-val">' + money(row.stripeProtect) + '</span></div>',
    '<div class="calc-math-total"><span>Chargeflow net recovered</span><span>' + money(row.netRecovered) + ' / yr</span></div>',
    '</div>'
  ].join('');

  const maxCost = Math.max(row.manualTotal, row.stripeProtect, row.chargeflowTotal, 1);
  const bars = [
    {{ name: 'Manual In-House Dispute Handling', cost: row.manualTotal, cls: 'viz-seg-ai' }},
    {{ name: 'Stripe Chargeback Protection (0.40% of GMV)', cost: row.stripeProtect, cls: 'viz-seg-onboarding' }},
    {{ name: 'Chargeflow Pay-On-Performance', cost: row.chargeflowTotal, cls: 'viz-seg-seats' }}
  ];
  document.getElementById('cb-bars').innerHTML = bars.map(function(b) {{
    const pct = Math.max(4, (b.cost / maxCost) * 100);
    return '<div class="viz-row"><div class="viz-label">' + b.name + '</div><div class="viz-bar-wrap"><div class="viz-bar-track"><div class="' + b.cls + '" style="width:' + pct.toFixed(1) + '%"></div></div></div><div class="viz-total-label">' + money(b.cost) + '</div></div>';
  }}).join('');

  const costOptions = [
    {{ key: 'manual', name: 'Manual in-house handling', cost: row.manualTotal }},
    {{ key: 'chargeflow', name: 'Chargeflow pay-on-performance', cost: row.chargeflowTotal }},
    {{ key: 'protect', name: 'Stripe Chargeback Protection', cost: row.stripeProtect }}
  ].sort(function(a, b) {{ return a.cost - b.cost; }});
  const cheapest = costOptions[0];
  const cfCaveat = '25% of recovered dispute dollars ($0/mo base). Does not refund the processor\\'s $15 to $20 dispute fee when a dispute is lost, and a 65% win rate is a planning benchmark; actual recovery varies by dispute reason code.';
  document.getElementById('cb-best').innerHTML = '<strong>Lowest annual cost at these inputs:</strong> ' + cheapest.name + ' (' + money(cheapest.cost) + '/yr).';
  function mathDrawer(rowsHtml) {{
    return '<details class="math-drawer"><summary>Show calculation</summary><div class="math-drawer-body"><div class="calc-math-list">' + rowsHtml + '</div></div></details>';
  }}
  function cardOpen(key) {{
    let cls = 'summary-card result-card';
    if (cheapest.key === key) cls += ' best-card card-lowest';
    return '<div class="' + cls + '">';
  }}
  const cfScenario = (cheapest.key === 'chargeflow' ? 'Highest Net Recovery. ' : 'Dispute-recovery add-on, not a payment processor. ') + '65% automated win rate, 25% fee only on won disputes, $0/mo fixed fee, and $0 manual labor. Annual drain ' + money(row.chargeflowTotal) + '.';
  document.getElementById('cb-summary').innerHTML = [
    cardOpen('manual') + '<div class="summary-label">Manual In-House Dispute Handling</div><div class="summary-metric">' + money(row.manualTotal) + ' / yr</div>' + mathDrawer('<div class="calc-math-row"><span class="calc-math-label"><strong>Unrecovered disputed revenue</strong></span><span class="calc-math-val">' + money(row.manualUnrecovered) + '</span></div><div class="calc-math-total"><span>Manual annual drain</span><span>' + money(row.manualTotal) + '</span></div>') + '<p class="summary-scenario">Baseline (20% Win Rate). Gross recovered ' + money(row.manualRecovered) + ', unrecovered ' + money(row.manualUnrecovered) + ', plus processor fees and $30 evidence prep per dispute.</p><p class="summary-breakdown">80% of disputed revenue stays unrecovered at a 20% manual win rate.</p><p class="summary-caveat"><strong>Hidden Cost Highlight:</strong> Evidence prep is $30 on every dispute, won or lost.</p></div>',
    cardOpen('chargeflow') + '<div class="summary-label">Chargeflow Pay-On-Performance</div><div class="summary-metric">' + money(row.netRecovered) + ' / yr net</div>' + mathDrawer('<div class="calc-math-row"><span class="calc-math-label"><strong>Gross recovered at 65%</strong></span><span class="calc-math-val">' + money(row.recovered) + '</span></div><div class="calc-math-row"><span class="calc-math-label"><strong>25% success fee</strong></span><span class="calc-math-val">' + money(row.successFee) + '</span></div><div class="calc-math-total"><span>Net recovered</span><span>' + money(row.netRecovered) + '</span></div>') + '<p class="summary-scenario">' + cfScenario + '</p><p class="summary-breakdown">$0/mo fixed. The 25% fee applies only to disputes Chargeflow wins.</p><p class="summary-caveat">' + cfCaveat + '</p><div class="summary-actions"><a class="btn-cta" href="' + CHARGEFLOW_URL + '" target="_blank" rel="nofollow noopener" data-track="vendor_cta_click" data-vendor="chargeflow">Recover ' + money(row.netRecovered) + '/yr net with Chargeflow →</a></div></div>',
    cardOpen('protect') + '<div class="summary-label">Stripe Chargeback Protection (0.40% of GMV)</div><div class="summary-metric">' + money(row.stripeProtect) + ' / yr</div>' + mathDrawer('<div class="calc-math-row"><span class="calc-math-label"><strong>0.40% of annual GMV</strong></span><span class="calc-math-val">' + money(row.gmvYr) + '</span></div><div class="calc-math-total"><span>Flat volume fee</span><span>' + money(row.stripeProtect) + '</span></div>') + '<p class="summary-scenario">Flat Volume Fee. 0.40% of ' + money(row.gmvYr) + ' GMV, charged on volume even when the dispute rate is ordinary.</p><p class="summary-breakdown">Charged on every processed dollar, not only disputed orders.</p></div>'
  ].join('');

  const tableRows = [
    {{ name: 'Manual In-House Dispute Handling', pay: '20% win rate + $30 evidence prep per dispute', cost: money(row.manualTotal) + '/yr', cover: 'Baseline. 80% of disputed revenue stays unrecovered.' }},
    {{ name: 'Chargeflow Pay-On-Performance', pay: '$0/mo, $0 setup, 25% of won disputes', cost: money(row.chargeflowTotal) + '/yr', cover: '65% automated win rate. Net recovered after the fee is ' + money(row.netRecovered) + '/yr.' }},
    {{ name: 'Stripe Chargeback Protection (0.40% of GMV)', pay: '0.40% of total GMV', cost: money(row.stripeProtect) + '/yr', cover: 'Flat volume fee on all card volume, including orders that are never disputed.' }},
    {{ name: 'Shopify Protect', pay: 'Included on eligible Shop Pay checkouts', cost: 'Shop Pay, US only', cover: 'Not a fee on every Shopify Payments order. US Shop Pay coverage only.' }}
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
        "The cardholder's bank pulls the order value back, and the processor adds a dispute fee (Stripe and Shopify Payments $15, Paddle $20 on this page) that the model treats as non-refundable. Stripe's option also names a $15 counter fee; the default Stripe line uses the $15 dispute fee.",
    ),
    (
        "How is the Chargeflow number on this page calculated?",
        "Disputes equal monthly orders times the dispute rate, times 12. Chargeflow uses a 65% automated win rate and a 25% fee only on won disputes, with $0 per month, $0 setup, and $0 manual labor. Your live win rate will differ.",
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

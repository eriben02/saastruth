/**
 * Chargeback calculator checks. Run: node scripts/test_calculators.js
 * Reads the built page so the labels and formula stay in lockstep.
 */
const fs = require("fs");
const path = require("path");
const assert = require("assert");

const pages = [
  "public/chargeback-fee-and-recovery-calculator/index.html",
  "public/pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html",
];

function moneyRound(n) {
  return Math.round(n);
}

let failed = 0;
function check(name, fn) {
  try {
    fn();
    console.log("ok", name);
  } catch (err) {
    failed += 1;
    console.error("FAIL", name);
    console.error(err && err.stack ? err.stack : err);
  }
}

for (const rel of pages) {
  const html = fs.readFileSync(path.join(__dirname, "..", rel), "utf8");
  check(rel + " labels", () => {
    assert.ok(html.includes("Stripe ($15 dispute fee + $15 counter fee)"));
    assert.ok(html.includes("Shopify Payments ($15 dispute fee)"));
    assert.ok(html.includes("Paddle ($20 dispute fee)"));
    assert.ok(!html.includes("High-Volume / High-Risk"));
    assert.ok(html.includes("Manual In-House Dispute Handling"));
    assert.ok(html.includes("Baseline (20% Win Rate)"));
    assert.ok(html.includes("Chargeflow Pay-On-Performance"));
    assert.ok(html.includes("Highest Net Recovery"));
    assert.ok(html.includes("best-card"));
    assert.ok(html.includes("Stripe Chargeback Protection (0.40% of GMV)"));
    assert.ok(html.includes("Flat Volume Fee"));
    assert.ok(html.includes("Recover $9,126/yr net with Chargeflow"));
    assert.ok(html.includes("$9,126/yr net recovered"));
    assert.ok(html.includes("$10,062/yr saved vs. manual in-house handling"));
    assert.ok(html.includes("$11,520/yr"));
    assert.ok(!html.includes("\u2014"));
    assert.ok(!html.includes("&mdash;"));
    assert.ok(!html.includes("SaaSTruth"));
    assert.ok(!html.includes("Erik Bengtsson"));
  });

  check(rel + " math", () => {
    const start = html.indexOf("const MANUAL_WIN");
    const end = html.indexOf("function money");
    assert.ok(start > 0 && end > start);
    const fn = new Function(html.slice(start, end) + "\nreturn calcChargeback(2000, 120, 0.65, 15);");
    const row = fn();
    assert.strictEqual(moneyRound(row.gmvYr), 2880000);
    assert.strictEqual(moneyRound(row.disputesYr), 156);
    assert.strictEqual(moneyRound(row.disputed), 18720);
    assert.strictEqual(moneyRound(row.disputeFees), 2340);
    assert.strictEqual(moneyRound(row.manualRecovered), 3744);
    assert.strictEqual(moneyRound(row.manualUnrecovered), 14976);
    assert.strictEqual(moneyRound(row.labor), 4680);
    assert.strictEqual(moneyRound(row.manualTotal), 21996);
    assert.strictEqual(moneyRound(row.recovered), 12168);
    assert.strictEqual(moneyRound(row.successFee), 3042);
    assert.strictEqual(moneyRound(row.netRecovered), 9126);
    assert.strictEqual(moneyRound(row.unrecovered), 6552);
    assert.strictEqual(moneyRound(row.chargeflowTotal), 11934);
    assert.strictEqual(moneyRound(row.savings), 10062);
    assert.strictEqual(moneyRound(row.stripeProtect), 11520);
  });
}

function usd(n) {
  return "$" + Math.round(n).toLocaleString("en-US");
}

function payoutDispute(vol, disputeRate) {
  const tx = vol / 100;
  const disputesMo = tx * (disputeRate / 100);
  const disputesYr = disputesMo * 12;
  const disputed = disputesYr * 100;
  const fees = disputesYr * 15;
  const labor = disputesYr * 30;
  const drain = disputed + fees + labor;
  const cfNet = Math.round(disputed * 0.65 * 0.75);
  return { tx, disputesMo, disputesYr, disputed, fees, labor, drain, cfNet };
}

function billingDispute(mrr, disputeRate) {
  const txCount = Math.round(mrr / 50);
  const disputesYr = txCount * (disputeRate / 100) * 12;
  const disputedMrr = Math.round(disputesYr * 50);
  const fee = Math.round(disputesYr * 15);
  const prep = Math.round(disputesYr * 15);
  const drain = disputedMrr + fee + prep;
  const cfNet = Math.round(disputedMrr * 0.65 * 0.75);
  return { txCount, disputesYr, disputedMrr, fee, prep, drain, cfNet };
}

function paddleCompareDispute(gmv, disputeRate) {
  const tx = Math.round(gmv / 50);
  const disputesYr = tx * (disputeRate / 100) * 12;
  const disputedRev = Math.round(disputesYr * 50);
  const stripeFees = Math.round(disputesYr * 15);
  const paddleFees = Math.round(disputesYr * 20);
  const cfNet = Math.round(disputedRev * 0.65 * 0.75);
  return {
    stripeLine: disputedRev + stripeFees,
    paddleLine: disputedRev + paddleFees,
    cfNet,
  };
}

function gumroadLost(price, sales, disputePct) {
  const lostYr = price * sales * (disputePct / 100) * 12;
  return { lostYr, cfNet: Math.round(lostYr * 0.65 * 0.75) };
}

check("payout-hold dispute slider and $1,901 Chargeflow CTA", () => {
  const html = fs.readFileSync(
    path.join(__dirname, "..", "public/exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html"),
    "utf8"
  );
  assert.ok(html.includes('id="res-dispute-rate" min="0.1" max="2.0" step="0.05" value="0.65"'));
  assert.ok(html.includes("Dispute / chargeback rate:"));
  assert.ok(html.includes('id="res-output"'));
  assert.ok(html.includes("Recover $1,901/yr"));
  assert.ok(html.includes("prevent reserves with Chargeflow"));
  assert.ok(html.includes('href="https://www.chargeflow.io/"'));
  assert.ok(html.includes('data-track="vendor-cta"'));
  assert.ok(html.includes('data-vendor="chargeflow"'));
  assert.ok(html.includes("Net Annual Recovery with Chargeflow"));
  assert.ok(!html.includes("\u2014") && !html.includes("&mdash;"));
  assert.ok(!html.includes("SaaSTruth") && !html.includes("Erik Bengtsson"));
  const row = payoutDispute(50000, 0.65);
  assert.strictEqual(moneyRound(row.cfNet), 1901);
  assert.strictEqual(moneyRound(row.drain), 5655);
  assert.strictEqual(usd(row.cfNet), "$1,901");
});

check("stripe billing dispute drain and Chargeflow CTA", () => {
  const html = fs.readFileSync(
    path.join(__dirname, "..", "public/pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html"),
    "utf8"
  );
  assert.ok(html.includes('id="sb-dispute-rate" min="0.0" max="2.0" step="0.05" value="0.50"'));
  assert.ok(html.includes("Subscription dispute / chargeback rate:"));
  assert.ok(html.includes("Annual Chargeback &amp; Dispute Drain") || html.includes("Annual Chargeback & Dispute Drain"));
  assert.ok(html.includes("Recover ${usd(cfNet)}/yr net with Chargeflow") || html.includes("Recover $1,170/yr net with Chargeflow"));
  assert.ok(html.includes("Dispute Recovery: Chargeflow Pay-On-Performance"));
  assert.ok(html.includes("Best Value: Whop Payments"));
  assert.ok(html.includes('href="https://www.chargeflow.io/"'));
  assert.ok(html.includes('data-track="vendor-cta" data-vendor="chargeflow"') || (html.includes('data-track="vendor-cta"') && html.includes('data-vendor="chargeflow"')));
  assert.ok(html.includes("Show calculation"));
  assert.ok(!html.includes("\u2014") && !html.includes("&mdash;"));
  assert.ok(!html.includes("SaaSTruth") && !html.includes("Erik Bengtsson"));
  const row = billingDispute(40000, 0.5);
  assert.strictEqual(row.drain, 3840);
  assert.strictEqual(row.cfNet, 1170);
});

check("stripe vs paddle dispute fees and Chargeflow CTA", () => {
  const html = fs.readFileSync(
    path.join(__dirname, "..", "public/faq/stripe-vs-paddle-true-cost/index.html"),
    "utf8"
  );
  assert.ok(html.includes('id="sp-dispute-rate" min="0.0" max="2.0" step="0.05" value="0.50"'));
  assert.ok(html.includes("Dispute / chargeback rate:"));
  assert.ok(html.includes("Annual Chargeback &amp; Dispute Fees") || html.includes("Annual Chargeback & Dispute Fees"));
  assert.ok(html.includes("$15/dispute") || html.includes("$15 Stripe") || html.includes("at $15/dispute"));
  assert.ok(html.includes("$20/dispute") || html.includes("at $20/dispute"));
  assert.ok(html.includes("Recover ${usd(cfNet)}/yr net with Chargeflow") || html.includes("Recover $1,463/yr net with Chargeflow"));
  assert.ok(html.includes("Dispute Recovery: Chargeflow Pay-On-Performance"));
  assert.ok(html.includes("Best Value: Whop Payments"));
  assert.ok(html.includes('href="https://www.chargeflow.io/"'));
  assert.ok(html.includes('data-vendor="chargeflow"'));
  assert.ok(!html.includes("\u2014") && !html.includes("&mdash;"));
  assert.ok(!html.includes("SaaSTruth") && !html.includes("Erik Bengtsson"));
  const row = paddleCompareDispute(50000, 0.5);
  assert.strictEqual(row.stripeLine, 3900);
  assert.strictEqual(row.paddleLine, 4200);
  assert.strictEqual(row.cfNet, 1463);
});

check("gumroad chargeback recovery callout", () => {
  const html = fs.readFileSync(
    path.join(__dirname, "..", "public/compare/gumroad-vs-whop-vs-lemon-squeezy-take-rate-calculator/index.html"),
    "utf8"
  );
  assert.ok(html.includes('id="tr-dispute"'));
  assert.ok(html.includes('id="tr-chargeflow"'));
  assert.ok(html.includes("Dispute Recovery: Chargeflow"));
  assert.ok(html.includes("Recover $170/yr in disputes with Chargeflow"));
  assert.ok(html.includes("$0/mo, 25% fee only on won disputes"));
  assert.ok(html.includes('href="https://www.chargeflow.io/"'));
  assert.ok(html.includes('data-track="vendor-cta"'));
  assert.ok(html.includes('data-vendor="chargeflow"'));
  assert.ok(!html.includes("\u2014") && !html.includes("&mdash;"));
  assert.ok(!html.includes("SaaSTruth") && !html.includes("Erik Bengtsson"));
  const row = gumroadLost(29, 200, 0.5);
  assert.strictEqual(Math.round(row.lostYr), 348);
  assert.strictEqual(row.cfNet, 170);
});

check("homepage dispute exposure in payment breakdown", () => {
  const html = fs.readFileSync(path.join(__dirname, "..", "public/index.html"), "utf8");
  assert.ok(html.includes("Dispute & chargeback exposure"));
  assert.ok(html.includes("0.5%\u20130.75%"));
  assert.ok(html.includes("25% performance fee"));
  assert.ok(html.includes("stripe-payments"));
  assert.ok(html.includes("paddle-mor"));
  assert.ok(html.includes("lemon-squeezy"));
  assert.ok(html.includes("Won-dispute recovery"));
  assert.ok(!html.includes("\u2014") && !html.includes("&mdash;"));
  assert.ok(!html.includes("SaaSTruth") && !html.includes("Erik Bengtsson"));
});

if (failed) {
  console.error(failed + " failed");
  process.exit(1);
}
console.log("All chargeback calculator checks passed.");

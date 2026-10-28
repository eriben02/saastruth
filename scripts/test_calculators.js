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

if (failed) {
  console.error(failed + " failed");
  process.exit(1);
}
console.log("All chargeback calculator checks passed.");

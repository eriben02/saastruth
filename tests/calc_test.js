/**
 * Calculation drawer checks. Run: node tests/calc_test.js
 * Confirms the short label, one body wrapper, and popover CSS.
 */
const fs = require("fs");
const path = require("path");
const assert = require("assert");

const root = path.join(__dirname, "..");
const pages = [
  "public/index.html",
  "public/pricing/hubspot-true-cost-and-onboarding-fees/index.html",
  "public/chargeback-fee-and-recovery-calculator/index.html",
  "public/exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html",
  "public/pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html",
  "public/faq/stripe-vs-paddle-true-cost/index.html",
];

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
  const html = fs.readFileSync(path.join(root, rel), "utf8");
  check(rel + " label", () => {
    assert.ok(html.includes(">Show calculation<"), rel);
    assert.ok(!html.includes("See exactly how we calculated this"), rel);
    assert.ok(!html.includes(">See calculation<"), rel);
    assert.ok(html.includes('class="math-drawer"'), rel);
    assert.ok(html.includes('class="math-drawer-body"'), rel);
    assert.ok(html.includes("assets/app.js"), rel);
  });
}

check("app.js closes other drawers and outside clicks", () => {
  const js = fs.readFileSync(path.join(root, "public/assets/app.js"), "utf8");
  assert.ok(js.includes('details.math-drawer[open]'));
  assert.ok(js.includes("Escape"));
  assert.ok(js.includes("drawer.contains(event.target)"));
});

check("popover css does not grow the card", () => {
  const css = fs.readFileSync(path.join(root, "public/assets/styles.css"), "utf8");
  assert.ok(css.includes(".math-drawer > summary"));
  assert.ok(css.includes("position: absolute;"));
  assert.ok(css.includes("top: calc(100% + 8px);"));
  assert.ok(css.includes("z-index: 40"));
  assert.ok(css.includes(".summary-card:has(.math-drawer[open])"));
  assert.ok(css.includes("overflow: visible;"));
});

if (failed) {
  console.error(failed + " failed");
  process.exit(1);
}
console.log("All calculation drawer checks passed.");

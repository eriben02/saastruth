"""Chargeback calculator and the live Chargeflow listing."""
import json
import os
import subprocess
import unittest

BASE_DIR = "/workspace/saastruth"
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

import sys
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
import build_chargeback_calculator as cb


class TestChargebackCalculator(unittest.TestCase):
    def test_default_math_matches_the_page_formula(self):
        row = cb.calc_chargeback(2000, 120, 0.65, 15)
        expected = {
            "gmv_yr": 2880000,
            "disputes_yr": 156,
            "disputed": 18720,
            "fees": 2340,
            "manual": 21996,
            "manual_recovered": 3744,
            "recovered": 12168,
            "success_fee": 3042,
            "net_recovered": 9126,
            "stripe_protect": 11520,
            "chargeflow": 11934,
            "savings": 10062,
        }
        for key, value in expected.items():
            self.assertEqual(round(row[key]), value, key)

    def test_pages_lead_cta_and_workbench(self):
        pages = [
            (
                "chargeback-fee-and-recovery-calculator/index.html",
                "https://saasbill.io/chargeback-fee-and-recovery-calculator/",
            ),
            (
                "pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/index.html",
                "https://saasbill.io/pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/",
            ),
        ]
        lead = (
            "Every chargeback costs the full order value plus a non-refundable $15 to $25 processor dispute fee. "
            "Adjust your monthly volume and dispute rate below to see total annual loss versus automated recovery."
        )
        h1 = "Stripe & Shopify Chargeback Cost Calculator (2026): Dispute Fees, Lost Revenue & Chargeflow ROI"
        for rel, canonical in pages:
            with open(os.path.join(PUBLIC_DIR, rel), encoding="utf-8") as f:
                html = f.read()
            self.assertIn(f'<link rel="canonical" href="{canonical}" />', html)
            self.assertIn(f"<h1>{h1}</h1>", html)
            self.assertIn(f'<p class="lead">{lead}</p>', html)
            self.assertIn('class="calc-box editorial-workbench"', html)
            self.assertIn('class="wb-col-controls"', html)
            self.assertIn('class="wb-result-col"', html)
            self.assertIn('id="cb-orders" min="100" max="25000" step="100" value="2000"', html)
            self.assertIn('id="cb-aov" min="20" max="500" step="5" value="120"', html)
            self.assertIn('id="cb-rate" min="10" max="200" step="5" value="65"', html)
            self.assertIn('class="val-pill"', html)
            self.assertIn("Stripe ($15 dispute fee + $15 counter fee)", html)
            self.assertIn("Shopify Payments ($15 dispute fee)", html)
            self.assertIn("Paddle ($20 dispute fee)", html)
            self.assertNotIn("High-Volume / High-Risk", html)
            self.assertIn("0.75% Visa", html)
            self.assertIn("1.00% Mastercard", html)
            self.assertIn("See exactly how we calculated this", html)
            self.assertIn('id="full-table-details"', html)
            self.assertIn("Compare all tools in this category", html)
            self.assertIn("Shopify Protect", html)
            self.assertIn("Shop Pay, US only", html)
            self.assertIn('data-track="vendor_cta_click"', html)
            self.assertIn('data-vendor="chargeflow"', html)
            self.assertIn("https://www.chargeflow.io/pricing", html)
            self.assertIn("Recover $9,126/yr net with Chargeflow", html)
            self.assertIn("Manual In-House Dispute Handling", html)
            self.assertIn("Chargeflow Pay-On-Performance", html)
            self.assertIn("best-card", html)
            self.assertIn("Baseline (20% Win Rate)", html)
            self.assertIn("Highest Net Recovery", html)
            self.assertIn("Stripe Chargeback Protection (0.40% of GMV)", html)
            self.assertIn("Flat Volume Fee", html)
            self.assertIn("$9,126/yr net recovered", html)
            self.assertIn("$10,062/yr saved vs. manual in-house handling", html)
            self.assertIn('class="summary-strip"', html)
            for bad in ["—", "&mdash;", "SaaSTruth", "Erik Bengtsson"]:
                self.assertNotIn(bad, html, rel)
            start = html.find("const MANUAL_WIN")
            end = html.find("function money")
            self.assertGreater(start, 0, rel)
            self.assertGreater(end, start, rel)
            runner = html[start:end] + """
            const row = calcChargeback(2000, 120, 0.65, 15);
            console.log(JSON.stringify(row));
            """
            res = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
            out = json.loads(res.stdout)
            self.assertEqual(round(out["gmvYr"]), 2880000)
            self.assertEqual(round(out["stripeProtect"]), 11520)
            self.assertEqual(round(out["chargeflowTotal"]), 11934)
            self.assertEqual(round(out["netRecovered"]), 9126)
            self.assertEqual(round(out["manualTotal"]), 21996)
            self.assertEqual(round(out["manualRecovered"]), 3744)
            self.assertEqual(round(out["recovered"]), 12168)
            self.assertEqual(round(out["successFee"]), 3042)
            self.assertEqual(round(out["savings"]), 10062)

    def test_cross_links_and_sitemap(self):
        checks = [
            "index.html",
            "pricing/stripe-billing-0-7-percent-recurring-tax-calculator/index.html",
            "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html",
        ]
        for rel in checks:
            with open(os.path.join(PUBLIC_DIR, rel), encoding="utf-8") as f:
                html = f.read()
            self.assertIn("chargeback-fee-and-recovery-calculator/", html, rel)
        with open(os.path.join(PUBLIC_DIR, "sitemap.xml"), encoding="utf-8") as f:
            sitemap = f.read()
        self.assertEqual(sitemap.count("<url><loc>"), 29)
        self.assertIn("https://saasbill.io/chargeback-fee-and-recovery-calculator/", sitemap)
        self.assertIn(
            "https://saasbill.io/pricing/stripe-shopify-chargeback-fee-and-chargeflow-roi-calculator/",
            sitemap,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

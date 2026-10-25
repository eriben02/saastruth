import json
import os
import re
import subprocess
import unittest
from urllib.parse import urlparse

BASE_DIR = "/workspace/saastruth"
DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")


def load_tools_and_affiliates():
    with open(os.path.join(DATA_DIR, "tools.json")) as f:
        tools = json.load(f)
    with open(os.path.join(DATA_DIR, "affiliate_links.json")) as f:
        affiliates = json.load(f)
    return {t["id"]: t for t in tools}, tools, affiliates


def run_homepage_js_calc(seats, ai_vol, mode, cat="ALL"):
    """Executes the exact JS calculator functions embedded in public/index.html via Node.js."""
    with open(os.path.join(PUBLIC_DIR, "index.html")) as f:
        html = f.read()
    m = re.search(r"<script>\s*(const TOOLS = .*?)\['cat-filter'", html, re.S)
    if not m:
        raise RuntimeError("Could not extract calculator script from public/index.html")
    js_core = m.group(1)
    runner = f"""
    {js_core}
    const cat = {json.dumps(cat)};
    const seats = {seats};
    const aiVol = {ai_vol};
    const mode = {json.dumps(mode)};
    const filtered = TOOLS.filter(t => {{
      if (cat === 'ALL') return t.category !== 'Payment Processors & MoR';
      return t.category === cat;
    }});
    const rows = filtered.map(t => calcToolYear1(t, seats, aiVol, mode));
    rows.sort((a, b) => a.year1Total - b.year1Total);
    console.log(JSON.stringify(rows));
    """
    res = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


class TestSaaSBillCalculators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools_by_id, cls.tools_list, cls.affiliates = load_tools_and_affiliates()

    def test_1_user_vs_5_users_seat_minimums(self):
        """1 user vs 5 users: monday CRM 3-seat minimum & buckets, Close CRM 1:1, Pipedrive 1:1, HubSpot Marketing Pro 3-seat base."""
        rows_1 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=1, ai_vol=0, mode="annual")}
        rows_4 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=4, ai_vol=0, mode="annual")}
        rows_5 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=0, mode="annual")}

        # monday-crm (Basic: $12/seat annual): 1 user -> 3 billed seats ($36/mo = $432/yr); 4 users -> 5 billed seats ($60/mo = $720/yr)
        self.assertEqual(rows_1["monday-crm"]["effSeats"], 3)
        self.assertEqual(rows_1["monday-crm"]["year1Total"], 3 * 12 * 12)
        self.assertEqual(rows_4["monday-crm"]["effSeats"], 5)
        self.assertEqual(rows_4["monday-crm"]["year1Total"], 5 * 12 * 12)
        self.assertEqual(rows_5["monday-crm"]["effSeats"], 5)
        self.assertEqual(rows_5["monday-crm"]["year1Total"], 5 * 12 * 12)

        # close-crm (Essentials: $35/user annual): 1 user -> $35*12 = $420/yr; 5 users -> 5*$35*12 = $2,100/yr
        self.assertEqual(rows_1["close-crm"]["effSeats"], 1)
        self.assertEqual(rows_1["close-crm"]["year1Total"], 1 * 35 * 12)
        self.assertEqual(rows_5["close-crm"]["effSeats"], 5)
        self.assertEqual(rows_5["close-crm"]["year1Total"], 5 * 35 * 12)

        # pipedrive-crm: 1:1 seat billing ($14/mo = $168/yr for 1 user; $70/mo = $840/yr for 5 users)
        self.assertEqual(rows_1["pipedrive-crm"]["effSeats"], 1)
        self.assertEqual(rows_1["pipedrive-crm"]["year1Total"], 1 * 14 * 12)
        self.assertEqual(rows_5["pipedrive-crm"]["effSeats"], 5)
        self.assertEqual(rows_5["pipedrive-crm"]["year1Total"], 5 * 14 * 12)

        # hubspot-marketing-pro: $800/mo includes 3 seats (+$3,000 onboarding = $12,600/yr at 1-3 seats); at 5 seats adds 2 * $45 = $890/mo ($13,680/yr)
        self.assertEqual(rows_1["hubspot-marketing-pro"]["monthlySoftware"], 800)
        self.assertEqual(rows_1["hubspot-marketing-pro"]["year1Total"], 800 * 12 + 3000)
        self.assertEqual(rows_5["hubspot-marketing-pro"]["monthlySoftware"], 890)
        self.assertEqual(rows_5["hubspot-marketing-pro"]["year1Total"], 890 * 12 + 3000)

    def test_annual_vs_monthly_billing(self):
        """Annual vs Monthly billing for HubSpot, Jotform HIPAA, Close CRM, monday CRM, and 1Password Business."""
        rows_ann_1 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=1, ai_vol=0, mode="annual")}
        rows_mo_1 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=1, ai_vol=0, mode="monthly")}
        rows_ann = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=0, mode="annual")}
        rows_mo = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=0, mode="monthly")}

        # HubSpot Sales Pro (5 seats): $90*5*12 + $1500 = $6,900 annual; $100*5*12 + $1500 = $7,500 monthly
        self.assertEqual(rows_ann["hubspot-sales-pro"]["year1Total"], 6900)
        self.assertEqual(rows_mo["hubspot-sales-pro"]["year1Total"], 7500)

        # Jotform HIPAA Gold (1-user flat plan): $99*12 = $1,188 annual; $129*12 = $1,548 monthly
        self.assertEqual(self.tools_by_id["jotform-hipaa"]["advertised_monthly_price_usd"], 99)
        self.assertEqual(self.tools_by_id["jotform-hipaa"]["monthly_billing_price_usd"], 129)
        self.assertEqual(rows_ann["jotform-hipaa"]["year1Total"], 1188)
        self.assertEqual(rows_mo["jotform-hipaa"]["year1Total"], 1548)

        # Close CRM (Essentials): $35/user/mo annual vs $49/user/mo monthly
        self.assertEqual(self.tools_by_id["close-crm"]["name"], "Close CRM (Essentials)")
        self.assertEqual(self.tools_by_id["close-crm"]["advertised_monthly_price_usd"], 35)
        self.assertEqual(self.tools_by_id["close-crm"]["monthly_billing_price_usd"], 49)
        self.assertEqual(rows_ann["close-crm"]["year1Total"], 5 * 35 * 12)  # $2,100
        self.assertEqual(rows_mo["close-crm"]["year1Total"], 5 * 49 * 12)   # $2,940

        # monday CRM (Basic): $12/seat/mo annual vs $18/seat/mo monthly (with 3-seat minimum)
        self.assertEqual(self.tools_by_id["monday-crm"]["name"], "monday CRM (Basic)")
        self.assertEqual(self.tools_by_id["monday-crm"]["advertised_monthly_price_usd"], 12)
        self.assertEqual(self.tools_by_id["monday-crm"]["monthly_billing_price_usd"], 18)
        self.assertEqual(rows_ann_1["monday-crm"]["year1Total"], 3 * 12 * 12)  # $432
        self.assertEqual(rows_mo_1["monday-crm"]["year1Total"], 3 * 18 * 12)   # $648
        self.assertEqual(rows_ann["monday-crm"]["year1Total"], 5 * 12 * 12)    # $720
        self.assertEqual(rows_mo["monday-crm"]["year1Total"], 5 * 18 * 12)     # $1,080

        # 1Password Business: $8.99/user/mo annual vs $10.99/user/mo monthly
        self.assertEqual(self.tools_by_id["1password-business"]["advertised_monthly_price_usd"], 8.99)
        self.assertEqual(self.tools_by_id["1password-business"]["monthly_billing_price_usd"], 10.99)
        self.assertEqual(rows_ann_1["1password-business"]["year1Total"], round(1 * 8.99 * 12))  # $108
        self.assertEqual(rows_mo_1["1password-business"]["year1Total"], round(1 * 10.99 * 12))  # $132
        self.assertEqual(rows_ann["1password-business"]["year1Total"], round(5 * 8.99 * 12))    # $539
        self.assertEqual(rows_mo["1password-business"]["year1Total"], round(5 * 10.99 * 12))    # $659

    def test_zero_vs_high_ai_volume_and_included_allowances(self):
        """0 AI vs 1,000 AI tickets/month across Intercom, Help Scout, Zendesk Team & Pro, and Freshdesk."""
        rows_0 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=0, mode="annual")}
        rows_1k_ann = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=1000, mode="annual")}
        rows_1k_mo = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=1000, mode="monthly")}

        self.assertEqual(rows_0["intercom-fin-ai"]["year1Total"], 1740)
        self.assertEqual(rows_1k_ann["intercom-fin-ai"]["year1Total"], 1740 + 11880)

        self.assertEqual(rows_0["help-scout-plus"]["year1Total"], 2700)
        self.assertEqual(rows_1k_ann["help-scout-plus"]["year1Total"], 2700 + 9000)

        self.assertEqual(rows_0["zendesk-suite-team"]["year1Total"], 3300)
        self.assertEqual(rows_1k_ann["zendesk-suite-team"]["year1Total"], 3300 + 17550)
        self.assertEqual(rows_1k_mo["zendesk-suite-team"]["year1Total"], 4140 + 23400)

        self.assertEqual(rows_0["zendesk-suite-professional"]["year1Total"], 6900)
        self.assertEqual(rows_1k_ann["zendesk-suite-professional"]["year1Total"], 6900 + 17100)
        self.assertEqual(rows_1k_mo["zendesk-suite-professional"]["year1Total"], 8940 + 22800)

        self.assertEqual(rows_0["freshdesk-support"]["year1Total"], 1140)
        self.assertEqual(rows_1k_ann["freshdesk-support"]["year1Total"], 1140 + 115 * 49)

    def test_payment_processors_excluded_from_default_all_ranking(self):
        """Payment processors must not appear as $0/yr 'cheapest' tools in the default ALL seat-based view."""
        default_rows = run_homepage_js_calc(seats=5, ai_vol=500, mode="annual", cat="ALL")
        self.assertEqual(len(default_rows), 15)
        for r in default_rows:
            self.assertNotEqual(r["tool"]["category"], "Payment Processors & MoR")
            self.assertGreater(r["year1Total"], 0)

        payment_rows = run_homepage_js_calc(seats=5, ai_vol=500, mode="annual", cat="Payment Processors & MoR")
        self.assertEqual(len(payment_rows), 5)

    def test_hipaa_and_soc2_flat_vs_per_seat_rules(self):
        """Jotform Gold ($99/mo), Vanta ($833/mo), and Drata ($625/mo) are flat fees; 1Password ($8.99/mo) scales per seat."""
        rows_1 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=1, ai_vol=0, mode="annual")}
        rows_10 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=10, ai_vol=0, mode="annual")}

        self.assertEqual(rows_1["jotform-hipaa"]["year1Total"], 99 * 12)
        self.assertEqual(rows_10["jotform-hipaa"]["year1Total"], 99 * 12)
        self.assertEqual(rows_1["vanta-soc2"]["year1Total"], 833 * 12)
        self.assertEqual(rows_10["vanta-soc2"]["year1Total"], 833 * 12)
        self.assertEqual(rows_1["drata-soc2"]["year1Total"], 625 * 12)
        self.assertEqual(rows_10["drata-soc2"]["year1Total"], 625 * 12)
        self.assertEqual(rows_1["1password-business"]["year1Total"], round(1 * 8.99 * 12))
        self.assertEqual(rows_10["1password-business"]["year1Total"], round(10 * 8.99 * 12))

    def test_stacked_bar_cost_composition_identity(self):
        """Stacked bar segments (annualSeatsCost + onboarding + aiAnnual) must sum identically to year1Total."""
        for seats in (1, 5, 12):
            for ai_vol in (0, 500, 2000):
                for mode in ("annual", "monthly"):
                    rows = run_homepage_js_calc(seats=seats, ai_vol=ai_vol, mode=mode, cat="ALL")
                    for r in rows:
                        comp_sum = r["annualSeatsCost"] + r["onboarding"] + r["aiAnnual"]
                        self.assertEqual(
                            comp_sum,
                            r["year1Total"],
                            f"Component sum mismatch for {r['tool']['id']} at seats={seats}, ai={ai_vol}, mode={mode}",
                        )
                        self.assertGreaterEqual(r["annualSeatsCost"], 0)
                        self.assertGreaterEqual(r["onboarding"], 0)
                        self.assertGreaterEqual(r["aiAnnual"], 0)

    def test_verification_status_and_inline_sources(self):
        """Every tool must have a valid verification_status ('Verified' or 'Estimated (Benchmark)') and valid https source_urls."""
        valid_statuses = {"Verified", "Estimated (Benchmark)"}
        for t in self.tools_list:
            self.assertIn(t.get("verification_status"), valid_statuses, f"Invalid status on {t['id']}")
            urls = t.get("source_urls") or []
            self.assertGreater(len(urls), 0, f"Missing source_urls on {t['id']}")
            for u in urls:
                self.assertTrue(u.startswith("https://"), f"Non-https source URL {u} on {t['id']}")

        self.assertEqual(self.tools_by_id["vanta-soc2"]["verification_status"], "Estimated (Benchmark)")
        self.assertEqual(self.tools_by_id["drata-soc2"]["verification_status"], "Estimated (Benchmark)")

        with open(os.path.join(PUBLIC_DIR, "index.html")) as f:
            index_html = f.read()
        self.assertIn('id="wb-vbar-mount"', index_html)
        self.assertIn('id="wb-result-mount"', index_html)
        self.assertIn('id="methodology"', index_html)
        self.assertIn("mobile-cards", index_html)
        self.assertIn('data-label="Platform"', index_html)
        self.assertNotIn("$7.99", index_html)

    def test_outbound_vendor_links_match_vendors(self):
        """Every tool in tools.json and every CTA link across all 7 HTML pages must point to the right vendor."""
        expected_domains = {
            "hubspot-sales-pro": "hubspot.com",
            "hubspot-marketing-pro": "hubspot.com",
            "hubspot-service-hub": "hubspot.com",
            "close-crm": "close.com",
            "pipedrive-crm": "pipedrive.com",
            "monday-crm": "monday.com",
            "intercom-fin-ai": "intercom.com",
            "freshdesk-support": "freshworks.com",
            "zendesk-suite-team": "zendesk.com",
            "zendesk-suite-professional": "zendesk.com",
            "help-scout-plus": "helpscout.com",
            "stripe-payments": "stripe.com",
            "paddle-mor": "paddle.com",
            "whop-payments": "whop.com",
            "lemon-squeezy": "lemonsqueezy.com",
            "chargeflow": "chargeflow.io",
            "jotform-hipaa": "jotform.com",
            "1password-business": "1password.com",
            "vanta-soc2": "vanta.com",
            "drata-soc2": "drata.com",
        }
        for tool_id, expected_domain in expected_domains.items():
            tool = self.tools_by_id[tool_id]
            slug = tool["affiliate_slug"]
            self.assertIn(slug, self.affiliates, f"Missing affiliate slug {slug} for {tool_id}")
            dest_url = self.affiliates[slug]["destination_url"]
            host = urlparse(dest_url).netloc.lower()
            self.assertTrue(
                host == expected_domain or host.endswith("." + expected_domain),
                f"Tool {tool_id} links to {dest_url} (expected {expected_domain})",
            )

        comp_page = os.path.join(PUBLIC_DIR, "compliance/hipaa-baa-and-soc2-pricing-tiers/index.html")
        with open(comp_page) as f:
            comp_html = f.read()
        self.assertIn("https://trycomp.ai/", comp_html)
        self.assertIn("https://1password.com/pricing/business", comp_html)
        self.assertIn("$8.99/user/mo", comp_html)
        self.assertNotIn("$7.99", comp_html)

        hs_page = os.path.join(PUBLIC_DIR, "pricing/hubspot-true-cost-and-onboarding-fees/index.html")
        with open(hs_page) as f:
            hs_html = f.read()
        self.assertIn("seats * 35", hs_html)
        self.assertIn("Close CRM (Essentials)", hs_html)

        ic_page = os.path.join(PUBLIC_DIR, "pricing/intercom-fin-ai-resolution-cost-calculator/index.html")
        with open(ic_page) as f:
            ic_html = f.read()
        self.assertIn("seats * 55", ic_html)
        self.assertIn("fdMonthlyPacks * 49", ic_html)

    def test_handoff2_conversion_ux_and_honest_ctas(self):
        """Verify Handoff 2 conversion & UX requirements across all 7 generated HTML pages."""
        pages = [
            "index.html",
            "pricing/hubspot-true-cost-and-onboarding-fees/index.html",
            "pricing/intercom-fin-ai-resolution-cost-calculator/index.html",
            "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html",
            "compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html",
            "compliance/hipaa-baa-and-soc2-pricing-tiers/index.html",
            "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html",
        ]
        summary_ids = {
            "index.html": "wb-result-mount",
            "pricing/hubspot-true-cost-and-onboarding-fees/index.html": "hs-summary",
            "pricing/intercom-fin-ai-resolution-cost-calculator/index.html": "ic-summary",
            "exit/stripe-shopify-paddle-frozen-funds-alternatives/index.html": "hold-summary",
            "compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/index.html": "sm-summary",
            "compliance/hipaa-baa-and-soc2-pricing-tiers/index.html": "soc2-summary",
            "pricing/zendesk-ai-resolution-and-automated-outcome-cost/index.html": "zd-summary",
        }
        forbidden_phrases = [
            "Partner link",
            "sponsored",
            "Check pricing",
            "Try Close free",
            "Try Pipedrive free",
            "Try Freshdesk free",
            "Try Help Scout free",
            "Request Vanta quote",
            "Request Drata quote",
            "Add Whop failover",
            "Install Chargeflow",
        ]
        for rel in pages:
            full_path = os.path.join(PUBLIC_DIR, rel)
            with open(full_path) as f:
                html = f.read()
            for phrase in forbidden_phrases:
                self.assertNotIn(phrase, html, f"Forbidden phrase '{phrase}' found in {rel}")
            self.assertIn(f'id="{summary_ids[rel]}"', html, f"Missing summary strip #{summary_ids[rel]} in {rel}")
            self.assertIn("Based on ", html, f"Missing scenario description ('Based on ...') in {rel}")
            self.assertIn("Hidden Cost Highlight:", html, f"Missing 'Hidden Cost Highlight:' in {rel}")
            self.assertIn('data-track="vendor-cta"', html, f"Missing data-track='vendor-cta' in {rel}")
            self.assertIn("Direct vendor link", html, f"Missing 'Direct vendor link' label in {rel}")
            self.assertIn("window.__saasbillEvents", html, f"Missing local __saasbillEvents instrumentation in {rel}")
            # Ensure no external analytics tracker is loaded
            self.assertNotIn("googletagmanager.com", html)
            self.assertNotIn("plausible.io", html)
            self.assertNotIn("posthog.com", html)

        # Verify homepage pre-filled category tabs and vendor-specific CTA dictionary
        with open(os.path.join(PUBLIC_DIR, "index.html")) as f:
            index_html = f.read()
        self.assertIn('class="cat-tabs"', index_html)
        self.assertIn('data-track="category-select"', index_html)
        self.assertIn('<option value="Helpdesk & AI Support" selected>', index_html)
        for expected_cta in [
            "View HubSpot pricing",
            "View Close pricing",
            "View Pipedrive pricing",
            "View monday CRM pricing",
            "View Intercom pricing",
            "View Freshdesk pricing",
            "View Zendesk pricing",
            "View Help Scout pricing",
            "View Vanta pricing",
            "View Drata pricing",
            "View Jotform HIPAA pricing",
            "View 1Password pricing",
            "View Stripe pricing",
            "View Whop Payments pricing",
            "View Chargeflow pricing",
            "View Paddle pricing",
            "View Lemon Squeezy pricing",
        ]:
            self.assertIn(expected_cta, index_html, f"Missing specific CTA '{expected_cta}' in index.html")

        # Verify Editorial Layout v2: no prefill-banner clutter, 3-column workbench, and Sage Green palette
        self.assertNotIn('id="calc-prefill-banner"', index_html)
        self.assertIn('id="wb-vbar-mount"', index_html)
        self.assertIn('id="wb-big-amount"', index_html)

        with open(os.path.join(PUBLIC_DIR, "assets/styles.css")) as f:
            css = f.read()
        for token in ["#FAF9F5", "#536B56", "#E8EEE6", "#20231F", ".prefill-banner", ".direct-link-tag"]:
            self.assertIn(token, css, f"Missing Sage Green / UX Finishing Pass token '{token}' in styles.css")


    def test_payment_processor_scenario_transparency_and_math_identity(self):
        """Verify Payment Processors & MoR separate processing fees (b + s + h == total) from temporary reserves (held), unify CTAs, and tone down hero lead."""
        with open(os.path.join(PUBLIC_DIR, "index.html")) as f:
            html = f.read()
        self.assertIn("can significantly increase the real Year-1 cost", html)
        self.assertNotIn("often doubling", html)
        self.assertNotIn("Explore Whop Payments", html)

        m = re.search(r"const PAY_PROFILES = (\{.*?\n\});", html, re.S)
        self.assertIsNotNone(m, "Could not find PAY_PROFILES in public/index.html")
        runner = f"const PAY_PROFILES = {m.group(1)}; console.log(JSON.stringify(PAY_PROFILES));"
        res = subprocess.run(["node", "-e", runner], capture_output=True, text=True, check=True)
        profiles = json.loads(res.stdout)
        expected_totals_and_holds = {
            "stripe-payments": (2325, 12500),
            "paddle-mor": (3450, 12500),
            "whop-payments": (2275, 0),
            "lemon-squeezy": (3475, 12500),
            "chargeflow": (500, 0),
        }
        self.assertEqual(set(profiles.keys()), set(expected_totals_and_holds.keys()))
        for pid, (exp_total, exp_held) in expected_totals_and_holds.items():
            p = profiles[pid]
            self.assertEqual(
                p["b"] + p["s"] + p["h"],
                p["total"],
                f"Payment profile {pid} fee segments ({p['b']} + {p['s']} + {p['h']}) != total ({p['total']})",
            )
            self.assertEqual(p["total"], exp_total, f"Unexpected fee total for {pid}")
            self.assertEqual(p["held"], exp_held, f"Unexpected temporary reserve hold for {pid}")
            self.assertIn("Estimated monthly processing fees:", p["quote"])
            self.assertIn("Potential funds temporarily held:", p["quote"])
            self.assertIn("Assumptions ($50k/mo GMV", p["sub"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

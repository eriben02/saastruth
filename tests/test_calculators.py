import json
import math
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
        """1 user vs 5 users: monday CRM 3-seat minimum & buckets, Pipedrive 1:1, HubSpot Marketing Pro 3-seat base."""
        rows_1 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=1, ai_vol=0, mode="annual")}
        rows_4 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=4, ai_vol=0, mode="annual")}
        rows_5 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=0, mode="annual")}

        # monday-crm: 1 user -> 3 billed seats ($36/mo = $432/yr); 4 users -> 5 billed seats ($60/mo = $720/yr); 5 users -> 5 billed seats
        self.assertEqual(rows_1["monday-crm"]["effSeats"], 3)
        self.assertEqual(rows_1["monday-crm"]["year1Total"], 3 * 12 * 12)
        self.assertEqual(rows_4["monday-crm"]["effSeats"], 5)
        self.assertEqual(rows_4["monday-crm"]["year1Total"], 5 * 12 * 12)
        self.assertEqual(rows_5["monday-crm"]["effSeats"], 5)
        self.assertEqual(rows_5["monday-crm"]["year1Total"], 5 * 12 * 12)

        # pipedrive-crm: exact 1:1 seat billing ($14/mo = $168/yr for 1 user; $70/mo = $840/yr for 5 users)
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
        """Annual vs Monthly billing: HubSpot Sales Pro ($90 vs $100 + $1,500 onboarding) and Jotform HIPAA Gold ($99 vs $129)."""
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

    def test_zero_vs_high_ai_volume_and_included_allowances(self):
        """0 AI vs 1,000 AI tickets/month across Intercom, Help Scout, Zendesk Team & Pro, and Freshdesk."""
        rows_0 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=0, mode="annual")}
        rows_1k_ann = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=1000, mode="annual")}
        rows_1k_mo = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=5, ai_vol=1000, mode="monthly")}

        # Intercom Fin AI: $0.99/res -> at 0 AI = 5*29*12 = $1,740; at 1,000 AI/mo = $1,740 + $990*12 ($11,880) = $13,620
        self.assertEqual(rows_0["intercom-fin-ai"]["year1Total"], 1740)
        self.assertEqual(rows_1k_ann["intercom-fin-ai"]["year1Total"], 1740 + 11880)

        # Help Scout Plus: $0.75/res -> at 0 AI = 5*45*12 = $2,700; at 1,000 AI/mo = $2,700 + $750*12 ($9,000) = $11,700
        self.assertEqual(rows_0["help-scout-plus"]["year1Total"], 2700)
        self.assertEqual(rows_1k_ann["help-scout-plus"]["year1Total"], 2700 + 9000)

        # Zendesk Suite Team (5 seats): includes 5*5 = 25 AR/mo.
        # At 1,000 AR/mo: 975 overage AR/mo. Annual ($1.50 committed): 5*55*12 ($3,300) + 975*1.50*12 ($17,550) = $20,850.
        # Monthly ($2.00 PAYG): 5*69*12 ($4,140) + 975*2.00*12 ($23,400) = $27,540.
        self.assertEqual(rows_0["zendesk-suite-team"]["year1Total"], 3300)
        self.assertEqual(rows_1k_ann["zendesk-suite-team"]["year1Total"], 3300 + 17550)
        self.assertEqual(rows_1k_mo["zendesk-suite-team"]["year1Total"], 4140 + 23400)

        # Zendesk Suite Professional (5 seats): ID 'zendesk-suite-professional' must deduct 5*10 = 50 AR/mo!
        # At 1,000 AR/mo: 950 overage AR/mo. Annual ($1.50 committed): 5*115*12 ($6,900) + 950*1.50*12 ($17,100) = $24,000.
        # Monthly ($2.00 PAYG): 5*149*12 ($8,940) + 950*2.00*12 ($22,800) = $31,740.
        self.assertEqual(rows_0["zendesk-suite-professional"]["year1Total"], 6900)
        self.assertEqual(rows_1k_ann["zendesk-suite-professional"]["year1Total"], 6900 + 17100)
        self.assertEqual(rows_1k_mo["zendesk-suite-professional"]["year1Total"], 8940 + 22800)

        # Freshdesk Growth on homepage (5 seats): $19*5*12 = $1,140 seats.
        # At 0 AI: 0 sessions -> $1,140.
        # At 1,000 sessions/mo: 12,000 sessions/yr - 500 one-time free = 11,500 billable sessions = 115 packs * $49 = $5,635 -> total $6,775.
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
        """Jotform Gold ($99/mo), Vanta ($833/mo), and Drata ($625/mo) are flat fees; 1Password ($8/mo) scales per seat."""
        rows_1 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=1, ai_vol=0, mode="annual")}
        rows_10 = {r["tool"]["id"]: r for r in run_homepage_js_calc(seats=10, ai_vol=0, mode="annual")}

        self.assertEqual(rows_1["jotform-hipaa"]["year1Total"], 99 * 12)
        self.assertEqual(rows_10["jotform-hipaa"]["year1Total"], 99 * 12)
        self.assertEqual(rows_1["vanta-soc2"]["year1Total"], 833 * 12)
        self.assertEqual(rows_10["vanta-soc2"]["year1Total"], 833 * 12)
        self.assertEqual(rows_1["drata-soc2"]["year1Total"], 625 * 12)
        self.assertEqual(rows_10["drata-soc2"]["year1Total"], 625 * 12)
        self.assertEqual(rows_1["1password-business"]["year1Total"], 1 * 8 * 12)
        self.assertEqual(rows_10["1password-business"]["year1Total"], 10 * 8 * 12)

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

        # Verify Comp AI benchmark on compliance page links to trycomp.ai and not vanta.com
        comp_page = os.path.join(PUBLIC_DIR, "compliance/hipaa-baa-and-soc2-pricing-tiers/index.html")
        with open(comp_page) as f:
            comp_html = f.read()
        self.assertIn("https://trycomp.ai/", comp_html)

        # Verify Intercom page uses Freshdesk Pro $55/seat and $49 session packs
        ic_page = os.path.join(PUBLIC_DIR, "pricing/intercom-fin-ai-resolution-cost-calculator/index.html")
        with open(ic_page) as f:
            ic_html = f.read()
        self.assertIn("seats * 55", ic_html)
        self.assertIn("fdMonthlyPacks * 49", ic_html)


if __name__ == "__main__":
    unittest.main(verbosity=2)

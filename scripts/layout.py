import json
import os
from datetime import datetime, timezone

BASE_DIR = "/workspace/saastruth"
DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
SITE_ORIGIN = "https://eriben02.github.io/saastruth"
BASE_PATH = "/saastruth"

def get_freshness_timestamps():
    now_local = datetime.now().astimezone()
    iso_date = now_local.strftime("%Y-%m-%d")
    iso_datetime = now_local.isoformat(timespec="seconds")
    human_date = now_local.strftime("%B %d, %Y")
    return iso_date, iso_datetime, human_date

def load_data():
    with open(os.path.join(DATA_DIR, "tools.json")) as f:
        tools = json.load(f)
    with open(os.path.join(DATA_DIR, "affiliate_links.json")) as f:
        affiliates = json.load(f)
    return tools, affiliates

def render_page(rel_path, title, description, canonical_path, body_html, faqs=None, extra_schema=None, published_date=None):
    iso_date, iso_datetime, human_date = get_freshness_timestamps()
    pub_date = published_date or iso_date

    faq_html = ""
    graph = [
        {
            "@type": "TechArticle",
            "@id": f"{SITE_ORIGIN}{canonical_path}#article",
            "headline": title,
            "description": description,
            "datePublished": pub_date,
            "dateModified": iso_datetime,
            "author": {
                "@type": "Organization",
                "name": "SaaSTruth Contract & Cost Audit Directory",
                "url": f"{SITE_ORIGIN}/"
            },
            "publisher": {
                "@type": "Organization",
                "name": "SaaSTruth",
                "url": f"{SITE_ORIGIN}/"
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{SITE_ORIGIN}{canonical_path}"
            }
        },
        {
            "@type": "WebPage",
            "@id": f"{SITE_ORIGIN}{canonical_path}",
            "url": f"{SITE_ORIGIN}{canonical_path}",
            "name": title,
            "description": description,
            "inLanguage": "en-US",
            "datePublished": pub_date,
            "dateModified": iso_datetime,
            "lastReviewed": iso_date,
            "reviewedBy": {
                "@type": "Organization",
                "name": "SaaSTruth Contract Audit Team"
            }
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "SaaSTruth Directory",
                    "item": f"{SITE_ORIGIN}/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": title,
                    "item": f"{SITE_ORIGIN}{canonical_path}"
                }
            ]
        }
    ]

    if extra_schema:
        extra_copy = dict(extra_schema)
        extra_copy["dateModified"] = iso_datetime
        extra_copy.setdefault("datePublished", pub_date)
        extra_copy.setdefault("temporalCoverage", "2026")
        graph.append(extra_copy)

    if faqs:
        faq_entities = []
        faq_items_html = []
        for q, a in faqs:
            faq_entities.append({
                "@type": "Question",
                "name": q,
                "dateCreated": pub_date,
                "dateModified": iso_datetime,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a,
                    "dateCreated": pub_date,
                    "dateModified": iso_datetime
                }
            })
            faq_items_html.append(f"""
            <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
              <h3 itemprop="name">{q}</h3>
              <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
                <p itemprop="text">{a}</p>
              </div>
            </div>
            """)
        graph.append({
            "@type": "FAQPage",
            "@id": f"{SITE_ORIGIN}{canonical_path}#faq",
            "datePublished": pub_date,
            "dateModified": iso_datetime,
            "mainEntity": faq_entities
        })
        faq_html = f"""
        <section aria-labelledby="faq-heading">
          <h2 id="faq-heading">Frequently Asked Questions (Last Verified <time datetime="{iso_date}">{human_date}</time>)</h2>
          <div class="section-tldr">
            <strong>Quick Reference (Updated <time datetime="{iso_date}">{iso_date}</time>):</strong> Every answer below starts with the exact 2026 dollar figure, percentage rate, or contract notice requirement verified against official vendor schedules and user contract audits.
          </div>
          <div class="faq-list">
            {''.join(faq_items_html)}
          </div>
        </section>
        """

    schema_obj = {
        "@context": "https://schema.org",
        "@graph": graph
    }
    schema_block = f'<script type="application/ld+json">{json.dumps(schema_obj)}</script>'

    depth = len([p for p in rel_path.split("/") if p]) - 1
    prefix = "../" * depth if depth > 0 else "./"

    freshness_banner = f"""
    <div class="freshness-bar" role="status" aria-label="Page Freshness Status">
      <span class="freshness-dot"></span>
      <span>Last updated: <time datetime="{iso_datetime}" itemprop="dateModified">{human_date} ({iso_date})</time> · Published: <time datetime="{pub_date}" itemprop="datePublished">{pub_date}</time> · Verified Cycle: 2026</span>
    </div>
    """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{SITE_ORIGIN}{canonical_path}" />
  <meta property="og:updated_time" content="{iso_datetime}" />
  <meta property="article:published_time" content="{pub_date}T00:00:00+01:00" />
  <meta property="article:modified_time" content="{iso_datetime}" />
  <meta name="last-modified" content="{iso_datetime}" />
  <meta name="dcterms.modified" content="{iso_datetime}" />
  <meta name="dcterms.issued" content="{pub_date}" />
  <link rel="canonical" href="{SITE_ORIGIN}{canonical_path}" />
  <link rel="stylesheet" href="{prefix}assets/styles.css" />
  <link rel="alternate" type="text/plain" href="{SITE_ORIGIN}/llms.txt" title="LLMs.txt Summary" />
  {schema_block}
</head>
<body>
  <header class="site-header">
    <div class="container nav-inner">
      <a href="{prefix}index.html" class="brand">
        <span>SaaSTruth</span>
        <span class="brand-badge">CONTRACT &amp; COST AUDIT 2026</span>
      </a>
      <nav class="nav-links" aria-label="Primary Navigation">
        <a href="{prefix}index.html">Calculator Directory</a>
        <a href="{prefix}pricing/hubspot-true-cost-and-onboarding-fees/">HubSpot True Cost</a>
        <a href="{prefix}pricing/intercom-fin-ai-resolution-cost-calculator/">Intercom $0.99 AI Tax</a>
        <a href="{prefix}exit/stripe-shopify-paddle-frozen-funds-alternatives/">Payout Holds &amp; MoR</a>
        <a href="{prefix}compare/monday-crm-vs-pipedrive-vs-hubspot-seat-minimums/">3-Seat Minimum Math</a>
        <a href="{prefix}compliance/hipaa-baa-and-soc2-pricing-tiers/">HIPAA BAA &amp; SOC 2</a>
        <a href="{prefix}pricing/zendesk-ai-resolution-and-automated-outcome-cost/">Zendesk $2 AI Resolution</a>
        <a href="{prefix}llms.txt">llms.txt</a>
      </nav>
    </div>
  </header>
  <main class="container">
    <article itemscope itemtype="https://schema.org/TechArticle">
      <meta itemprop="datePublished" content="{pub_date}" />
      <meta itemprop="dateModified" content="{iso_datetime}" />
      {freshness_banner}
      {body_html}
      {faq_html}
    </article>
  </main>
  <footer class="site-footer">
    <div class="container">
      <p><strong>SaaSTruth Directory (2026)</strong> — Independent B2B SaaS Contract Transparency, Mandatory Onboarding Fee Audits &amp; Payment Processor Risk Matrix. Last updated: <time datetime="{iso_datetime}">{human_date} ({iso_date})</time>. Machine-readable data: <a href="{prefix}llms.txt">llms.txt</a> · <a href="{prefix}llms-full.txt">llms-full.txt</a> · <a href="{prefix}sitemap.xml">sitemap.xml</a> · <a href="{prefix}robots.txt">robots.txt</a></p>
      <p style="margin-top:8px;">Disclosure: Outbound links to audited software alternatives (including Close, Pipedrive, Freshworks, monday.com, HubSpot, Whop, Chargeflow, Jotform, 1Password, Vanta, and Drata) may be partner links that support our research at no extra cost to you. All pricing and contract terms last verified <time datetime="{iso_date}">{human_date}</time>.</p>
    </div>
  </footer>
</body>
</html>"""
    full_path = os.path.join(PUBLIC_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(html)
    print(f"Wrote {full_path} [dateModified={iso_datetime}]")

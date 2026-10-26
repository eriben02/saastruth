import json
import os
from datetime import datetime

BASE_DIR = "/workspace/saastruth"
DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
SITE_ORIGIN = "https://saasbill.io"
BASE_PATH = ""

def get_freshness_timestamps():
    now_local = datetime.now().astimezone()
    iso_date = now_local.strftime("%Y-%m-%d")
    iso_datetime = now_local.isoformat(timespec="seconds")
    human_date = now_local.strftime("%b %d, %Y")
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
    full_title = title if ("saasbill" in title.lower()) else f"{title} – saasbill.io"

    faq_html = ""
    graph = [
        {
            "@type": "TechArticle",
            "@id": f"{SITE_ORIGIN}{canonical_path}#article",
            "headline": full_title,
            "description": description,
            "datePublished": pub_date,
            "dateModified": iso_datetime,
            "author": {
                "@type": "Organization",
                "name": "SaaSBill Editorial",
                "url": f"{SITE_ORIGIN}/"
            },
            "publisher": {
                "@type": "Organization",
                "name": "SaaSBill",
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
            "name": full_title,
            "description": description,
            "inLanguage": "en-US",
            "datePublished": pub_date,
            "dateModified": iso_datetime,
            "lastReviewed": iso_date,
            "reviewedBy": {
                "@type": "Organization",
                "name": "SaaSBill Editorial"
            }
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "SaaSBill",
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
          <h2 id="faq-heading">Common questions</h2>
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

    byline_bar = f'<span class="byline-bar">Updated <time datetime="{iso_date}" itemprop="dateModified">{human_date}</time></span>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{full_title}</title>
  <meta name="description" content="{description}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <meta property="og:site_name" content="SaaSBill" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{full_title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{SITE_ORIGIN}{canonical_path}" />
  <meta property="og:updated_time" content="{iso_datetime}" />
  <meta property="article:published_time" content="{pub_date}T00:00:00+01:00" />
  <meta property="article:modified_time" content="{iso_datetime}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{full_title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="last-modified" content="{iso_datetime}" />
  <meta name="dcterms.modified" content="{iso_datetime}" />
  <meta name="dcterms.issued" content="{pub_date}" />
  <link rel="canonical" href="{SITE_ORIGIN}{canonical_path}" />
  <link rel="stylesheet" href="{prefix}assets/styles.css?v=20261026n" />
  <link rel="alternate" type="text/plain" href="{SITE_ORIGIN}/llms.txt" title="SaaSBill LLMs.txt Summary" />
  <!-- Privacy-friendly analytics by Plausible -->
  <script defer data-domain="saasbill.io" src="https://plausible.io/js/pa-VAaSVNs5XOobt9cv2UtKo.js"></script>
  <script>
    window.plausible=window.plausible||function(){{(plausible.q=plausible.q||[]).push(arguments)}},plausible.init=plausible.init||function(i){{plausible.o=i||{{}}}};
    plausible.init()
  </script>
  {schema_block}
</head>
<body>
  <header class="site-header">
    <div class="container nav-inner">
      <div class="brand-wrap">
        <a href="{prefix}index.html" class="brand">SaaSBill<span>.io</span></a>
        <span class="brand-tagline">Independent software cost &amp; contract audits</span>
      </div>
      <nav class="nav-links" aria-label="Primary Navigation">
        <a href="{prefix}index.html#all-calculators">Audits &amp; Guides</a>
        <a href="{prefix}index.html#methodology">Methodology</a>
        {byline_bar}
      </nav>
    </div>
  </header>
  <main class="container">
    <article itemscope itemtype="https://schema.org/TechArticle">
      <meta itemprop="datePublished" content="{pub_date}" />
      <meta itemprop="dateModified" content="{iso_datetime}" />
      {body_html}
      {faq_html}
    </article>
  </main>
  <footer class="site-footer">
    <div class="container">
      <p><strong>SaaSBill</strong> &mdash; Independent Year-1 cost calculators for B2B software.</p>
      <p class="footer-note">Updated <time datetime="{iso_date}">{human_date}</time> &middot; Some links are affiliate links &middot; Inquiries: <a href="mailto:info@saasbill.io">info@saasbill.io</a></p>
    </div>
  </footer>
  <script>
  /* Local event buffer only (no external analytics scripts loaded).
     Prepared events: calculator_interaction, category_select, result_rendered, vendor_cta_click */
  window.__saasbillEvents = window.__saasbillEvents || [];
  document.addEventListener('click', function(e) {{
    var cta = e.target.closest('[data-track="vendor-cta"]');
    if (cta) {{
      window.__saasbillEvents.push({{
        event: 'vendor_cta_click',
        vendor: cta.getAttribute('data-vendor') || '',
        location: cta.getAttribute('data-cta-location') || 'subpage-result',
        href: cta.getAttribute('href') || '',
        ts: Date.now()
      }});
      return;
    }}
    var catBtn = e.target.closest('[data-track="category-select"]');
    if (catBtn) {{
      window.__saasbillEvents.push({{
        event: 'category_select',
        category: catBtn.getAttribute('data-cat') || '',
        ts: Date.now()
      }});
    }}
  }});
  document.addEventListener('input', function(e) {{
    var ctrl = e.target.closest('[data-track="calculator-control"], input[type="range"], select');
    if (ctrl) {{
      window.__saasbillEvents.push({{
        event: 'calculator_interaction',
        control: ctrl.getAttribute('data-control') || ctrl.id || '',
        value: ctrl.value,
        ts: Date.now()
      }});
    }}
  }});
  </script>
</body>
</html>"""
    full_path = os.path.join(PUBLIC_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(html)
    print(f"Wrote {full_path} [dateModified={iso_datetime}]")

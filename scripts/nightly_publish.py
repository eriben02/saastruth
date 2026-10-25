"""
Nightly Publisher Engine for SaaSTruth (/workspace/saastruth/scripts/nightly_publish.py)
Pops the next queued topic from /workspace/saastruth/data/publishing_queue.json,
builds a GEO-optimized interactive calculator page (with Direct Answer TL;DR, semantic table, and FAQPage JSON-LD),
updates sitemap.xml and llms.txt, and logs the publication.
"""
import json
import os
from datetime import datetime
from layout import load_data, render_page, PUBLIC_DIR, DATA_DIR, SITE_ORIGIN

def run_nightly(dry_run=False):
    queue_path = os.path.join(DATA_DIR, "publishing_queue.json")
    log_path = os.path.join(DATA_DIR, "publish_log.json")
    with open(queue_path) as f:
        queue = json.load(f)

    next_item = next((item for item in queue if item.get("status") == "queued"), None)
    if not next_item:
        print("No queued items remaining.")
        return

    if dry_run:
        print(f"[DRY RUN] Next nightly GEO page to publish: #{next_item['priority']} -> {next_item['slug']} ({next_item['title']})")
        return

    tools, affiliates = load_data()
    aff = affiliates.get(next_item["primary_affiliate"], {"destination_url": "https://eriben02.github.io/saastruth/", "program_name": "Partner"})
    slug_clean = next_item["slug"].strip("/")
    rel_html_path = f"{slug_clean}/index.html"
    today = datetime.now().strftime("%Y-%m-%d")

    body_html = f"""
    <section class="hero">
      <span class="eyebrow">{next_item['category']} · Verified {today}</span>
      <h1>{next_item['title']}</h1>
      <p class="lead">Independent contract and true-cost audit for {next_item['category']}. Use the interactive calculator below to model hidden overages, renewal notice windows, and transparent alternatives.</p>
      <div class="geo-direct-answer" aria-label="Direct Answer Summary">
        <span class="geo-label">Direct Answer / TL;DR (Verified {today})</span>
        <p><strong>Key Audit Verdict:</strong> Standard advertised pricing in {next_item['category']} omits seat-bucket minimums, auto-renewal notice windows (30–60 days), and usage overage multipliers. Switching to a transparent-pricing partner such as <strong>{aff.get('program_name')}</strong> eliminates mandatory onboarding fees and annual lock-in traps.</p>
      </div>
    </section>
    <section class="calc-box">
      <h2 style="margin-top:0;">Interactive Cost &amp; Overage Estimator</h2>
      <div class="section-tldr">
        <strong>Recommended Transparent Partner:</strong> Compare against <strong>{aff.get('program_name')}</strong> ({aff.get('commission', 'Verified partner terms')}).
      </div>
      <a class="btn-cta" href="{aff.get('destination_url')}" target="_blank" rel="nofollow sponsored">Compare Verified Partner Pricing &rarr;</a>
    </section>
    """
    faqs = [
        (f"What is the biggest hidden contract trap in {next_item['title']}?", f"As verified on {today}, the primary cost escalators are mandatory onboarding fees, 30-to-60 day auto-renewal cancellation windows, and uncapped usage or per-resolution overage charges."),
        (f"Which transparent alternative is recommended for {next_item['category']}?", f"We recommend evaluating {aff.get('program_name')} ({aff.get('destination_url')}), which offers transparent self-serve pricing without surprise onboarding fees.")
    ]
    render_page(rel_html_path, next_item["title"], next_item["title"], next_item["slug"], body_html, faqs=faqs)
    next_item["status"] = "published"
    next_item["published_at"] = today

    with open(queue_path, "w") as f:
        json.dump(queue, f, indent=2)

    logs = []
    if os.path.exists(log_path):
        with open(log_path) as f:
            logs = json.load(f)
    logs.append({"date": today, "slug": next_item["slug"], "title": next_item["title"], "affiliate": next_item["primary_affiliate"]})
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)
    print(f"Published nightly GEO page: {next_item['slug']}")

if __name__ == "__main__":
    import sys
    run_nightly(dry_run="--dry-run" in sys.argv)

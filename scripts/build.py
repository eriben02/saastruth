import subprocess
import sys

# Calculation drawers are <details class="math-drawer"> labeled "Show calculation".
# layout.py loads public/assets/app.js, which closes other drawers and outside clicks.

subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_part1.py"], check=True)
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_part2.py"], check=True)
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_zendesk_ai_page.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_gumroad_whop_lemonsqueezy_page.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_queued_batch1.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_workspace_m365_hipaa_page.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_jotform_wix_guide.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_intercom_fin_calculator.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_zoominfo_renewal_page.py"], check=True, cwd="/workspace/saastruth/scripts")
# Payment calculators in part1 (PAY_PROFILES), part2 (payout-hold sim),
# build_queued_batch1 (Stripe Billing and Stripe vs Paddle), and the Gumroad
# take-rate page include a live chargeback drain line plus a Chargeflow CTA.
# The dedicated Chargeflow calculator below stays on the same 65% / 25% model.
subprocess.run([sys.executable, "/workspace/saastruth/scripts/build_chargeback_calculator.py"], check=True, cwd="/workspace/saastruth/scripts")
subprocess.run([sys.executable, "/workspace/saastruth/scripts/update_meta_files.py"], check=True)
print("Full SaaSBill build + dynamic freshness metadata completed.")

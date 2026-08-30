#!/usr/bin/env python3
"""
Schedule Publisher Tool for VerifyReviews (Affiliate Global)
Round-Robin Topic Queue: 6 Batches (Batches 1-6) + 6 New Batches (Batches 7-12)
Total 60 Articles scheduled across 6 project categories.
"""

import sys
import os
import argparse
import subprocess

SCHEDULED_ARTICLES = [
    # --- PHASE 1: BATCHES 1 TO 6 (30 ARTICLES) ---
    # Batch 1 (Day 1)
    {"file": "fathom-vs-syft-analytics.html", "cluster": "Financial Reporting", "batch": 1, "time": "07:00"},
    {"file": "warmupinbox-vs-instantly-warmup.html", "cluster": "Email Deliverability", "batch": 1, "time": "09:00"},
    {"file": "elevenlabs-vs-playht.html", "cluster": "AI Video & Voice", "batch": 1, "time": "11:00"},
    {"file": "iproyal-vs-smartproxy.html", "cluster": "Proxy Networks", "batch": 1, "time": "13:00"},
    {"file": "affitor-vs-rewardful.html", "cluster": "SaaS Partner Platforms", "batch": 1, "time": "15:00"},

    # Batch 2 (Day 3)
    {"file": "best-multi-entity-consolidation-software.html", "cluster": "Financial Reporting", "batch": 2, "time": "07:00"},
    {"file": "best-email-warmup-tools-cold-outreach.html", "cluster": "Email Deliverability", "batch": 2, "time": "09:00"},
    {"file": "best-ai-voice-generators-content-creators.html", "cluster": "AI Video & Voice", "batch": 2, "time": "11:00"},
    {"file": "best-proxies-for-web-scraping-python.html", "cluster": "Proxy Networks", "batch": 2, "time": "13:00"},
    {"file": "best-affiliate-software-for-stripe.html", "cluster": "SaaS Partner Platforms", "batch": 2, "time": "15:00"},

    # Batch 3 (Day 5)
    {"file": "joiin-review-financial-consolidation.html", "cluster": "Financial Reporting", "batch": 3, "time": "07:00"},
    {"file": "how-to-fix-emails-going-to-spam.html", "cluster": "Email Deliverability", "batch": 3, "time": "09:00"},
    {"file": "elevenlabs-review-ai-voice-cloning.html", "cluster": "AI Video & Voice", "batch": 3, "time": "11:00"},
    {"file": "webshare-proxy-review.html", "cluster": "Proxy Networks", "batch": 3, "time": "13:00"},
    {"file": "firstpromoter-review-saas-affiliate.html", "cluster": "SaaS Partner Platforms", "batch": 3, "time": "15:00"},

    # Batch 4 (Day 7)
    {"file": "quickbooks-multi-currency-reporting-guide.html", "cluster": "Financial Reporting", "batch": 4, "time": "07:00"},
    {"file": "warmy-io-review.html", "cluster": "Email Deliverability", "batch": 4, "time": "09:00"},
    {"file": "audiorista-review.html", "cluster": "AI Video & Voice", "batch": 4, "time": "11:00"},
    {"file": "bright-data-vs-iproyal.html", "cluster": "Proxy Networks", "batch": 4, "time": "13:00"},
    {"file": "rewardful-review-stripe-affiliate.html", "cluster": "SaaS Partner Platforms", "batch": 4, "time": "15:00"},

    # Batch 5 (Day 9)
    {"file": "syft-analytics-review.html", "cluster": "Financial Reporting", "batch": 5, "time": "07:00"},
    {"file": "folderly-review.html", "cluster": "Email Deliverability", "batch": 5, "time": "09:00"},
    {"file": "best-ai-video-generators-youtube-faceless.html", "cluster": "AI Video & Voice", "batch": 5, "time": "11:00"},
    {"file": "best-mobile-proxies-multi-accounting.html", "cluster": "Proxy Networks", "batch": 5, "time": "13:00"},
    {"file": "how-to-launch-saas-referral-program.html", "cluster": "SaaS Partner Platforms", "batch": 5, "time": "15:00"},

    # Batch 6 (Day 11)
    {"file": "fathom-reporting-review.html", "cluster": "Financial Reporting", "batch": 6, "time": "07:00"},
    {"file": "google-workspace-cold-email-warmup-guide.html", "cluster": "Email Deliverability", "batch": 6, "time": "09:00"},
    {"file": "deepseek-v4-vs-claude-api-gateway.html", "cluster": "AI Video & Voice", "batch": 6, "time": "11:00"},
    {"file": "how-to-bypass-cloudflare-captcha-proxies.html", "cluster": "Proxy Networks", "batch": 6, "time": "13:00"},
    {"file": "affiliate-fraud-prevention-saas-guide.html", "cluster": "SaaS Partner Platforms", "batch": 6, "time": "15:00"},

    # --- PHASE 2: BATCHES 7 TO 12 (30 NEW ARTICLES ACROSS 6 CATEGORIES) ---
    # Batch 7 (Day 13)
    {"file": "xero-vs-quickbooks-multi-entity-reporting.html", "cluster": "Financial Reporting", "batch": 7, "time": "07:00"},
    {"file": "instantly-vs-smartlead-deliverability.html", "cluster": "Email Deliverability", "batch": 7, "time": "09:00"},
    {"file": "heygen-vs-synthesia-ai-avatar-video.html", "cluster": "AI Video & Voice", "batch": 7, "time": "11:00"},
    {"file": "datacenter-vs-residential-proxies-scraping.html", "cluster": "Proxy Networks", "batch": 7, "time": "13:00"},
    {"file": "promotekit-vs-rewardful.html", "cluster": "SaaS Partner Platforms", "batch": 7, "time": "15:00"},

    # Batch 8 (Day 15)
    {"file": "best-fp-and-a-software-for-saas-startups.html", "cluster": "Financial Reporting", "batch": 8, "time": "07:00"},
    {"file": "how-to-warmup-new-domain-for-cold-email.html", "cluster": "Email Deliverability", "batch": 8, "time": "09:00"},
    {"file": "best-ai-text-to-speech-apis-developers.html", "cluster": "AI Video & Voice", "batch": 8, "time": "11:00"},
    {"file": "best-static-isp-proxies-multi-account.html", "cluster": "Proxy Networks", "batch": 8, "time": "13:00"},
    {"file": "cloudways-vs-kinsta-wordpress-hosting.html", "cluster": "Managed Web Hosting", "batch": 8, "time": "15:00"},

    # Batch 9 (Day 17)
    {"file": "how-to-automate-intercompany-eliminations-accounting.html", "cluster": "Financial Reporting", "batch": 9, "time": "07:00"},
    {"file": "b2b-cold-email-spam-filter-triggers-2026.html", "cluster": "Email Deliverability", "batch": 9, "time": "09:00"},
    {"file": "descript-vs-elevenlabs.html", "cluster": "AI Video & Voice", "batch": 9, "time": "11:00"},
    {"file": "oxylabs-vs-bright-data.html", "cluster": "Proxy Networks", "batch": 9, "time": "13:00"},
    {"file": "how-to-structure-saas-affiliate-commissions.html", "cluster": "SaaS Partner Platforms", "batch": 9, "time": "15:00"},

    # Batch 10 (Day 19)
    {"file": "liveplan-vs-fathom.html", "cluster": "Financial Reporting", "batch": 10, "time": "07:00"},
    {"file": "glockapps-vs-warmupinbox.html", "cluster": "Email Deliverability", "batch": 10, "time": "09:00"},
    {"file": "best-ai-subtitle-caption-generators-tiktok-reels.html", "cluster": "AI Video & Voice", "batch": 10, "time": "11:00"},
    {"file": "how-to-rotate-user-agents-and-proxies-python.html", "cluster": "Proxy Networks", "batch": 10, "time": "13:00"},
    {"file": "best-nvme-cloud-hosting-providers-high-traffic.html", "cluster": "Managed Web Hosting", "batch": 10, "time": "15:00"},

    # Batch 11 (Day 21)
    {"file": "financial-dashboard-reporting-best-practices-cfo.html", "cluster": "Financial Reporting", "batch": 11, "time": "07:00"},
    {"file": "dkim-spf-dmarc-setup-google-workspace-outlook.html", "cluster": "Email Deliverability", "batch": 11, "time": "09:00"},
    {"file": "ai-dubbing-multilingual-video-translation-guide.html", "cluster": "AI Video & Voice", "batch": 11, "time": "11:00"},
    {"file": "best-cheap-proxies-budget-scraping.html", "cluster": "Proxy Networks", "batch": 11, "time": "13:00"},
    {"file": "best-partner-relationship-management-prm-software.html", "cluster": "SaaS Partner Platforms", "batch": 11, "time": "15:00"},

    # Batch 12 (Day 23)
    {"file": "wp-engine-vs-kinsta.html", "cluster": "Managed Web Hosting", "batch": 12, "time": "07:00"},
    {"file": "partnerstack-vs-firstpromoter.html", "cluster": "SaaS Partner Platforms", "batch": 12, "time": "09:00"},
    {"file": "paddle-affiliate-marketing-integration-guide.html", "cluster": "SaaS Partner Platforms", "batch": 12, "time": "11:00"},
    {"file": "how-to-speed-up-wordpress-ttfb-core-web-vitals.html", "cluster": "Managed Web Hosting", "batch": 12, "time": "13:00"},
    {"file": "best-cheap-vps-hosting-developers.html", "cluster": "Managed Web Hosting", "batch": 12, "time": "15:00"}
]

def is_in_sitemap(filename):
    sitemap_path = "sitemap.xml"
    if not os.path.exists(sitemap_path):
        return False
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    return filename in content

def list_articles():
    print("==========================================================================")
    print("📋 FULL PUBLICATION QUEUE (BATCHES 1 TO 12 • 60 ARTICLES)")
    print("==========================================================================")
    current_batch = None
    for idx, item in enumerate(SCHEDULED_ARTICLES, 1):
        if item["batch"] != current_batch:
            current_batch = item["batch"]
            print(f"\n--- 📦 BATCH {current_batch} (Publishing Day {current_batch*2 - 1}) ---")
        
        status = "✅ Published" if is_in_sitemap(item["file"]) else "⏳ Staged"
        print(f"{idx:02d}. [{status}] [{item['time']}] {item['file']} ({item['cluster']})")
    print("\n==========================================================================")

def add_to_sitemap(filename):
    sitemap_path = "sitemap.xml"
    if is_in_sitemap(filename):
        return
    
    url_entry = f"""    <url>
        <loc>https://verifyreviews.net/{filename}</loc>
        <lastmod>2026-08-30</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.95</priority>
    </url>
</urlset>"""
    
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("</urlset>", url_entry)
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Added {filename} to sitemap.xml")

def publish_batch(batch_num):
    items = [item for item in SCHEDULED_ARTICLES if item["batch"] == batch_num]
    if not items:
        print(f"Error: Batch {batch_num} not found.")
        return False

    print(f"🚀 Publishing Batch {batch_num} ({len(items)} articles across 6 categories)...")
    files_to_add = []
    for item in items:
        if os.path.exists(item["file"]):
            add_to_sitemap(item["file"])
            files_to_add.append(item["file"])
        else:
            print(f"Warning: {item['file']} missing locally.")

    if not files_to_add:
        print("No files found to publish.")
        return False

    cmd_add = ["git", "add"] + files_to_add + ["sitemap.xml"]
    subprocess.run(cmd_add, check=True)
    subprocess.run(["git", "commit", "-m", f"Publish Batch {batch_num} ({len(files_to_add)} articles)"], check=False)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(f"\n✅ SUCCESS! Batch {batch_num} has been published to verifyreviews.net!")
    return True

def publish_file(filename):
    target_item = None
    for item in SCHEDULED_ARTICLES:
        if item["file"] == filename:
            target_item = item
            break
            
    if not target_item:
        print(f"Error: {filename} not found in scheduled articles list.")
        return False

    if not os.path.exists(filename):
        print(f"Error: {filename} does not exist locally.")
        return False

    print(f"🚀 Publishing [{target_item['time']}] {filename} ({target_item['cluster']})...")
    add_to_sitemap(filename)

    subprocess.run(["git", "add", filename, "sitemap.xml"], check=True)
    subprocess.run(["git", "commit", "-m", f"Publish scheduled article: {filename}"], check=False)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(f"✅ Successfully published {filename} to https://verifyreviews.net/{filename}!")
    return True

def publish_next():
    for item in SCHEDULED_ARTICLES:
        if not is_in_sitemap(item["file"]):
            publish_file(item["file"])
            return
    print("All scheduled articles have already been published!")

def main():
    parser = argparse.ArgumentParser(description="Publish scheduled articles to verifyreviews.net")
    parser.add_argument("--list", action="store_true", help="List all scheduled articles and their status")
    parser.add_argument("--publish", type=str, help="Publish a specific article filename")
    parser.add_argument("--publish-batch", type=int, help="Publish an entire batch by batch number (e.g., 7)")
    parser.add_argument("--publish-next", action="store_true", help="Publish the next staged article in queue")

    args = parser.parse_args()

    if args.list:
        list_articles()
    elif args.publish_batch:
        publish_batch(args.publish_batch)
    elif args.publish:
        publish_file(args.publish)
    elif args.publish_next:
        publish_next()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

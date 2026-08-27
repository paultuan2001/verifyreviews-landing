#!/usr/bin/env python3
"""
Schedule Publisher Tool for VerifyReviews (Affiliate Global)
Round-Robin Topic Queue: 5 articles from 5 different topics per publishing day.
"""

import sys
import os
import argparse
import subprocess

# Exact Round-Robin order: 6 batches of 5 articles across 5 topics
SCHEDULED_ARTICLES = [
    # Batch 1 (Day 1)
    {"file": "fathom-vs-syft-analytics.html", "cluster": "Financial Reporting", "batch": 1, "time": "07:00"},
    {"file": "warmupinbox-vs-instantly-warmup.html", "cluster": "Email Deliverability", "batch": 1, "time": "09:00"},
    {"file": "elevenlabs-vs-playht.html", "cluster": "AI Video & Voice", "batch": 1, "time": "11:00"},
    {"file": "iproyal-vs-smartproxy.html", "cluster": "Proxy Networks", "batch": 1, "time": "13:00"},
    {"file": "affitor-vs-rewardful.html", "cluster": "SaaS Partner Platforms", "batch": 1, "time": "15:00"},

    # Batch 2 (Day 3 - 2 days later)
    {"file": "best-multi-entity-consolidation-software.html", "cluster": "Financial Reporting", "batch": 2, "time": "07:00"},
    {"file": "best-email-warmup-tools-cold-outreach.html", "cluster": "Email Deliverability", "batch": 2, "time": "09:00"},
    {"file": "best-ai-voice-generators-content-creators.html", "cluster": "AI Video & Voice", "batch": 2, "time": "11:00"},
    {"file": "best-proxies-for-web-scraping-python.html", "cluster": "Proxy Networks", "batch": 2, "time": "13:00"},
    {"file": "best-affiliate-software-for-stripe.html", "cluster": "SaaS Partner Platforms", "batch": 2, "time": "15:00"},

    # Batch 3 (Day 5 - 2 days later)
    {"file": "joiin-review-financial-consolidation.html", "cluster": "Financial Reporting", "batch": 3, "time": "07:00"},
    {"file": "how-to-fix-emails-going-to-spam.html", "cluster": "Email Deliverability", "batch": 3, "time": "09:00"},
    {"file": "elevenlabs-review-ai-voice-cloning.html", "cluster": "AI Video & Voice", "batch": 3, "time": "11:00"},
    {"file": "webshare-proxy-review.html", "cluster": "Proxy Networks", "batch": 3, "time": "13:00"},
    {"file": "firstpromoter-review-saas-affiliate.html", "cluster": "SaaS Partner Platforms", "batch": 3, "time": "15:00"},

    # Batch 4 (Day 7 - 2 days later)
    {"file": "quickbooks-multi-currency-reporting-guide.html", "cluster": "Financial Reporting", "batch": 4, "time": "07:00"},
    {"file": "warmy-io-review.html", "cluster": "Email Deliverability", "batch": 4, "time": "09:00"},
    {"file": "audiorista-review.html", "cluster": "AI Video & Voice", "batch": 4, "time": "11:00"},
    {"file": "bright-data-vs-iproyal.html", "cluster": "Proxy Networks", "batch": 4, "time": "13:00"},
    {"file": "rewardful-review-stripe-affiliate.html", "cluster": "SaaS Partner Platforms", "batch": 4, "time": "15:00"},

    # Batch 5 (Day 9 - 2 days later)
    {"file": "syft-analytics-review.html", "cluster": "Financial Reporting", "batch": 5, "time": "07:00"},
    {"file": "folderly-review.html", "cluster": "Email Deliverability", "batch": 5, "time": "09:00"},
    {"file": "best-ai-video-generators-youtube-faceless.html", "cluster": "AI Video & Voice", "batch": 5, "time": "11:00"},
    {"file": "best-mobile-proxies-multi-accounting.html", "cluster": "Proxy Networks", "batch": 5, "time": "13:00"},
    {"file": "how-to-launch-saas-referral-program.html", "cluster": "SaaS Partner Platforms", "batch": 5, "time": "15:00"},

    # Batch 6 (Day 11 - 2 days later)
    {"file": "fathom-reporting-review.html", "cluster": "Financial Reporting", "batch": 6, "time": "07:00"},
    {"file": "google-workspace-cold-email-warmup-guide.html", "cluster": "Email Deliverability", "batch": 6, "time": "09:00"},
    {"file": "deepseek-v4-vs-claude-api-gateway.html", "cluster": "AI Video & Voice", "batch": 6, "time": "11:00"},
    {"file": "how-to-bypass-cloudflare-captcha-proxies.html", "cluster": "Proxy Networks", "batch": 6, "time": "13:00"},
    {"file": "affiliate-fraud-prevention-saas-guide.html", "cluster": "SaaS Partner Platforms", "batch": 6, "time": "15:00"}
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
    print("📋 ROUND-ROBIN PUBLICATION QUEUE (5 TOPICS / BATCH • 2-HOUR INTERVALS)")
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
        <lastmod>2026-08-27</lastmod>
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
    parser.add_argument("--publish-next", action="store_true", help="Publish the next staged article in queue")

    args = parser.parse_args()

    if args.list:
        list_articles()
    elif args.publish:
        publish_file(args.publish)
    elif args.publish_next:
        publish_next()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

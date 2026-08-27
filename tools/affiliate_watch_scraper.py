#!/usr/bin/env python3
"""
============================================================
AGOS OFFER DISCOVERY ENGINE - AFFILIATE.WATCH SCRAPER
============================================================
Cào tự động các dự án Affiliate chất lượng từ Affiliate.watch
nhắm vào các thẻ: googleads, saas, ai, proxy, hosting, vpn
và nạp tự động vào kho dữ liệu research/offers_db.csv
============================================================
"""

import json
import re
import urllib.request
import csv
import os

TAGS_TO_SCRAPE = ['googleads', 'saas', 'ai', 'proxy', 'hosting', 'vpn']
OUTPUT_CSV = 'research/offers_db.csv'

def fetch_tag_data(tag):
    url = f"https://affiliate.watch/tag/{tag}"
    print(f"[*] Đang cào dữ liệu từ: {url} ...")
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        m = re.search(r'data-page=\"([^\"]+)\"', html)
        if m:
            raw_json = m.group(1).replace('&quot;', '"')
            data = json.loads(raw_json)
            affiliates = data.get('props', {}).get('affiliates', {}).get('data', [])
            print(f"[+] Tìm thấy {len(affiliates)} offer cho thẻ '{tag}'.")
            return affiliates
    except Exception as e:
        print(f"[-] Lỗi khi cào thẻ '{tag}': {e}")
    return []

def run_scraper():
    all_offers = []
    seen_names = set()
    
    for tag in TAGS_TO_SCRAPE:
        offers = fetch_tag_data(tag)
        for item in offers:
            name = item.get('name')
            if name and name not in seen_names:
                seen_names.add(name)
                all_offers.append({
                    'Offer ID': f"AW-{item.get('id', '000')}",
                    'Merchant': name,
                    'Network': 'Direct / Affiliate.Watch',
                    'Category': tag.upper(),
                    'Geo': 'Global',
                    'Commission': item.get('teaser_affiliate', 'N/A'),
                    'Cookie (Days)': item.get('cookie_days', 'N/A'),
                    'PPC Allowed': 'Check Terms',
                    'Brand Bidding Allowed': 'No',
                    'Direct Link Allowed': 'No',
                    'Landing Required': 'Yes',
                    'Status': 'Research (Scraped)',
                    'Notes': f"Web: {item.get('website', '')} | AI Rating: {item.get('rating_ai', '')}"
                })

    if not all_offers:
        print("[-] Không cào được dữ liệu mới.")
        return

    # Check if file exists to write header
    file_exists = os.path.exists(OUTPUT_CSV)
    
    fieldnames = [
        'Offer ID', 'Merchant', 'Network', 'Category', 'Geo', 
        'Commission', 'Cookie (Days)', 'PPC Allowed', 'Brand Bidding Allowed', 
        'Direct Link Allowed', 'Landing Required', 'Status', 'Notes'
    ]

    with open(OUTPUT_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for offer in all_offers:
            writer.writerow(offer)
            
    print(f"\n[============================================================]")
    print(f"[+] HOÀN THÀNH! Đã thêm {len(all_offers)} offer mới vào {OUTPUT_CSV}")
    print(f"[============================================================]")

if __name__ == '__main__':
    run_scraper()

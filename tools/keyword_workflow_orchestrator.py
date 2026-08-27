#!/usr/bin/env python3
import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

# Ensure we can import from keyword_classifier.py in the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from keyword_classifier import classify_keyword
except ImportError:
    # Fallback classification if import fails
    import re
    def classify_keyword(keyword):
        kw_lower = keyword.strip().lower()
        if re.search(r"\b(free|cheap|crack|null|torrent|download|job|salary|login|signin)\b", kw_lower):
            return "NEGATIVE_CANDIDATE"
        if re.search(r"\b(buy|price|pricing|cost|discount|coupon|best|top|review|vs|alternative)\b", kw_lower):
            return "CONVERSION"
        if re.search(r"\b(how to|what is|why|tutorial|guide|learn)\b", kw_lower):
            return "EDUCATION"
        return "AWARENESS"

def scrape_autocomplete(seed_query):
    print(f"[*] Bắt đầu cào gợi ý Google Autocomplete cho từ khóa hạt giống: '{seed_query}'...")
    suggestions = set()
    
    # 1. Scrape base query
    base_suggs = get_suggestions(seed_query)
    suggestions.update(base_suggs)
    
    # 2. Alphabet Soup Scrape (seed + 'a'..'z')
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for char in alphabet:
        query = f"{seed_query} {char}"
        suggs = get_suggestions(query)
        suggestions.update(suggs)
        time.sleep(0.1) # Be gentle to Google API
        
    # 3. Question Modifiers Scrape
    questions = ['how to', 'does', 'can i', 'should i', 'what is', 'why is']
    for q in questions:
        query = f"{q} {seed_query}"
        suggs = get_suggestions(query)
        suggestions.update(suggs)
        time.sleep(0.1)
        
    print(f"[+] Hoàn thành cào! Tìm được {len(suggestions)} từ khóa duy nhất.")
    return list(suggestions)

def get_suggestions(query):
    encoded_query = urllib.parse.quote(query)
    url = f"http://suggestqueries.google.com/complete/search?client=chrome&hl=en&q={encoded_query}"
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8', errors='ignore'))
            return data[1] # suggestions list
    except Exception as e:
        # Silently fail to keep console output clean
        return []

def main():
    parser = argparse.ArgumentParser(description="AGOS Keyword Workflow Orchestrator - Tự động cào và xuất file Google Ads.")
    parser.add_argument("--seed", type=str, required=True, help="Từ khóa hạt giống (Ví dụ: 'get ex back')")
    parser.add_argument("--campaign", type=str, default="AGOS-MVP-Campaign", help="Tên chiến dịch Google Ads")
    parser.add_argument("--adgroup", type=str, default="Sơn Piaz Flow", help="Tên nhóm quảng cáo (Ad Group)")
    parser.add_argument("--match-type", type=str, default="Phrase", choices=["Phrase", "Exact", "Broad"], help="Loại đối sánh từ khóa quảng cáo")
    
    args = parser.parse_args()
    
    # Ensure research folder exists
    os.makedirs("research", exist_ok=True)
    
    # Step 1: Scrape
    raw_keywords = scrape_autocomplete(args.seed)
    
    # Sanitize seed name for file path
    safe_seed = "".join([c if c.isalnum() else "_" for c in args.seed.lower()]).strip("_")
    while "__" in safe_seed:
        safe_seed = safe_seed.replace("__", "_")
        
    # Save raw keywords list
    raw_file_path = f"research/keywords_raw_{safe_seed}.txt"
    with open(raw_file_path, "w", encoding="utf-8") as f:
        for kw in raw_keywords:
            f.write(f"{kw}\n")
    print(f"[+] Đã lưu danh sách từ khóa thô vào: {raw_file_path}")
    
    # Step 2: Classify
    ads_keywords = []
    negative_keywords = []
    
    for kw in raw_keywords:
        category = classify_keyword(kw)
        if category == "CONVERSION":
            ads_keywords.append(kw)
        elif category == "NEGATIVE_CANDIDATE":
            negative_keywords.append(kw)
            
    # Step 3: Format Google Ads Editor Import CSVs
    keywords_csv_path = f"research/google_ads_keywords_import_{safe_seed}.csv"
    negatives_csv_path = f"research/google_ads_negatives_import_{safe_seed}.csv"
    
    # Write Ads Keywords Import CSV
    try:
        with open(keywords_csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Campaign", "Ad Group", "Keyword", "Match Type", "Status"])
            for kw in ads_keywords:
                writer.writerow([args.campaign, args.adgroup, kw, args.match_type, "Enabled"])
        print(f"[+] Đã tạo file nhập từ khóa Google Ads: {keywords_csv_path} ({len(ads_keywords)} từ khóa)")
    except Exception as e:
        print(f"Lỗi tạo file keywords CSV: {e}")
        
    # Write Negatives Import CSV
    try:
        with open(negatives_csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Google Ads Editor negative list columns
            writer.writerow(["Campaign", "Keyword", "Match Type"])
            for kw in negative_keywords:
                writer.writerow([args.campaign, kw, "Negative Phrase"])
        print(f"[+] Đã tạo file nhập từ khóa PHỦ ĐỊNH Google Ads: {negatives_csv_path} ({len(negative_keywords)} từ khóa)")
    except Exception as e:
        print(f"Lỗi tạo file negatives CSV: {e}")
        
    print("\n" + "=" * 60)
    print("        HOÀN THÀNH LUỒNG ĐIỀU PHỐI TỪ KHÓA AGOS")
    print("=" * 60)
    print(f"1. Tổng từ khóa cào được   : {len(raw_keywords)}")
    print(f"2. Từ khóa Conversion chạy Ads: {len(ads_keywords)}")
    print(f"3. Từ khóa Phủ định chặn tiền : {len(negative_keywords)}")
    print("-" * 60)
    print("👉 Hãy import 2 file CSV trên vào Google Ads Editor để thiết lập chiến dịch!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

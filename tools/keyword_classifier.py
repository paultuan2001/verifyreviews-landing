#!/usr/bin/env python3
import argparse
import csv
import os
import re
import sys

# Define classification rules
INTENTS = {
    "CONVERSION": {
        "patterns": [
            r"\b(?:buy|purchase|order|pricing|price|cost|subscription|discount|coupon|promo|code|deal|discounted)\b",
            r"\b(?:best|top|review|reviews|vs|versus|comparison|alternative|alternatives|compare)\b",
            r"\b(?:hire|professional|agency|service|services|tool|software|platform)\b"
        ],
        "description": "TẦNG 1: CHUYỂN ĐỔI (CONVERSION INTENT) - ƯU TIÊN CHẠY ADS HÀNG ĐẦU"
    },
    "EDUCATION": {
        "patterns": [
            r"\b(?:how to|what is|why|explain|definition|tutorial|tutorials|guide|guides|course|courses|learn|training|book|pdf)\b",
            r"\b(?:example|examples|case study|template|templates|how do i)\b"
        ],
        "description": "TẦNG 2: GIÁO DỤC (EDUCATIONAL INTENT) - NUÔI DƯỠNG KHÁCH HÀNG"
    },
    "NEGATIVE_CANDIDATE": {
        "patterns": [
            r"\b(?:free|cheap|cheapest|crack|cracked|null|nulled|torrent|download|bypass|hack|key generator|serial generator|license generator|coupon generator)\b",
            r"\b(?:job|jobs|career|careers|hiring|salary|resume|work at|internship|interview)\b",
            r"\b(?:login|signin|sign in|support|customer service|phone number|address|contact support|contact us|contact number|refund|cancel)\b"
        ],
        "description": "🔴 PHỦ ĐỊNH (NEGATIVE CANDIDATE) - CẦN PHỦ ĐỊNH ĐỂ TRÁNH MẤT TIỀN ADS"
    }
}

def classify_keyword(keyword):
    kw_lower = keyword.strip().lower()
    
    # Check Negative first to prevent wasted budget
    for pattern in INTENTS["NEGATIVE_CANDIDATE"]["patterns"]:
        if re.search(pattern, kw_lower):
            return "NEGATIVE_CANDIDATE"
            
    # Check Conversion
    for pattern in INTENTS["CONVERSION"]["patterns"]:
        if re.search(pattern, kw_lower):
            return "CONVERSION"
            
    # Check Education
    for pattern in INTENTS["EDUCATION"]["patterns"]:
        if re.search(pattern, kw_lower):
            return "EDUCATION"
            
    # Default is Awareness/Other
    return "AWARENESS"

def process_keywords(file_path):
    print("=" * 60)
    print("        AGOS KEYWORD CLASSIFIER - INTENT ENGINE")
    print("=" * 60)
    
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file {file_path}")
        sys.exit(1)
        
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        keywords = [line.strip() for line in f if line.strip()]
        
    if not keywords:
        print("Tệp rỗng. Không có từ khóa để xử lý.")
        sys.exit(1)
        
    results = {
        "CONVERSION": [],
        "EDUCATION": [],
        "AWARENESS": [],
        "NEGATIVE_CANDIDATE": []
    }
    
    for kw in keywords:
        category = classify_keyword(kw)
        results[category].append(kw)
        
    total_kws = len(keywords)
    print(f"Tổng số từ khóa phân tích: {total_kws}")
    print("-" * 60)
    print(f"🟢 Conversion (Chạy Ads chính) : {len(results['CONVERSION'])} ({len(results['CONVERSION'])/total_kws*100:.1f}%)")
    print(f"🔵 Education (Nuôi dưỡng SEO)   : {len(results['EDUCATION'])} ({len(results['EDUCATION'])/total_kws*100:.1f}%)")
    print(f"🟡 Awareness (Traffic rộng)      : {len(results['AWARENESS'])} ({len(results['AWARENESS'])/total_kws*100:.1f}%)")
    print(f"🔴 Negative (Phủ định Ads)      : {len(results['NEGATIVE_CANDIDATE'])} ({len(results['NEGATIVE_CANDIDATE'])/total_kws*100:.1f}%)")
    print("=" * 60)
    
    # Save output to CSV
    output_path = file_path.rsplit(".", 1)[0] + "_classified.csv"
    try:
        with open(output_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Keyword", "Intent Category", "Action Recommendation"])
            
            for cat, kws in results.items():
                rec = ""
                if cat == "CONVERSION":
                    rec = "Chạy Search Campaign (Exact/Phrase match)"
                elif cat == "EDUCATION":
                    rec = "Làm Content Blog/SEO/YouTube"
                elif cat == "NEGATIVE_CANDIDATE":
                    rec = "Thêm vào danh sách Phủ Định (Negative Keywords)"
                else:
                    rec = "Theo dõi hoặc chạy quảng cáo bám đuôi (Retargeting)"
                    
                for kw in kws:
                    writer.writerow([kw, cat, rec])
        print(f"Đã lưu kết quả phân loại vào: {output_path}")
    except Exception as e:
        print(f"Lỗi khi ghi file CSV: {e}")
        
    # Print sample of Negative candidates
    if results["NEGATIVE_CANDIDATE"]:
        print(f"\n[!] CẢNH BÁO: Phát hiện {len(results['NEGATIVE_CANDIDATE'])} từ khóa rác lãng phí ngân sách Ads:")
        for kw in results["NEGATIVE_CANDIDATE"][:5]:
            print(f"  - \"{kw}\"")
        if len(results["NEGATIVE_CANDIDATE"]) > 5:
            print(f"  ... và {len(results['NEGATIVE_CANDIDATE']) - 5} từ khóa khác (Xem chi tiết trong file CSV).")
            
    print("=" * 60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="AGOS Keyword Classifier - Phân loại từ khóa theo phễu chuyển đổi.")
    parser.add_argument("file", nargs="?", help="Đường dẫn đến file text chứa danh sách từ khóa (mỗi dòng một từ khóa)")
    
    args = parser.parse_args()
    
    if not args.file:
        print("Lỗi: Vui lòng cung cấp đường dẫn đến file chứa danh sách từ khóa.")
        print("Ví dụ: python3 tools/keyword_classifier.py research/keywords_input.txt")
        sys.exit(1)
        
    process_keywords(args.file)

if __name__ == "__main__":
    main()

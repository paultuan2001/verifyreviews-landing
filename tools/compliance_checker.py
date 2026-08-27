#!/usr/bin/env python3
import argparse
import os
import re
import sys

# Define regex patterns for compliance scanning
RULES = {
    "PPC / SEM Prohibited": {
        "patterns": [
            r"no (?:ppc|sem|paid search|search engine marketing|google ads|adwords|bing ads)",
            r"(?:ppc|sem|paid search|search ads|google ads) is prohibited",
            r"not allowed to (?:bid|run ads|advertise) on search engines",
            r"prohibit (?:bidding on|running ads on) search engines"
        ],
        "category": "🔴 CRITICAL: CẤM CHẠY PPC (SEARCH ADS)",
        "description": "Merchant cấm hoàn toàn hình thức chạy quảng cáo tìm kiếm trả phí."
    },
    "Brand Bidding Prohibited": {
        "patterns": [
            r"brand bidding is (?:prohibited|not allowed|forbidden)",
            r"no (?:trademark|tm|brand|brand name|keyword) bidding",
            r"do not bid on (?:our brand|trademark|brand keywords)",
            r"bidding on trademarked terms is prohibited",
            r"negative keywords are required",
            r"must add.*negative keywords"
        ],
        "category": "⚠️ WARNING: CẤM BRAND BIDDING (TRADEMARK)",
        "description": "Bạn không được phép chạy từ khóa có chứa tên thương hiệu của merchant."
    },
    "Direct Linking Prohibited": {
        "patterns": [
            r"no direct linking",
            r"direct linking is (?:prohibited|not allowed|forbidden)",
            r"must use a landing page",
            r"no redirects to (?:our site|merchant site|destination url)",
            r"do not use final url as display url"
        ],
        "category": "⚠️ WARNING: CẤM DIRECT LINKING",
        "description": "Cấm trỏ quảng cáo trực tiếp qua affiliate link vào trang merchant. Bắt buộc dùng Landing Page."
    },
    "Compliance & Disclosure Required": {
        "patterns": [
            r"must disclose",
            r"affiliate disclosure",
            r"disclosure policy",
            r"disclose (?:your relationship|affiliate link|commission)",
            r"privacy policy",
            r"clear disclosure"
        ],
        "category": "ℹ️ INFO: YÊU CẦU MINH BẠCH (DISCLOSURE)",
        "description": "Landing Page bắt buộc phải hiển thị tuyên bố liên kết (Affiliate Disclosure) rõ ràng."
    },
    "Allowed Traffic Signals": {
        "patterns": [
            r"ppc is allowed",
            r"paid search is permitted",
            r"landing pages are allowed",
            r"allowed traffic:.*search",
            r"search traffic is accepted"
        ],
        "category": "✅ ALLOWED: CHẤP NHẬN TRAFFIC SEARCH",
        "description": "Các tín hiệu cho thấy merchant cho phép chạy quảng cáo tìm kiếm."
    }
}

def analyze_terms(text):
    print("=" * 60)
    print("        AGOS COMPLIANCE ENGINE - TERMS SCANNER")
    print("=" * 60)
    
    findings = []
    
    # Clean text to make matching easier
    text_clean = text.lower()
    
    for rule_name, rule_data in RULES.items():
        matches = []
        for pattern in rule_data["patterns"]:
            # Find all matches with context (50 chars before and after)
            for m in re.finditer(pattern, text_clean):
                start = max(0, m.start() - 40)
                end = min(len(text), m.end() + 40)
                context = text[start:end].replace('\n', ' ').strip()
                matches.append(context)
        
        if matches:
            findings.append({
                "rule": rule_name,
                "category": rule_data["category"],
                "description": rule_data["description"],
                "matches": list(set(matches)) # unique matches
            })
            
    if not findings:
        print("Không tìm thấy điều khoản cấm hoặc yêu cầu đặc biệt rõ ràng.")
        print("Lưu ý: Bạn vẫn phải đọc kỹ bản Official Terms thủ công để tránh bỏ sót.")
    else:
        for f in findings:
            print(f"\n{f['category']}")
            print(f"Chi tiết: {f['description']}")
            print("Đoạn trích phát hiện được trong Terms:")
            for m in f["matches"]:
                print(f"  - \"... {m} ...\"")
            print("-" * 60)
            
    print("\nKết luận ban đầu:")
    critical_count = sum(1 for f in findings if "🔴 CRITICAL" in f["category"])
    warning_count = sum(1 for f in findings if "⚠️ WARNING" in f["category"])
    
    if critical_count > 0:
        print("👉 KHÔNG NÊN CHẠY: Offer này cấm hoàn toàn hình thức quảng cáo PPC.")
    elif warning_count > 0:
        print("👉 CẦN LƯU Ý: Chạy được nhưng cần tuân thủ nghiêm ngặt (Ví dụ: phủ định từ khóa thương hiệu, dùng Landing Page riêng).")
    else:
        print("👉 CÓ THỂ CHẠY: Chưa tìm thấy điều khoản cấm, vui lòng xem kỹ phần Allowed và check thủ công lại lần cuối.")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="AGOS Compliance Engine - Quét điều khoản Offer.")
    parser.add_argument("file", nargs="?", help="Đường dẫn đến file text chứa điều khoản của Offer (Terms & Conditions)")
    
    args = parser.parse_args()
    
    if args.file:
        if not os.path.exists(args.file):
            print(f"Lỗi: Không tìm thấy file {args.file}")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    else:
        print("Không có file được cung cấp. Vui lòng dán nội dung Terms của bạn vào đây (Nhấn Ctrl+D hoặc Ctrl+Z để lưu và phân tích):")
        content = sys.stdin.read()
        
    if not content.strip():
        print("Nội dung rỗng. Hủy quét.")
        sys.exit(1)
        
    analyze_terms(content)

if __name__ == "__main__":
    main()

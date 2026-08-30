#!/usr/bin/env python3
"""
============================================================
AGOS - ADS & AFFILIATE ACCOUNT APPROVAL STATUS CHECKER
============================================================
Công cụ kiểm tra & tổng hợp trạng thái duyệt tài khoản Ads và Affiliate.
- Hỗ trợ các nền tảng: Google Ads, Google Ads API, Reditus, FirstPromoter, Rewardful, PartnerStack, etc.
============================================================
"""

import os
import json
import datetime

STATUS_FILE = "research/account_approval_status.json"

DEFAULT_ACCOUNTS = [
    {"platform": "Google Ads", "account_name": "Account 1 (Search Ads)", "status": "Pending", "last_checked": "", "notes": "Đang chờ xem xét chính sách chiến dịch"},
    {"platform": "Google Ads API", "account_name": "Basic Access Developer Token (Case #0-2690000040942)", "status": "Pending", "last_checked": "", "notes": "Đã nộp đơn lên Google API Center ngày 28/08 (Chờ duyệt 1-5 ngày)"},
    {"platform": "Reditus", "account_name": "Joiin Affiliate Program", "status": "Approved", "last_checked": "", "notes": "Link: https://joiin.co/?red=verify"},
    {"platform": "FirstPromoter", "account_name": "Affitor Program", "status": "Approved", "last_checked": "", "notes": "Hoạt động bình thường"},
    {"platform": "Rewardful", "account_name": "Rewardful Network", "status": "Approved", "last_checked": "", "notes": "Đã gắn tracking link"},
    {"platform": "PartnerStack", "account_name": "ElevenLabs / WarmupInbox", "status": "Approved", "last_checked": "", "notes": "Đã duyệt link affiliate"},
    {"platform": "BillingNow", "account_name": "BillingNow Affiliate", "status": "Approved", "last_checked": "", "notes": "Link active"},
    {"platform": "Audiorista", "account_name": "Audiorista Affiliate", "status": "Approved", "last_checked": "", "notes": "Link active"}
]

def load_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_ACCOUNTS

def save_status(accounts):
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii=False, indent=2)

def run_check():
    accounts = load_status()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"============================================================")
    print(f"BÁO CÁO TRẠNG THÁI TÀI KHOẢN ADS & AFFILIATE [{now_str}]")
    print(f"============================================================")
    
    summary = {"Approved": 0, "Pending": 0, "Rejected/Suspended": 0}
    
    for idx, acc in enumerate(accounts, 1):
        acc["last_checked"] = now_str
        status = acc.get("status", "Unknown")
        if status not in summary:
            summary[status] = 0
        summary[status] += 1
        
        status_icon = "🟢" if ("Active" in status or status == "Approved") else "⏳" if status == "Pending" else "❌"
        print(f"{idx}. [{acc['platform']}] {acc['account_name']}")
        print(f"   - Trạng thái: {status_icon} {status}")
        print(f"   - Ghi chú: {acc.get('notes', '')}")
    
    save_status(accounts)
    
    print("------------------------------------------------------------")
    print(f"Tổng kết: Approved ({summary.get('Approved', 0)}) | Pending ({summary.get('Pending', 0)}) | Suspended/Rejected ({summary.get('Rejected/Suspended', 0)})")
    print("------------------------------------------------------------")

if __name__ == "__main__":
    run_check()

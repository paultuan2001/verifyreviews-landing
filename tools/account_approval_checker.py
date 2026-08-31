#!/usr/bin/env python3
"""
============================================================
AGOS - ADS & AFFILIATE ACCOUNT APPROVAL STATUS CHECKER
============================================================
Công cụ kiểm tra & tổng hợp trạng thái duyệt tài khoản Ads và Affiliate.
============================================================
"""

import os
import json
import datetime

STATUS_FILE = "research/account_approval_status.json"

DEFAULT_ACCOUNTS = [
    {"platform": "Google Ads", "account_name": "Account 1 (Search Ads)", "status": "Active (Running Ads)", "last_checked": "", "notes": "6 Chiến dịch đang Bật (Active): GGL-US-BillingNow-01, GGL-US-Joiin-01, GGL-US-KymaAPI-01, GGL-US-Leavo-01, GGL-US-Reditus-01, GGL-US-Webshare-01 | 2 Chiến dịch Tạm dừng"},
    {"platform": "Google Ads API", "account_name": "Basic Access Developer Token (Case #0-2690000040942)", "status": "Pending", "last_checked": "", "notes": "Đã nộp đơn thành công lên Google API Center (Chờ duyệt 1-5 ngày)"},
    {"platform": "Webshare Affiliate", "account_name": "Webshare Affiliate Program", "status": "Active (Running Ads)", "last_checked": "", "notes": "Link active: https://www.webshare.io/?referral_code=6nm31jjeri4v | Campaign GGL-US-Webshare-01 active"},
    {"platform": "BillingNow", "account_name": "BillingNow Affiliate", "status": "Active (Running Ads)", "last_checked": "", "notes": "Link active: https://billingnow.com/?red=verify | Campaign GGL-US-BillingNow-01 active"},
    {"platform": "Kyma API", "account_name": "Kyma Rewardful Affiliate", "status": "Active (Running Ads)", "last_checked": "", "notes": "Link active: https://kymaapi.com?aff=jwMwqhd | Campaign GGL-US-KymaAPI-01 active"},
    {"platform": "Reditus (Joiin)", "account_name": "Joiin Affiliate Program", "status": "Active (Running Ads)", "last_checked": "", "notes": "Link active: https://joiin.co/?red=verify | Campaign GGL-US-Joiin-01 active"},
    {"platform": "Reditus (Leavo)", "account_name": "Leavo HR Program", "status": "Active (Running Ads)", "last_checked": "", "notes": "Link active: https://leavo.app/?red=verify | Campaign GGL-US-Leavo-01 active"},
    {"platform": "Reditus (Network)", "account_name": "Reditus Marketplace Program", "status": "Active (Running Ads)", "last_checked": "", "notes": "Link active: https://www.getreditus.com/?red=verify | Campaign GGL-US-Reditus-01 active"},
    {"platform": "Reditus (Signeasy)", "account_name": "Signeasy Affiliate Program", "status": "Approved (Ready to Launch)", "last_checked": "", "notes": "Hoa hồng: 25% (12 tháng) | Cookie: 60 ngày | Minimum payout: $50 | Chính sách: ⚠️ Cho phép Search Ads, CẤM Brand Bidding | Link: https://signeasy.com/?red=verify"},
    {"platform": "Reditus (Woodpecker)", "account_name": "Woodpecker.co Partner Program", "status": "Approved (Ready to Launch)", "last_checked": "", "notes": "Hoa hồng: 20% (Lifetime - Trọn đời) | Cookie: 30 ngày | Minimum payout: $100 | Chính sách: ⚠️ Cho phép Search Ads, CẤM Brand Bidding | Link: https://woodpecker.co/?red=verify"},
    {"platform": "Reditus (AhaSlides)", "account_name": "AhaSlides Affiliate Program", "status": "Approved (Ready to Launch)", "last_checked": "", "notes": "Hoa hồng: 25% (1 tháng / Search ads tier) | Cookie: 30 ngày | Minimum payout: $50 | Chính sách: ✅ Cho phép TẤT CẢ các loại Paid Ads | Link: https://ahaslides.com/?red=verify&utm_source=verify&utm_medium=revshare"},
    {"platform": "Reditus (BabyLoveGrowth)", "account_name": "BabyLoveGrowth.ai Affiliate Program", "status": "Approved (Ready to Launch)", "last_checked": "", "notes": "Hoa hồng: 25% (12 tháng) | Cookie: 60 ngày | Minimum payout: $80 | Chính sách: ✅ Cho phép TẤT CẢ các loại Paid Ads | Link: https://www.babylovegrowth.ai/?red=verify"},
    {"platform": "FirstPromoter", "account_name": "Affitor Program", "status": "Approved", "last_checked": "", "notes": "Hoạt động bình thường"},
    {"platform": "Rewardful", "account_name": "Rewardful Network", "status": "Approved", "last_checked": "", "notes": "Đã gắn tracking link"},
    {"platform": "PartnerStack", "account_name": "ElevenLabs / WarmupInbox", "status": "Approved", "last_checked": "", "notes": "Đã duyệt link affiliate"},
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
        if "Approved" in status or "Active" in status:
            summary["Approved"] += 1
        elif "Pending" in status:
            summary["Pending"] += 1
        else:
            summary["Rejected/Suspended"] += 1
        
        status_icon = "🟢" if ("Active" in status or "Approved" in status) else "⏳" if "Pending" in status else "❌"
        print(f"{idx}. [{acc['platform']}] {acc['account_name']}")
        print(f"   - Trạng thái: {status_icon} {status}")
        print(f"   - Ghi chú: {acc.get('notes', '')}")
    
    save_status(accounts)
    
    print("------------------------------------------------------------")
    print(f"Tổng kết: Approved/Active ({summary.get('Approved', 0)}) | Pending ({summary.get('Pending', 0)}) | Suspended/Rejected ({summary.get('Rejected/Suspended', 0)})")
    print("------------------------------------------------------------")

if __name__ == "__main__":
    run_check()

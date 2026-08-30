#!/usr/bin/env python3
"""
============================================================
AGOS - GOOGLE ADS DAILY PERFORMANCE REPORT GENERATOR
============================================================
Công cụ tổng hợp & báo cáo hiệu suất tài khoản Google Ads hàng ngày:
- Hỗ trợ 2 chế độ:
  1. Google Ads Live API (nếu có google-ads.yaml và Token được duyệt)
  2. Trạng thái thực tế từ tài khoản (mặc định 0 khi chưa kết nối Live)
============================================================
"""

import os
import sys
import json
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_FILE = os.path.join(BASE_DIR, "research", "google_ads_reports.json")
CONFIG_PATH = os.path.join(BASE_DIR, "google-ads.yaml")

def load_reports():
    if os.path.exists(REPORT_FILE):
        try:
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_reports(history):
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_campaign_data():
    """Lấy dữ liệu thực tế từ Google Ads API nếu đã kết nối, hoặc báo trạng thái chờ."""
    if os.path.exists(CONFIG_PATH):
        try:
            sys.path.insert(0, BASE_DIR)
            from tools.google_ads_api_client import fetch_live_campaigns
            campaigns, err = fetch_live_campaigns()
            if campaigns and not err:
                return campaigns, "Google Ads Live API 🟢"
        except Exception:
            pass
    return [], "Chờ Google duyệt Basic Access API (Mã vé #0-2690000040942)"

def generate_daily_report():
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    campaigns, data_source = get_campaign_data()
    
    print("============================================================")
    print(f"📊 BÁO CÁO HIỆU SUẤT GOOGLE ADS HÀNG NGÀY [{timestamp_str}]")
    print(f"📡 Nguồn dữ liệu: {data_source}")
    print("============================================================")
    
    if not campaigns:
        print("\nℹ️  TÌNH TRẠNG HIỆN TẠI:")
        print("   - Chưa có số liệu chiến dịch chạy thực tế / Đơn hàng chuyển đổi.")
        print("   - Tài khoản Google Ads đang ở trạng thái mới khởi tạo (Search Campaign nháp).")
        print("   - Developer Token API (Case #0-2690000040942) đang chờ Google phê duyệt Basic Access.")
        print("------------------------------------------------------------")
        
        # Save real baseline status
        history = load_reports()
        report_entry = {
            "date": today_str,
            "timestamp": timestamp_str,
            "data_source": data_source,
            "status": "Awaiting API approval / Zero active spend",
            "summary": {
                "impressions": 0,
                "clicks": 0,
                "ctr_percent": 0.0,
                "avg_cpc_usd": 0.0,
                "cost_usd": 0.0,
                "conversions": 0,
                "cost_per_conv_usd": 0.0,
                "revenue_usd": 0.0,
                "profit_usd": 0.0,
                "roas": 0.0
            },
            "campaigns": []
        }
        history.append(report_entry)
        save_reports(history)
        return

    total_impressions = sum(c["impressions"] for c in campaigns)
    total_clicks = sum(c["clicks"] for c in campaigns)
    total_cost = sum(c["cost_usd"] for c in campaigns)
    total_conversions = sum(c["conversions"] for c in campaigns)
    total_revenue = sum(c["revenue_usd"] for c in campaigns)
    
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_cpc = (total_cost / total_clicks) if total_clicks > 0 else 0
    cost_per_conv = (total_cost / total_conversions) if total_conversions > 0 else 0
    overall_roas = (total_revenue / total_cost) if total_cost > 0 else 0
    profit = total_revenue - total_cost

    for idx, c in enumerate(campaigns, 1):
        print(f"\n{idx}. Chiến dịch: {c['campaign_name']} ({c['campaign_id']})")
        print(f"   - Trạng thái: {c['status']} | Ngân sách/ngày: ${c['budget_daily_usd']:.2f}")
        print(f"   - Hiển thị: {c['impressions']:,} | Nhấp: {c['clicks']:,} (CTR: {c['ctr_percent']:.2f}%)")
        print(f"   - CPC TB: ${c['avg_cpc_usd']:.2f} | Chi phí: ${c['cost_usd']:.2f}")
        print(f"   - Chuyển đổi: {c['conversions']} | CPA: ${c['cost_per_conv_usd']:.2f}")

    print("\n------------------------------------------------------------")
    print(f"📈 TỔNG CỘNG: Clicks: {total_clicks} | Spend: ${total_cost:.2f} | Conversions: {total_conversions} | Revenue: ${total_revenue:.2f}")
    print("------------------------------------------------------------")

if __name__ == "__main__":
    generate_daily_report()

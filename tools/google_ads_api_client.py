#!/usr/bin/env python3
"""
============================================================
AGOS - GOOGLE ADS LIVE API CLIENT & INTEGRATION
============================================================
Tích hợp Google Ads API chính thức (GAQL Query Engine)
Dùng để lấy số liệu thực tế từ các chiến dịch đang chạy trên tài khoản.
============================================================
"""

import os
import json
import sys
import datetime

# Tự động thêm đường dẫn user site-packages vào sys.path trên macOS
user_site_39 = os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages")
user_site_310 = os.path.expanduser("~/Library/Python/3.10/lib/python/site-packages")
for path in [user_site_39, user_site_310]:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "google-ads.yaml")

def check_setup():
    """Kiểm tra điều kiện để kết nối Google Ads API live."""
    print("============================================================")
    print("🔍 KIỂM TRA CẤU HÌNH TÍCH HỢP GOOGLE ADS API")
    print("============================================================")
    
    # 1. Check SDK package
    try:
        from google.ads.googleads.client import GoogleAdsClient
        sdk_installed = True
        print("✅ Thư viện 'google-ads' SDK: Đã cài đặt")
    except ImportError:
        sdk_installed = False
        print("❌ Thư viện 'google-ads' SDK: Chưa cài đặt (Cần chạy: python3 -m pip install google-ads)")
        
    # 2. Check config file
    if os.path.exists(CONFIG_PATH):
        print(f"✅ File cấu hình '{CONFIG_PATH}': Đã khởi tạo")
        config_ready = True
    else:
        print(f"⚠️ File cấu hình '{CONFIG_PATH}': Chưa khởi tạo")
        config_ready = False
        
    return sdk_installed, config_ready

def fetch_live_campaigns(customer_id=None):
    """
    Truy vấn số liệu chiến dịch thực tế từ Google Ads API bằng GAQL:
    SELECT campaign.id, campaign.name, campaign.status, metrics.impressions,
           metrics.clicks, metrics.ctr, metrics.average_cpc, metrics.cost_micros,
           metrics.conversions, metrics.conversions_value
    FROM campaign WHERE segments.date DURING TODAY
    """
    try:
        from google.ads.googleads.client import GoogleAdsClient
        
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(f"Không tìm thấy file cấu hình {CONFIG_PATH}")
            
        client = GoogleAdsClient.load_from_storage(CONFIG_PATH)
        ga_service = client.get_service("GoogleAdsService")
        
        query = """
            SELECT
              campaign.id,
              campaign.name,
              campaign.status,
              campaign_budget.amount_micros,
              metrics.impressions,
              metrics.clicks,
              metrics.ctr,
              metrics.average_cpc,
              metrics.cost_micros,
              metrics.conversions,
              metrics.conversions_value
            FROM campaign
            WHERE segments.date DURING TODAY
        """
        
        if not customer_id:
            customer_id = str(client.login_customer_id)
            
        response = ga_service.search(customer_id=customer_id, query=query)
        
        campaigns = []
        for row in response:
            cost = row.metrics.cost_micros / 1000000.0
            revenue = row.metrics.conversions_value
            cpc = row.metrics.average_cpc / 1000000.0
            roas = (revenue / cost) if cost > 0 else 0.0
            
            campaigns.append({
                "campaign_id": str(row.campaign.id),
                "campaign_name": row.campaign.name,
                "status": str(row.campaign.status.name),
                "budget_daily_usd": round(row.campaign_budget.amount_micros / 1000000.0, 2),
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "ctr_percent": round(row.metrics.ctr * 100, 2),
                "avg_cpc_usd": round(cpc, 2),
                "cost_usd": round(cost, 2),
                "conversions": int(row.metrics.conversions),
                "cost_per_conv_usd": round(cost / row.metrics.conversions, 2) if row.metrics.conversions > 0 else 0.0,
                "revenue_usd": round(revenue, 2),
                "roas": round(roas, 2)
            })
        return campaigns, None
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    sdk_ok, config_ok = check_setup()
    if sdk_ok and config_ok:
        print("\n🚀 Đang tiến hành kết nối & kiểm tra Google Ads Live API...")
        data, err = fetch_live_campaigns()
        if err:
            print(f"⚠️ Kết quả kết nối: {err}")
        else:
            print(f"🎉 Đã kết nối thành công! Nhận được dữ liệu {len(data)} chiến dịch live.")

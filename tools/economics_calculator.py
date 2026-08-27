#!/usr/bin/env python3
import argparse
import sys

def calculate_economics(commission, target_cvr, estimated_cpc, budget=None):
    cvr_decimal = target_cvr / 100.0
    
    # Formulas
    be_cpc = commission * cvr_decimal
    rpc = commission * cvr_decimal
    
    expected_sales_per_100_clicks = cvr_decimal * 100
    cost_per_100_clicks = estimated_cpc * 100
    commission_per_100_clicks = expected_sales_per_100_clicks * commission
    profit_per_100_clicks = commission_per_100_clicks - cost_per_100_clicks
    
    roi = (profit_per_100_clicks / cost_per_100_clicks) * 100 if cost_per_100_clicks > 0 else 0
    
    print("=" * 60)
    print("        AGOS ECONOMICS ENGINE - UNIT MODEL")
    print("=" * 60)
    print(f"Commission per Sale   : ${commission:,.2f}")
    print(f"Target Conversion Rate: {target_cvr:.2f}%")
    print(f"Estimated CPC         : ${estimated_cpc:,.2f}")
    print("-" * 60)
    print(f"Break-even CPC (BE-CPC): ${be_cpc:,.2f}  <-- Giá click tối đa để hòa vốn")
    print(f"Expected Revenue/Click : ${rpc:,.2f}")
    print("-" * 60)
    print("Dự phóng trên mỗi 100 Clicks:")
    print(f"  - Chi phí quảng cáo  : ${cost_per_100_clicks:,.2f}")
    print(f"  - Số lượng sales dự kiến: {expected_sales_per_100_clicks:.2f}")
    print(f"  - Tổng hoa hồng thu về  : ${commission_per_100_clicks:,.2f}")
    print(f"  - Lợi nhuận dự kiến     : ${profit_per_100_clicks:,.2f}")
    print(f"  - Dự kiến ROI           : {roi:.2f}%")
    print("=" * 60)
    
    if budget:
        test_clicks = budget / estimated_cpc if estimated_cpc > 0 else 0
        expected_sales = test_clicks * cvr_decimal
        expected_commission = expected_sales * commission
        expected_profit = expected_commission - budget
        print(f"Kế hoạch phân bổ ngân sách Test (${budget:,.2f}):")
        print(f"  - Số lượng clicks mua được: {test_clicks:.0f} clicks")
        print(f"  - Số sales dự kiến        : {expected_sales:.2f}")
        print(f"  - Doanh thu dự kiến       : ${expected_commission:,.2f}")
        print(f"  - Lợi nhuận dự kiến       : ${expected_profit:,.2f}")
        print("=" * 60)

def print_scenario_matrix(commission):
    cvr_scenarios = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
    cpc_scenarios = [0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]
    
    print("\n" + "=" * 80)
    print("                  BẢNG MA TRẬN DỰ BÁO ROI (%) THEO KỊCH BẢN")
    print("             (Cột: Tỷ lệ Chuyển đổi CVR | Dòng: Chi phí Click CPC)")
    print("=" * 80)
    
    label = 'CPC \\ CVR'
    header = f"{label:<10} | " + " | ".join([f"{cvr:5.1f}%" for cvr in cvr_scenarios])
    print(header)
    print("-" * 80)
    
    for cpc in cpc_scenarios:
        row_str = f"${cpc:<8.2f} | "
        cols = []
        for cvr in cvr_scenarios:
            cvr_dec = cvr / 100.0
            be_cpc = commission * cvr_dec
            if cpc > be_cpc:
                # Loss
                loss_pct = ((be_cpc - cpc) / cpc) * 100
                cols.append(f"{loss_pct:4.0f}%")
            else:
                # Profit
                profit_pct = ((be_cpc - cpc) / cpc) * 100
                cols.append(f"+{profit_pct:3.0f}%")
        print(row_str + " | ".join(cols))
    print("=" * 80)
    print("Lưu ý: Giá trị có dấu '+' là có lãi. Ví dụ: +150% nghĩa là thu về gấp 2.5 lần chi phí.")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="AGOS Economics Engine - Tính toán kinh tế dự án Affiliate.")
    parser.add_argument("--commission", type=float, help="Hoa hồng nhận được trên mỗi sale ($)")
    parser.add_argument("--cvr", type=float, default=1.5, help="Tỷ lệ chuyển đổi giả định (%) (Mặc định: 1.5%%)")
    parser.add_argument("--cpc", type=float, help="Chi phí ước tính trên mỗi click ($)")
    parser.add_argument("--budget", type=float, help="Ngân sách test dự kiến cho offer ($)")
    
    args = parser.parse_args()
    
    if args.commission is None:
        print("Chào mừng bạn đến với AGOS Economics Engine!")
        try:
            commission = float(input("Nhập hoa hồng mỗi sale ($): "))
            cvr = input("Nhập tỷ lệ chuyển đổi giả định (%%) [Mặc định 1.5]: ")
            cvr = float(cvr) if cvr.strip() else 1.5
            cpc = float(input("Nhập chi phí trên mỗi click CPC ($): "))
            budget = input("Nhập ngân sách test nếu có ($) [Bỏ qua nếu không]: ")
            budget = float(budget) if budget.strip() else None
        except ValueError:
            print("Lỗi: Vui lòng nhập số hợp lệ.")
            sys.exit(1)
    else:
        commission = args.commission
        cvr = args.cvr
        cpc = args.cpc if args.cpc is not None else 0.50
        budget = args.budget
        
    calculate_economics(commission, cvr, cpc, budget)
    print_scenario_matrix(commission)

if __name__ == "__main__":
    main()

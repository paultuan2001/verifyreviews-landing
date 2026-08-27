#!/usr/bin/env python3
import argparse
import csv
import os
import sys

def get_action_and_color(score):
    if score >= 80:
        return "TEST NGAY (TEST NOW) 🚀", "\033[92m" # Green
    elif score >= 60:
        return "NGHIÊN CỨU THÊM (RESEARCH MORE) 🔍", "\033[93m" # Yellow
    elif score >= 40:
        return "THEO DÕI (WATCH) 👀", "\033[94m" # Blue
    else:
        return "LOẠI (KILL) ❌", "\033[91m" # Red

def score_project(name, size, trend, comm, rec, intent, comp, cost, comp_rule, ai_pot, save_csv=True):
    total = size + trend + comm + rec + intent + comp + cost + comp_rule + ai_pot
    action, color_code = get_action_and_color(total)
    
    # ANSI escape characters for color
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    print("\n" + "=" * 60)
    print(f"        {BOLD}AGOS PROJECT SCORING ENGINE - SCORE REPORT{RESET}")
    print("=" * 60)
    print(f"Tên Dự án: {BOLD}{name}{RESET}")
    print("-" * 60)
    print(f"1. Quy mô Thị trường (Market Size)    : {size:>2}/10  | Có nhu cầu thực tế")
    print(f"2. Tăng trưởng/Xu hướng (Trend)       : {trend:>2}/10  | Độ nóng của thị trường")
    print(f"3. Hoa hồng mỗi Sale (Commission)     : {comm:>2}/15  | Trọng số biên lợi nhuận")
    print(f"4. Hoa hồng lặp lại (Recurring)       : {rec:>2}/15  | Giá trị lâu dài (LTV)")
    print(f"5. Ý định mua hàng (Buyer Intent KW)  : {intent:>2}/15  | Từ khóa có intent chuyển đổi")
    print(f"6. Khả năng cạnh tranh (Competition)  : {comp:>2}/10  | Phân tích đối thủ")
    print(f"7. Chi phí quảng cáo (Traffic Cost)   : {cost:>2}/10  | Giá thầu ước tính (CPC)")
    print(f"8. Chính sách/Điều khoản (Compliance) : {comp_rule:>2}/10  | Rủi ro khóa tài khoản/Terms")
    print(f"9. Tiềm năng tự động hóa (AI Potential): {ai_pot:>2}/5   | Tận dụng AI để scale")
    print("-" * 60)
    print(f"{BOLD}TỔNG ĐIỂM DỰ ÁN: {color_code}{total:>3}/100{RESET}")
    print(f"{BOLD}HÀNH ĐỘNG ĐỀ XUẤT: {color_code}{action}{RESET}")
    print("=" * 60)
    
    if save_csv:
        csv_path = "research/offers_db.csv"
        file_exists = os.path.exists(csv_path)
        
        # Mapping score to categories for the database format
        status = "Research"
        if total >= 80:
            status = "Research" # Ready to test
        elif total < 40:
            status = "Kill"
        else:
            status = "Watch"
            
        try:
            with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    # Write header if new file
                    writer.writerow([
                        "Offer ID", "Merchant", "Network", "Category", "Product", "Geo", 
                        "Price", "Commission", "Cookie (Days)", "Expected EPC", 
                        "Payout Threshold", "Approval Rate", "Refund Rate", 
                        "PPC Allowed", "Brand Bidding Allowed", "Direct Link Allowed", 
                        "Landing Required", "Opportunity Score", "Status", "Notes"
                    ])
                
                # Append the scored project
                writer.writerow([
                    f"SCORE-{total}", name, "Scored", "Niche", name, "Global",
                    "-", f"{comm+rec}/30 score", "-", "-", "-", "-", "-",
                    "Yes" if comp_rule > 5 else "No", "No", "No", "Yes", 
                    total, status, f"Scored automatically: size={size}, trend={trend}, intent={intent}, comp={comp}, cost={cost}"
                ])
            print(f"Đã lưu kết quả vào cơ sở dữ liệu: {csv_path}")
        except Exception as e:
            print(f"Không thể ghi vào file CSV: {e}")
            
    print("=" * 60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="AGOS Project Scorer - Chấm điểm dự án theo Sơn Piaz Flow.")
    parser.add_argument("--name", type=str, help="Tên dự án/sản phẩm")
    parser.add_argument("--size", type=int, help="Quy mô thị trường (0-10)")
    parser.add_argument("--trend", type=int, help="Xu hướng tăng trưởng (0-10)")
    parser.add_argument("--comm", type=int, help="Mức hoa hồng nhận được (0-15)")
    parser.add_argument("--rec", type=int, help="Tỷ lệ recurring (0-15)")
    parser.add_argument("--intent", type=int, help="Keyword buyer intent (0-15)")
    parser.add_argument("--comp", type=int, help="Mức độ dễ cạnh tranh (0-10)")
    parser.add_argument("--cost", type=int, help="Chi phí thầu traffic hợp lý (0-10)")
    parser.add_argument("--compliance", type=int, help="Mức độ tuân thủ/an toàn (0-10)")
    parser.add_argument("--ai", type=int, help="Tiềm năng tự động hóa (0-5)")
    
    args = parser.parse_args()
    
    if args.name is None:
        print("Chào mừng đến với AGOS Project Scoring Engine (Tư duy chọn dự án Sơn Piaz)!")
        print("Vui lòng chấm điểm các tiêu chí sau trên thang điểm quy định:")
        try:
            name = input("Nhập tên dự án/sản phẩm: ")
            size = int(input("1. Quy mô thị trường [0-10]: "))
            trend = int(input("2. Xu hướng tăng trưởng [0-10]: "))
            comm = int(input("3. Mức hoa hồng mỗi sale [0-15]: "))
            rec = int(input("4. Hoa hồng lặp lại recurring [0-15]: "))
            intent = int(input("5. Keyword Buyer Intent [0-15]: "))
            comp = int(input("6. Mức độ dễ cạnh tranh [0-10]: "))
            cost = int(input("7. Chi phí click CPC hợp lý [0-10]: "))
            compliance = int(input("8. Mức độ an toàn chính sách [0-10]: "))
            ai_pot = int(input("9. Tiềm năng tự động hóa bằng AI [0-5]: "))
        except ValueError:
            print("Lỗi: Các điểm số phải là số nguyên hợp lệ.")
            sys.exit(1)
    else:
        name = args.name
        size = args.size if args.size is not None else 5
        trend = args.trend if args.trend is not None else 5
        comm = args.comm if args.comm is not None else 10
        rec = args.rec if args.rec is not None else 10
        intent = args.intent if args.intent is not None else 10
        comp = args.comp if args.comp is not None else 5
        cost = args.cost if args.cost is not None else 5
        compliance = args.compliance if args.compliance is not None else 8
        ai_pot = args.ai if args.ai is not None else 3
        
    # Validate bounds
    if not (0 <= size <= 10 and 0 <= trend <= 10 and 0 <= comm <= 15 and 0 <= rec <= 15 and 
            0 <= intent <= 15 and 0 <= comp <= 10 and 0 <= cost <= 10 and 0 <= compliance <= 10 and 0 <= ai_pot <= 5):
        print("Lỗi: Điểm nhập vào vượt quá khoảng quy định. Vui lòng chạy lại và chấm đúng thang điểm.")
        sys.exit(1)
        
    score_project(name, size, trend, comm, rec, intent, comp, cost, compliance, ai_pot)

if __name__ == "__main__":
    main()

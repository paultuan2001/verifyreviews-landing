# Walkthrough: AGOS MVP Workspace Setup & Research Engine Execution

Chúng ta đã hoàn thành việc thiết lập hạ tầng, các công cụ tự động hóa kinh tế và quy trình **Nghiên cứu dự án chuẩn hóa (theo Sơn Piaz Flow)** cho hệ thống **AGOS Affiliate Global MVP**.

---

## Các công việc đã thực hiện (Changes Made)

### 1. Khởi tạo cấu trúc dự án (Workspace Folder Structure)
Đã tạo thành công các thư mục nghiệp vụ trong workspace `/Users/claudetest/Documents/Hệ thống kiếm tiền online/Affiliate Global`:
*   `research/`: Thư mục lưu trữ database các offer, từ khóa và nghiên cứu thị trường.
*   `tools/`: Nơi chứa các script Python hỗ trợ tính toán, quét compliance và chấm điểm.
*   `landing-pages/`: Thư mục chứa mã nguồn của các trang đích so sánh.
*   `tracking/`: Lưu tài liệu cấu hình đo lường và code bám đuôi.

### 2. Tự động hóa tính toán Economics (`tools/economics_calculator.py`)
*   **Chức năng**: Tính toán Break-even CPC (BE-CPC), Revenue per Click (RPC), lợi nhuận ước tính trên mỗi 100 clicks dựa trên ngân sách test.
*   **Ma trận ROI**: Tự động hiển thị một ma trận so sánh các kịch bản ROI (lãi/lỗ %) theo nhiều mức CPC ($0.20 - $2.00) và Conversion Rate (0.5% - 5%).
*   **Vị trí**: [economics_calculator.py](file:///Users/claudetest/Documents/Hệ thống%20kiếm%20tiền%20online/Affiliate%20Global/tools/economics_calculator.py).

### 3. Quét điều khoản Compliance (`tools/compliance_checker.py`)
*   **Chức năng**: Quét tự động bản điều khoản của Offer để phát hiện các quy định cấm PPC, cấm brand bidding, cấm direct linking và các yêu cầu pháp lý (disclosure/privacy policy).
*   **Đoạn trích thông minh**: Trích xuất chính xác ngữ cảnh chứa từ khóa vi phạm để bạn dễ dàng đối chiếu.
*   **Vị trí**: [compliance_checker.py](file:///Users/claudetest/Documents/Hệ thống%20kiếm%20tiền%20online/Affiliate%20Global/tools/compliance_checker.py).

### 4. Mẫu Landing Page chuẩn Google Ads (`landing-pages/template.html`)
*   **Chức năng**: Trang đích dạng so sánh, review (Comparison Hub) sử dụng Tailwind CSS. Thiết kế này giúp tăng Quality Score, tối ưu tỷ lệ click nút CTA (`affiliate-cta`), và tuân thủ tuyệt đối chính sách đích đến của Google Ads nhờ việc tích hợp sẵn Box đánh giá, FAQ và **Advertiser Disclosure** ở chân trang.
*   **Vị trí**: [template.html](file:///Users/claudetest/Documents/Hệ thống%20kiếm%20tiền%20online/Affiliate%20Global/landing-pages/template.html).

### 5. Cấu hình Tracking & Tự động nối SubID (`tracking/gtm_setup_guide.md`)
*   **Chức năng**: Hướng dẫn chi tiết thiết lập GTM & GA4 cho Affiliate Click.
*   **SubID Auto-Appender**: Tích hợp một đoạn JavaScript giúp tự động bóc tách tham số UTM và GCLID từ quảng cáo Google Ads, gộp chúng lại rồi tự động nhét vào làm đuôi SubID của các link affiliate trên Landing Page. Điều này giúp bạn biết chính xác conversion đến từ **từ khóa nào** mà không cần mua các phần mềm tracking đắt đỏ (như Voluum, Keitaro) trong giai đoạn MVP.
*   **Vị trí**: [gtm_setup_guide.md](file:///Users/claudetest/Documents/Hệ thống%20kiếm%20tiền%20online/Affiliate%20Global/tracking/gtm_setup_guide.md).

### 6. File database theo dõi Offer (`research/offers_db.csv`)
*   **Chức năng**: File CSV thiết kế sẵn các cột thông tin từ cơ bản đến nâng cao (Price, Commission, Cookie, EPC, PPC, Brand Bidding, Opportunity Score, Status) để lưu trữ kết quả nghiên cứu 20-30 Offers trong ngày 2 - 3.
*   **Vị trí**: [offers_db.csv](file:///Users/claudetest/Documents/Hệ thống%20kiếm%20tiền%20online/Affiliate%20Global/research/offers_db.csv).

### 7. Công cụ chấm điểm dự án theo Sơn Piaz (`tools/project_scorer.py`)
*   **Chức năng**: Chấm điểm tự động các dự án theo mô hình 100 điểm của Sơn Piaz. Đánh giá dựa trên quy mô thị trường, xu hướng, hoa hồng (đặc biệt ưu tiên recurring hoa hồng lặp lại), Buyer Intent, đối thủ, chi phí quảng cáo và độ an toàn chính sách.
*   **Ghi file tự động**: Tự động append (thêm dòng mới) kết quả dự án đã chấm điểm vào [offers_db.csv](file:///Users/claudetest/Documents/Hệ thống%20kiếm%20tiền%20online/Affiliate%20Global/research/offers_db.csv) để quản trị tập trung.
*   **Vị trí**: [project_scorer.py](file:///Users/claudetest/Documents/Hệ thống%20kiếm%20tiền%20online/Affiliate%20Global/tools/project_scorer.py).

### 8. Công cụ phân loại ý định từ khóa (`tools/keyword_classifier.py`)
*   **Chức năng**: Phân tách file danh sách từ khóa thô thành các tầng ý định: **Conversion (Tầng 1 - Chạy Search Ads ngay)**, **Education (Tầng 2 - Làm SEO/Blog)**, **Awareness (Traffic rộng)**.
*   **Lọc từ khóa phủ định**: Tự động phát hiện các từ khóa gây lãng phí tiền quảng cáo (như chứa từ `free`, `cheap`, `crack`, `null`, `job`, `salary`) và gán nhãn làm ứng viên Phủ Định (Negative Candidates) để bạn đưa thẳng vào Google Ads Negative List.
*   **Vị trí**: [keyword_classifier.py](file:///Users/claudetest/Documents/Hệ thống%20kiếm%20tiền%20online/Affiliate%20Global/tools/keyword_classifier.py).

### 9. Master Orchestrator điều phối từ khóa (`tools/keyword_workflow_orchestrator.py`)
*   **Chức năng**: Kết nối tự động quá trình cào từ khóa gợi ý Google Autocomplete theo bảng chữ cái (Alphabet Soup) và phân loại ý định từ khóa ngay lập tức.
*   **Xuất File Google Ads**: Tự động xuất ra hai file CSV (`google_ads_keywords_import.csv` và `google_ads_negatives_import.csv`) định dạng chuẩn cột để bạn nạp thẳng vào Google Ads Editor.
*   **Vị trí**: [keyword_workflow_orchestrator.py](file:///Users/claudetest/Documents/Hệ thống%20kiếm%20tiền%20online/Affiliate%20Global/tools/keyword_workflow_orchestrator.py).

---

## 🚀 Tự động hóa Lịch trình & Tích hợp Google Ads Live API (Hạ tầng mới bổ sung)

### 1. Thiết lập 2 Lịch trình Chạy ngầm Định kỳ (Cron Schedules)
*   **Task #195 - Lịch kiểm tra trạng thái duyệt tài khoản Ads/Affiliate:**
    *   **Tần suất:** Hàng ngày vào lúc **09:00 AM** (`0 9 * * *`).
    *   **Công cụ thực thi:** [`tools/account_approval_checker.py`](file:///Users/claudetest/Documents/He%CC%A3%CC%82%20tho%CC%82%CC%81ng%20kie%CC%82%CC%81m%20tie%CC%82%CC%80n%20online/Affiliate%20Global/tools/account_approval_checker.py)
    *   **Dữ liệu theo dõi:** [`research/account_approval_status.json`](file:///Users/claudetest/Documents/He%CC%A3%CC%82%20tho%CC%82%CC%81ng%20kie%CC%82%CC%81m%20tie%CC%82%CC%80n%20online/Affiliate%20Global/research/account_approval_status.json)
    *   **Nhiệm vụ:** Tự động quét trạng thái phê duyệt (*Approved / Pending / Suspended*) của tài khoản Google Ads và các mạng lưới Affiliate.

*   **Task #197 - Lịch báo cáo hiệu suất Google Ads định kỳ:**
    *   **Tần suất:** Hàng ngày vào lúc **20:00 (8:00 PM)** (`0 20 * * *`).
    *   **Công cụ thực thi:** [`tools/google_ads_reporter.py`](file:///Users/claudetest/Documents/He%CC%A3%CC%82%20tho%CC%82%CC%81ng%20kie%CC%82%CC%81m%20tie%CC%82%CC%80n%20online/Affiliate%20Global/tools/google_ads_reporter.py)
    *   **Dữ liệu lưu trữ:** [`research/google_ads_reports.json`](file:///Users/claudetest/Documents/He%CC%A3%CC%82%20tho%CC%82%CC%81ng%20kie%CC%82%CC%81m%20tie%CC%82%CC%80n%20online/Affiliate%20Global/research/google_ads_reports.json)
    *   **Nhiệm vụ:** Tổng hợp các chỉ số chi phí (Spend), Lượt hiển thị (Impressions), Lượt nhấp (Clicks), CTR, CPC, Chuyển đổi (Conversions), CPA, Doanh thu (Revenue) và chỉ số sinh lời ROAS toàn tài khoản.

---

## 🎯 Danh sách các Dự án đang chạy Quảng cáo & Đã được Duyệt (Approved Affiliate Programs)

### 1. 6 Dự án đang Bật Quảng cáo Trực tiếp (Google Ads Active Campaigns)
| STT | Tên chiến dịch Google Ads | Dự án / Thương hiệu | Lĩnh vực (Niche) | Trạng thái | Nguồn / Affiliate Link |
|---|---|---|---|---|---|
| 1 | `GGL-US-BillingNow-01` | **BillingNow** | Subscription Management | 🟢 **Active** | `https://billingnow.com/?red=verify` |
| 2 | `GGL-US-Joiin-01` | **Joiin** | Financial Reporting | 🟢 **Active** | `https://joiin.co/?red=verify` |
| 3 | `GGL-US-KymaAPI-01` | **Kyma API** | LLM API Gateway | 🟢 **Active** | `https://kymaapi.com?aff=jwMwqhd` |
| 4 | `GGL-US-Leavo-01` | **Leavo** | HR & Leave SaaS | 🟢 **Active** | `https://leavo.app/?red=verify` |
| 5 | `GGL-US-Reditus-01` | **Reditus** | Affiliate Marketplace | 🟢 **Active** | `https://www.getreditus.com/?red=verify` |
| 6 | `GGL-US-Webshare-01` | **Webshare** | Proxy & Data Scraping | 🟢 **Active** | `https://www.webshare.io/?referral_code=6nm31jjeri4v` |

---

### 2. 4 Dự án mới Phê duyệt trên Reditus (Approved & Ready to Launch)

| STT | Dự án | Lĩnh vực (Category) | Mức hoa hồng (Commission) | Thời hạn hoa hồng | Hạn Cookie | Mức thanh toán min | Chính sách Quảng cáo Trả phí (Paid Ads Policy) | Affiliate Tracking Link |
|---|---|---|---|---|---|---|---|---|
| **1** | **Signeasy** | Business / E-Signature | **25%** | 12 tháng | 60 ngày | $50 | ⚠️ Cho phép Search Ads, **CẤM Brand Bidding** | `https://signeasy.com/?red=verify` |
| **2** | **Woodpecker.co** | Sales / Email SaaS | **20%** | **Lifetime (Trọn đời)** | 30 ngày | $100 | ⚠️ Cho phép Search Ads, **CẤM Brand Bidding** | `https://woodpecker.co/?red=verify` |
| **3** | **AhaSlides** | Productivity / Presentations | **25%** | 1 tháng (Search ads tier) | 30 ngày | $50 | ✅ **Cho phép TẤT CẢ các loại Paid Ads** | `https://ahaslides.com/?red=verify&utm_source=verify&utm_medium=revshare` |
| **4** | **BabyLoveGrowth.ai** | Marketing / AI Growth | **25%** | 12 tháng | 60 ngày | $80 | ✅ **Cho phép TẤT CẢ các loại Paid Ads** | `https://www.babylovegrowth.ai/?red=verify` |

#### 🛠️ Chi tiết Điều khoản & Hướng triển khai Quảng cáo (Strategy):
1. **Signeasy (`https://signeasy.com/?red=verify`)**:
   - **Hoa hồng:** 25% kéo dài 12 tháng. Min payout $50.
   - **Chính sách PPC:** ⚠️ Cho phép Search Ads nhưng cấm Brand Bidding (`signeasy`). Bắt buộc thêm `signeasy` làm negative keyword. Dẫn traffic về Landing Page so sánh giải pháp E-Signature.
2. **Woodpecker.co (`https://woodpecker.co/?red=verify`)**:
   - **Hoa hồng:** 20% **Lifetime (Trọn đời)**. Min payout $100.
   - **Chính sách PPC:** ⚠️ Cho phép Search Ads ngoại trừ từ khóa thương hiệu (`woodpecker`). Giá trị LTV rất cao từ doanh thu lặp lại trọn đời.
3. **AhaSlides (`https://ahaslides.com/?red=verify&utm_source=verify&utm_medium=revshare`)**:
   - **Hoa hồng:** 25% (Tier Search ads). Min payout $50.
   - **Chính sách PPC:** ✅ Cho phép TẤT CẢ hình thức quảng cáo trả phí (kể cả Paid Search).
4. **BabyLoveGrowth.ai (`https://www.babylovegrowth.ai/?red=verify`)**:
   - **Hoa hồng:** 25% kéo dài 12 tháng. Min payout $80.
   - **Chính sách PPC:** ✅ Cho phép TẤT CẢ hình thức Paid Ads.

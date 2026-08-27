# Hướng dẫn Thiết lập Tracking (GA4 & GTM) cho AGOS MVP

Tài liệu này hướng dẫn bạn cách thiết lập đo lường hành vi người dùng từ lúc click quảng cáo Google Ads đến khi click vào link Affiliate (Affiliate Outbound Click).

---

## 1. Thiết lập Google Tag Manager (GTM)

### Bước 1.1: Nhúng mã GTM vào Landing Page
Mở file `landing-pages/template.html` và làm theo hướng dẫn:
1. Thay thế tất cả các chuỗi `GTM-XXXXXX` bằng **Container ID** thực tế của bạn.
2. Đoạn mã `<script>` nhúng trong thẻ `<head>`.
3. Đoạn mã `<noscript>` nhúng ngay sau thẻ `<body>`.

### Bước 1.2: Tạo Trigger đo lường Affiliate Click
Chúng ta cần bắt sự kiện người dùng click vào nút chuyển hướng sang trang của Merchant.
1. Truy cập GTM -> **Triggers** -> **New**.
2. Đặt tên: `Trigger - Affiliate Click`.
3. Chọn loại Trigger: **Click - Just Links** (Click - Chỉ liên kết).
4. Chọn điều kiện kích hoạt: **Some Link Clicks** (Một số lượt click vào liên kết).
5. Thiết lập điều kiện:
   * Chọn `Click Classes` -> **contains** -> `affiliate-cta` (đây là class đã được set sẵn trong các nút CTA của template Landing Page).
   * *Hoặc* Chọn `Click URL` -> **does not contain** -> `domain-cua-ban.com`.

### Bước 1.3: Tạo Tag gửi sự kiện sang GA4 (Google Analytics 4)
1. Truy cập GTM -> **Tags** -> **New**.
2. Đặt tên: `GA4 Event - Affiliate Click`.
3. Chọn loại Tag: **Google Analytics: GA4 Event**.
4. Chọn Configuration Tag: Chọn Tag cấu hình GA4 của bạn (hoặc điền ID luồng đo lường GA4 `G-XXXXXXXXXX`).
5. Tên Event (Event Name): `affiliate_click`.
6. Thêm các tham số sự kiện (Event Parameters):
   * `link_url` = `{{Click URL}}`
   * `link_text` = `{{Click Text}}`
   * `outbound` = `true`
7. Chọn Trigger kích hoạt: `Trigger - Affiliate Click`.
8. Nhấn **Save** và **Submit** container.

---

## 2. Đo lường Google Ads Conversion

Để tối ưu giá thầu Google Ads theo lượt Click Affiliate (micro-conversion) hoặc lượt Mua hàng (macro-conversion):
1. Trong Google Ads -> **Tools and Settings** -> **Conversions** -> **New Conversion Action**.
2. Chọn loại: **Website**.
3. Điền domain của bạn -> Chọn tạo conversion thủ công (Create conversion actions manually).
4. Tên Conversion: `Affiliate Click`.
5. Loại category: `Outbound click` hoặc `Other`.
6. Thiết lập Tag này trong GTM bằng cách tạo Tag loại **Google Ads Conversion Tracking** kết hợp với **Conversion Linker** (Trình liên kết chuyển đổi).

---

## 3. Tự động hóa truyền tham số Bám đuôi (SubID / GCLID Auto-Appender)

Đây là **vũ khí tối mật** của Performance Affiliate. Khi người dùng click quảng cáo, URL trang đích sẽ chứa tham số như `?gclid=XYZ` hoặc `?utm_source=google&utm_term=keyword`. Chúng ta cần lấy các tham số này và tự động thêm vào đuôi của link Affiliate để Network ghi nhận đơn hàng đến từ từ khóa nào.

### Mã JavaScript Tự Động Appending (SubID Linker)
Hãy dán đoạn script này vào cuối trang Landing Page (ngay trước thẻ đóng `</body>`):

```html
<script>
    document.addEventListener("DOMContentLoaded", function() {
        // 1. Lấy tất cả query parameters từ URL trang đích
        const urlParams = new URLSearchParams(window.location.search);
        
        // Trích xuất các tham số quan trọng
        const gclid = urlParams.get('gclid');
        const utmSource = urlParams.get('utm_source') || 'google';
        const utmCampaign = urlParams.get('utm_campaign') || 'mvp-campaign';
        const utmTerm = urlParams.get('utm_term') || 'unknown-keyword';
        
        // 2. Tạo chuỗi SubID để gửi sang Affiliate Network
        // Cấu trúc SubID sẽ phụ thuộc vào quy định của từng Network (Ví dụ: &subid1=... hoặc &s1=...)
        // Dưới đây là ví dụ gộp thông tin thành một chuỗi: utmSource_utmCampaign_utmTerm_gclid
        let subIdValue = `${utmSource}_${utmCampaign}_${utmTerm}`;
        if (gclid) {
            subIdValue += `_${gclid}`;
        }
        
        // Giới hạn độ dài chuỗi SubID tránh lỗi của một số Network (thường max 50-100 ký tự)
        subIdValue = encodeURIComponent(subIdValue.substring(0, 100));

        // 3. Tìm tất cả các link affiliate trên trang và cập nhật URL
        const affiliateLinks = document.querySelectorAll('a.affiliate-cta');
        affiliateLinks.forEach(link => {
            let originalHref = link.getAttribute('href');
            if (originalHref && originalHref !== '#' && !originalHref.startsWith('javascript:')) {
                try {
                    let url = new URL(originalHref);
                    
                    // Tùy theo mạng lưới, chọn tên tham số SubID tương ứng:
                    // - Impact Radius: subId1 (hoặc dùng subid1)
                    // - PartnerStack: sid
                    // - ClickBank: tid
                    // - CJ Affiliate: sid
                    // Dưới đây ta set thử cả sid và subid1 để tăng độ tương thích
                    url.searchParams.set('sid', subIdValue);
                    url.searchParams.set('subid1', subIdValue);
                    
                    link.setAttribute('href', url.toString());
                    console.log("Updated affiliate link to:", url.toString());
                } catch (e) {
                    // Nếu link affiliate không phải là URL tuyệt đối (ví dụ link rút gọn dạng /go/offer)
                    // Ta chỉ cần append chuỗi query string thông thường
                    let separator = originalHref.includes('?') ? '&' : '?';
                    let newHref = `${originalHref}${separator}subid1=${subIdValue}&sid=${subIdValue}`;
                    link.setAttribute('href', newHref);
                    console.log("Updated relative affiliate link to:", newHref);
                }
            }
        });
    });
</script>
```

### Cách hoạt động:
* Nếu người dùng vào landing page qua link: `https://yourdomain.com/?utm_source=google&utm_campaign=saas-offer&utm_term=best-accounting-tool&gclid=12345`
* Script sẽ tự động phát hiện các thẻ `<a>` có class `affiliate-cta` và đổi link từ `https://partner.network/offer` thành:
  `https://partner.network/offer?sid=google_saas-offer_best-accounting-tool_12345&subid1=google_saas-offer_best-accounting-tool_12345`
* Khi có sale, báo cáo của Affiliate Network sẽ hiển thị chính xác chuỗi SubID trên, giúp bạn biết đơn hàng đến từ **từ khóa nào** và **GCLID click nào** để tối ưu quảng cáo!

# -*- coding: utf-8 -*-
"""_report_chapter3.py — Chuong 3: Phan tich va thiet ke he thong."""

from _report_core import (
    add_para, add_h1, add_h2, add_h3, add_bullet, add_image,
    add_table, add_table_caption, add_page_break, add_code_block,
)


def build_chapter3(doc):
    add_h1(doc, "CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG")

    add_h2(doc, "3.1. Tiến trình phát triển tổng thể")
    add_image(doc, "quy_trinh_du_an_tong_the.png", width_cm=15,
              fig_num="3.1",
              caption="Tiến trình phát triển 4 giai đoạn của đồ án theo PAD Engineering")
    add_para(doc,
        "Đề tài được tổ chức theo 4 giai đoạn liên tiếp, ánh xạ trực tiếp vào vòng đời "
        "Detection Engineering: (i) Reconnaissance & Build — xây dựng server Vulnerable "
        "với endpoint /authenticate không có lớp PAD; (ii) Red Teaming — thực thi 5 kịch "
        "bản TTP, ghi nhận telemetry và đo Attack Success Rate; (iii) Detection Engineering "
        "— huấn luyện Detection Engine MobileNetV2, Threshold Tuning trên ROC; (iv) "
        "Validation — tích hợp PAD vào server Secured, đánh giá APCER/BPCER/FAR/FRR và "
        "kết luận. Mỗi giai đoạn có deliverable riêng và đầu ra của giai đoạn n trở thành "
        "đầu vào của giai đoạn n+1, đảm bảo tính khép kín của chu trình.",
        indent_first=1.0)

    add_h3(doc, "3.1.1. Phân tích chi tiết Hình 3.1 — Bốn giai đoạn của vòng đời")
    add_para(doc,
        "Hình 3.1 là bản đồ tổng thể của toàn bộ đề tài và đáng được phân tích kỹ "
        "vì nó phản ánh trực tiếp tư duy “Detection Engineering” thay vì lối tiếp "
        "cận “build-and-pray” thường thấy. Bốn giai đoạn không phải là các bước "
        "tuần tự rời rạc mà là một vòng tròn khép kín (closed-loop), trong đó "
        "mỗi giai đoạn vừa là consumer vừa là producer của giai đoạn liền kề.",
        indent_first=1.0)

    add_para(doc,
        "Giai đoạn 1 — Reconnaissance & Build (tuần 1-2). Mục tiêu: xây dựng một "
        "“sandbox” server có lỗ hổng cố ý để thực hiện Red Teaming có kiểm soát. "
        "Đây là điều kiện cần — không thể đánh giá hiệu quả của lớp phòng vệ nếu "
        "không có baseline “không phòng vệ” để so sánh. Deliverable: server "
        "Vulnerable cổng 5000 + database 5 user + endpoint /authenticate, /users, "
        "/healthz. Output của giai đoạn này (cấu trúc DB, format payload, mã lỗi "
        "trả về) trở thành input cho giai đoạn 2.",
        indent_first=1.0)

    add_para(doc,
        "Giai đoạn 2 — Red Teaming (tuần 3-4). Mục tiêu: thực thi 5 kịch bản TTP "
        "(Print, Screen Replay, API Replay, Injection, Chained) với 50 attempts/"
        "TTP để có đủ mẫu thống kê. Mỗi attempt được ghi nhận đầy đủ: payload "
        "gửi, response nhận được, latency, success/failure. Đây là giai đoạn "
        "“Threat Intelligence” trong thuật ngữ SOC — biết kẻ tấn công làm gì, "
        "với công cụ gì, và pattern nào lặp lại. Output: bộ telemetry log + "
        "Attack Success Rate cho từng TTP → đầu vào cho thiết kế Detection Logic "
        "ở giai đoạn 3.",
        indent_first=1.0)

    add_para(doc,
        "Giai đoạn 3 — Detection Engineering (tuần 5-6). Mục tiêu: thiết kế và "
        "huấn luyện lớp PAD MobileNetV2 dựa trên insight từ giai đoạn 2. Ba "
        "công việc chính: (i) Data Collection — thu thập 200 ảnh Real + 200 ảnh "
        "Fake mô phỏng đúng các PAI mà attacker dùng ở giai đoạn 2; (ii) Model "
        "Training — Transfer Learning hai pha trên backbone MobileNetV2; "
        "(iii) Threshold Tuning — vẽ ROC, chọn threshold tối ưu (t = 0.7) "
        "đáp ứng APCER < 3% theo ISO 30107-3. Output: Detection Engine sẵn sàng "
        "tích hợp.",
        indent_first=1.0)

    add_para(doc,
        "Giai đoạn 4 — Validation (tuần 7-8). Mục tiêu: tích hợp Detection "
        "Engine vào server Secured (cổng 5001), chạy lại toàn bộ 5 TTP đã làm "
        "ở giai đoạn 2, đo APCER/BPCER/FAR/FRR/Latency. Đặc biệt quan trọng là "
        "“controlled comparison”: cùng tập PAI, cùng tập user, cùng kịch bản — "
        "chỉ khác duy nhất là có/không có PAD. Đây là điều kiện đủ để khẳng "
        "định hiệu quả thực sự của lớp phòng vệ chứ không phải hiệu quả do "
        "thay đổi yếu tố khác. Output: bộ số liệu chứng minh APCER giảm từ "
        "97% xuống 1.5% — feedback ngược lại giai đoạn 1 cho vòng tuning kế "
        "tiếp (Continuous Tuning).",
        indent_first=1.0)

    add_para(doc,
        "Hai mũi tên feedback trong Hình 3.1 đáng chú ý nhất: (a) mũi tên từ "
        "giai đoạn 4 quay về giai đoạn 2 — khi phát hiện một TTP mới (ví dụ "
        "chained Print + Injection có ASR 4% trên Secured), Red Teaming phải "
        "cập nhật danh sách TTP và chạy lại; (b) mũi tên từ giai đoạn 4 về "
        "giai đoạn 3 — khi BPCER vượt ngưỡng người dùng có thể chấp nhận, "
        "model phải được retrain với dataset mở rộng. Hai vòng feedback này "
        "biến PAD Engineering thành quá trình liên tục thay vì dự án một lần.",
        indent_first=1.0)

    add_para(doc,
        "Lý do cách tổ chức 4 giai đoạn này quan trọng đối với một đồ án bảo "
        "mật: nó giúp người đọc và phản biện kiểm tra được tính reproducibility. "
        "Bất cứ ai có cùng môi trường lab và cùng dataset đều có thể chạy lại "
        "từng giai đoạn theo thứ tự và kiểm chứng kết quả. Đây là tiêu chuẩn "
        "khoa học — và cũng là tiêu chuẩn của Detection Engineering trong "
        "production: mọi rule, mọi model, mọi alert đều phải có thể trace ngược "
        "về dữ liệu gốc đã sinh ra nó.",
        indent_first=1.0)

    add_h2(doc, "3.2. Mô hình kiến trúc tổng thể")
    add_image(doc, "fig_3_1_kien_truc_tong_the.png", width_cm=15,
              fig_num="3.2",
              caption="Kiến trúc client-server của hệ thống thí nghiệm")
    add_para(doc,
        "Hệ thống thí nghiệm bao gồm 3 thành phần chính: (i) Client — trình duyệt web "
        "hoặc Python attacker script tạo Image Telemetry; (ii) Network — kênh HTTPS/HTTP "
        "qua REST API JSON; (iii) Server — Flask 3.0 (Python 3.10) với hai phiên bản "
        "song song chạy trên cùng máy nhưng khác cổng (5000 cho Vulnerable, 5001 cho "
        "Secured). Cả hai cùng chia sẻ một database pickle (face_database.pkl) chứa "
        "encoding 128-d và metadata.",
        indent_first=1.0)
    add_para(doc,
        "Quan trọng nhất: hai server CHỈ KHÁC NHAU ở việc có hay không có lớp Detection "
        "Engine. Mọi yếu tố khác (face_recognition library, threshold matching = 0.6, "
        "định dạng response, log format) đều giống hệt. Điều này đảm bảo so sánh APCER/"
        "BPCER giữa hai server là so sánh có kiểm soát (controlled comparison) — biến "
        "duy nhất bị thay đổi là sự hiện diện của PAD Engine.",
        indent_first=1.0)

    add_h2(doc, "3.3. Thiết kế Pipeline xử lý Image Telemetry")
    add_image(doc, "fig_image_telemetry.png", width_cm=15.5,
              fig_num="3.3",
              caption="Pipeline xử lý Image Telemetry trên server Secured")
    add_para(doc,
        "Pipeline Image Telemetry trên server Secured (Hình 3.3) gồm 7 bước:",
        indent_first=1.0)
    add_bullet(doc, "Bước 1 — Capture: Camera client lấy frame 640×480 RGB ở 30 fps qua OpenCV.")
    add_bullet(doc, "Bước 2 — Encode: Frame được encode JPEG quality 85 → base64 → đóng gói "
                    "JSON kèm metadata (username, timestamp, frame_id, device_id).")
    add_bullet(doc, "Bước 3 — Transport: POST /authenticate qua HTTPS với JWT (môi trường lab "
                    "dùng HTTP để dễ phân tích traffic).")
    add_bullet(doc, "Bước 4 — Preprocessing: CLAHE (Contrast Limited Adaptive Histogram "
                    "Equalization) trên kênh L của LAB color space để cân bằng độ tương phản.")
    add_bullet(doc, "Bước 5 — Detection Engine (PAD): MobileNetV2 trả về spoof_score ∈ [0,1]. "
                    "Nếu spoof_score > 0.3 → reject 401 ngay, không cần đi xuống bước Match.")
    add_bullet(doc, "Bước 6 — Face Embedding: face_recognition trích xuất vector 128-d, "
                    "so sánh với template trong DB bằng khoảng cách Euclid.")
    add_bullet(doc, "Bước 7 — Decision & Audit: trả 200 + token nếu Access, 401 + reason "
                    "nếu Reject. Mọi event được log với 7 trường: timestamp, src_ip, "
                    "username, frame_hash, spoof_score, decision, latency_ms.")

    add_h2(doc, "3.4. Phiên bản server Vulnerable")
    add_image(doc, "fig_3_2_server_vulnerable.png", width_cm=14,
              fig_num="3.4",
              caption="Luồng xử lý /authenticate trên server Vulnerable (không có PAD)")

    add_h3(doc, "3.4.1. Mã nguồn cốt lõi của /authenticate")
    add_para(doc,
        "Server Vulnerable (server/app.py) cố tình không có lớp PAD. Endpoint /authenticate "
        "thực hiện đúng quy trình “feature matching cổ điển”: nhận ảnh base64 → decode → "
        "face_recognition.face_encodings → compare với DB → trả về kết quả. Toàn bộ logic "
        "vỏn vẹn ~25 dòng, phản ánh đúng tình trạng nhiều hệ thống thực tế: nhanh, gọn, "
        "thiếu defensive coding.",
        indent_first=1.0)

    add_h3(doc, "3.4.2. Bề mặt tấn công")
    add_table_caption(doc, "3.1", "Bề mặt tấn công của server Vulnerable")
    add_table(doc,
        ["Tầng", "Bề mặt", "TTP áp dụng được", "Ghi chú"],
        [
            ["Cảm biến", "Không có liveness check",       "TTP-01, TTP-02", "PAI vật lý dễ vượt"],
            ["Kênh truyền", "HTTP plain (lab), không nonce", "TTP-03",         "Replay không bị phát hiện"],
            ["API",     "Không device attestation",        "TTP-04",         "Injection trực tiếp"],
            ["DB",      "Pickle không ký số",              "Tampering",      "Đọc/ghi không xác minh"],
            ["/users",  "Liệt kê toàn bộ user",            "Enumeration",    "Lộ danh sách target"],
        ],
        widths=[2.5, 4, 3.5, 5])

    add_h2(doc, "3.5. Phiên bản server Secured")
    add_image(doc, "fig_4_3_server_secured.png", width_cm=14,
              fig_num="3.5",
              caption="Luồng xử lý /authenticate trên server Secured (có Detection Engine)")
    add_para(doc,
        "Server Secured giữ nguyên endpoint /authenticate nhưng chèn thêm bước PAD ngay "
        "sau preprocessing. Nếu spoof_score vượt ngưỡng, server từ chối với mã 401 và lý "
        "do cụ thể (\"liveness_failed\"). Toàn bộ event được ghi vào file log với cấu trúc "
        "JSON, sẵn sàng để forward sang Wazuh/ELK trong môi trường production.",
        indent_first=1.0)

    add_h2(doc, "3.6. So sánh hai phiên bản server")
    add_table_caption(doc, "3.2", "So sánh đặc điểm kỹ thuật của hai phiên bản server")
    add_table(doc,
        ["Đặc điểm", "Vulnerable (port 5000)", "Secured (port 5001)"],
        [
            ["Endpoint /authenticate",    "Có",                          "Có (đã gia cố)"],
            ["PAD / Liveness",            "KHÔNG",                       "MobileNetV2 (Detection Engine)"],
            ["Preprocessing CLAHE",       "Không",                       "Có"],
            ["Threshold matching",        "0.6",                         "0.6 (giữ nguyên)"],
            ["Threshold liveness",        "—",                           "0.7 (qua Tuning)"],
            ["Anti-replay nonce",         "Không",                       "Có (timestamp + HMAC)"],
            ["Audit log JSON",            "Có (rút gọn)",                "Có (đầy đủ 7 trường)"],
            ["Latency trung bình",        "~140 ms",                     "~200 ms (+60 ms)"],
        ],
        widths=[5, 5, 5])

    add_h2(doc, "3.7. Tiền xử lý Image Telemetry — CLAHE")
    add_para(doc,
        "Trong môi trường lab có ánh sáng không đồng đều, ảnh capture từ camera laptop "
        "thường bị over-/under-exposed cục bộ, ảnh hưởng đến cả Detection Engine và Face "
        "Embedding. CLAHE (Contrast Limited Adaptive Histogram Equalization) [27] giải "
        "quyết vấn đề này bằng cách:",
        indent_first=1.0)
    add_bullet(doc, "Chia ảnh thành các tile 8×8 nhỏ, tính histogram cho từng tile.")
    add_bullet(doc, "Áp dụng equalization riêng từng tile, sau đó dùng bilinear interpolation "
                    "để loại bỏ ranh giới giữa các tile.")
    add_bullet(doc, "Giới hạn clip-limit = 2.0 để tránh khuếch đại nhiễu trong vùng đồng nhất.")
    add_para(doc,
        "Trong pipeline, CLAHE chỉ được áp lên kênh L (lightness) của không gian màu LAB "
        "để giữ nguyên thông tin màu sắc. Điều này đặc biệt quan trọng với PAD vì màu sắc "
        "chứa thông tin moiré và texture quan trọng để phân biệt PAI.",
        indent_first=1.0)

    add_h2(doc, "3.8. Mô hình đe dọa (Threat Model)")
    add_image(doc, "fig_threat_model.png", width_cm=15.5,
              fig_num="3.6",
              caption="Threat Model — Bề mặt tấn công ba zone (Client / Network / Server)")
    add_para(doc,
        "Threat Model (Hình 3.6) chia hệ thống thành 3 vùng tin cậy: Client Zone (camera "
        "+ browser), Network Zone (HTTPS / REST), Server Zone (Flask + PAD + DB). Mỗi "
        "zone có các tài sản khác nhau và bị phơi nhiễm với các nhóm tấn công khác nhau:",
        indent_first=1.0)
    add_bullet(doc, "Client Zone — PAI tấn công vật lý: TTP-01 (Print), TTP-02 (Screen).")
    add_bullet(doc, "Network Zone — MITM, replay, sniffing trên kênh chưa TLS hoặc TLS yếu.")
    add_bullet(doc, "Server Zone — TTP-04 (API Injection), DB poisoning, side-channel "
                    "leakage qua /users.")
    add_para(doc,
        "Áp dụng STRIDE cho mỗi zone giúp xác định cụ thể đối tượng cần phòng vệ:",
        indent_first=1.0)
    add_table_caption(doc, "3.3", "Phân tích STRIDE cho từng zone")
    add_table(doc,
        ["Zone", "Spoofing", "Tampering", "Repudiation", "Info Disclosure", "DoS", "Elevation"],
        [
            ["Client",  "★★★", "★",   "★",   "★",   "—",   "★"],
            ["Network", "★",   "★★",  "★★",  "★★",  "★",   "—"],
            ["Server",  "★★",  "★★★", "★",   "★★★", "★★",  "★★"],
        ],
        widths=[2.2, 2, 2, 2, 2.5, 1.5, 2])

    add_h2(doc, "3.9. Phân tích cấu trúc pickle database")
    add_para(doc,
        "Database face_database.pkl là một dict serialized bằng pickle với cấu trúc:",
        indent_first=1.0)
    add_bullet(doc, "Key: username (str)")
    add_bullet(doc, "Value: dict gồm encoding (numpy array 128-d), name (str), email (str), "
                    "registered_at (ISO timestamp).")
    add_para(doc,
        "Hai vấn đề bảo mật cốt lõi của định dạng này:",
        indent_first=1.0)
    add_bullet(doc, "Pickle không có integrity check — kẻ tấn công có quyền ghi file có thể "
                    "thay encoding của bất kỳ user nào, biến hệ thống thành \"backdoor "
                    "biometric\". Trong production, thay bằng SQLite + HMAC, hoặc lưu "
                    "encoding trong HSM.")
    add_bullet(doc, "Pickle deserialization là RCE vector — đọc một file pickle độc hại có "
                    "thể thực thi mã tùy ý. Server Vulnerable đọc pickle ngay khi khởi động "
                    "→ một cuộc tấn công ghi file có thể leo thang lên RCE.")

    add_h2(doc, "3.10. Lỗ hổng tại endpoint /users (Enumeration)")
    add_para(doc,
        "Server Vulnerable expose endpoint /users trả về toàn bộ danh sách user đã đăng ký "
        "dưới dạng JSON. Đây là một lỗ hổng Information Disclosure điển hình theo OWASP "
        "API Security Top 10 (BOLA — Broken Object Level Authorization). Trong góc nhìn "
        "Recon của attacker, /users cung cấp:",
        indent_first=1.0)
    add_bullet(doc, "Danh sách target để chuẩn bị PAI cho từng user cụ thể.")
    add_bullet(doc, "Email + tên đầy đủ → social engineering ngoài hệ thống biometric.")
    add_bullet(doc, "Timestamp đăng ký → suy luận pattern hoạt động (giờ đăng ký, tần suất).")
    add_para(doc,
        "Server Secured loại bỏ endpoint này khỏi production routes và chỉ giữ trong môi "
        "trường admin được bảo vệ bằng MFA. Đây là một thay đổi nhỏ nhưng có giá trị "
        "phòng vệ rất lớn — bịt một bước Recon then chốt trong Attack Chain.",
        indent_first=1.0)

    add_h2(doc, "3.11. Đặc tả API endpoint /authenticate")
    add_para(doc,
        "Endpoint /authenticate là cửa vào duy nhất của hệ thống xác thực. Đặc tả "
        "đầy đủ của endpoint cho phiên bản Secured như sau:",
        indent_first=1.0)
    add_table_caption(doc, "3.4", "Đặc tả request/response cho POST /authenticate (Secured)")
    add_table(doc,
        ["Phần", "Trường", "Kiểu", "Mô tả"],
        [
            ["Request Header",  "Content-Type",   "string",  "application/json"],
            ["Request Header",  "X-Device-Id",    "uuid",    "Định danh thiết bị, ký số"],
            ["Request Header",  "X-Timestamp",    "iso8601", "Thời điểm gửi, ±30s"],
            ["Request Header",  "X-Nonce",        "32hex",   "Anti-replay nonce"],
            ["Request Body",    "username",       "string",  "Tên đăng nhập"],
            ["Request Body",    "image",          "base64",  "Ảnh JPEG, ≤500KB"],
            ["Request Body",    "frame_id",       "string",  "ID frame phục vụ trace"],
            ["Request Body",    "client_signature","hex",    "HMAC-SHA256 của body"],
            ["Response 200",    "token",          "jwt",     "Token có thời hạn 12h"],
            ["Response 200",    "expires_in",     "int",     "Số giây hiệu lực"],
            ["Response 401",    "error",          "string",  "liveness_failed / face_mismatch"],
            ["Response 401",    "spoof_score",    "float",   "Điểm số PAD (debug)"],
            ["Response 429",    "retry_after",    "int",     "Rate limit, đợi N giây"],
        ],
        widths=[3.5, 4, 2.5, 6])
    add_para(doc,
        "Lưu ý: server Vulnerable chỉ yêu cầu ba trường (username, image, frame_id) "
        "và không kiểm tra header. Sự khác biệt này tạo ra một bề mặt tấn công lớn — "
        "client_signature, X-Nonce, X-Timestamp là ba lớp “canary” mà attacker phải "
        "vượt qua đồng thời trên Secured.",
        indent_first=1.0)

    add_h2(doc, "3.12. Schema log audit và mapping với chuẩn ECS")
    add_para(doc,
        "Mỗi sự kiện xác thực được log dưới dạng JSON với schema cố định, tương "
        "thích với Elastic Common Schema (ECS) — chuẩn de facto cho SOC dùng "
        "ELK/Wazuh. Mục đích: log có thể ingest trực tiếp vào SIEM mà không cần "
        "transformation, sẵn sàng cho detection rule và threat hunting.",
        indent_first=1.0)
    add_table_caption(doc, "3.5", "Schema log audit của Detection Engine (mapping với ECS)")
    add_table(doc,
        ["Trường log nội bộ", "Trường ECS tương ứng", "Ví dụ giá trị", "Mục đích"],
        [
            ["timestamp",       "@timestamp",          "2026-06-07T10:23:45.123Z", "Pivoting theo thời gian"],
            ["src_ip",          "source.ip",           "10.0.1.42",                "Block IP nếu bất thường"],
            ["username",        "user.name",           "alice@example.vn",         "Liên kết với HR/AD"],
            ["frame_hash",      "file.hash.sha256",    "a3f5...c1",                "Detect duplicate frame"],
            ["spoof_score",     "biometric.pad_score", "0.84",                     "Trigger alert nếu cao"],
            ["decision",        "event.outcome",       "deny",                     "success/failure"],
            ["latency_ms",      "event.duration",      "212",                      "Profiling hiệu năng"],
            ["device_id",       "device.id",           "uuid-123",                 "Tracking thiết bị"],
            ["geo.country",     "client.geo.country_iso_code", "VN",               "Geo-impossible detection"],
        ],
        widths=[3.5, 4, 4, 4.5])
    add_para(doc,
        "Việc tuân thủ ECS không chỉ là “best practice” mà còn là yêu cầu thực tế: "
        "khi tích hợp với Wazuh hoặc Elastic SIEM, các detection rule có sẵn (như "
        "“Multiple Failed Logins”, “Geo-Impossible Travel”, “Anomalous Behavior”) "
        "có thể áp dụng ngay vào log biometric mà không cần viết lại. Đây là khoản "
        "tiết kiệm công sức đáng kể cho đội Blue Team [38].",
        indent_first=1.0)

    add_h2(doc, "3.13. Sequence diagram chi tiết — phiên xác thực thành công")
    add_para(doc,
        "Để minh họa pipeline 7 bước trong thực tế, mục này mô tả chi tiết một "
        "phiên xác thực thành công của user Alice trên server Secured:",
        indent_first=1.0)
    add_code_block(doc,
        "T+0    ms - Client mo camera, hien thi preview\n"
        "T+ 50  ms - User nhan 'Dang nhap', capture frame 640x480 tu camera\n"
        "T+ 80  ms - Client encode JPEG quality=85, base64, append metadata\n"
        "T+ 95  ms - Client tao HMAC-SHA256(body, secret_key), them X-Nonce\n"
        "T+100  ms - POST /authenticate (HTTPS)\n"
        "T+150  ms - Server nhan request, verify HMAC, X-Nonce, X-Timestamp\n"
        "T+155  ms - Decode base64 -> numpy array RGB\n"
        "T+165  ms - Ap dung CLAHE tren kenh L (LAB), resize 224x224\n"
        "T+170  ms - PAD MobileNetV2 inference -> spoof_score = 0.12\n"
        "T+225  ms - spoof_score <= 0.7 -> tiep tuc\n"
        "T+230  ms - face_recognition tim 1 face (HOG-based)\n"
        "T+275  ms - ResNet-34 sinh embedding 128-d\n"
        "T+350  ms - So sanh voi DB.alice.encoding, distance = 0.42 < 0.6\n"
        "T+355  ms - Sinh JWT token, ky bang HS256, exp=12h\n"
        "T+360  ms - Log JSON event vao file authenticate.log\n"
        "T+365  ms - Tra response 200 + token\n"
        "T+412  ms - Client parse token, luu localStorage, chuyen dashboard")
    add_para(doc,
        "Tổng latency end-to-end: 412 ms. Trong đó server-side tính từ T+150 đến "
        "T+365 ≈ 215 ms, tương đương với chỉ số đo trong Chương 5 (200±12 ms). "
        "Phần còn lại (197 ms) là network round-trip và xử lý client-side.",
        indent_first=1.0)

    add_h2(doc, "3.14. Phân tích sâu STRIDE cho từng zone")

    add_h3(doc, "3.14.1. Client Zone — Spoofing là rủi ro chính")
    add_para(doc,
        "Trong Client Zone, Spoofing chiếm trọng tâm: attacker giơ PAI trước "
        "camera người dùng (TTP-01, TTP-02). Tampering có thể xảy ra nếu "
        "attacker cài malware trên thiết bị để swap camera input. Repudiation "
        "thấp vì đã có device_id ký số. Information Disclosure trung bình — "
        "thiết bị có thể bị lấy được khóa client_secret nếu jailbroken. "
        "DoS không áp dụng (client tự gây DoS lên mình). Elevation of Privilege "
        "thấp — client chỉ có quyền của user đăng nhập.",
        indent_first=1.0)

    add_h3(doc, "3.14.2. Network Zone — Tampering và Info Disclosure")
    add_para(doc,
        "Trong Network Zone, hai rủi ro nổi bật là Tampering (sửa payload "
        "trên đường truyền) và Info Disclosure (sniff ảnh khuôn mặt). Cả hai "
        "đều bị bịt bằng TLS 1.3 — nhưng chỉ khi server bắt buộc TLS chứ "
        "không cho phép HTTP plain. Đề tài thiết lập rule HSTS với max-age=1 "
        "năm để buộc client luôn upgrade lên HTTPS. Repudiation cũng cao — "
        "không có log nào ở tầng network có thể chứng minh ai gửi gì khi đã "
        "qua proxy/CDN, do đó server-side log là source of truth duy nhất.",
        indent_first=1.0)

    add_h3(doc, "3.14.3. Server Zone — Tampering và Info Disclosure cao nhất")
    add_para(doc,
        "Server Zone là khu vực rủi ro cao nhất vì đây là nơi tập trung dữ "
        "liệu sinh trắc của tất cả user. Tampering hệ thống file (sửa pickle "
        "DB), Info Disclosure (lộ encoding qua /users), DoS (botnet flood "
        "/authenticate), và Elevation (lỗ hổng RCE qua pickle deserialize) "
        "đều có khả năng xảy ra cao. Đó là lý do server Secured áp dụng "
        "nguyên tắc Least Privilege: process chạy với uid riêng không có "
        "quyền ghi vào pickle DB, chỉ có một process backup chuyên biệt mới "
        "có quyền cập nhật DB và phải qua MFA admin.",
        indent_first=1.0)

    add_h2(doc, "3.15. Tổng kết chương")
    add_para(doc,
        "Chương 3 đã chuyển hóa lý thuyết của Chương 2 thành kiến trúc cụ thể: hai phiên "
        "bản server song song để so sánh có kiểm soát, Pipeline Image Telemetry 7 bước, "
        "Threat Model phân tầng theo STRIDE, và phân tích chi tiết các bề mặt tấn công "
        "phụ (pickle DB, /users). Toàn bộ thiết kế tuân theo nguyên tắc “Detection over "
        "Prevention” của Detection Engineering: thay vì hứa sẽ chặn 100% tấn công, hệ "
        "thống đảm bảo mọi sự kiện được giám sát, log và có thể truy vết. Chương tiếp "
        "theo sẽ trình bày quy trình triển khai thực tế và các kịch bản Red Teaming.",
        indent_first=1.0, space_after=10)
    add_page_break(doc)

# -*- coding: utf-8 -*-
"""_report_chapters.py — Noi dung 5 chuong cua bao cao."""

from _report_core import (
    add_para, add_h1, add_h2, add_h3, add_bullet, add_image,
    add_table, add_table_caption, add_page_break,
)


# ============================================================
# CHUONG 1
# ============================================================
def build_chapter1(doc):
    add_h1(doc, "CHƯƠNG 1: GIỚI THIỆU")

    add_h2(doc, "1.1. Đặt vấn đề")
    add_para(doc,
        "Trong kiến trúc bảo mật hiện đại, hệ thống xác thực danh tính là tuyến phòng thủ "
        "đầu tiên — “cổng vào” mà mọi tác nhân đe dọa (threat actor) đều buộc phải vượt qua "
        "để xâm nhập. Cùng với xu hướng dịch chuyển từ mật khẩu (something you know) sang "
        "đặc trưng vật lý (something you are), xác thực sinh trắc học khuôn mặt đã trở thành "
        "phương thức xác thực mặc định cho hơn 80% điện thoại thông minh hiện đại và là "
        "yêu cầu bắt buộc đối với mọi giao dịch trực tuyến trên 10 triệu đồng tại Việt Nam "
        "kể từ tháng 7 năm 2024 [39].",
        indent_first=1.0)
    add_para(doc,
        "Tuy nhiên, từ góc nhìn của một SOC Analyst — vốn quen với việc giám sát log, "
        "telemetry và phân tích chuỗi tấn công theo MITRE ATT&CK — phần lớn hệ thống nhận "
        "diện khuôn mặt thế hệ đầu đang tồn tại một “Visibility Gap” (điểm mù giám sát) "
        "nghiêm trọng: hệ thống chỉ thực hiện so khớp đặc trưng (feature matching) mà bỏ "
        "qua bước kiểm tra sống (Liveness Detection / PAD — Presentation Attack Detection). "
        "Hệ quả là pipeline xác thực không thể phân biệt giữa khuôn mặt người thật và một "
        "PAI (Presentation Attack Instrument) như ảnh in giấy A4, ảnh hiển thị trên màn "
        "hình điện thoại, hay dữ liệu ảnh được injection trực tiếp vào tầng API [1][2][9].",
        indent_first=1.0)

    add_h3(doc, "1.1.1. Visibility Gap — Điểm mù giám sát")
    add_image(doc, "fig_visibility_gap.png", width_cm=15,
              fig_num="1.1",
              caption="Visibility Gap — sự khác biệt giữa hệ thống thiếu PAD và hệ thống có Detection Engine")
    add_para(doc,
        "Hình 1.1 minh họa rõ ràng khái niệm Visibility Gap: trên hệ thống Vulnerable, "
        "luồng Image Telemetry đi thẳng từ Camera → Capture → API → Match → Decision mà "
        "không có bất kỳ checkpoint nào kiểm chứng tính “sống” của mẫu trình diện. Trong "
        "ngôn ngữ Detection Engineering, đây là tình trạng “unmonitored attack surface” — "
        "bề mặt tấn công không được giám sát. Mọi sự kiện bypass (TTP-01, TTP-02, TTP-03, "
        "TTP-04) đều đi qua mà không để lại dấu vết để Threat Hunter có thể truy ngược, "
        "không sinh alert tại SIEM, và không kích hoạt bất kỳ phản ứng phòng vệ nào.",
        indent_first=1.0)
    add_para(doc,
        "Trên hệ thống Secured, lớp Detection Engine (PAD MobileNetV2) được chèn vào ngay "
        "sau bước Capture, bịt kín điểm mù bằng cách gắn nhãn liveness_score cho mọi frame "
        "đi qua pipeline. Mỗi quyết định Access/Reject đều được log vào hệ thống audit "
        "(Wazuh / SIEM) kèm theo telemetry đầy đủ: timestamp, device_id, frame_id, "
        "spoof_score, decision_id. Đây là nền tảng để xây dựng các detection rule và "
        "playbook ứng phó sự cố sau này.",
        indent_first=1.0)

    add_h3(doc, "1.1.2. Phân tầng tấn công theo vị trí trong pipeline")
    add_para(doc,
        "Mức độ nguy hiểm của Visibility Gap được phân tầng theo vị trí mà tác nhân "
        "đe dọa lựa chọn để thực hiện tấn công:",
        indent_first=1.0)
    add_bullet(doc, "Tấn công tầng cảm biến (Presentation Attack — TTP-01, TTP-02): tác nhân "
                    "đưa PAI vào trực tiếp trước camera. Chỉ cần ảnh chân dung từ mạng xã hội "
                    "và máy in văn phòng, tỷ lệ vượt qua hệ thống không có PAD lên tới gần 100%.")
    add_bullet(doc, "Tấn công tầng kênh truyền (Replay — TTP-03): tác nhân chặn payload hợp lệ "
                    "đã được capture trước đó và replay lại trên kênh chưa có anti-replay nonce.")
    add_bullet(doc, "Tấn công tầng API (Injection — TTP-04): nguy hiểm nhất — tác nhân không "
                    "cần tiếp xúc vật lý với cảm biến. Một lệnh `curl --data` mang theo ảnh "
                    "khuôn mặt hợp lệ là đủ để bypass HOÀN TOÀN lớp cảm biến và chiếm quyền "
                    "xác thực. Đây là vector có thể tự động hóa quy mô triệu request/giờ.")
    add_image(doc, "fig_2_4_injection_pipeline.png", width_cm=14,
              fig_num="1.2",
              caption="Ba điểm tấn công trong pipeline xác thực sinh trắc học theo ISO/IEC 30107")

    add_h3(doc, "1.1.3. Hậu quả không thể đảo ngược")
    add_para(doc,
        "Khác với mật khẩu có thể đặt lại bất cứ lúc nào, dữ liệu sinh trắc học một khi bị "
        "lộ thì KHÔNG THỂ THAY ĐỔI — hậu quả của một cuộc tấn công thành công là vĩnh viễn. "
        "Trong giai đoạn 2024–2025, cơ quan công an Việt Nam ghi nhận hàng loạt vụ lừa đảo "
        "sử dụng deepfake và ảnh giả mạo để chiếm đoạt tài khoản ngân hàng giá trị lớn [39]. "
        "Đây không còn là mối đe dọa lý thuyết — nó đã hiện hữu trong vai trò một incident "
        "loại P1 (Priority-1) trong các báo cáo của ngân hàng và tổ chức tín dụng.",
        indent_first=1.0)
    add_para(doc,
        "Trước bối cảnh đó, tư duy “xây dựng hệ thống xác thực sinh trắc học” cần được "
        "nâng cấp thành tư duy “triển khai vòng đời PAD Engineering” — chu trình khép kín "
        "từ Threat Modeling, Detection Logic, Validation, Deployment, Continuous Tuning. "
        "Đây là hướng tiếp cận đồ án theo đuổi.",
        indent_first=1.0)

    add_h2(doc, "1.2. Mục tiêu nghiên cứu")
    add_h3(doc, "1.2.1. Mục tiêu nghiên cứu")
    add_bullet(doc, "Hệ thống hóa cơ sở lý thuyết xác thực sinh trắc khuôn mặt, phân loại "
                    "Attack Surface từ tầng cảm biến đến tầng API, ánh xạ vào ngôn ngữ TTPs "
                    "của ma trận MITRE ATT&CK để chuẩn hóa mô tả mối đe dọa [10].")
    add_bullet(doc, "Nghiên cứu sâu tiêu chuẩn ISO/IEC 30107 về Presentation Attack Detection, "
                    "định nghĩa APCER, BPCER và các mức chứng nhận FIDO Biometric Component "
                    "Certification [1][2][31].")
    add_bullet(doc, "Phân tích kiến trúc MobileNetV2 với Inverted Residual và Linear Bottleneck "
                    "như một “Detection Engine” chi phí thấp, có khả năng phân loại Real/Fake "
                    "thời gian thực trên CPU [3].")

    add_h3(doc, "1.2.2. Mục tiêu triển khai")
    add_bullet(doc, "Xây dựng môi trường thí nghiệm gồm hai phiên bản server song song: "
                    "Vulnerable (không có PAD) và Secured (tích hợp Detection Engine).")
    add_bullet(doc, "Thiết kế và triển khai Pipeline xử lý Image Telemetry hoàn chỉnh: "
                    "Capture → CLAHE → PAD Engine → Matching → Decision/Audit.")
    add_bullet(doc, "Tổ chức chiến dịch Red Teaming có kiểm soát với 5 kịch bản tấn công "
                    "thực chứng (TTP-01 đến TTP-05).")
    add_bullet(doc, "Thực hiện Threshold Tuning để tối ưu điểm vận hành trên ROC, cân bằng "
                    "APCER (bảo mật) và BPCER (trải nghiệm người dùng).")
    add_bullet(doc, "Đánh giá định lượng theo ISO/IEC 30107-3: FAR, FRR, APCER, BPCER, "
                    "Accuracy, Latency — đối chiếu trực tiếp Vulnerable vs. Secured.")

    add_h2(doc, "1.3. Phạm vi và giới hạn đề tài")
    add_para(doc,
        "Để bảo đảm tính khả thi và tính khoa học, đề tài giới hạn phạm vi như sau:",
        indent_first=1.0)
    add_bullet(doc, "Trong phạm vi lab: Toàn bộ hoạt động Red Teaming chỉ thực hiện trên "
                    "hệ thống do sinh viên tự xây dựng, không nhằm vào bất kỳ hệ thống "
                    "thương mại hay cá nhân nào khác.")
    add_bullet(doc, "Đối tượng sinh trắc: tập trung khuôn mặt 2D từ camera RGB. "
                    "Không khảo sát IR, 3D depth, vân tay, mống mắt.")
    add_bullet(doc, "Kịch bản tấn công: ảnh in, ảnh hiển thị trên điện thoại, ảnh chụp "
                    "lại từ màn hình máy tính, injection ảnh tĩnh qua API. Deepfake video "
                    "thời gian thực không được thực nghiệm nhưng được phân tích lý thuyết "
                    "và đề xuất hướng phát triển.")
    add_bullet(doc, "Hạ tầng: chạy trên CPU Intel Core i5/i7 laptop (không có GPU rời) — "
                    "điều kiện thực tế của đại đa số tổ chức vừa và nhỏ tại Việt Nam.")

    add_h2(doc, "1.4. Phương pháp nghiên cứu")
    add_para(doc,
        "Đồ án kết hợp nhiều phương pháp nghiên cứu mang đặc trưng của một "
        "Detection Engineer:",
        indent_first=1.0)
    add_bullet(doc, "Nghiên cứu lý thuyết: tổng hợp tiêu chuẩn ISO/IEC 30107 [1][2], "
                    "công bố khoa học về PAD [6][7][8][9], OWASP Biometric Risks [11] "
                    "và NIST SP 800-63B [13].")
    add_bullet(doc, "Mô hình hóa đe dọa (Threat Modeling) theo STRIDE: xác định Attack "
                    "Surface, Attack Vector và mục tiêu của attacker tại từng tầng pipeline.")
    add_bullet(doc, "Red Teaming có kiểm soát: thiết kế và thực thi các kịch bản tấn công "
                    "trên server Vulnerable để đo lường mức độ nguy hiểm thực tế.")
    add_bullet(doc, "PAD Engineering lifecycle: huấn luyện Detection Engine theo vòng đời "
                    "Threat Intel → Data Collection → Model Training → Validation → "
                    "Deployment → Continuous Tuning.")
    add_bullet(doc, "So sánh định lượng: đối chiếu FAR/FRR/APCER/BPCER giữa server "
                    "Vulnerable và Secured trên cùng bộ kiểm thử theo chuẩn ISO/IEC 30107-3 [2].")

    add_h2(doc, "1.5. Đóng góp của đề tài")
    add_bullet(doc, "Mô hình đe dọa có thể tái sử dụng: Threat Model phân tầng cụ thể cho "
                    "hệ thống xác thực sinh trắc học client-server, phân tách rõ "
                    "Presentation Attack vs. Injection Attack.")
    add_bullet(doc, "Bộ tài liệu mở: mã nguồn server Vulnerable/Secured, script huấn luyện "
                    "MobileNetV2, bộ ảnh mẫu Real/Fake — phục vụ đào tạo và kiểm thử bảo mật.")
    add_bullet(doc, "Bằng chứng định lượng về hiệu quả PAD: APCER ≈ 1,5%, FAR ≈ 2%, latency "
                    "tăng thêm chỉ ~60 ms — chứng minh tính khả thi của Detection Engine "
                    "chi phí thấp cho môi trường không có GPU.")
    add_bullet(doc, "Kiến trúc Defense in Depth: lộ trình 6 lớp phòng vệ từ TLS/Device "
                    "Attestation đến MFA và Logging, phù hợp ngân sách triển khai của "
                    "doanh nghiệp vừa và nhỏ.")

    add_h2(doc, "1.6. Cấu trúc báo cáo")
    add_para(doc, "Báo cáo được tổ chức thành 5 chương:", indent_first=1.0)
    add_bullet(doc, "Chương 1 — Giới thiệu: đặt vấn đề theo hướng SOC, xác định Visibility "
                    "Gap, mục tiêu, phạm vi và phương pháp nghiên cứu.")
    add_bullet(doc, "Chương 2 — Cơ sở lý thuyết: hệ thống hóa từ quy trình xác thực sinh "
                    "trắc đến tiêu chuẩn ISO/IEC 30107. Phân tích sâu MobileNetV2 và các "
                    "biến thể AttackNet như Detection Engine.")
    add_bullet(doc, "Chương 3 — Phân tích và thiết kế hệ thống: Pipeline Image Telemetry, "
                    "Threat Model chi tiết, ánh xạ kỹ thuật tấn công.")
    add_bullet(doc, "Chương 4 — Triển khai và phòng vệ: huấn luyện Detection Engine với "
                    "Transfer Learning, Threshold Tuning APCER/BPCER, tích hợp PAD vào "
                    "server Secured.")
    add_bullet(doc, "Chương 5 — Thực nghiệm và đánh giá: kết quả Red Teaming, so sánh FAR/"
                    "FRR/APCER giữa Vulnerable và Secured, kết luận tính khả thi mô hình "
                    "phòng vệ đa tầng.")

    add_h2(doc, "1.7. Bối cảnh kinh tế và pháp lý")
    add_h3(doc, "1.7.1. Quy mô thiệt hại của tấn công sinh trắc tại Việt Nam")
    add_para(doc,
        "Theo báo cáo An toàn Thông tin Quốc gia 2024 do Cục An ninh mạng và Phòng "
        "chống tội phạm sử dụng công nghệ cao (A05) công bố, tổng thiệt hại tài chính "
        "do các vụ lừa đảo công nghệ cao trên không gian mạng Việt Nam ước tính 18.900 "
        "tỷ đồng trong năm 2024 — tăng 47% so với năm 2023. Trong đó, các vụ lừa đảo "
        "có yếu tố deepfake và giả mạo khuôn mặt qua hệ thống định danh điện tử (eKYC) "
        "chiếm tỷ trọng đáng kể: 1.380 vụ với tổng thiệt hại ước tính trên 2.100 tỷ "
        "đồng [40]. Mỗi vụ trung bình gây thiệt hại 1,5 tỷ đồng cho cá nhân hoặc doanh "
        "nghiệp bị tấn công.",
        indent_first=1.0)
    add_para(doc,
        "Đặc trưng chung của các vụ tấn công này là: (i) attacker thu thập video / "
        "ảnh nạn nhân từ mạng xã hội hoặc qua các cuộc gọi giả mạo công an, ngân hàng; "
        "(ii) sử dụng công cụ deepfake hoặc đơn giản chỉ là ảnh tĩnh để vượt qua bước "
        "“xác thực sinh trắc” trong ứng dụng eKYC; (iii) chiếm đoạt tài khoản ngân hàng "
        "và thực hiện chuyển khoản trước khi nạn nhân kịp phát hiện. Toàn bộ chuỗi "
        "tấn công có thể hoàn thành trong vài phút, trong khi thời gian phản ứng trung "
        "bình của ngân hàng để chặn giao dịch lên tới 4-6 giờ.",
        indent_first=1.0)

    add_h3(doc, "1.7.2. Khung pháp lý và yêu cầu tuân thủ")
    add_para(doc,
        "Hệ thống xác thực sinh trắc tại Việt Nam hiện chịu sự điều chỉnh đồng thời "
        "của ba khung pháp lý chính:",
        indent_first=1.0)
    add_bullet(doc, "Quyết định 2345/QĐ-NHNN (2024) [39] — bắt buộc xác thực sinh "
                    "trắc cho mọi giao dịch chuyển khoản trên 10 triệu đồng và mọi "
                    "giao dịch kích hoạt trên thiết bị mới. Đây là hành lang pháp lý "
                    "đầu tiên áp đặt yêu cầu sinh trắc bắt buộc cho ngành tài chính.")
    add_bullet(doc, "Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân — phân loại "
                    "dữ liệu sinh trắc thuộc nhóm “dữ liệu cá nhân nhạy cảm”, yêu "
                    "cầu cơ chế bảo vệ chuyên biệt, quyền truy cập tối thiểu và "
                    "thông báo vi phạm trong vòng 72 giờ.")
    add_bullet(doc, "Luật An ninh mạng 2018 và các Thông tư hướng dẫn — yêu cầu hệ "
                    "thống quan trọng phải có giải pháp giám sát, ghi nhật ký và "
                    "khả năng cung cấp dữ liệu cho cơ quan chức năng khi điều tra.")
    add_para(doc,
        "Sự xuất hiện đồng thời của ba khung pháp lý đặt ra một bài toán kép cho các "
        "tổ chức triển khai biometric: vừa phải bảo vệ dữ liệu sinh trắc khỏi tấn "
        "công, vừa phải đảm bảo log đầy đủ để truy vết. Detection Engineering với "
        "chu trình giám sát + log telemetry là cách tiếp cận trực tiếp đáp ứng cả "
        "hai yêu cầu này.",
        indent_first=1.0)

    add_h2(doc, "1.8. Stakeholder và phân tích các bên liên quan")
    add_para(doc,
        "Một hệ thống xác thực sinh trắc trong môi trường thực tế không chỉ ảnh "
        "hưởng tới hai bên (người dùng và hệ thống) như mô hình lý thuyết, mà liên "
        "quan tới ít nhất 5 nhóm stakeholder với lợi ích và mức độ rủi ro khác nhau:",
        indent_first=1.0)
    add_table_caption(doc, "1.1", "Phân tích các bên liên quan của hệ thống biometric")
    add_table(doc,
        ["Stakeholder", "Lợi ích chính", "Rủi ro chịu nhận", "Yêu cầu kỹ thuật ưu tiên"],
        [
            ["Người dùng cuối", "Trải nghiệm nhanh, tiện", "Mất tiền nếu bị mạo danh",
             "BPCER thấp + MFA fallback"],
            ["Tổ chức triển khai", "Giảm gian lận, đáp ứng quy định",
             "Phạt vi phạm, mất uy tín",
             "APCER thấp + log đầy đủ"],
            ["SOC / Blue Team", "Phát hiện và ứng phó sự cố",
             "Bị quá tải bởi false alert",
             "Detection Engine có alert chất lượng cao"],
            ["Cơ quan quản lý", "Kiểm tra tuân thủ, điều tra",
             "Khó truy vết khi có sự cố",
             "Audit log đủ 7 trường, lưu 12 tháng"],
            ["Attacker", "Kiếm lợi từ tấn công",
             "Bị truy tố nếu lộ danh tính",
             "—"],
        ],
        widths=[3.5, 4, 4, 4.5])
    add_para(doc,
        "Bảng 1.1 cho thấy một thực tế quan trọng: trong khi người dùng cuối chỉ cần "
        "BPCER thấp (đừng từ chối nhầm tôi), thì tổ chức triển khai và cơ quan quản "
        "lý lại ưu tiên APCER thấp (đừng cho phép kẻ giả mạo). Đây là xung đột mục "
        "tiêu (objective conflict) cố hữu của bài toán PAD và là lý do Threshold "
        "Tuning trở thành quyết định kinh doanh chứ không chỉ là quyết định kỹ thuật. "
        "Đề tài tiếp cận xung đột này bằng cách xác định một “điểm vận hành” cân bằng "
        "(t = 0.7) đồng thời cung cấp khả năng cấu hình động cho từng phân khúc giao "
        "dịch (giao dịch nhỏ → ngưỡng lỏng, giao dịch lớn → ngưỡng chặt).",
        indent_first=1.0)

    add_h2(doc, "1.9. Lịch sử nghiên cứu và state-of-the-art")
    add_para(doc,
        "Lĩnh vc Phát hiện tấn công trình diện (PAD) đã trải qua bốn thế hệ kỹ thuật "
        "chính trong khoảng 25 năm qua. Việc nắm rõ tiến trình này giúp định vị "
        "chính xác đóng góp của đề tài:",
        indent_first=1.0)
    add_bullet(doc, "Thế hệ 1 (2000–2010) — Texture-based: dựa vào LBP (Local Binary "
                    "Pattern), HOG, GLCM. Anjos & Marcel (2011) [21] công bố bộ "
                    "Replay-Attack với accuracy ~85%. Hạn chế: sensitive với ánh sáng.")
    add_bullet(doc, "Thế hệ 2 (2010–2016) — Motion-based: yêu cầu user nháy mắt, "
                    "quay đầu (challenge-response). Hạn chế: trải nghiệm kém, dễ "
                    "bypass bằng video replay.")
    add_bullet(doc, "Thế hệ 3 (2016–2020) — Deep CNN: AlexNet, ResNet, MobileNet "
                    "[3][13] cho accuracy >95%. Boulkenafet et al. (2017) [6], Liu "
                    "et al. (2018) [9] tạo state-of-the-art trên CASIA-FASD và "
                    "OULU-NPU. Đây là thế hệ Detection Engine của đề tài.")
    add_bullet(doc, "Thế hệ 4 (2020–nay) — Multi-modal & Adversarial-robust: kết "
                    "hợp RGB + depth + IR + rPPG (remote photoplethysmography). "
                    "Stehouwer et al. (2020) [33], Tolosana et al. (2020) [36] "
                    "đề xuất các kiến trúc chống deepfake. Yêu cầu phần cứng cao "
                    "hơn nhưng accuracy gần 99%.")
    add_para(doc,
        "Đồ án định vị tại thế hệ 3 — sử dụng MobileNetV2 đơn modal RGB — vì lý do "
        "thực tế: phần lớn doanh nghiệp vừa và nhỏ tại Việt Nam không có hạ tầng GPU "
        "và không có camera depth/IR. Hệ thống ở thế hệ 4 là mục tiêu dài hạn (phần "
        "5.8) chứ không phải giải pháp khả thi ngay lập tức. Đóng góp của đề tài là "
        "đưa ra một blueprint hoàn chỉnh — từ Threat Model, Pipeline đến Defense in "
        "Depth — trên nền công nghệ Generation 3 phổ biến và rẻ.",
        indent_first=1.0)

    add_h2(doc, "1.10. Dự kiến kết quả định lượng")
    add_table_caption(doc, "1.2", "Mục tiêu KPI cho server Secured")
    add_table(doc,
        ["Chỉ số", "Mục tiêu", "Cơ sở tham chiếu"],
        [
            ["FAR (False Acceptance Rate)", "< 5%", "FIDO Level A: APCER < 5% [31]"],
            ["FRR (False Rejection Rate)",  "< 8%", "Cân bằng trải nghiệm người dùng"],
            ["APCER",                        "< 3%", "ISO/IEC 30107-3 [2]"],
            ["BPCER",                        "< 6%", "ISO/IEC 30107-3 [2]"],
            ["Latency tăng thêm",            "< 100 ms", "Ngưỡng cảm nhận người dùng"],
        ],
        widths=[5, 3, 8])
    add_para(doc,
        "Chương 5 sẽ trình bày kết quả đo đạc thực tế và đối chiếu trực tiếp với các mục "
        "tiêu này. Mọi sai lệch giữa mục tiêu và kết quả thực tế đều được phân tích nguyên "
        "nhân để rút kinh nghiệm cho các vòng tuning tiếp theo.",
        indent_first=1.0, space_after=10)

    add_page_break(doc)

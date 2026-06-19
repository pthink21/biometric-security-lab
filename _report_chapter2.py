# -*- coding: utf-8 -*-
"""_report_chapter2.py — Chuong 2: Co so ly thuyet."""

from _report_core import (
    add_para, add_h1, add_h2, add_h3, add_bullet, add_image,
    add_table, add_table_caption, add_page_break,
)


def build_chapter2(doc):
    add_h1(doc, "CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ NỀN TẢNG")

    add_h2(doc, "2.1. Tổng quan về xác thực sinh trắc học")
    add_para(doc,
        "Xác thực sinh trắc học (biometric authentication) là phương thức định danh dựa trên "
        "các đặc trưng vật lý hoặc hành vi của chủ thể. Khác với mật khẩu (something you know) "
        "hay token (something you have), sinh trắc học thuộc nhóm yếu tố “something you are” — "
        "đặc trưng không thể quên và rất khó sao chép trong điều kiện kiểm soát tốt [1][13]. "
        "Trong ngôn ngữ Detection Engineering, mỗi mẫu sinh trắc khi đi vào hệ thống được xem "
        "như một “telemetry record” mang ngữ cảnh nhận dạng (subject_id, timestamp, sensor_id) "
        "và buộc phải đi qua chuỗi kiểm chứng trước khi được chuyển hóa thành quyết định "
        "Access/Reject.",
        indent_first=1.0)

    add_h3(doc, "2.1.1. Phân loại sinh trắc học")
    add_bullet(doc, "Sinh trắc vật lý: khuôn mặt, vân tay, mống mắt, hình dạng bàn tay, ADN.")
    add_bullet(doc, "Sinh trắc hành vi: chữ ký, dáng đi, cách gõ phím, giọng nói.")
    add_para(doc,
        "Đề tài tập trung vào sinh trắc khuôn mặt 2D từ camera RGB do (i) đây là phương thức "
        "phổ biến nhất hiện nay, (ii) chi phí triển khai thấp nhất, và (iii) cũng là bề mặt "
        "tấn công có nhiều TTPs nhất theo OWASP Biometric Risks [11].",
        indent_first=1.0)

    add_h3(doc, "2.1.2. Quy trình xác thực sinh trắc học")
    add_image(doc, "fig_2_1_quy_trinh_bio.png", width_cm=14,
              fig_num="2.1",
              caption="Quy trình 6 bước của một hệ thống xác thực sinh trắc khuôn mặt")
    add_para(doc,
        "Hình 2.1 mô tả 6 bước chuẩn của quy trình xác thực: (1) Capture — thu nhận ảnh từ "
        "cảm biến; (2) Preprocessing — chuẩn hóa ánh sáng/kích thước/ROI; (3) Feature "
        "Extraction — trích xuất vector đặc trưng (ví dụ embedding 128-d của face_recognition); "
        "(4) Matching — so khớp với template lưu trong database; (5) Decision — ra quyết định "
        "Access/Reject dựa trên ngưỡng; (6) Audit — log sự kiện vào hệ thống giám sát. "
        "Trong các hệ thống thiếu PAD, bước (1) và (2) chính là điểm yếu cấu trúc — không có "
        "checkpoint nào đảm bảo dữ liệu đến từ một nguồn “sống” thực sự [1][2].",
        indent_first=1.0)

    add_h3(doc, "2.1.3. So sánh các loại sinh trắc học")
    add_table_caption(doc, "2.1", "So sánh đặc điểm các loại sinh trắc học phổ biến")
    add_table(doc,
        ["Loại", "Độ chính xác", "Chi phí thiết bị", "Khả năng bị giả mạo", "Mức phổ cập"],
        [
            ["Khuôn mặt 2D (RGB)", "Cao (~99%)", "Rất thấp",   "Trung bình–Cao",   "Rất phổ biến"],
            ["Khuôn mặt 3D (depth)","Rất cao",   "Cao",         "Thấp",              "Trung bình"],
            ["Vân tay",            "Rất cao",   "Thấp",        "Trung bình",        "Phổ biến"],
            ["Mống mắt",           "Cực cao",   "Cao",         "Rất thấp",          "Thấp"],
            ["Giọng nói",          "Trung bình","Rất thấp",    "Cao (deepfake)",    "Phổ biến"],
        ],
        widths=[3.5, 3, 3, 3, 3])

    add_h2(doc, "2.2. Nhận diện khuôn mặt với face_recognition và dlib")
    add_para(doc,
        "Hệ thống thí nghiệm sử dụng thư viện face_recognition (Python) — một wrapper trên "
        "thư viện C++ dlib [4][5]. Pipeline rút gọn của face_recognition bao gồm: HOG-based "
        "face detector → 5-point shape predictor → ResNet-34 metric learning network sinh "
        "embedding 128 chiều. Khoảng cách Euclid giữa hai embedding < 0.6 được coi là cùng "
        "một danh tính. Đây là lựa chọn cân bằng giữa độ chính xác (LFW accuracy ~99,38%) và "
        "tốc độ (~80 ms/frame trên CPU laptop).",
        indent_first=1.0)
    add_para(doc,
        "Điểm cần lưu ý từ góc nhìn Detection Engineering: bản thân face_recognition "
        "KHÔNG có liveness — nó chỉ trả lời câu hỏi “khuôn mặt này có giống template hay "
        "không?”, không trả lời “khuôn mặt này có sống không?”. Điều này tạo ra một câu "
        "trả lời sai-chân-thực mà các kẻ tấn công khai thác triệt để: gửi một ảnh in của "
        "nạn nhân vẫn cho ra distance < 0.6 — hệ thống vẫn cấp Access [6][9].",
        indent_first=1.0)

    add_h2(doc, "2.3. Phân loại và phân tích các kỹ thuật tấn công (TTPs)")
    add_image(doc, "fig_2_2_phan_loai_tan_cong.png", width_cm=14,
              fig_num="2.2",
              caption="Phân loại các hình thức tấn công trình diện theo ISO/IEC 30107")

    add_h3(doc, "2.3.1. TTP-01 — Print Attack (Sensor Spoofing)")
    add_para(doc,
        "Tác nhân in ảnh chân dung của nạn nhân lên giấy A4 hoặc bìa cứng và giơ trước "
        "camera. PAI: ảnh in. Chi phí: ~2.000 VND/lần in. Tỷ lệ thành công trên hệ thống "
        "không có PAD: ~95-100% [6]. Đây là TTP đơn giản nhất nhưng có hiệu quả cao nhất "
        "đối với hệ thống không Liveness — cũng chính là lý do nó được ưu tiên đưa vào "
        "Red Teaming bài đầu tiên.",
        indent_first=1.0)

    add_h3(doc, "2.3.2. TTP-02 — Screen Replay (PAI điện thoại / màn hình)")
    add_para(doc,
        "Tác nhân hiển thị ảnh chân dung của nạn nhân lên màn hình điện thoại hoặc tablet "
        "và giơ trước camera. PAI: thiết bị hiển thị. Khác biệt với Print Attack: ảnh có "
        "ánh sáng phát xạ (emissive light) thay vì phản xạ (reflective light), độ sắc nét "
        "cao hơn, và có thể tạo hiệu ứng chuyển động giả. Một số hệ thống phát hiện moiré "
        "pattern để chống TTP này, nhưng tỷ lệ phát hiện thay đổi mạnh theo độ phân giải "
        "camera [7].",
        indent_first=1.0)

    add_h3(doc, "2.3.3. TTP-03 — Replay Attack (Signal Replay over API)")
    add_para(doc,
        "Tác nhân chặn payload xác thực hợp lệ trên kênh truyền (qua MITM hoặc reverse "
        "engineering ứng dụng client) rồi replay lại sau đó. Khi server không có anti-replay "
        "nonce hoặc timestamp signing, một payload duy nhất có thể tái sử dụng nhiều lần. "
        "Đây là TTP nguy hiểm vì nó bypass được cả lớp PAD nếu PAD chỉ chạy ở client [9][29].",
        indent_first=1.0)

    add_h3(doc, "2.3.4. TTP-04 — Injection Attack (API Injection)")
    add_para(doc,
        "Tác nhân không tiếp xúc cảm biến — gửi trực tiếp ảnh khuôn mặt vào endpoint "
        "/authenticate dưới dạng multipart hoặc base64 JSON. Khi server không thực hiện "
        "device attestation hay ký số ảnh tại client, không có gì phân biệt được giữa ảnh "
        "“thật” từ camera người dùng và ảnh “in” từ thư viện attacker. Đây là TTP nguy hiểm "
        "nhất vì có thể tự động hóa quy mô lớn (botnet, automated framework) [9][11].",
        indent_first=1.0)

    add_h3(doc, "2.3.5. TTP-05 — Synthetic Media (Deepfake Generation)")
    add_para(doc,
        "Tác nhân dùng GAN (FaceSwap, DeepFaceLab, generative models) để tổng hợp video "
        "khuôn mặt nạn nhân với biểu cảm thật, sau đó stream vào hệ thống thông qua virtual "
        "camera (OBS Virtual Cam, ManyCam). TTP này yêu cầu kỹ năng cao hơn nhưng có khả "
        "năng vượt qua các Liveness Detection thế hệ đầu vốn dựa vào blink/head-movement "
        "[16][17][18]. Đề tài chỉ phân tích lý thuyết, không thực nghiệm.",
        indent_first=1.0)

    add_h3(doc, "2.3.6. Ánh xạ TTPs vào ma trận MITRE ATT&CK")
    add_image(doc, "fig_mitre_mapping.png", width_cm=15,
              fig_num="2.3",
              caption="Ánh xạ TTPs tấn công sinh trắc học vào ma trận MITRE ATT&CK")
    add_para(doc,
        "Hình 2.3 cho thấy chuỗi tấn công sinh trắc học có thể được mô tả hoàn toàn bằng "
        "ngôn ngữ MITRE ATT&CK, từ Reconnaissance (T1589.001 — thu thập ảnh nạn nhân từ "
        "social media) cho đến Impact (T1531 — Account Access Removal). Việc ánh xạ này có "
        "ý nghĩa thực tế: cho phép SOC tích hợp các sự kiện từ hệ thống biometric vào cùng "
        "một detection framework với các log Windows/Linux/Network, sinh ra cảnh báo nhất "
        "quán và playbook ứng phó dùng chung [10].",
        indent_first=1.0)

    add_table_caption(doc, "2.2", "Bảng ánh xạ TTPs tấn công sinh trắc vào MITRE ATT&CK")
    add_table(doc,
        ["TTP nội bộ", "Mô tả", "MITRE Tactic", "MITRE Technique"],
        [
            ["TTP-01", "Print Attack",      "Initial Access", "T1078 — Valid Accounts (sub: physical PAI)"],
            ["TTP-02", "Screen Replay",     "Initial Access", "T1078 — Valid Accounts (sub: replay PAI)"],
            ["TTP-03", "Replay over API",   "Credential Access", "T1212 — Exploitation for Credential Access"],
            ["TTP-04", "API Injection",     "Credential Access", "T1556 — Modify Authentication Process"],
            ["TTP-05", "Deepfake Stream",   "Defense Evasion",   "T1036.005 — Masquerading: Match Legitimate Name"],
        ],
        widths=[2.2, 3.5, 3.5, 6])

    add_image(doc, "fig_attack_chain.png", width_cm=15.5,
              fig_num="2.4",
              caption="Attack Chain — chuỗi tấn công sinh trắc khuôn mặt theo Cyber Kill Chain")
    add_para(doc,
        "Hình 2.4 trình bày chuỗi tấn công đầy đủ theo mô hình Cyber Kill Chain biến thể: "
        "Recon → Weaponize → Delivery → Exploit → Install → C2 → Action. Lớp PAD Engine "
        "đặt ngay ở giai đoạn Exploit — phá vỡ chuỗi tại điểm sớm nhất khả dĩ. Nếu thiếu "
        "PAD, chuỗi đi thẳng đến Action với thiệt hại không thể đảo ngược như chiếm đoạt "
        "tài khoản, chuyển khoản trái phép, lộ thông tin nhạy cảm.",
        indent_first=1.0)

    add_h2(doc, "2.4. PAD Engineering và tiêu chuẩn ISO/IEC 30107")
    add_image(doc, "fig_pad_lifecycle.png", width_cm=13,
              fig_num="2.5",
              caption="Vòng đời PAD Engineering — Detection Engineering Lifecycle")
    add_para(doc,
        "ISO/IEC 30107 là bộ tiêu chuẩn quốc tế về Phát hiện tấn công trình diện, gồm 3 phần: "
        "Phần 1 — khung lý thuyết và thuật ngữ; Phần 2 — định dạng dữ liệu trao đổi; "
        "Phần 3 — phương pháp và chỉ số đánh giá. Trong đó, Phần 3 định nghĩa hai chỉ số "
        "trụ cột mà mọi PAD Engine phải báo cáo [1][2]:",
        indent_first=1.0)
    add_bullet(doc, "APCER (Attack Presentation Classification Error Rate) — tỷ lệ tấn công "
                    "bị phân loại nhầm thành mẫu thật. Càng thấp càng an toàn.")
    add_bullet(doc, "BPCER (Bona-fide Presentation Classification Error Rate) — tỷ lệ mẫu "
                    "thật bị từ chối. Càng thấp càng tốt cho trải nghiệm người dùng.")
    add_para(doc,
        "Tương đồng với Detection Engineering trong SOC, PAD Engineering là một vòng đời "
        "khép kín gồm 6 pha (Hình 2.5): (1) Threat Intelligence & Hunt Hypothesis, "
        "(2) Data Collection — Image Telemetry, (3) Detection Logic — Model Training, "
        "(4) Validation — Threshold Tuning, (5) Deployment — tích hợp vào server Secured, "
        "(6) Continuous Tuning — Red Teaming và retrain định kỳ. Mỗi pha tạo input cho pha "
        "tiếp theo và feedback ngược về pha đầu khi xuất hiện TTP mới [10][11].",
        indent_first=1.0)

    add_h2(doc, "2.5. Detection Engine — MobileNetV2 và Transfer Learning")
    add_image(doc, "fig_attacknet_detail.png", width_cm=15.5,
              fig_num="2.6",
              caption="Kiến trúc AttackNet (MobileNetV2 + classifier head Real/Fake)")
    add_para(doc,
        "MobileNetV2 [3] là kiến trúc CNN chuyên biệt cho thiết bị tài nguyên hạn chế. "
        "Hai cải tiến cốt lõi:",
        indent_first=1.0)
    add_bullet(doc, "Inverted Residual Block: thay vì nén kênh ở giữa khối (như ResNet), "
                    "MobileNetV2 expand kênh đầu vào lên 6 lần (t=6), thực hiện depthwise "
                    "conv 3×3 trên không gian rộng, rồi project về kích thước nhỏ. Skip "
                    "connection chỉ áp dụng khi stride=1.")
    add_bullet(doc, "Linear Bottleneck: lớp project cuối khối KHÔNG dùng ReLU vì ReLU phá "
                    "hủy thông tin trên không gian thấp chiều. Đây là điểm khác biệt then "
                    "chốt với MobileNetV1 [3].")
    add_para(doc,
        "Khi áp dụng vào bài toán Real/Fake (PAD), backbone MobileNetV2 đóng vai trò "
        "extractor; classifier head được thay thế bằng GlobalAvgPool → Dropout(0.3) → "
        "Linear(1280, 1) → Sigmoid. Toàn bộ network — gọi là “AttackNet” trong báo cáo — "
        "có 3,4 triệu tham số, 300 MFLOPs, đạt 28-32 FPS trên Intel i7 không GPU. Đây là "
        "Detection Engine chi phí thấp đáp ứng được yêu cầu real-time [3][6][8].",
        indent_first=1.0)

    add_para(doc,
        "Transfer Learning hai pha được áp dụng để tận dụng tri thức ImageNet và tránh "
        "overfit trên dataset nhỏ:",
        indent_first=1.0)
    add_bullet(doc, "Pha 1 — Frozen backbone: khóa toàn bộ Inverted Residual blocks, chỉ "
                    "huấn luyện classifier head với LR=1e-3 trong 8 epoch.")
    add_bullet(doc, "Pha 2 — Fine-tune cuối: mở khóa 30 layer cuối, giảm LR xuống 1e-5 "
                    "trong 17 epoch tiếp theo. Tổng 25 epoch.")

    add_h2(doc, "2.6. Các chỉ số đánh giá PAD theo ISO/IEC 30107-3")
    add_para(doc,
        "Đề tài sử dụng 6 chỉ số chuẩn để đánh giá Detection Engine và toàn hệ thống:",
        indent_first=1.0)
    add_table_caption(doc, "2.3", "Định nghĩa các chỉ số PAD theo ISO/IEC 30107-3")
    add_table(doc,
        ["Chỉ số", "Định nghĩa", "Áp dụng"],
        [
            ["APCER", "Tỷ lệ PAI bị phân loại nhầm thành bona-fide",  "Đánh giá Detection Engine"],
            ["BPCER", "Tỷ lệ bona-fide bị phân loại nhầm thành PAI",   "Đánh giá Detection Engine"],
            ["FAR",   "Tỷ lệ chấp nhận sai cuối cùng (toàn pipeline)", "Đánh giá hệ thống tổng thể"],
            ["FRR",   "Tỷ lệ từ chối sai cuối cùng (toàn pipeline)",   "Đánh giá hệ thống tổng thể"],
            ["EER",   "Điểm mà FAR = FRR",                             "Đánh giá tổng quát"],
            ["Latency", "Thời gian xử lý 1 frame end-to-end (ms)",     "Khả thi triển khai"],
        ],
        widths=[2.5, 8, 5])

    add_image(doc, "fig_roc_threshold.png", width_cm=14,
              fig_num="2.7",
              caption="ROC Curve & Threshold Tuning — APCER vs BPCER trade-off")
    add_para(doc,
        "Hình 2.7 minh họa nguyên lý Threshold Tuning: trên đường cong ROC, mỗi điểm là "
        "một threshold cụ thể. Việc dịch điểm vận hành sang trái giảm APCER (an ninh tốt "
        "hơn) nhưng tăng BPCER (người dùng thật bị từ chối nhiều hơn). Threshold = 0.7 "
        "được chọn cho server Secured như một thỏa hiệp tốt nhất giữa hai yếu tố này.",
        indent_first=1.0)

    add_h2(doc, "2.7. OWASP Biometric Risks và NIST SP 800-63B")
    add_para(doc,
        "OWASP Biometric Risks [11] liệt kê 10 rủi ro hàng đầu cho hệ thống biometric: "
        "(1) Spoofing, (2) Replay, (3) Cross-matching, (4) DB compromise, (5) Profiling, "
        "(6) Bias, (7) DoS sensor, (8) Man-in-the-Middle, (9) Insufficient privacy, "
        "(10) Lack of presentation attack detection. Đề tài giải quyết trực tiếp các rủi "
        "ro số (1), (2), (8), (10) trong hệ thống Secured.",
        indent_first=1.0)
    add_para(doc,
        "NIST SP 800-63B [13] phân chia mức xác thực thành 3 AAL (Authenticator Assurance "
        "Level): AAL1 (single-factor — không yêu cầu PAD), AAL2 (multi-factor + chống "
        "replay), AAL3 (hardware-based + PAD bắt buộc). Hệ thống Secured trong đề tài đáp "
        "ứng yêu cầu AAL2 cho biometric primary và sẵn sàng nâng cấp lên AAL3 khi tích "
        "hợp HSM/Secure Enclave.",
        indent_first=1.0)

    add_h2(doc, "2.8. FIDO Alliance và FIDO Biometric Component Certification")
    add_para(doc,
        "FIDO Alliance định nghĩa quy trình chứng nhận thành phần biometric với 3 cấp [31]:",
        indent_first=1.0)
    add_bullet(doc, "Level A: APCER ≤ 5%, BPCER ≤ 15% — đủ điều kiện sử dụng kết hợp MFA.")
    add_bullet(doc, "Level B: APCER ≤ 1%, BPCER ≤ 7% — phù hợp giao dịch tài chính trung bình.")
    add_bullet(doc, "Level C: APCER ≤ 0,15%, BPCER ≤ 3% — yêu cầu cho ngân hàng/định danh quốc gia.")
    add_para(doc,
        "Mục tiêu của Detection Engine trong đề tài là đạt FIDO Level A trên dataset 400 "
        "ảnh tự thu thập, đồng thời thiết kế kiến trúc cho phép nâng lên Level B khi mở "
        "rộng dataset (>10.000 ảnh) và bổ sung GPU tăng tốc.",
        indent_first=1.0)

    add_h2(doc, "2.9. Lịch sử phát triển kỹ thuật phát hiện tấn công trình diện")
    add_para(doc,
        "Để định vị chính xác vị trí của Detection Engine MobileNetV2 trong dòng "
        "chảy nghiên cứu, mục này điểm lại bốn giai đoạn phát triển chính của lĩnh "
        "vực PAD (Presentation Attack Detection):",
        indent_first=1.0)

    add_h3(doc, "2.9.1. Giai đoạn 2000–2010 — Texture descriptors thủ công")
    add_para(doc,
        "Các nghiên cứu sớm nhất tập trung vào việc trích xuất đặc trưng kết cấu "
        "(texture descriptor) từ ảnh RGB. Local Binary Pattern (LBP) của Ojala "
        "(2002) trở thành công cụ chuẩn — biến đổi mỗi pixel thành chuỗi bit dựa "
        "trên 8 láng giềng, sau đó dùng histogram làm đặc trưng cho SVM. "
        "Chingovska et al. [8] báo cáo accuracy 80–85% trên Replay-Attack DB với "
        "LBP-TOP (Three Orthogonal Planes). Hạn chế lớn nhất: descriptor thủ công "
        "không tổng quát hóa được sang điều kiện ánh sáng và camera mới.",
        indent_first=1.0)

    add_h3(doc, "2.9.2. Giai đoạn 2010–2016 — Motion và challenge-response")
    add_para(doc,
        "Khi texture-based bộc lộ giới hạn, hướng nghiên cứu chuyển sang phân tích "
        "chuyển động: blink detection (đo tỷ lệ EAR — Eye Aspect Ratio), micro-"
        "movement (đo dao động pixel quanh mắt), 3D structure-from-motion. Đáng "
        "chú ý là Pan et al. (2007) đề xuất eyeblink-based liveness và đạt accuracy "
        "~95% trong điều kiện kiểm soát. Tuy nhiên, hai vấn đề khiến hướng này khó "
        "đưa vào sản phẩm: (i) yêu cầu user thực hiện hành động (nháy mắt, gật đầu) "
        "làm chậm UX, (ii) bypass được bằng video replay 5–10 giây có chứa sẵn "
        "chuyển động.",
        indent_first=1.0)

    add_h3(doc, "2.9.3. Giai đoạn 2016–2020 — Deep Learning takeover")
    add_para(doc,
        "Sự xuất hiện của AlexNet (2012) và làn sóng deep learning đã tạo ra bước "
        "ngoặt cho PAD. Nguyen et al. (2017), Atoum et al. [23] báo cáo CNN-based "
        "PAD đạt EER < 5% trên CASIA-FASD và OULU-NPU. Đặc biệt:",
        indent_first=1.0)
    add_bullet(doc, "Boulkenafet et al. (2017) [6] đề xuất kết hợp đặc trưng từ "
                    "không gian màu YCbCr — phát hiện rằng kênh màu Cb/Cr nhạy với "
                    "ảnh in hơn kênh RGB do mất thông tin sắc tố trong quá trình "
                    "in-tái-chụp.")
    add_bullet(doc, "Liu et al. (2018) [9] giới thiệu Auxiliary Supervision — học "
                    "đồng thời depth map giả định từ ảnh 2D, tạo thêm tín hiệu "
                    "giám sát cho PAD học các đặc trưng có ý nghĩa vật lý.")
    add_bullet(doc, "MobileNet (Howard, 2017) và MobileNetV2 (Sandler, 2018) [3] "
                    "đưa CNN tới khả năng inference real-time trên thiết bị di "
                    "động — chính là backbone đề tài lựa chọn.")

    add_h3(doc, "2.9.4. Giai đoạn 2020–nay — Multi-modal và Adversarial-robust")
    add_para(doc,
        "Sự bùng nổ của deepfake (StyleGAN [18], FaceForensics++ [17]) buộc PAD "
        "phải tiến hóa. Bốn hướng chính của thế hệ 4:",
        indent_first=1.0)
    add_bullet(doc, "Multi-modal fusion — kết hợp RGB + depth (Intel RealSense) + "
                    "IR (Apple TrueDepth) + rPPG (đo mạch máu từ video) để khó "
                    "bypass đồng thời tất cả modality.")
    add_bullet(doc, "Domain Generalization — huấn luyện trên nhiều dataset để mô "
                    "hình tổng quát hóa cho domain chưa thấy. Stehouwer et al. "
                    "[33] đạt domain-generalization tốt với noise modeling.")
    add_bullet(doc, "Adversarial Training — huấn luyện chống lại adversarial "
                    "patches. Quan trọng vì attacker tinh vi có thể tạo PAI tối "
                    "ưu hóa cụ thể cho mô hình PAD.")
    add_bullet(doc, "Vision Transformer cho PAD — thay thế CNN bằng ViT/Swin với "
                    "self-attention. Accuracy gần 99% nhưng yêu cầu GPU và dataset "
                    "rất lớn (>100k ảnh).")
    add_para(doc,
        "Đề tài định vị tại thế hệ 3 — Detection Engine MobileNetV2 — vì lý do "
        "thực tiễn rõ ràng: phần lớn doanh nghiệp vừa và nhỏ tại Việt Nam không "
        "có GPU tăng tốc, không có camera depth/IR, và dataset PAD cấp trên "
        "100.000 ảnh không sẵn có cho ngôn ngữ và đặc thù dân số Việt. Đóng góp "
        "của đề tài không nằm ở việc đẩy state-of-the-art tăng thêm 0,5% accuracy "
        "mà nằm ở việc đưa ra một blueprint khả thi và có thể tái triển khai trên "
        "phần cứng phổ thông.",
        indent_first=1.0)

    add_h2(doc, "2.10. Phân tích sâu kiến trúc dlib và face_recognition")
    add_para(doc,
        "Vì face_recognition là thư viện cốt lõi của cả hai server, hiểu nội tại "
        "của nó là điều kiện cần để thiết kế các lớp phòng vệ phù hợp. Mục này "
        "phân tích từng giai đoạn pipeline mà thư viện thực hiện khi xử lý một "
        "frame ảnh:",
        indent_first=1.0)

    add_h3(doc, "2.10.1. HOG-based face detector")
    add_para(doc,
        "Dlib mặc định dùng Histogram of Oriented Gradients + Linear SVM cho face "
        "detection. Pipeline: ảnh được chia thành các cell 8×8, mỗi cell tính "
        "histogram của hướng gradient theo 9 bin (0–180°). Ghép thành descriptor "
        "vector 36-d cho mỗi block 16×16, sau đó SVM phân loại face/non-face. Ưu "
        "điểm: nhanh trên CPU (~30 FPS), nhẹ. Hạn chế: chỉ phát hiện được khuôn "
        "mặt frontal hoặc near-frontal (±30°), miss nếu user nghiêng đầu lớn hơn "
        "45° hoặc một phần khuôn mặt bị che. Với attacker, hạn chế này là một "
        "“feature” — họ có thể che một phần khuôn mặt thật để buộc hệ thống "
        "không detect, sau đó thay thế bằng PAI.",
        indent_first=1.0)

    add_h3(doc, "2.10.2. 5-point shape predictor")
    add_para(doc,
        "Sau khi face được phát hiện, dlib trích xuất 5 landmarks: hai khóe mắt "
        "ngoài, hai khóe mắt trong, đỉnh mũi. Mục đích: align ảnh khuôn mặt về "
        "vị trí chuẩn (mắt nằm trên trục ngang, khoảng cách giữa hai mắt = 64 "
        "pixel) để giảm variance trước khi đưa vào ResNet. Đây là bước alignment "
        "quan trọng — chính xác alignment cải thiện embedding accuracy ~2–3 điểm "
        "phần trăm.",
        indent_first=1.0)

    add_h3(doc, "2.10.3. ResNet-34 metric learning network")
    add_para(doc,
        "Thành phần “học sâu” thật sự của face_recognition là một biến thể "
        "ResNet-34 huấn luyện theo Triplet Loss trên 3 triệu ảnh khuôn mặt từ "
        "VGGFace2 và FaceScrub. Hàm loss: L = max(0, ‖f(A) − f(P)‖² − ‖f(A) − "
        "f(N)‖² + α), với A = anchor, P = positive (cùng người), N = negative "
        "(khác người), α = 0.2 là margin. Sau huấn luyện, mỗi khuôn mặt được nén "
        "thành embedding 128-d nằm trên unit sphere — nghĩa là ‖f(x)‖ ≈ 1.",
        indent_first=1.0)
    add_para(doc,
        "Ý nghĩa bảo mật: KHÔNG có gì trong embedding 128-d phản ánh tính “sống” "
        "của ảnh. Embedding của ảnh in cùng người và ảnh thật cùng người sẽ rất "
        "gần nhau — đó chính là Visibility Gap mà Detection Engine phải bịt. Điều "
        "thú vị: các embedding bị normalized về unit sphere nên distance Euclid "
        "≈ 2(1 − cosine_similarity), giải thích ngưỡng 0.6 phổ biến tương ứng với "
        "cosine similarity ≈ 0.82.",
        indent_first=1.0)

    add_h3(doc, "2.10.4. Threshold matching và sự đánh đổi với PAD threshold")
    add_para(doc,
        "Hệ thống có hai threshold độc lập: (i) match_threshold = 0.6 cho face "
        "matching và (ii) liveness_threshold = 0.7 cho PAD. Hai threshold tác "
        "động ngược chiều — siết match_threshold (0.5) làm tăng FRR matching "
        "trong khi giảm FAR matching, còn siết liveness_threshold (0.8) làm tăng "
        "BPCER trong khi giảm APCER. Đề tài lựa chọn tuning độc lập: match giữ "
        "0.6 (mặc định của face_recognition đã tốt), tinh chỉnh chỉ liveness ở "
        "0.7. Đây là cách tiếp cận “một biến tại một thời điểm” chuẩn trong "
        "thiết kế thực nghiệm.",
        indent_first=1.0)

    add_h2(doc, "2.11. So sánh các kiến trúc CNN khả dĩ cho Detection Engine")
    add_para(doc,
        "Trước khi chốt MobileNetV2, đề tài đã khảo sát 5 kiến trúc CNN có thể "
        "đóng vai trò Detection Engine. Bảng 2.4 tổng hợp so sánh:",
        indent_first=1.0)
    add_table_caption(doc, "2.4", "So sánh các kiến trúc CNN khả dĩ cho Detection Engine")
    add_table(doc,
        ["Kiến trúc", "Params (M)", "FLOPs (G)", "FPS CPU", "Top-1 ImageNet", "Phù hợp PAD"],
        [
            ["VGG-16",       "138",  "15.5", "3-5",  "71.5%", "Quá nặng cho CPU"],
            ["ResNet-50",    "25.6", "4.1",  "8-12", "76.0%", "Chậm hơn 3-4× MobileNetV2"],
            ["MobileNetV1",  "4.2",  "0.57", "20",   "70.6%", "Có thể, nhưng accuracy thấp hơn"],
            ["MobileNetV2",  "3.4",  "0.30", "28-32","72.0%", "★ Lựa chọn — cân bằng"],
            ["EfficientNet-B0","5.3","0.39", "20-25","77.1%", "Accuracy tốt hơn nhưng cần GPU"],
            ["MobileNetV3-Small","2.5","0.06","45-50","67.4%","Quá nhẹ — accuracy không đủ"],
        ],
        widths=[3.5, 2.2, 2, 2, 2.5, 4])
    add_para(doc,
        "Kết quả khảo sát: MobileNetV2 cho điểm cân bằng tốt nhất giữa số tham số "
        "(3,4M — nhỏ hơn ResNet-50 ~7,5×), FLOPs (0,3G — nhỏ hơn ~14×), FPS trên "
        "CPU (28-32 — đủ real-time) và accuracy ImageNet (72% — đủ cho transfer "
        "learning hiệu quả). Đặc biệt, các Inverted Residual block của MobileNetV2 "
        "có khả năng học đặc trưng phức tạp hơn MobileNetV1 do được expand kênh "
        "đầu vào trước khi depthwise conv [3].",
        indent_first=1.0)

    add_h2(doc, "2.12. NIST SP 800-63B và mức xác thực AAL chi tiết")
    add_para(doc,
        "NIST SP 800-63B [13] là tiêu chuẩn của Mỹ về Digital Identity Guidelines "
        "— cung cấp khung phân tầng cho các cấp độ xác thực. Mục này chi tiết hóa "
        "yêu cầu cụ thể của từng cấp:",
        indent_first=1.0)
    add_table_caption(doc, "2.5", "Yêu cầu kỹ thuật cho từng AAL theo NIST SP 800-63B")
    add_table(doc,
        ["Yêu cầu", "AAL1", "AAL2", "AAL3"],
        [
            ["Số lượng yếu tố",          "1",        "≥ 2",       "≥ 2 + hardware"],
            ["Yêu cầu PAD",              "Khuyến cáo","Bắt buộc",  "Bắt buộc + ISO 30107"],
            ["Chống replay",             "Không",     "Bắt buộc",  "Bắt buộc"],
            ["Chống MITM",               "Khuyến cáo","Bắt buộc TLS","Bắt buộc TLS + cert pinning"],
            ["Tần suất xác thực lại",   "30 ngày",   "12 giờ",    "12 giờ + reauth nếu inactivity"],
            ["Lưu trữ secret",           "Plaintext OK","Hashed",  "HSM bắt buộc"],
            ["Ví dụ thực tế",            "Forum, blog","Email, eKYC","Banking, gov ID"],
        ],
        widths=[4.5, 3.5, 3.5, 4])
    add_para(doc,
        "Hệ thống Secured trong đề tài đáp ứng yêu cầu của AAL2: có PAD (Detection "
        "Engine MobileNetV2), có anti-replay nonce, có TLS. Để nâng lên AAL3, cần "
        "bổ sung: (i) HSM cho lưu trữ encoding sinh trắc và private key, (ii) "
        "device attestation (SafetyNet/iOS DeviceCheck) bắt buộc, (iii) yêu cầu "
        "reauthentication sau mỗi lần inactivity > 15 phút. Đây là kế hoạch "
        "mở rộng được trình bày chi tiết trong Chương 5.",
        indent_first=1.0)

    add_h2(doc, "2.13. Các tiêu chuẩn liên quan: ISO/IEC 19795 và 19989")
    add_para(doc,
        "Bên cạnh ISO/IEC 30107, còn có hai tiêu chuẩn ISO khác liên quan trực "
        "tiếp đến đánh giá hệ thống biometric:",
        indent_first=1.0)
    add_bullet(doc, "ISO/IEC 19795 — Biometric Performance Testing and Reporting: "
                    "định nghĩa cách thiết kế thí nghiệm, tính FAR/FRR, ROC, DET, "
                    "và quy tắc báo cáo. Đề tài tuân theo Phần 1 (framework) và "
                    "Phần 4 (interoperability) khi đo các chỉ số.")
    add_bullet(doc, "ISO/IEC 19989 — Biometric Security Evaluation theo Common "
                    "Criteria: cung cấp framework đánh giá an toàn cho hệ thống "
                    "biometric trong context bảo mật cao. Đề tài chưa đạt chứng "
                    "chỉ Common Criteria nhưng thiết kế theo guideline.")
    add_para(doc,
        "Việc đáp ứng đồng thời ISO/IEC 30107 (PAD) + ISO/IEC 19795 (đo lường) + "
        "NIST SP 800-63B (AAL) tạo thành một bộ ba tiêu chuẩn mà bất kỳ hệ thống "
        "biometric production nào cũng cần kiểm tra. Đề tài lấy bộ ba này làm "
        "kim chỉ nam cho các quyết định thiết kế, đảm bảo blueprint đề xuất có "
        "tính tương thích cao với chuẩn quốc tế.",
        indent_first=1.0)

    add_h2(doc, "2.14. Tổng kết chương")
    add_para(doc,
        "Chương 2 đã thiết lập nền tảng lý thuyết: từ quy trình xác thực sinh trắc 6 bước, "
        "phân loại TTPs theo ISO/IEC 30107 và ánh xạ vào MITRE ATT&CK, đến kiến trúc "
        "MobileNetV2 với Inverted Residual và quy trình Transfer Learning hai pha. Các chỉ "
        "số APCER/BPCER/FAR/FRR đã được định nghĩa rõ làm cơ sở đánh giá định lượng. Chương "
        "tiếp theo sẽ chuyển sang giai đoạn Phân tích & Thiết kế hệ thống — cụ thể hóa các "
        "khái niệm trên thành kiến trúc client-server, Pipeline Image Telemetry và Threat "
        "Model chi tiết.",
        indent_first=1.0, space_after=10)
    add_page_break(doc)

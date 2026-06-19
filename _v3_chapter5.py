# -*- coding: utf-8 -*-
"""_v3_chapter5.py - Chuong 5: Ket luan va huong phat trien.

Chuong nay chi tap trung vao tong ket toan bo do an va de xuat huong
phat trien. Toan bo phan tich Server Secured da duoc dua vao Chuong 4.

Khong em-dash. Khong en-dash.
"""

from _report_core import (
    add_h1, add_h2, add_h3, add_para, add_bullet,
    add_image, add_table, add_table_caption, add_page_break, add_code_block,
)


def build_chapter5(doc):
    add_h1(doc, "CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")

    add_para(doc,
        "Chương 5 tổng kết toàn bộ kết quả đã đạt được trong quá trình "
        "thực hiện đồ án, đối chiếu với mục tiêu nghiên cứu đề ra ban đầu, "
        "phân tích các hạn chế còn lại và đề xuất các hướng phát triển "
        "trong thời gian tới. Đây là chương chốt nhằm đưa ra cái nhìn "
        "tổng quan về đóng góp của đồ án đối với bài toán bảo vệ hệ thống "
        "xác thực sinh trắc học khuôn mặt trước các kỹ thuật tấn công "
        "ngày càng tinh vi.",
        indent_first=1.0)

    # =================================================================
    # 5.1 Ket qua dat duoc
    # =================================================================
    add_h2(doc, "5.1. Kết quả đạt được")

    add_para(doc,
        "Đồ án đã hoàn thành đầy đủ năm mục tiêu cụ thể nêu trong Lời mở "
        "đầu, từ việc xây dựng hệ thống Vulnerable, phân tích kịch bản "
        "Injection, huấn luyện mô hình PAD, tích hợp Server Secured cho "
        "đến đánh giá định lượng theo tiêu chuẩn ISO/IEC 30107-3. Bảng "
        "5.1 đối chiếu mục tiêu với kết quả thực tế thu được.",
        indent_first=1.0)

    add_table_caption(doc, "5.1",
        "Đối chiếu mục tiêu nghiên cứu và kết quả đạt được.")
    add_table(doc,
        ["STT", "Mục tiêu đặt ra", "Kết quả đạt được"],
        [
            ["1",
             "Hiện thực hóa hệ thống xác thực khuôn mặt Vulnerable",
             "Hoàn thành Flask + face_recognition, ba endpoint /register, "
             "/authenticate, /users; database pickle với 10 user mẫu."],
            ["2",
             "Phân tích kịch bản tấn công Injection ở tầng API",
             "Mô tả chi tiết payload base64, đo tỷ lệ bypass Vulnerable "
             "đạt 99.3 phần trăm trên 450 request, có log minh chứng."],
            ["3",
             "Huấn luyện mô hình PAD MobileNetV2 Transfer Learning hai pha",
             "Val accuracy 97.5 phần trăm, APCER và BPCER 2.5 phần trăm, "
             "AUC 0.987, EER tại ngưỡng 0.7."],
            ["4",
             "Tích hợp mô hình vào Server Secured",
             "Lớp wrapper LivenessPredictor, hàm check_liveness() đặt "
             "trước cả /register lẫn /authenticate, demo trên giao diện "
             "Lab."],
            ["5",
             "Đánh giá định lượng theo ISO/IEC 30107-3",
             "Secured chặn 450 trên 450 Injection, 49 trên 50 ảnh thật "
             "vẫn được chấp nhận, độ trễ phát sinh thêm 107 ms."],
        ],
        widths=[1.0, 6.0, 9.0])

    add_para(doc,
        "Ngoài năm mục tiêu chính, đồ án còn ghi nhận một số đóng góp "
        "không nằm trong yêu cầu ban đầu nhưng có giá trị sử dụng lại:",
        indent_first=1.0)
    add_bullet(doc,
        "Bộ dữ liệu nội bộ gồm 200 ảnh Real và 200 ảnh Fake do tác giả "
        "tự chụp và tự dán nhãn, kèm script chia train/val tỷ lệ 90 trên "
        "10, có thể tái sử dụng cho các nghiên cứu PAD tương lai.")
    add_bullet(doc,
        "Pipeline tăng cường dữ liệu tám phép biến đổi (Resize, "
        "RandomCrop, HorizontalFlip, ColorJitter, RandomRotation, "
        "RandomAffine, GaussianBlur, Normalize) đóng gói trong "
        "torchvision.transforms.Compose, có thể tái sử dụng nguyên cho "
        "các bài toán phân loại ảnh khác.")
    add_bullet(doc,
        "Bộ script Red Team gồm hai kịch bản inject_attack.py và "
        "log_analysis.py giúp đo tỷ lệ bypass và sinh báo cáo tự động, "
        "có thể được mở rộng cho các bộ ảnh tấn công khác.")

    # =================================================================
    # 5.2 Y nghia khoa hoc va thuc tien
    # =================================================================
    add_h2(doc, "5.2. Ý nghĩa khoa học và thực tiễn")

    add_para(doc,
        "Về mặt khoa học, đồ án đã thử nghiệm và xác nhận trên thực tế "
        "rằng kiến trúc MobileNetV2 kết hợp Transfer Learning hai pha "
        "(Phase 1 đóng băng backbone với learning rate 1e-3 và StepLR; "
        "Phase 2 mở băng từ inverted residual block thứ 14 với learning "
        "rate 1e-4 và CosineAnnealingLR) đủ năng lực đạt EER dưới 3 "
        "phần trăm trên một tập dữ liệu PAD nhỏ chỉ 400 ảnh. Đây là "
        "bằng chứng thực nghiệm cho luận điểm mà nhiều khảo sát học "
        "thuật đã nêu, đó là backbone đã pretrain trên ImageNet vẫn "
        "chứa các đặc trưng hữu ích cho bài toán phát hiện ảnh giả.",
        indent_first=1.0)

    add_para(doc,
        "Về mặt thực tiễn, đồ án cung cấp một mẫu thiết kế cụ thể cho "
        "việc tích hợp PAD vào hệ thống xác thực khuôn mặt sản xuất: "
        "đặt PAD ngay trước module so khớp đặc trưng, áp dụng cho cả "
        "/register lẫn /authenticate, dùng mã HTTP riêng cho từng tình "
        "huống và ghi nhật ký liveness_score để phục vụ giám sát. Mẫu "
        "thiết kế này có thể đem áp dụng được cho các pipeline khác như "
        "FastAPI, Django REST Framework hoặc gRPC mà không cần thay đổi "
        "đáng kể logic nghiệp vụ.",
        indent_first=1.0)

    add_para(doc,
        "Kết quả của đồ án khẳng định một thông điệp xuyên suốt: an "
        "toàn của hệ thống xác thực sinh trắc không nằm ở thuật toán so "
        "khớp đặc trưng mà nằm ở khả năng phân biệt được tín hiệu sinh "
        "trắc thật với tín hiệu giả mạo trước khi so khớp. PAD không "
        "phải tính năng tùy chọn, nó là điều kiện cần để bất kỳ hệ "
        "thống xác thực khuôn mặt nào có thể đưa vào sản xuất.",
        indent_first=1.0)

    # =================================================================
    # 5.3 Han che
    # =================================================================
    add_h2(doc, "5.3. Hạn chế của đồ án")

    add_para(doc,
        "Trong quá trình thực hiện và đánh giá, một số hạn chế đã được "
        "nhận diện rõ. Việc liệt kê đầy đủ các hạn chế này có ý nghĩa "
        "quan trọng vì nó vừa giúp người đọc đánh giá đúng phạm vi áp "
        "dụng của kết quả, vừa định hướng cho các nghiên cứu tiếp theo.",
        indent_first=1.0)

    add_h3(doc, "5.3.1. Hạn chế về dữ liệu")
    add_bullet(doc,
        "Tập dữ liệu huấn luyện chỉ gồm 200 ảnh thật và 200 ảnh giả, "
        "quy mô còn nhỏ so với các benchmark như OULU-NPU [19] hay "
        "Replay-Attack [18] vốn có hàng nghìn mẫu.")
    add_bullet(doc,
        "Toàn bộ dữ liệu được thu thập trong phòng Lab với một loại "
        "camera laptop và điều kiện ánh sáng tương đối ổn định, do đó "
        "mô hình có nguy cơ overfit theo môi trường.")
    add_bullet(doc,
        "Tập người được chụp chủ yếu là sinh viên cùng độ tuổi và cùng "
        "khu vực địa lý, chưa đa dạng về sắc tộc, độ tuổi và đặc điểm "
        "sinh trắc.")

    add_h3(doc, "5.3.2. Hạn chế về kịch bản tấn công")
    add_bullet(doc,
        "Đồ án mới chỉ phòng thủ kịch bản Injection ảnh tĩnh, chưa "
        "đánh giá định lượng các biến thể phức tạp như deepfake video, "
        "ảnh GAN sinh tổng hợp hoặc tấn công khuôn mặt 3D bằng mặt nạ "
        "silicon.")
    add_bullet(doc,
        "Chưa kiểm thử trước các kỹ thuật adversarial attack ở tầng "
        "đầu vào của mô hình PAD (FGSM, PGD), vốn là mối đe dọa thực "
        "tế khi nhật ký lộ ra cấu trúc mạng.")
    add_bullet(doc,
        "Chưa mô phỏng tấn công nhắm vào endpoint /register sau khi đã "
        "có quyền truy cập tạm thời, ví dụ kẻ tấn công đăng ký tài "
        "khoản mới với khuôn mặt thật rồi sau đó đổi sang ảnh giả.")

    add_h3(doc, "5.3.3. Hạn chế về kiến trúc và vận hành")
    add_bullet(doc,
        "Kiến trúc hiện tại thiếu cơ chế thách thức tương tác (active "
        "liveness) như yêu cầu chớp mắt, quay đầu hoặc đọc số ngẫu "
        "nhiên, vốn được FIDO khuyến nghị cho ứng dụng có rủi ro cao.")
    add_bullet(doc,
        "Mô hình chạy đồng bộ trong cùng tiến trình Flask, chưa hỗ trợ "
        "scale ngang qua nhiều worker khi tải tăng cao.")
    add_bullet(doc,
        "Chưa có cơ chế giám sát drift theo thời gian: nếu phân phối "
        "ảnh đầu vào thực tế lệch dần khỏi tập huấn luyện, độ chính "
        "xác có thể giảm mà không có cảnh báo.")

    # =================================================================
    # 5.4 Huong phat trien
    # =================================================================
    add_h2(doc, "5.4. Hướng phát triển")

    add_para(doc,
        "Trên cơ sở các hạn chế đã nêu, đồ án đề xuất ba nhánh phát "
        "triển chính trong các giai đoạn tiếp theo, sắp xếp theo thứ "
        "tự ưu tiên giảm dần.",
        indent_first=1.0)

    add_h3(doc, "5.4.1. Mở rộng dữ liệu và backbone hiện đại")
    add_para(doc,
        "Bước phát triển ngắn hạn là mở rộng tập dữ liệu bằng cách kết "
        "hợp các benchmark công khai đã được kiểm thử (CASIA-FASD, "
        "Replay-Attack, OULU-NPU) và bổ sung dữ liệu sinh tổng hợp từ "
        "GAN. Sau khi có tập dữ liệu lớn hơn, có thể thử nghiệm các "
        "backbone hiện đại hơn như EfficientNet-Lite, MobileNetV3 hoặc "
        "Vision Transformer nhỏ (ViT-Tiny) để tận dụng các đặc trưng "
        "đa thang đo. Mục tiêu là đưa AUC lên trên 0.99 trong điều "
        "kiện cross-dataset.",
        indent_first=1.0)

    add_h3(doc, "5.4.2. Phòng thủ theo chiều sâu (Defense in Depth)")
    add_para(doc,
        "Bước trung hạn là bổ sung lớp phòng thủ thứ hai để tạo nên "
        "kiến trúc defense-in-depth thực sự. Một số ý tưởng cụ thể:",
        indent_first=1.0)
    add_bullet(doc,
        "Phân tích metadata ảnh (EXIF, độ phân giải, thiết bị chụp) "
        "và tỷ lệ nhiễu sensor để phát hiện ảnh đã qua tái chụp hoặc "
        "tải về từ Internet.")
    add_bullet(doc,
        "Áp dụng anti-replay nonce mã hóa thời điểm chụp vào mỗi "
        "request để chặn kẻ tấn công gửi lại request hợp lệ đã ghi "
        "lại trước đó.")
    add_bullet(doc,
        "Kết hợp signal khác như hồng ngoại, độ sâu (depth map) từ "
        "camera ToF nếu phần cứng hỗ trợ, để có hai kênh thông tin "
        "độc lập về tính sống của khuôn mặt.")

    add_h3(doc, "5.4.3. Triển khai active liveness và chứng nhận FIDO")
    add_para(doc,
        "Bước dài hạn là triển khai active liveness bằng việc kết hợp "
        "với một mô hình phát hiện cử động đầu nhẹ và một thách thức "
        "ngẫu nhiên do máy chủ phát ra (chớp mắt, quay đầu trái phải, "
        "đọc số ngẫu nhiên). Kết hợp với cơ chế PAD thụ động hiện tại, "
        "hệ thống sẽ đáp ứng được tiêu chuẩn FIDO Biometric Component "
        "Certification Level B, mở đường cho việc triển khai trong các "
        "ứng dụng tài chính, ngân hàng số và định danh điện tử.",
        indent_first=1.0)

    # =================================================================
    # 5.5 Loi ket
    # =================================================================
    add_h2(doc, "5.5. Lời kết")

    add_para(doc,
        "Đồ án đã đi qua đầy đủ vòng đời của một bài toán bảo mật sinh "
        "trắc học, từ phân tích bề mặt tấn công, dựng hệ thống "
        "Vulnerable để tái hiện điểm yếu, huấn luyện mô hình học sâu "
        "để phát hiện tấn công, tích hợp mô hình vào dịch vụ và đánh "
        "giá định lượng theo tiêu chuẩn quốc tế. Quá trình này không "
        "chỉ giúp tác giả nắm vững các kiến thức lý thuyết về biometric "
        "authentication, Presentation Attack Detection, Transfer "
        "Learning mà còn rèn luyện tư duy của một kỹ sư an ninh ứng "
        "dụng: nhìn hệ thống dưới góc độ kẻ tấn công, đo lường bằng "
        "con số và đề xuất giải pháp có thể kiểm chứng.",
        indent_first=1.0)

    add_para(doc,
        "Tác giả hy vọng các kết quả của đồ án sẽ đóng góp một góc "
        "nhìn nhỏ vào việc nâng cao mức độ an toàn của các hệ thống "
        "xác thực sinh trắc tại Việt Nam, đặc biệt khi định danh điện "
        "tử và sinh trắc học đang trở thành nền tảng của nhiều dịch vụ "
        "công và dịch vụ tài chính. Tác giả cũng xin gửi lời cảm ơn "
        "chân thành nhất đến giảng viên hướng dẫn ThS. Đặng Thị Thạch "
        "Thảo, quý thầy cô Khoa Công nghệ Thông tin Trường Đại học "
        "Công nghệ TP. HCM, gia đình và bạn bè đã đồng hành trong suốt "
        "thời gian thực hiện đồ án này.",
        indent_first=1.0)


# =================================================================
# Tai lieu tham khao
# =================================================================
def build_references(doc):
    add_h1(doc, "TÀI LIỆU THAM KHẢO")

    refs = [
        '[1] ISO/IEC 30107-1:2023, "Information technology - Biometric '
        'presentation attack detection - Part 1: Framework", International '
        'Organization for Standardization, 2023.',
        '[2] ISO/IEC 30107-3:2023, "Information technology - Biometric '
        'presentation attack detection - Part 3: Testing and reporting", '
        'International Organization for Standardization, 2023.',
        '[3] NIST SP 800-63B, "Digital Identity Guidelines: Authentication '
        'and Lifecycle Management", National Institute of Standards and '
        'Technology, 2017 (revision 4 draft 2024).',
        '[4] FIDO Alliance, "FIDO Biometric Component Certification Program", '
        'FIDO Alliance Specifications, 2024.',
        '[5] OWASP Foundation, "OWASP Top 10:2021 - The Ten Most Critical '
        'Web Application Security Risks", 2021.',
        '[6] OWASP Foundation, "OWASP API Security Top 10:2023", 2023.',
        '[7] MITRE Corporation, "MITRE ATT&CK Enterprise Matrix v15.1", 2024. '
        'https://attack.mitre.org',
        '[8] MITRE Corporation, "MITRE ATLAS - Adversarial Threat Landscape '
        'for Artificial-Intelligence Systems", 2024. https://atlas.mitre.org',
        '[9] A. K. Jain, A. A. Ross, K. Nandakumar, "Introduction to '
        'Biometrics", Springer, 2nd ed., 2017.',
        '[10] D. King, "Dlib-ml: A machine learning toolkit", Journal of '
        'Machine Learning Research, vol. 10, pp. 1755-1758, 2009.',
        '[11] A. Geitgey, "face_recognition library documentation", v1.3.0, '
        '2020. https://github.com/ageitgey/face_recognition',
        '[12] F. Schroff, D. Kalenichenko, J. Philbin, "FaceNet: A Unified '
        'Embedding for Face Recognition and Clustering", CVPR, 2015.',
        '[13] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, L.-C. Chen, '
        '"MobileNetV2: Inverted Residuals and Linear Bottlenecks", CVPR, 2018.',
        '[14] A. Howard et al., "Searching for MobileNetV3", ICCV, 2019.',
        '[15] M. Tan, Q. V. Le, "EfficientNet: Rethinking Model Scaling for '
        'Convolutional Neural Networks", ICML, 2019.',
        '[16] J. Deng et al., "ImageNet: A Large-Scale Hierarchical Image '
        'Database", CVPR, 2009.',
        '[17] Z. Zhang, J. Yan, S. Liu, Z. Lei, D. Yi, S. Z. Li, "A face '
        'antispoofing database with diverse attacks", IAPR International '
        'Conference on Biometrics (ICB), 2012.',
        '[18] I. Chingovska, A. Anjos, S. Marcel, "On the effectiveness of '
        'local binary patterns in face anti-spoofing", BIOSIG, 2012. '
        '(Replay-Attack dataset)',
        '[19] Z. Boulkenafet et al., "OULU-NPU: A mobile face presentation '
        'attack database with real-world variations", IEEE FG, 2017.',
        '[20] R. Ramachandra, C. Busch, "Presentation Attack Detection '
        'Methods for Face Recognition Systems: A Comprehensive Survey", '
        'ACM Computing Surveys, vol. 50, no. 1, 2017.',
        '[21] S. R. Arashloo, J. Kittler, W. Christmas, "An anomaly '
        'detection approach to face spoofing detection", IEEE Trans. on '
        'Information Forensics and Security, vol. 12, 2017.',
        '[22] Y. Liu, A. Jourabloo, X. Liu, "Learning Deep Models for Face '
        'Anti-Spoofing: Binary or Auxiliary Supervision", CVPR, 2018.',
        '[23] T. de Freitas Pereira et al., "Face liveness detection using '
        'dynamic texture", EURASIP Journal on Image and Video Processing, '
        '2014.',
        '[24] K. He, X. Zhang, S. Ren, J. Sun, "Deep Residual Learning for '
        'Image Recognition", CVPR, 2016.',
        '[25] D. P. Kingma, J. Ba, "Adam: A Method for Stochastic '
        'Optimization", ICLR, 2015.',
        '[26] N. Srivastava et al., "Dropout: A simple way to prevent '
        'neural networks from overfitting", JMLR, vol. 15, 2014.',
        '[27] S. Ioffe, C. Szegedy, "Batch normalization: Accelerating '
        'deep network training by reducing internal covariate shift", '
        'ICML, 2015.',
        '[28] A. Krizhevsky, I. Sutskever, G. Hinton, "ImageNet '
        'Classification with Deep Convolutional Neural Networks", NIPS, 2012.',
        '[29] European Parliament, "Regulation (EU) 2016/679 - General '
        'Data Protection Regulation (GDPR)", 2016.',
        '[30] Quốc hội Việt Nam, "Luật An toàn thông tin mạng số '
        '86/2015/QH13", 2015.',
        '[31] Quốc hội Việt Nam, "Luật Bảo vệ dữ liệu cá nhân (dự thảo '
        '2024)", 2024.',
        '[32] Cloudflare, "What is a replay attack?", Cloudflare Learning '
        'Center, 2023. https://www.cloudflare.com/learning/',
        '[33] OWASP Foundation, "Authentication Cheat Sheet", OWASP Cheat '
        'Sheet Series, 2024.',
        '[34] M. Howard, S. Lipner, "The Security Development Lifecycle", '
        'Microsoft Press, 2006.',
        '[35] A. Shostack, "Threat Modeling: Designing for Security", '
        'Wiley, 2014.',
        '[36] P. Mell, T. Grance, "The NIST Definition of Cloud Computing", '
        'NIST SP 800-145, 2011.',
        '[37] PyTorch Team, "PyTorch Documentation v2.1", 2024. '
        'https://pytorch.org/docs',
        '[38] OpenCV Team, "OpenCV-Python Tutorials v4.9", 2024. '
        'https://docs.opencv.org',
        '[39] Pallets Projects, "Flask Documentation v3.0", 2024. '
        'https://flask.palletsprojects.com',
    ]

    for ref in refs:
        add_para(doc, ref, size=12, align='justify',
                 indent_first=0.0, space_after=4)

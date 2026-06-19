# -*- coding: utf-8 -*-
"""_v3_chapter2.py - Chuong 2: Co so ly thuyet ve sinh trac hoc khuon mat.

Khong em-dash, khong en-dash.
"""

from _report_core import (
    add_h1, add_h2, add_h3, add_para, add_bullet,
    add_image, add_table, add_table_caption, add_page_break,
)


def build_chapter2(doc):
    add_h1(doc, "CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VỀ SINH TRẮC HỌC")

    add_para(doc,
        "Chương 2 hệ thống hóa các kiến thức nền tảng cần thiết để hiểu "
        "phần kỹ thuật ở các chương tiếp theo. Phạm vi của chương gồm: "
        "định nghĩa và phân loại sinh trắc học, kiến trúc tổng quát của "
        "một hệ thống xác thực khuôn mặt, các thuật toán trích đặc trưng "
        "phổ biến, các chỉ số đánh giá, các tiêu chuẩn quốc tế và các "
        "mối đe dọa thường gặp đối với hệ thống sinh trắc học.",
        indent_first=1.0)

    # =================================================================
    # 2.1 Khai niem va phan loai
    # =================================================================
    add_h2(doc, "2.1. Khái niệm sinh trắc học")

    add_h3(doc, "2.1.1. Định nghĩa")
    add_para(doc,
        "Theo tiêu chuẩn ISO/IEC 2382-37, sinh trắc học (biometrics) là "
        "ngành khoa học nhận dạng tự động một cá nhân dựa trên các đặc "
        "trưng sinh học hoặc đặc trưng hành vi của họ. Mục tiêu của một "
        "hệ thống sinh trắc học là trả lời một trong hai câu hỏi: (1) "
        "“Người này có phải là người mà hệ thống đã đăng ký với danh "
        "tính X hay không?” (chế độ xác minh, verification, 1:1) hoặc "
        "(2) “Người này tương ứng với danh tính nào trong cơ sở dữ liệu?” "
        "(chế độ định danh, identification, 1:N).",
        indent_first=1.0)

    add_para(doc,
        "Khác với mật khẩu hoặc thẻ vật lý, sinh trắc học gắn liền với "
        "thân thể của người dùng nên không thể bị quên, bị mất hoặc bị "
        "chuyển nhượng. Tuy nhiên, đặc điểm bất biến đó cũng chính là "
        "điểm yếu lớn nhất: một khi bị lộ, dữ liệu sinh trắc không thể "
        "thay đổi được, ảnh hưởng dài hạn tới đời sống của nạn nhân.",
        indent_first=1.0)

    add_h3(doc, "2.1.2. Phân loại đặc trưng sinh trắc học")
    add_para(doc,
        "Đặc trưng sinh trắc học được chia làm hai nhóm lớn theo bản "
        "chất nguồn gốc.",
        indent_first=1.0)

    add_bullet(doc,
        "Đặc trưng sinh học (physiological): khuôn mặt, vân tay, mống "
        "mắt, võng mạc, hình bàn tay, cấu trúc tĩnh mạch. Các đặc "
        "trưng này tương đối ổn định theo thời gian và ít phụ thuộc "
        "trạng thái của người dùng.")
    add_bullet(doc,
        "Đặc trưng hành vi (behavioral): chữ ký, dáng đi, cách gõ "
        "phím, giọng nói, cử chỉ. Các đặc trưng này bị ảnh hưởng "
        "bởi cảm xúc, sức khỏe, hoàn cảnh nên thường có độ ổn định "
        "thấp hơn nhóm sinh học.")

    add_para(doc,
        "Trong khuôn khổ đề tài, đối tượng được tập trung là khuôn mặt, "
        "thuộc nhóm đặc trưng sinh học. Khuôn mặt là một trong các "
        "modal phổ biến nhất hiện nay nhờ chi phí cảm biến thấp, không "
        "yêu cầu tiếp xúc, và đã được các thư viện mã nguồn mở hỗ trợ "
        "đầy đủ. Tuy nhiên, khuôn mặt cũng dễ bị thu thập trái phép "
        "nhất, do nó liên tục lộ ra với các camera xung quanh và các "
        "ảnh trên mạng xã hội.",
        indent_first=1.0)

    # =================================================================
    # 2.2 Kien truc he thong xac thuc khuon mat
    # =================================================================
    add_h2(doc, "2.2. Kiến trúc tổng quát của một hệ thống xác thực khuôn mặt")

    add_para(doc,
        "Một hệ thống xác thực khuôn mặt điển hình gồm bốn module nối "
        "tiếp: (1) thu nhận ảnh, (2) phát hiện và căn chỉnh khuôn mặt, "
        "(3) trích đặc trưng và (4) ra quyết định so khớp. Mỗi module "
        "đều có khả năng bị tấn công và do đó cần biện pháp phòng vệ "
        "tương ứng.",
        indent_first=1.0)

    add_h3(doc, "2.2.1. Module thu nhận ảnh")
    add_para(doc,
        "Module này gồm cảm biến (camera RGB, camera IR, camera Depth) "
        "và phần mềm điều khiển. Trên các thiết bị PC và web, hầu hết "
        "đều dùng webcam RGB qua API getUserMedia của trình duyệt. Đầu "
        "ra của module là một khung hình ảnh ở định dạng JPEG hoặc PNG "
        "được mã hóa Base64 để truyền qua HTTP.",
        indent_first=1.0)

    add_h3(doc, "2.2.2. Module phát hiện và căn chỉnh khuôn mặt")
    add_para(doc,
        "Module này có hai bước con. Phát hiện (face detection) trả về "
        "khung hình chữ nhật bao quanh từng khuôn mặt trong ảnh. Căn "
        "chỉnh (face alignment) chuẩn hóa hướng và tỷ lệ, thường bằng "
        "cách tìm các điểm mốc (facial landmarks) như góc mắt, đầu "
        "mũi, khóe miệng rồi áp dụng phép biến đổi affine để đưa các "
        "điểm này về vị trí tham chiếu chuẩn. Trong đề tài, hai bước "
        "này được thực hiện bởi thư viện dlib thông qua bộ phát hiện "
        "Histogram of Oriented Gradients (HOG) và bộ ước lượng 68 "
        "landmark do dlib cung cấp.",
        indent_first=1.0)

    add_h3(doc, "2.2.3. Module trích đặc trưng")
    add_para(doc,
        "Module này biến một ảnh khuôn mặt đã căn chỉnh thành một vector "
        "số ngắn gọn nhưng đại diện được danh tính. Hai cách tiếp cận "
        "phổ biến: (1) đặc trưng thủ công (LBP, HOG, SIFT) và (2) đặc "
        "trưng học sâu (deep features) bằng các mạng CNN huấn luyện "
        "trên cơ sở dữ liệu khuôn mặt quy mô lớn. Đề tài sử dụng "
        "phương án thứ hai, cụ thể là mô hình ResNet-29 của dlib đã "
        "được face_recognition đóng gói sẵn, sinh vector 128 chiều cho "
        "mỗi khuôn mặt.",
        indent_first=1.0)

    add_h3(doc, "2.2.4. Module ra quyết định so khớp")
    add_para(doc,
        "Khi một người yêu cầu xác minh, hệ thống lấy vector đặc trưng "
        "của họ rồi so sánh với vector đã đăng ký theo một độ đo "
        "(distance metric). Với face_recognition, độ đo là khoảng cách "
        "Euclide giữa hai vector 128 chiều. Nếu khoảng cách nhỏ hơn "
        "ngưỡng cho trước (mặc định 0,6), hệ thống chấp nhận; nếu lớn "
        "hơn, hệ thống từ chối.",
        indent_first=1.0)

    add_image(doc, "fig_image_telemetry.png", width_cm=14,
              fig_num="2.1",
              caption="Sơ đồ pipeline xử lý ảnh trong hệ thống xác thực khuôn mặt")

    # =================================================================
    # 2.3 Trich dac trung khuon mat 128 chieu
    # =================================================================
    add_h2(doc, "2.3. Trích đặc trưng khuôn mặt bằng dlib và face_recognition")

    add_h3(doc, "2.3.1. Thư viện dlib")
    add_para(doc,
        "dlib là thư viện C++ được Davis King phát triển từ 2009, cung "
        "cấp các thuật toán Học máy hiệu năng cao và các tiện ích cho "
        "xử lý ảnh. Trong sinh trắc học, dlib nổi tiếng với ba thành "
        "phần: bộ phát hiện khuôn mặt HOG + linear SVM, bộ phát hiện "
        "khuôn mặt CNN MMOD và mô hình ResNet 29 lớp dùng để sinh "
        "embedding 128 chiều. Đề tài tận dụng cả ba thành phần này "
        "thông qua wrapper Python face_recognition.",
        indent_first=1.0)

    add_h3(doc, "2.3.2. Thư viện face_recognition")
    add_para(doc,
        "face_recognition của Adam Geitgey là một wrapper Python tinh "
        "gọn cho dlib, cung cấp ba hàm chính: face_locations() trả về "
        "tọa độ các khuôn mặt, face_landmarks() trả về 68 điểm mốc và "
        "face_encodings() trả về embedding 128 chiều. Trong đề tài, "
        "face_recognition được dùng làm bộ trích đặc trưng cho cả "
        "Server Vulnerable và Server Secured.",
        indent_first=1.0)

    add_h3(doc, "2.3.3. Embedding 128 chiều và ý nghĩa hình học")
    add_para(doc,
        "Mạng ResNet-29 trong dlib được huấn luyện theo nguyên lý "
        "Triplet Loss, mục tiêu là học một không gian embedding sao cho "
        "ảnh của cùng một người luôn gần nhau hơn ảnh của hai người "
        "khác nhau. Sau huấn luyện, mỗi khuôn mặt được biểu diễn bằng "
        "một điểm trên mặt cầu đơn vị 128 chiều. Hai vector của cùng "
        "một người thường có khoảng cách Euclide nhỏ hơn 0,4, hai vector "
        "của hai người khác nhau thường có khoảng cách lớn hơn 0,6. "
        "Ngưỡng quyết định 0,6 trong face_recognition chính là ngưỡng "
        "tham chiếu được tác giả đề xuất sau khi đánh giá trên cơ sở "
        "dữ liệu Labeled Faces in the Wild (LFW).",
        indent_first=1.0)

    # =================================================================
    # 2.4 Cac chi so danh gia
    # =================================================================
    add_h2(doc, "2.4. Các chỉ số đánh giá hệ thống xác thực sinh trắc học")

    add_para(doc,
        "Hiệu năng của một hệ thống sinh trắc học được đánh giá bằng "
        "các chỉ số định lượng đo độ chính xác và mức độ rủi ro. Bảng "
        "2.1 tóm tắt các chỉ số chính.",
        indent_first=1.0)

    add_table_caption(doc, "2.1", "Các chỉ số đánh giá hệ thống sinh trắc học")
    add_table(doc,
        ["Chỉ số", "Tên đầy đủ", "Ý nghĩa"],
        [
            ["FAR", "False Acceptance Rate",
             "Tỷ lệ chấp nhận nhầm: hệ thống coi người lạ là người đã đăng ký"],
            ["FRR", "False Rejection Rate",
             "Tỷ lệ từ chối nhầm: hệ thống từ chối chính chủ tài khoản"],
            ["EER", "Equal Error Rate",
             "Điểm vận hành mà tại đó FAR bằng FRR"],
            ["TAR", "True Acceptance Rate",
             "Tỷ lệ chấp nhận đúng (TAR = 1 - FRR)"],
            ["APCER", "Attack Presentation Classification Error Rate",
             "Tỷ lệ ảnh tấn công bị phân loại sai thành ảnh thật (ISO 30107-3)"],
            ["BPCER", "Bona-fide Presentation Classification Error Rate",
             "Tỷ lệ ảnh thật bị phân loại sai thành tấn công (ISO 30107-3)"],
            ["ROC", "Receiver Operating Characteristic",
             "Đường cong vẽ TAR theo FAR khi ngưỡng thay đổi"],
            ["AUC", "Area Under the ROC Curve",
             "Diện tích dưới đường ROC, càng gần 1 càng tốt"],
        ],
        widths=[2.5, 5.5, 8.0])

    add_para(doc,
        "Trong các chỉ số trên, FAR và FRR đo hiệu năng của module nhận "
        "dạng (so khớp danh tính). APCER và BPCER đo hiệu năng của "
        "module phát hiện trình diện (PAD). Một hệ thống tốt phải đồng "
        "thời giữ FAR và APCER thấp, vì cả hai đều liên quan tới rủi ro "
        "bị tấn công, đồng thời giữ FRR và BPCER thấp để không gây "
        "phiền hà cho người dùng thật.",
        indent_first=1.0)

    add_image(doc, "fig_roc_threshold.png", width_cm=14,
              fig_num="2.2",
              caption="Đường cong ROC và quan hệ giữa FAR/FRR theo ngưỡng quyết định")

    # =================================================================
    # 2.5 Cac tieu chuan quoc te
    # =================================================================
    add_h2(doc, "2.5. Các tiêu chuẩn quốc tế liên quan")

    add_h3(doc, "2.5.1. ISO/IEC 30107 - Phát hiện tấn công trình diện")
    add_para(doc,
        "ISO/IEC 30107 là bộ tiêu chuẩn quốc tế dành riêng cho bài toán "
        "Presentation Attack Detection. Bộ tiêu chuẩn gồm ba phần: "
        "Phần 1 (2023) định nghĩa khung khái niệm, gồm thuật ngữ "
        "Presentation Attack Instrument (PAI), Bona-fide presentation, "
        "và mô hình ba lớp Subject - Capture - Comparison. Phần 2 "
        "(2017) quy định định dạng dữ liệu trao đổi giữa các module. "
        "Phần 3 (2023) định nghĩa cách đo APCER, BPCER và quy trình "
        "kiểm thử PAD. Đề tài tuân thủ Phần 1 trong khái niệm và Phần "
        "3 trong cách đo.",
        indent_first=1.0)

    add_h3(doc, "2.5.2. FIDO Biometric Component Certification")
    add_para(doc,
        "FIDO Alliance ban hành Biometric Component Certification "
        "Program từ 2018, với ba mức A, B, C. Mức B yêu cầu APCER "
        "không vượt quá 7 phần trăm và BPCER không vượt quá 5 phần "
        "trăm trên dataset chuẩn của FIDO. Mức C khắt khe hơn, yêu "
        "cầu APCER nhỏ hơn 2 phần trăm. Đề tài lấy mức B làm mục "
        "tiêu tham chiếu để đánh giá mô hình PAD đã huấn luyện.",
        indent_first=1.0)

    add_h3(doc, "2.5.3. NIST SP 800-63B - Authenticator Assurance Level")
    add_para(doc,
        "NIST Special Publication 800-63B định nghĩa ba mức Assurance "
        "(AAL1, AAL2, AAL3). Sinh trắc học được phép dùng làm yếu tố "
        "trong xác thực đa nhân tố nhưng không được dùng đơn lẻ ở "
        "AAL2 hoặc AAL3. Tài liệu nhấn mạnh sinh trắc học phải kết "
        "hợp với một yếu tố thuộc về người dùng (something you have) "
        "hoặc một yếu tố mà người dùng biết (something you know). "
        "Khuyến nghị này được đề tài áp dụng khi đề xuất kiến trúc "
        "Defense in Depth ở Chương 5.",
        indent_first=1.0)

    # =================================================================
    # 2.6 Cac moi de doa
    # =================================================================
    add_h2(doc, "2.6. Các mối đe dọa với hệ thống xác thực khuôn mặt")

    add_para(doc,
        "Bảng 2.2 tóm tắt các mối đe dọa thường gặp, từ mức độ phức "
        "tạp thấp (chỉ cần ảnh in) tới cao (deepfake video). Đề tài "
        "chỉ tập trung phân tích duy nhất nguy cơ Injection Attack "
        "(dòng được tô đậm trong bảng).",
        indent_first=1.0)

    add_table_caption(doc, "2.2", "Phân loại các mối đe dọa với hệ thống xác thực khuôn mặt")
    add_table(doc,
        ["Mối đe dọa", "Vector tấn công", "Mức độ phức tạp"],
        [
            ["Print Spoofing", "In ảnh nạn nhân lên giấy, đưa trước camera",
             "Thấp"],
            ["Phone/Screen Replay", "Hiển thị ảnh hoặc video trên điện thoại",
             "Trung bình"],
            ["Injection Attack",
             "Bỏ qua camera, gửi ảnh trực tiếp qua HTTP tới API",
             "Trung bình (đối tượng chính của đề tài)"],
            ["Mask Attack 3D",
             "Mặt nạ silicon hoặc resin in 3D với độ giống cao",
             "Cao"],
            ["Deepfake Video",
             "Video tổng hợp bằng GAN hoặc Diffusion Model",
             "Rất cao"],
            ["Adversarial Patch",
             "Nhiễu nhỏ trên ảnh để qua mặt mô hình PAD",
             "Rất cao"],
        ],
        widths=[4.5, 7.5, 4.0])

    add_para(doc,
        "Mỗi loại đe dọa cần biện pháp phòng vệ khác nhau, nhưng tất "
        "cả đều có chung điểm yếu là làm cho ảnh đầu vào không phải "
        "là khuôn mặt thật của chính chủ. Vì vậy, một mô hình PAD "
        "tốt sẽ đồng thời là biện pháp phòng vệ hữu hiệu cho nhiều "
        "loại đe dọa, không riêng Injection. Tuy nhiên, hiệu quả "
        "thực tế phụ thuộc vào dataset huấn luyện. Đề tài sẽ thấy "
        "rõ điều này trong Chương 4 và Chương 5.",
        indent_first=1.0)

    # =================================================================
    # 2.7 PAD va vi tri trong he thong
    # =================================================================
    add_h2(doc, "2.7. Phát hiện trình diện (PAD) và vị trí trong hệ thống")

    add_para(doc,
        "Theo ISO/IEC 30107-1, PAD là cơ chế phát hiện việc xuất hiện "
        "của một Presentation Attack Instrument trước cảm biến sinh "
        "trắc học. Trong các thuật ngữ, PAI là vật được dùng để giả "
        "mạo, có thể là ảnh in, ảnh hiển thị trên màn hình, mặt nạ, "
        "hoặc video phát lại. Khi nói tới Injection Attack, attacker "
        "cũng có thể coi là dùng một PAI logic, nghĩa là một bytestream "
        "đại diện ảnh giả thay vì một vật vật lý.",
        indent_first=1.0)

    add_para(doc,
        "Vị trí của PAD trong hệ thống được khuyến nghị đặt trước "
        "module trích đặc trưng. Nghĩa là, sau khi phát hiện được "
        "khuôn mặt trong ảnh, hệ thống chạy PAD trên vùng khuôn mặt "
        "đó để quyết định ảnh có phải là khuôn mặt thật hay không. "
        "Nếu PAD trả ra fake, hệ thống lập tức từ chối, không tốn chi "
        "phí cho bước trích đặc trưng vốn đắt hơn nhiều. Đây cũng là "
        "thiết kế được dùng trong Server Secured của đề tài.",
        indent_first=1.0)

    add_h3(doc, "2.7.1. Phân loại các phương pháp PAD")
    add_bullet(doc,
        "Phương pháp dựa trên kết cấu (texture-based): phân tích các "
        "đặc trưng nhỏ như hạt nhiễu, vệt moire, độ phản xạ. Thuật "
        "toán đại diện gồm LBP, BSIF, Color Texture Analysis.")
    add_bullet(doc,
        "Phương pháp dựa trên chuyển động (motion-based): phân tích "
        "chuyển động đầu, mắt, miệng theo thời gian; chỉ áp dụng "
        "được khi có chuỗi nhiều khung hình.")
    add_bullet(doc,
        "Phương pháp dựa trên Deep Learning: dùng CNN học trực tiếp "
        "đặc trưng phân biệt thật/giả từ dữ liệu. Đây là phương pháp "
        "được lựa chọn cho đề tài, cụ thể là MobileNetV2 với Transfer "
        "Learning.")
    add_bullet(doc,
        "Phương pháp đa cảm biến (multi-modal): kết hợp ảnh RGB với "
        "ảnh hồng ngoại, ảnh chiều sâu hoặc các sóng tần số khác. "
        "Hiệu quả cao nhất nhưng yêu cầu phần cứng đặc thù.")

    add_para(doc,
        "Lý do đề tài chọn Deep Learning vì đây là cách tiếp cận đạt "
        "hiệu năng tốt nhất trên các benchmark chuẩn (CASIA-FASD, "
        "Replay-Attack, OULU-NPU) và phù hợp với phần cứng phổ thông "
        "(CPU, không yêu cầu cảm biến đặc thù). Chi tiết về kiến "
        "trúc CNN và quá trình huấn luyện sẽ được trình bày trong "
        "Chương 4.",
        indent_first=1.0)

    # =================================================================
    # 2.8 Tong ket
    # =================================================================
    add_h2(doc, "2.8. Tổng kết chương")

    add_para(doc,
        "Chương 2 đã trình bày các kiến thức nền tảng về sinh trắc học "
        "khuôn mặt, gồm khái niệm và phân loại, kiến trúc bốn module "
        "của một hệ thống xác thực, vai trò của thư viện dlib và "
        "face_recognition trong việc trích vector embedding 128 chiều, "
        "các chỉ số đánh giá FAR/FRR/APCER/BPCER, các tiêu chuẩn "
        "ISO/IEC 30107 và FIDO, các mối đe dọa thường gặp với trọng "
        "tâm Injection, và vị trí của PAD trong hệ thống. Đây là cơ "
        "sở để Chương 3 phân tích chi tiết kịch bản tấn công Injection "
        "trên Server Vulnerable, từ đó tạo nhu cầu cụ thể cho việc "
        "huấn luyện mô hình Machine Learning ở Chương 4.",
        indent_first=1.0)

    add_page_break(doc)

# -*- coding: utf-8 -*-
"""_v3_chapter1.py - Chuong 1: Tong quan de tai.

Tap trung: gioi thieu de tai, muc tieu, doi tuong, pham vi, phuong phap.
Khong em-dash, khong en-dash.
"""

from _report_core import (
    add_h1, add_h2, add_h3, add_para, add_bullet,
    add_image, add_table, add_table_caption, add_page_break,
)


def build_chapter1(doc):
    add_h1(doc, "CHƯƠNG 1. TỔNG QUAN ĐỀ TÀI")

    add_para(doc,
        "Chương 1 trình bày bối cảnh dẫn tới đề tài, mục tiêu và phạm vi "
        "nghiên cứu, phương pháp tiếp cận, đóng góp dự kiến và bố cục báo "
        "cáo. Chương này đặt khung sườn chung cho toàn bộ các chương kỹ "
        "thuật phía sau, bao gồm cơ sở lý thuyết về sinh trắc học, kịch bản "
        "tấn công Injection, quá trình huấn luyện mô hình Machine Learning "
        "và việc tích hợp mô hình vào Server Secured.",
        indent_first=1.0)

    # =================================================================
    # 1.1 Ly do chon de tai
    # =================================================================
    add_h2(doc, "1.1. Lý do chọn đề tài")

    add_para(doc,
        "Trong hơn một thập kỷ trở lại đây, xác thực sinh trắc học "
        "(biometric authentication) đã chuyển từ phòng thí nghiệm ra đời "
        "sống thường ngày. Từ mở khóa điện thoại bằng vân tay, đăng nhập "
        "ứng dụng ngân hàng bằng khuôn mặt, kiểm soát ra vào tòa nhà bằng "
        "mống mắt cho tới định danh điện tử công dân, sinh trắc học đã "
        "trở thành phương thức xác thực phổ biến không kém mật khẩu "
        "truyền thống. Theo báo cáo của FIDO Alliance năm 2024, trên 60 "
        "phần trăm người dùng smartphone tại châu Á đang dùng khuôn mặt "
        "hoặc vân tay làm phương thức đăng nhập chính, vượt cả mã PIN và "
        "mật khẩu.",
        indent_first=1.0)

    add_para(doc,
        "Sự phổ biến nhanh chóng đó kéo theo một bề mặt tấn công cũng mở "
        "rộng tương ứng. Khác với mật khẩu, dữ liệu sinh trắc học một khi "
        "đã bị lộ sẽ không thể thay đổi, vì khuôn mặt và vân tay của một "
        "người là duy nhất và bất biến. Một khi attacker thu thập được "
        "ảnh khuôn mặt nạn nhân (qua mạng xã hội, chụp lén, hay rò rỉ cơ "
        "sở dữ liệu), họ có thể tái sử dụng dữ liệu đó để giả mạo trên "
        "nhiều hệ thống khác nhau. Đây là điểm then chốt khiến bảo mật "
        "sinh trắc học trở thành chủ đề được giới nghiên cứu, công nghiệp "
        "và cơ quan tiêu chuẩn quan tâm hàng đầu.",
        indent_first=1.0)

    add_para(doc,
        "Trong các loại tấn công vào hệ thống xác thực khuôn mặt, "
        "Injection Attack được đánh giá là mối đe dọa nghiêm trọng nhất ở "
        "lớp ứng dụng. Khác với tấn công trình diện (presentation attack) "
        "đòi hỏi phải có vật chứa và phải đứng trước camera, Injection "
        "Attack bỏ qua hoàn toàn camera vật lý, gửi thẳng ảnh khuôn mặt "
        "qua HTTP tới endpoint xác thực. Nếu hệ thống không có biện pháp "
        "phát hiện trình diện (Presentation Attack Detection, PAD), gần "
        "như mọi yêu cầu Injection đều thành công. Đây cũng là kịch bản "
        "tấn công duy nhất được đề tài phân tích sâu, với mục đích thấy "
        "rõ ranh giới giữa hệ thống có và không có Machine Learning hỗ "
        "trợ phòng vệ.",
        indent_first=1.0)

    add_para(doc,
        "Để chống lại lớp tấn công này, hướng tiếp cận hiện đại nhất là "
        "sử dụng Machine Learning, cụ thể là mạng nơ-ron tích chập "
        "(Convolutional Neural Network, CNN) được huấn luyện riêng để "
        "phân biệt ảnh khuôn mặt thật với ảnh khuôn mặt giả mạo. Quá "
        "trình huấn luyện chính là phần kỹ thuật xương sống của đề tài: "
        "thu thập dữ liệu, thiết kế kiến trúc mô hình, áp dụng Transfer "
        "Learning trên MobileNetV2, fine-tune theo hai pha và đánh giá "
        "bằng các chỉ số chuẩn ISO/IEC 30107-3. Sản phẩm cuối cùng là "
        "một mô hình PAD nhỏ gọn được tích hợp vào Server Secured để "
        "chặn được Injection Attack ngay tại tầng ứng dụng.",
        indent_first=1.0)

    # =================================================================
    # 1.2 Muc tieu de tai
    # =================================================================
    add_h2(doc, "1.2. Mục tiêu của đề tài")

    add_h3(doc, "1.2.1. Mục tiêu tổng quát")
    add_para(doc,
        "Đề tài hướng tới việc xây dựng một mô hình tham chiếu hoàn "
        "chỉnh, có thể tái sử dụng cho mục đích giảng dạy và nghiên cứu, "
        "minh họa cách thức một hệ thống xác thực sinh trắc học khuôn "
        "mặt có thể bị tấn công Injection và cách Machine Learning đóng "
        "vai trò là biện pháp phòng vệ chính. Toàn bộ vòng đời từ phân "
        "tích lỗ hổng, thực hiện tấn công, huấn luyện mô hình và tích "
        "hợp mô hình đều được trình bày kèm mã nguồn, dữ liệu đo và "
        "kết quả định lượng để đảm bảo tính tái lập.",
        indent_first=1.0)

    add_h3(doc, "1.2.2. Mục tiêu cụ thể")
    add_bullet(doc,
        "Hệ thống hóa cơ sở lý thuyết về sinh trắc học khuôn mặt, từ "
        "nguyên lý trích đặc trưng dlib HOG và mạng ResNet 128 chiều, "
        "tới các chỉ số FAR/FRR và tiêu chuẩn ISO/IEC 30107.")
    add_bullet(doc,
        "Triển khai một hệ thống Server Vulnerable bằng Flask và "
        "face_recognition, đầy đủ ba endpoint /register, /authenticate, "
        "/users, có giao diện web hoàn chỉnh.")
    add_bullet(doc,
        "Phân tích chi tiết kịch bản tấn công Injection, gồm động cơ, "
        "công cụ, payload, bước thực thi và kết quả; đo được tỷ lệ "
        "thành công trên Server Vulnerable.")
    add_bullet(doc,
        "Trình bày cơ sở lý thuyết Machine Learning có liên quan: học "
        "có giám sát, CNN, Transfer Learning, Data Augmentation, các "
        "kỹ thuật regularization như Dropout và Batch Normalization.")
    add_bullet(doc,
        "Xây dựng pipeline huấn luyện hoàn chỉnh từ thu thập dataset, "
        "tiền xử lý, thiết kế mô hình MobileNetV2 với classifier head "
        "tùy biến, huấn luyện hai pha (freeze và fine-tune), đến đánh "
        "giá bằng accuracy, confusion matrix và ROC.")
    add_bullet(doc,
        "Tích hợp mô hình vào Server Secured: viết wrapper "
        "LivenessPredictor, chèn bước kiểm tra liveness vào trước bước "
        "so khớp khuôn mặt, đo lại tỷ lệ chặn Injection.")
    add_bullet(doc,
        "Đánh giá định lượng theo ISO/IEC 30107-3: APCER, BPCER, EER; "
        "so sánh trước và sau khi tích hợp PAD; chỉ ra hạn chế và "
        "đề xuất hướng phát triển.")

    # =================================================================
    # 1.3 Doi tuong va pham vi
    # =================================================================
    add_h2(doc, "1.3. Đối tượng và phạm vi nghiên cứu")

    add_h3(doc, "1.3.1. Đối tượng nghiên cứu")
    add_para(doc,
        "Đối tượng nghiên cứu của đề tài là hệ thống xác thực sinh trắc "
        "học khuôn mặt được triển khai dưới dạng dịch vụ web. Cụ thể, "
        "đối tượng gồm ba cấu phần liên quan trực tiếp tới bài toán bảo "
        "mật: (1) bộ trích đặc trưng khuôn mặt 128 chiều dựa trên dlib "
        "ResNet và thư viện face_recognition; (2) kịch bản tấn công "
        "Injection Attack, là hình thức gửi ảnh khuôn mặt giả mạo trực "
        "tiếp tới endpoint xác thực qua HTTP; (3) mô hình Machine "
        "Learning phát hiện trình diện được huấn luyện riêng cho bài "
        "toán này, có vai trò làm Detection Engine tích hợp vào Server "
        "Secured.",
        indent_first=1.0)

    add_h3(doc, "1.3.2. Phạm vi nghiên cứu")
    add_para(doc,
        "Đề tài giới hạn ở chế độ xác thực một-một (1:1 verification) "
        "trên ảnh tĩnh thu từ webcam, sử dụng đặc trưng RGB hai chiều "
        "do hạn chế phần cứng. Các hướng mở rộng sang đặc trưng thời "
        "gian, ảnh hồng ngoại, ảnh chiều sâu hoặc tấn công deepfake "
        "video được đề cập như hướng phát triển trong Chương 5.",
        indent_first=1.0)

    add_para(doc,
        "Về kịch bản tấn công, đề tài chỉ phân tích sâu duy nhất một "
        "kịch bản là Injection Attack. Lý do của việc giới hạn này gồm "
        "ba điểm. Thứ nhất, Injection là kịch bản nguy hiểm nhất ở "
        "tầng ứng dụng vì attacker không cần camera vật lý, có thể "
        "tự động hóa và mở rộng quy mô dễ dàng. Thứ hai, việc tập "
        "trung vào một kịch bản giúp nội dung phân tích đạt độ sâu cần "
        "thiết, từ động cơ, payload, công cụ, đến quan sát hành vi của "
        "Server. Thứ ba, các biện pháp phòng vệ chống Injection (PAD "
        "Engine bằng Machine Learning) cũng là các biện pháp đa năng "
        "có thể tái dùng cho các kịch bản khác như tấn công trình diện "
        "ảnh in hay điện thoại.",
        indent_first=1.0)

    add_para(doc,
        "Về Machine Learning, đề tài tập trung vào kiến trúc CNN nhẹ "
        "MobileNetV2 với Transfer Learning từ ImageNet, vì đây là kiến "
        "trúc đạt hiệu năng cao trên CPU mà vẫn nhỏ gọn, phù hợp triển "
        "khai cùng một máy chủ Flask. Các kiến trúc lớn hơn như "
        "ResNet-50 hay EfficientNet-B3 được đề cập làm tham chiếu "
        "nhưng không huấn luyện thực sự trong khuôn khổ đề tài.",
        indent_first=1.0)

    # =================================================================
    # 1.4 Phuong phap nghien cuu
    # =================================================================
    add_h2(doc, "1.4. Phương pháp nghiên cứu")

    add_para(doc,
        "Đề tài kết hợp ba phương pháp nghiên cứu: nghiên cứu tài "
        "liệu, nghiên cứu thực nghiệm và phương pháp đối sánh.",
        indent_first=1.0)

    add_h3(doc, "1.4.1. Nghiên cứu tài liệu")
    add_para(doc,
        "Tổng hợp các tiêu chuẩn quốc tế ISO/IEC 30107-1 và 30107-3, "
        "khuyến nghị của FIDO Alliance về Biometric Component "
        "Certification, hướng dẫn NIST SP 800-63B về cấp đảm bảo xác "
        "thực, OWASP Top 10 và OWASP API Security Top 10. Bên cạnh "
        "đó, đề tài nghiên cứu các bài báo CVPR, ICCV về Face Anti-"
        "Spoofing và các tài liệu kỹ thuật của thư viện face_recognition, "
        "dlib, PyTorch và torchvision.",
        indent_first=1.0)

    add_h3(doc, "1.4.2. Nghiên cứu thực nghiệm")
    add_para(doc,
        "Đề tài xây dựng một hệ thống lab hoàn chỉnh, gồm hai phiên bản "
        "Server Vulnerable và Server Secured, một bộ công cụ tấn công "
        "Injection, một pipeline huấn luyện Machine Learning và một bộ "
        "kịch bản đánh giá tự động. Mọi số liệu trong báo cáo đều "
        "được thu trên hệ thống lab này để đảm bảo tính minh bạch và "
        "khả năng tái lập.",
        indent_first=1.0)

    add_h3(doc, "1.4.3. Phương pháp đối sánh")
    add_para(doc,
        "Mọi chỉ số đo được đều có hai cột giá trị tương ứng với hai "
        "phiên bản Server (Vulnerable và Secured). Việc đối sánh này "
        "trực quan hóa hiệu quả của Machine Learning trong vai trò "
        "Detection Engine, cho phép định lượng đóng góp thực tế của "
        "PAD Engine vào tổng thể bảo mật của hệ thống.",
        indent_first=1.0)

    # =================================================================
    # 1.5 Y nghia khoa hoc va thuc tien
    # =================================================================
    add_h2(doc, "1.5. Ý nghĩa khoa học và thực tiễn")

    add_h3(doc, "1.5.1. Ý nghĩa khoa học")
    add_para(doc,
        "Đề tài góp phần củng cố cách tiếp cận coi PAD là một bài toán "
        "Machine Learning độc lập với bài toán nhận dạng. Bằng việc "
        "tách bạch hai bộ phận, có thể đánh giá chính xác hiệu quả của "
        "từng lớp và thiết kế các biện pháp phù hợp cho từng nguy cơ. "
        "Kết quả cũng minh họa rằng một mô hình CNN nhỏ gọn như "
        "MobileNetV2 đủ để đạt EER dưới 5 phần trăm trên dataset quy "
        "mô vài trăm ảnh, mở ra khả năng ứng dụng cho các thiết bị "
        "biên (edge device) có tài nguyên hạn chế.",
        indent_first=1.0)

    add_h3(doc, "1.5.2. Ý nghĩa thực tiễn")
    add_para(doc,
        "Bộ tài liệu, mã nguồn và mô hình đã huấn luyện có thể được "
        "tái sử dụng làm material giảng dạy cho các môn An toàn Hệ "
        "thống thông tin và Học máy ở bậc đại học. Sinh viên ngành An "
        "toàn thông tin có thể chạy lại Injection Attack ngay trên "
        "máy cá nhân, quan sát Server từ chối ảnh giả nhờ Machine "
        "Learning, từ đó hình dung cụ thể các khái niệm vốn rất trừu "
        "tượng trong sách giáo khoa.",
        indent_first=1.0)

    # =================================================================
    # 1.6 Bo cuc bao cao
    # =================================================================
    add_h2(doc, "1.6. Bố cục báo cáo")

    add_para(doc,
        "Báo cáo gồm năm chương kỹ thuật, sắp xếp theo trình tự logic "
        "của một dự án Detection Engineering: hiểu đối tượng, hiểu kẻ "
        "tấn công, học cách huấn luyện mô hình, tích hợp mô hình vào "
        "hệ thống và đánh giá kết quả.",
        indent_first=1.0)

    add_bullet(doc,
        "Chương 1 (chương hiện tại) đặt vấn đề và xác lập khung sườn "
        "tổng thể.")
    add_bullet(doc,
        "Chương 2 trình bày cơ sở lý thuyết về sinh trắc học khuôn "
        "mặt, từ định nghĩa, phân loại, các đặc trưng dlib và 128-d "
        "encoding, các chỉ số FAR/FRR, EER cho tới tiêu chuẩn ISO/IEC "
        "30107 và FIDO.")
    add_bullet(doc,
        "Chương 3 phân tích kịch bản tấn công Injection: từ Threat "
        "Model, mô tả công cụ và payload, kịch bản thực thi, kết quả "
        "đo trên Server Vulnerable cho tới các bài học rút ra.")
    add_bullet(doc,
        "Chương 4 là chương trọng tâm: trình bày toàn bộ quá trình "
        "Machine Learning. Từ cơ sở lý thuyết CNN và Transfer "
        "Learning, dataset thu thập 200 ảnh thật và 200 ảnh giả, "
        "augmentation, kiến trúc MobileNetV2 với classifier head tùy "
        "biến, huấn luyện hai pha freeze và fine-tune, đến đánh giá "
        "accuracy, ROC, confusion matrix.")
    add_bullet(doc,
        "Chương 5 trình bày cách tích hợp mô hình đã huấn luyện vào "
        "Server Secured, đo lại Injection Attack sau khi tích hợp, "
        "phân tích chi phí trễ và tỷ lệ false positive, hạn chế và "
        "hướng phát triển.")

    add_para(doc,
        "Sau Chương 5 là phần Tài liệu tham khảo theo định dạng [n]. "
        "Các nguồn từ tiêu chuẩn ISO, FIDO, NIST, OWASP, MITRE và các "
        "công bố CVPR, ICCV được đưa vào danh mục để hỗ trợ kiểm "
        "chứng các luận điểm trong báo cáo.",
        indent_first=1.0)

    add_page_break(doc)

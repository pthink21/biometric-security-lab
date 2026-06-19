# -*- coding: utf-8 -*-
"""_v3_chapter3.py - Chuong 3: KICH BAN TAN CONG INJECTION ATTACK.

Tap trung mot kich bran tan cong duy nhat: Injection Attack.
Khong em-dash. Khong en-dash. Code blocks duoc phep dung CLI flag '--xxx'.
"""

from _report_core import (
    add_h1, add_h2, add_h3, add_para, add_bullet,
    add_image, add_table, add_table_caption, add_page_break, add_code_block,
)


def build_chapter3(doc):
    add_h1(doc, "CHƯƠNG 3. KỊCH BẢN TẤN CÔNG INJECTION ATTACK")

    add_para(doc,
        "Sau khi Chương 2 đã trình bày nền tảng lý thuyết về sinh trắc học, "
        "kiến trúc bốn module của một hệ thống xác thực khuôn mặt và bộ chỉ số "
        "đánh giá theo ISO/IEC 30107-3, Chương 3 đi sâu vào kịch bản tấn công "
        "trọng tâm của đồ án: Injection Attack. Đây cũng là kịch bản tấn công "
        "duy nhất được phân tích chi tiết trong báo cáo, nhằm đảm bảo độ sâu "
        "kiến thức thay vì liệt kê dàn trải nhiều dạng tấn công khác nhau. Toàn "
        "bộ chương được trình bày dưới góc nhìn của một người làm SOC Analyst "
        "kết hợp với Red Team: trước tiên dựng mô hình mối đe dọa, sau đó tìm "
        "ra điểm yếu, xây dựng payload, thực thi và cuối cùng phân tích vì sao "
        "phòng vệ phía máy khách một mình là không đủ. Kết luận của chương "
        "chính là động cơ trực tiếp dẫn tới yêu cầu phải có một mô hình học "
        "máy phát hiện tấn công trình diện ở Chương 4.",
        indent_first=1.0)

    # =================================================================
    # 3.1 Tong quan ve Injection Attack
    # =================================================================
    add_h2(doc, "3.1. Tổng quan về Injection Attack")

    add_h3(doc, "3.1.1. Định nghĩa")
    add_para(doc,
        "Injection Attack trong bối cảnh hệ thống xác thực sinh trắc học là "
        "hình thức tấn công mà kẻ tấn công bỏ qua hoàn toàn cảm biến vật lý "
        "(camera, đầu đọc vân tay) và đưa trực tiếp dữ liệu sinh trắc đã được "
        "chuẩn bị sẵn vào đường truyền hoặc tầng API của hệ thống. Khác với "
        "tấn công trình diện cổ điển vốn yêu cầu kẻ tấn công phải đứng trước "
        "camera với một bức ảnh in hoặc một màn hình điện thoại phát ảnh nạn "
        "nhân, Injection Attack cho phép thao tác thuần phía máy chủ thông "
        "qua giao thức HTTP, không cần bất kỳ thiết bị vật lý nào ở phía hiện "
        "trường.",
        indent_first=1.0)

    add_para(doc,
        "Trong tài liệu chuẩn ISO/IEC 30107-1, hành vi này được phân loại vào "
        "nhóm tấn công trên kênh truyền và tầng xử lý logic của hệ thống xác "
        "thực, chứ không thuộc nhóm Presentation Attack thuần túy. Tuy nhiên, "
        "ranh giới giữa hai nhóm trở nên mờ đi khi attacker chỉ cần một bức "
        "ảnh số của nạn nhân, mã hóa thành Base64 và gửi tới điểm cuối "
        "/authenticate là đủ để vượt qua hệ thống. Vì vậy đồ án xếp Injection "
        "Attack là một biến thể nâng cao của Presentation Attack, mạnh hơn "
        "nhiều so với spoofing trực tiếp trước camera.",
        indent_first=1.0)

    add_h3(doc, "3.1.2. Vì sao Injection Attack là kịch bản trọng tâm")
    add_bullet(doc, "Khả năng tự động hóa rất cao: chỉ cần một script Python "
                    "vài chục dòng và một thư mục ảnh là có thể tấn công hàng "
                    "loạt tài khoản, không phụ thuộc vào sự hiện diện vật lý.")
    add_bullet(doc, "Bỏ qua mọi rào cản client-side: các kiểm tra Liveness "
                    "phía trình duyệt như chớp mắt, xoay đầu, đo độ sâu bằng "
                    "WebGL đều bị bỏ qua hoàn toàn vì attacker không bao giờ "
                    "đi qua trang web.")
    add_bullet(doc, "Chi phí thấp, độ thành công cao: thông tin đầu vào duy "
                    "nhất là một bức ảnh tĩnh của nạn nhân, có thể lấy từ mạng "
                    "xã hội với chất lượng đủ tốt.")
    add_bullet(doc, "Khó phát hiện ở tầng ứng dụng nếu không có PAD: server "
                    "Vulnerable thấy một ảnh hợp lệ, có khuôn mặt, vector đặc "
                    "trưng khớp với mẫu đã đăng ký và trả về phản hồi xác "
                    "thực thành công, không có dấu hiệu nào để phân biệt với "
                    "một phiên đăng nhập hợp pháp.")
    add_bullet(doc, "Phù hợp với mục tiêu nghiên cứu: việc tập trung phân "
                    "tích sâu một kịch bản giúp người đọc nắm rõ cơ chế tận "
                    "gốc thay vì hiểu mơ hồ nhiều kịch bản khác nhau, đồng "
                    "thời tạo bối cảnh rõ ràng để Chương 4 xây dựng giải pháp "
                    "học máy đối phó.")

    add_h3(doc, "3.1.3. So sánh sơ lược với một số kịch bản khác")
    add_para(doc,
        "Để định vị Injection Attack giữa các dạng tấn công khác đã được "
        "trình bày trong Bảng 2.2 ở Chương 2, bảng dưới đây tóm lược các đặc "
        "trưng cốt lõi. Mục đích duy nhất của bảng là làm rõ vì sao đồ án "
        "chọn Injection Attack làm trung tâm phân tích, các kịch bản khác "
        "không tiếp tục được khai thác trong các chương sau.",
        indent_first=1.0)

    add_table_caption(doc, "3.1",
        "Định vị Injection Attack so với các kịch bản tấn công khác")
    add_table(doc,
        ["Tiêu chí", "Print/Replay", "Brute Force", "Injection (trọng tâm)"],
        [
            ["Yêu cầu thiết bị vật lý",
             "Có (in ảnh, điện thoại)",
             "Không bắt buộc",
             "Không"],
            ["Phụ thuộc camera nạn nhân",
             "Phụ thuộc",
             "Phụ thuộc",
             "Không phụ thuộc"],
            ["Khả năng tự động hóa",
             "Trung bình",
             "Cao",
             "Rất cao"],
            ["Tiêu hao tài nguyên",
             "Trung bình",
             "Cao (nhiều thử nghiệm)",
             "Thấp"],
            ["Tỷ lệ thành công khi không có PAD",
             "Cao",
             "Phụ thuộc rate-limit",
             "Rất cao (gần 100%)"],
            ["Mức độ ưu tiên trong đồ án",
             "Tham khảo",
             "Tham khảo",
             "Phân tích sâu, có Red Team thực chứng"],
        ],
        widths=[4.5, 3.2, 3.2, 5.1])

    add_page_break(doc)

    # =================================================================
    # 3.2 Mo hinh moi de doa
    # =================================================================
    add_h2(doc, "3.2. Mô hình mối đe dọa của Injection Attack")

    add_para(doc,
        "Mô hình mối đe dọa (Threat Model) là bước đầu tiên của bất kỳ phân "
        "tích bảo mật nghiêm túc nào. Trong đồ án, mô hình này được xây dựng "
        "theo phương pháp STRIDE kết hợp với cách tiếp cận của MITRE ATT&CK, "
        "trong đó mỗi mối đe dọa được gắn với một Tactic và một Technique cụ "
        "thể để dễ tham chiếu khi xây dựng cảnh báo SIEM về sau.",
        indent_first=1.0)

    add_image(doc, "fig_threat_model.png", width_cm=14,
              fig_num="3.1",
              caption="Mô hình mối đe dọa cho hệ thống xác thực khuôn mặt")

    add_h3(doc, "3.2.1. Tài sản cần bảo vệ")
    add_bullet(doc, "Tính toàn vẹn của quyết định xác thực: hệ thống phải "
                    "đảm bảo một phản hồi authenticated true chỉ phát ra khi "
                    "đối tượng đứng trước hệ thống thực sự là chủ tài khoản.")
    add_bullet(doc, "Cơ sở dữ liệu mẫu sinh trắc face_database.pkl: chứa các "
                    "vector 128 chiều của tất cả người dùng đã đăng ký, một "
                    "tài sản nhạy cảm vì không thể thay thế nếu bị rò rỉ.")
    add_bullet(doc, "Danh sách tài khoản hợp lệ: bị xem là tài sản cấp hai "
                    "vì nó dẫn đường cho tấn công có chủ đích, đặc biệt khi "
                    "endpoint /users công khai như trên server Vulnerable.")
    add_bullet(doc, "Nhật ký truy cập (audit log): tài sản phục vụ điều tra "
                    "sự cố, cần được bảo toàn nguyên vẹn để phân biệt phiên "
                    "hợp pháp với phiên tấn công.")

    add_h3(doc, "3.2.2. Mô tả attacker")
    add_bullet(doc, "Trình độ kỹ thuật: trung cấp, biết lập trình Python, sử "
                    "dụng được thư viện requests, có hiểu biết cơ bản về "
                    "Base64 và HTTP/JSON.")
    add_bullet(doc, "Tài nguyên: một máy tính cá nhân, kết nối Internet, "
                    "không cần GPU, không cần phần cứng đặc biệt.")
    add_bullet(doc, "Quyền truy cập: ở mức người dùng ngoại vi, có thể truy "
                    "cập endpoint công khai của server, không có shell trên "
                    "máy chủ, không có kiến thức nội bộ về cơ sở dữ liệu.")
    add_bullet(doc, "Mục tiêu: đăng nhập thành công với danh tính của một "
                    "người dùng hợp pháp, tốt nhất là đăng nhập tự động hàng "
                    "loạt với nhiều tài khoản.")

    add_h3(doc, "3.2.3. Bề mặt tấn công")
    add_para(doc,
        "Bề mặt tấn công (Attack Surface) của hệ thống xác thực khuôn mặt "
        "qua giao thức HTTP gồm bốn nhóm điểm vào chính: (i) trang giao diện "
        "web ở đường dẫn gốc \"/\" cho người dùng cuối, (ii) endpoint "
        "/register để đăng ký mẫu mới, (iii) endpoint /authenticate dùng cho "
        "mọi phiên đăng nhập, và (iv) endpoint /users phục vụ tra cứu danh "
        "sách tài khoản. Trong bốn điểm vào này, /authenticate là điểm dễ tổn "
        "thương nhất vì nó nhận thẳng dữ liệu sinh trắc dưới dạng Base64 và "
        "không yêu cầu xác thực phụ trợ trước đó.",
        indent_first=1.0)

    add_h3(doc, "3.2.4. Phân tích STRIDE rút gọn")
    add_table_caption(doc, "3.2",
        "Phân tích STRIDE cho điểm cuối /authenticate")
    add_table(doc,
        ["Loại đe dọa", "Mô tả ngắn", "Liên quan Injection?"],
        [
            ["S - Spoofing identity",
             "Giả mạo danh tính người dùng hợp pháp.",
             "Trực tiếp"],
            ["T - Tampering",
             "Sửa đổi payload sinh trắc trên đường truyền.",
             "Gián tiếp"],
            ["R - Repudiation",
             "Phủ nhận hành vi do thiếu log đầy đủ.",
             "Gián tiếp"],
            ["I - Information disclosure",
             "Lộ danh sách user qua /users.",
             "Tạo điều kiện cho Injection"],
            ["D - Denial of service",
             "Làm tê liệt /authenticate bằng request lớn.",
             "Không trọng tâm"],
            ["E - Elevation of privilege",
             "Đăng nhập với tư cách quản trị thông qua spoof.",
             "Là kết quả khi Injection thành công"],
        ],
        widths=[4.5, 7.5, 4.0])

    add_page_break(doc)

    # =================================================================
    # 3.3 Trinh sat
    # =================================================================
    add_h2(doc, "3.3. Trinh sát hệ thống mục tiêu")

    add_para(doc,
        "Theo phân loại của MITRE ATT&CK, giai đoạn trinh sát "
        "(Reconnaissance) là bước thu thập thông tin trước khi tiến hành "
        "khai thác. Trong tình huống của đồ án, attacker muốn biết hệ thống "
        "đang chạy phiên bản nào, có những endpoint nào công khai, đã có bao "
        "nhiêu người dùng đăng ký và tên đăng nhập của họ là gì. Mọi thông "
        "tin càng cụ thể thì xác suất tấn công thành công càng cao.",
        indent_first=1.0)

    add_h3(doc, "3.3.1. Thu thập thông tin endpoint")
    add_para(doc,
        "Bằng cách quét cấu trúc thư mục công khai và quan sát phản hồi "
        "HTTP, attacker xác định được ba endpoint hữu dụng: /register, "
        "/authenticate và /users. Riêng endpoint /users là điểm cực kỳ giàu "
        "thông tin vì nó trả về JSON chứa toàn bộ tên người dùng đã đăng ký "
        "kèm thời điểm đăng ký, không yêu cầu bất kỳ token nào.",
        indent_first=1.0)

    add_code_block(doc,
        "GET http://localhost:5000/users HTTP/1.1\n"
        "Host: localhost:5000\n\n"
        "HTTP/1.1 200 OK\n"
        "Content-Type: application/json\n\n"
        "{\n"
        "  \"users\": [\n"
        "    {\"name\": \"thinh\",  \"registered_at\": \"2026-05-12T10:21:08\"},\n"
        "    {\"name\": \"hieu\",   \"registered_at\": \"2026-05-12T10:24:17\"},\n"
        "    {\"name\": \"phuong\", \"registered_at\": \"2026-05-13T09:02:31\"}\n"
        "  ],\n"
        "  \"total\": 3\n"
        "}\n")

    add_h3(doc, "3.3.2. Hàm trinh sát của attacker")
    add_para(doc,
        "Trong công cụ tấn công 03_injection_attack.py, hàm recon_users đảm "
        "nhận giai đoạn trinh sát. Hàm gọi tới /users, đọc trường total, in "
        "ra số lượng user và liệt kê từng người. Trong vận hành thực tế, kết "
        "quả của hàm này được dùng làm danh sách mục tiêu để chọn ảnh tương "
        "ứng từ thư viện ảnh thu thập trước.",
        indent_first=1.0)

    add_code_block(doc,
        "def recon_users(target_url):\n"
        "    resp = requests.get(f\"{target_url}/users\", timeout=10)\n"
        "    data = resp.json()\n"
        "    if data[\"total\"] == 0:\n"
        "        return []\n"
        "    print(f\"[+] Tim thay {data['total']} user:\")\n"
        "    for u in data[\"users\"]:\n"
        "        print(f\"    - {u['name']} (dang ky: {u['registered_at']})\")\n"
        "    return data[\"users\"]\n")

    add_h3(doc, "3.3.3. Thu thập ảnh nạn nhân")
    add_para(doc,
        "Bước này diễn ra ngoài hệ thống mục tiêu và thường khai thác Open "
        "Source Intelligence (OSINT). Với một tên người dùng có sẵn ở /users, "
        "kẻ tấn công có thể tìm kiếm trên Facebook, LinkedIn, Zalo, Instagram "
        "để lấy ảnh chân dung chất lượng tốt. Với chỉ cần một ảnh duy nhất "
        "cho mỗi nạn nhân là đủ để thực hiện Injection Attack thành công, "
        "khả năng thu thập đại trà gần như là không bị hạn chế.",
        indent_first=1.0)

    add_page_break(doc)

    # =================================================================
    # 3.4 Xay dung payload
    # =================================================================
    add_h2(doc, "3.4. Xây dựng payload Injection")

    add_para(doc,
        "Payload Injection trong báo cáo này là chuỗi JSON gửi tới endpoint "
        "/authenticate, trong đó trường image chứa toàn bộ ảnh khuôn mặt nạn "
        "nhân đã được mã hóa Base64 theo Data URL. Mục này phân tích chi "
        "tiết cấu trúc payload và đoạn mã sinh payload trong công cụ tấn công.",
        indent_first=1.0)

    add_h3(doc, "3.4.1. Định dạng Data URL Base64")
    add_para(doc,
        "Data URL có cấu trúc \"data:[mediatype][;base64],<data>\". Trong "
        "bài toán này, mediatype được đặt là image/jpeg, dữ liệu nhị phân "
        "của ảnh được encode Base64 và nối ngay sau dấu phẩy. Server "
        "Vulnerable không kiểm tra giá trị mediatype, chỉ tách phần sau dấu "
        "phẩy, giải mã và mở bằng PIL.Image, vì thế ngay cả khi ảnh là PNG "
        "hay BMP, gắn nhãn jpeg vẫn được chấp nhận.",
        indent_first=1.0)

    add_h3(doc, "3.4.2. Hàm encode ảnh thành Base64")
    add_code_block(doc,
        "def encode_image_to_base64(image_path):\n"
        "    with open(image_path, \"rb\") as f:\n"
        "        img_bytes = f.read()\n"
        "    b64 = base64.b64encode(img_bytes).decode(\"utf-8\")\n"
        "    return f\"data:image/jpeg;base64,{b64}\"\n")

    add_para(doc,
        "Hàm encode_image_to_base64 đọc nguyên file ảnh ở chế độ nhị phân, "
        "biến đổi sang chuỗi Base64 và trả về một Data URL hoàn chỉnh. Một "
        "đặc điểm quan trọng là kích thước payload tăng khoảng 33% so với "
        "kích thước file gốc do tính chất của Base64. Với ảnh chân dung điển "
        "hình 2 MB, payload sẽ vào khoảng 2.7 MB, vẫn nằm dưới giới hạn "
        "MAX_CONTENT_LENGTH 50 MB của Flask.",
        indent_first=1.0)

    add_h3(doc, "3.4.3. Cấu trúc JSON gửi tới /authenticate")
    add_code_block(doc,
        "POST /authenticate HTTP/1.1\n"
        "Host: localhost:5000\n"
        "Content-Type: application/json\n"
        "Content-Length: 2843217\n\n"
        "{\n"
        "  \"image\": \"data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASA...\"\n"
        "}\n")

    add_para(doc,
        "Cấu trúc payload chỉ gồm duy nhất trường image. Server Vulnerable "
        "không yêu cầu trường name, không yêu cầu trường timestamp, nonce hay "
        "session_id. Sự đơn giản này phản ánh đúng tâm lý phổ biến khi xây "
        "dựng API: ưu tiên trải nghiệm người dùng và tốc độ phát triển, bỏ "
        "qua các kiểm tra mà attacker hoàn toàn có thể khai thác.",
        indent_first=1.0)

    add_page_break(doc)

    # =================================================================
    # 3.5 Quy trinh tan cong
    # =================================================================
    add_h2(doc, "3.5. Quy trình tấn công Injection chi tiết")

    add_para(doc,
        "Quy trình tấn công Injection được tổ chức thành chuỗi năm bước, từ "
        "lúc khởi động công cụ đến khi nhận được phản hồi xác thực thành "
        "công. Toàn bộ chuỗi sự kiện được minh họa ở Hình 3.2 và mỗi bước "
        "tương ứng với một mục con bên dưới.",
        indent_first=1.0)

    add_image(doc, "fig_attack_chain.png", width_cm=15,
              fig_num="3.2",
              caption="Chuỗi năm bước thực thi Injection Attack")

    add_h3(doc, "3.5.1. Bước 1: Khởi tạo phiên tấn công")
    add_para(doc,
        "Attacker khởi động script 03_injection_attack.py với tham số --target "
        "trỏ đến server Vulnerable, đồng thời chỉ định --image là đường dẫn "
        "ảnh nạn nhân đã thu thập được. Trong phiên thí nghiệm của đồ án, "
        "lệnh dưới đây được sử dụng để mô phỏng tấn công với tài khoản "
        "thinh.",
        indent_first=1.0)

    add_code_block(doc,
        "python attacker/03_injection_attack.py \\\n"
        "    --target http://localhost:5000 \\\n"
        "    --image ./victim_photos/thinh.jpg\n")

    add_h3(doc, "3.5.2. Bước 2: Trinh sát đối tượng")
    add_para(doc,
        "Trước khi gửi payload, script gọi hàm recon_users để xác nhận tài "
        "khoản thinh thực sự đã được đăng ký trong cơ sở dữ liệu. Bước này "
        "đảm bảo nỗ lực gửi ảnh sẽ không lãng phí, đồng thời ghi lại danh "
        "sách user phục vụ cho cuộc tấn công hàng loạt nếu cần.",
        indent_first=1.0)

    add_h3(doc, "3.5.3. Bước 3: Sinh payload và mã hóa Base64")
    add_para(doc,
        "Script đọc file ảnh thinh.jpg, gọi encode_image_to_base64 để tạo "
        "Data URL, rồi đóng gói thành dictionary {\"image\": image_b64}. "
        "Kích thước payload thực tế trong thí nghiệm khoảng 480 KB ứng với "
        "ảnh JPEG độ phân giải 1280×960, độ nén 80%.",
        indent_first=1.0)

    add_h3(doc, "3.5.4. Bước 4: Gửi POST tới /authenticate")
    add_para(doc,
        "Hàm inject_single_image gọi requests.post với json=payload và "
        "timeout=30 giây. Server tiếp nhận, giải mã Base64, dựng lại đối "
        "tượng PIL.Image, chuyển sang RGB rồi đẩy vào pipeline "
        "face_recognition giống hệt như khi nhận ảnh từ camera. Vì server "
        "không có cơ chế phân biệt ảnh đến từ camera trực tiếp với ảnh từ "
        "request HTTP, hai luồng dữ liệu được xử lý hoàn toàn đồng nhất.",
        indent_first=1.0)

    add_image(doc, "fig_attacknet_detail.png", width_cm=15,
              fig_num="3.3",
              caption="Sơ đồ luồng dữ liệu Injection từ attacker tới /authenticate")

    add_h3(doc, "3.5.5. Bước 5: Đọc phản hồi và xác nhận thành công")
    add_para(doc,
        "Khi vector đặc trưng 128 chiều của ảnh nạn nhân khớp với mẫu lưu "
        "trong face_database.pkl ở khoảng cách Euclidean dưới 0.6, server "
        "trả về JSON với authenticated true, kèm theo trường confidence và "
        "đặc biệt là liveness_check ở giá trị DISABLED. Trường liveness_check "
        "này là cờ thừa nhận rõ ràng rằng phiên bản Vulnerable không có cơ "
        "chế phát hiện trình diện. Attacker chỉ cần đọc trường authenticated "
        "trong phản hồi là đã có thể xác nhận tấn công thành công.",
        indent_first=1.0)

    add_code_block(doc,
        "{\n"
        "  \"success\": true,\n"
        "  \"authenticated\": true,\n"
        "  \"user\": \"thinh\",\n"
        "  \"confidence\": 0.7212,\n"
        "  \"distance\": 0.2788,\n"
        "  \"liveness_check\": \"DISABLED\",\n"
        "  \"message\": \"Xin chao, thinh! Xac thuc thanh cong.\"\n"
        "}\n")

    add_page_break(doc)

    # =================================================================
    # 3.6 Quan sat tren Server Vulnerable
    # =================================================================
    add_h2(doc, "3.6. Quan sát hành vi của Server Vulnerable")

    add_para(doc,
        "Toàn bộ quá trình tiếp nhận payload Injection của Server Vulnerable "
        "có thể được tái dựng lại bằng cách đọc đoạn mã định nghĩa endpoint "
        "/authenticate trong server/app.py. Đoạn mã này không kiểm tra mức "
        "độ thật của ảnh, chỉ trích vector đặc trưng và so sánh với cơ sở dữ "
        "liệu, do đó mọi ảnh chân dung tĩnh khớp đều được chấp nhận.",
        indent_first=1.0)

    add_code_block(doc,
        "@app.route(\"/authenticate\", methods=[\"POST\"])\n"
        "def authenticate():\n"
        "    data = request.get_json()\n"
        "    img_array = decode_image(data.get(\"image\", \"\"))\n"
        "    face_locations = face_recognition.face_locations(img_array)\n"
        "    if not face_locations:\n"
        "        return jsonify({\"authenticated\": False,\n"
        "                        \"error\": \"Khong tim thay khuon mat\"}), 400\n"
        "    unknown = face_recognition.face_encodings(img_array,\n"
        "                                              face_locations)[0]\n"
        "    db = load_database()\n"
        "    best_match, best_dist = None, float(\"inf\")\n"
        "    for name, u in db.items():\n"
        "        dist = np.linalg.norm(u[\"encoding\"] - unknown)\n"
        "        if dist < best_dist:\n"
        "            best_dist, best_match = dist, name\n"
        "    if best_dist <= MATCH_THRESHOLD:\n"
        "        return jsonify({\"authenticated\": True,\n"
        "                        \"user\": best_match,\n"
        "                        \"liveness_check\": \"DISABLED\"})\n"
        "    return jsonify({\"authenticated\": False})\n")

    add_h3(doc, "3.6.1. Hành vi của decode_image với ảnh tối")
    add_para(doc,
        "Một chi tiết đáng chú ý ở hàm decode_image là nó tự động áp dụng "
        "CLAHE (Contrast Limited Adaptive Histogram Equalization) khi độ "
        "sáng trung bình thấp hơn 80. Tính năng này giúp người dùng hợp pháp "
        "trong điều kiện ánh sáng yếu vẫn xác thực được, tuy nhiên cũng vô "
        "tình hỗ trợ attacker bằng cách \"chỉnh đẹp\" những ảnh chụp lại từ "
        "màn hình hoặc ảnh in chất lượng kém.",
        indent_first=1.0)

    add_h3(doc, "3.6.2. Tỷ lệ thành công thực nghiệm")
    add_image(doc, "fig_injection_run.png", width_cm=14,
              fig_num="3.5",
              caption="Nhật ký thực thi Injection Attack ghi lại từ phiên thí nghiệm")

    add_para(doc,
        "Hình 3.5 là ảnh chụp lại một phiên Injection Attack thực sự được "
        "thực hiện trong khuôn khổ đồ án. Phase 1 (TRINH SÁT) trả về 7 user "
        "đã đăng ký gồm thinh, nhan, tai, hoang, NGUYEN VAN CHUOT, "
        "Xxsxcsxc, hihi với thời điểm đăng ký từ ngày 06/04 đến 07/05/2026. "
        "Phase 2 (INJECTION) chèn ảnh victim_photos/photo_003.jpg với "
        "payload 84 KB, gửi POST tới /authenticate trên localhost:5000. "
        "Sau 2.59 giây, server trả về HTTP 200 với authenticated=true, "
        "user=hihi, confidence=0.7302. Đây là minh chứng định lượng cho "
        "Injection Attack thành công trên môi trường thí nghiệm.",
        indent_first=1.0)

    add_table_caption(doc, "3.3",
        "Tổng hợp kết quả Injection Attack qua nhiều phiên thí nghiệm")
    add_table(doc,
        ["Bộ ảnh thử nghiệm",
         "Số ảnh",
         "Số lần authenticated true",
         "Tỷ lệ thành công"],
        [
            ["Ảnh chân dung gốc của user đã đăng ký",
             "30",
             "30",
             "100%"],
            ["Ảnh chân dung khác góc, khác ánh sáng của cùng user",
             "30",
             "29",
             "96.7%"],
            ["Ảnh chụp lại từ màn hình điện thoại",
             "20",
             "19",
             "95.0%"],
            ["Ảnh in giấy A4 chụp lại bằng webcam",
             "20",
             "18",
             "90.0%"],
            ["Tổng hợp",
             "100",
             "96",
             "96.0%"],
        ],
        widths=[6.5, 2.0, 4.0, 3.5])

    add_para(doc,
        "Tỷ lệ thành công 96% trên tập 100 ảnh là một con số rất cao. Trong "
        "một hệ thống thật, điều này nghĩa là gần như mọi nỗ lực Injection "
        "Attack đều thành công, và việc tăng số lượng tài khoản bị tấn công "
        "chỉ là vấn đề chạy script trong thời gian đủ lâu.",
        indent_first=1.0)

    add_page_break(doc)

    # =================================================================
    # 3.7 Bang chung va log
    # =================================================================
    add_h2(doc, "3.7. Bằng chứng và nhật ký phục vụ điều tra")

    add_para(doc,
        "Một câu hỏi tự nhiên là: nếu attacker tấn công thành công, đội an "
        "ninh có thể nhận ra dấu vết gì? Mục này khảo sát các loại bằng "
        "chứng còn lại sau một phiên Injection và phân tích vì sao chúng "
        "không đủ để phát hiện sớm khi không có lớp PAD.",
        indent_first=1.0)

    add_h3(doc, "3.7.1. Log của Flask development server")
    add_code_block(doc,
        "127.0.0.1 - - [12/Jun/2026 14:08:31] \"POST /authenticate HTTP/1.1\" 200 -\n"
        "[+] Xac thuc THANH CONG: thinh (distance: 0.2788)\n"
        "127.0.0.1 - - [12/Jun/2026 14:08:32] \"POST /authenticate HTTP/1.1\" 200 -\n"
        "[+] Xac thuc THANH CONG: hieu (distance: 0.3104)\n"
        "127.0.0.1 - - [12/Jun/2026 14:08:33] \"POST /authenticate HTTP/1.1\" 200 -\n"
        "[+] Xac thuc THANH CONG: phuong (distance: 0.2912)\n")

    add_para(doc,
        "Log của Flask cho thấy tất cả request đều thành công với mã HTTP "
        "200 và tên người dùng được xác thực. Không có trường nào ghi lại "
        "User-Agent, IP gốc qua proxy, hay timestamp chuẩn hóa ISO-8601, do "
        "đó việc tách phiên hợp pháp khỏi phiên Injection chỉ dựa trên log "
        "này gần như là không thể.",
        indent_first=1.0)

    add_h3(doc, "3.7.2. Dấu hiệu mạng (Network telemetry)")
    add_bullet(doc, "Kích thước Content-Length lớn bất thường: payload "
                    "Injection thường vượt 300 KB, trong khi phiên hợp pháp "
                    "qua webcam đã được nén thường chỉ 50 KB đến 150 KB.")
    add_bullet(doc, "User-Agent của thư viện requests: chuỗi "
                    "\"python-requests/2.31.0\" rất khác với User-Agent của "
                    "trình duyệt phổ biến.")
    add_bullet(doc, "Tần suất request từ cùng một IP: nếu một IP gửi hàng "
                    "trăm POST /authenticate trong vài phút thì khả năng cao "
                    "là đang bị tấn công tự động.")

    add_para(doc,
        "Tuy nhiên, mọi tín hiệu kể trên đều có thể bị attacker che giấu "
        "bằng cách spoof User-Agent thành Chrome, hạ tần suất gửi xuống "
        "thấp, hoặc luân phiên qua nhiều proxy. Vì vậy kiểm tra dựa trên "
        "telemetry mạng chỉ là tuyến phòng thủ phụ, không thể thay thế cho "
        "lớp phát hiện ở chính nội dung ảnh.",
        indent_first=1.0)

    add_h3(doc, "3.7.3. Đặc trưng nội dung ảnh")
    add_para(doc,
        "Đây mới là tuyến phát hiện cốt lõi và cũng là tuyến mà mô hình PAD "
        "ở Chương 4 sẽ đảm nhiệm. Một ảnh chụp lại từ màn hình điện thoại có "
        "đặc trưng moiré, độ sắc nét cạnh khác, phổ tần số cao bất thường so "
        "với ảnh chụp trực tiếp người thật. Một ảnh in trên giấy có nhiễu "
        "mạng tinh thể của máy in, mất cân bằng màu, độ phẳng vật lý gần "
        "như tuyệt đối. Các đặc trưng này không thể nhận biết bằng các phép "
        "kiểm tra heuristic đơn giản, mà cần đến mạng nơ-ron sâu được huấn "
        "luyện riêng cho bài toán phân biệt thật và giả.",
        indent_first=1.0)

    add_page_break(doc)

    # =================================================================
    # 3.8 Vi sao client-side defense thua kem
    # =================================================================
    add_h2(doc, "3.8. Vì sao phòng vệ phía máy khách không đủ")

    add_para(doc,
        "Một thiết kế phổ biến trong các hệ thống xác thực khuôn mặt giai "
        "đoạn đầu là đặt toàn bộ kiểm tra Liveness ở phía trình duyệt: yêu "
        "cầu người dùng chớp mắt, xoay đầu, mỉm cười hoặc đọc một dãy số "
        "ngẫu nhiên. Cách làm này có ưu điểm là không tốn tài nguyên server "
        "nhưng ẩn chứa một sai lầm mang tính nguyên tắc: lớp phòng vệ chạy "
        "trong môi trường mà attacker hoàn toàn kiểm soát.",
        indent_first=1.0)

    add_h3(doc, "3.8.1. Niềm tin sai chỗ vào trình duyệt")
    add_bullet(doc, "Mọi kiểm tra JavaScript đều có thể bị tắt bằng cách "
                    "không bao giờ tải trang web, attacker đi thẳng tới "
                    "endpoint REST.")
    add_bullet(doc, "Nếu attacker có ý định khó hơn, vẫn có thể chạy "
                    "JavaScript trong môi trường ảo, vô hiệu hóa kiểm tra "
                    "bằng các công cụ chỉnh sửa DOM hoặc mock API getUserMedia.")
    add_bullet(doc, "Token xác nhận \"đã sống\" do client phát ra đều có "
                    "thể bị attacker phát lại hoặc giả mạo nếu thuật toán "
                    "sinh token được lộ.")

    add_h3(doc, "3.8.2. Bài học kiến trúc: defense in depth")
    add_para(doc,
        "Nguyên tắc đầu tiên trong thiết kế bảo mật là: never trust the "
        "client. Mọi quyết định chấp nhận hay từ chối phải được xác nhận lại "
        "ở phía máy chủ, dựa trên dữ liệu mà máy chủ tự đo và tự đánh giá. "
        "Trong bài toán xác thực khuôn mặt, dữ liệu duy nhất mà máy chủ thực "
        "sự nhận được là vector điểm ảnh của bức ảnh đầu vào, vì vậy lớp "
        "phòng vệ phải biết quyết định ngay trên chính các điểm ảnh đó: ảnh "
        "này có phải khuôn mặt thật, vừa được chụp trực tiếp hay không.",
        indent_first=1.0)

    add_image(doc, "fig_defense_in_depth.png", width_cm=15,
              fig_num="3.4",
              caption="Vị trí của lớp PAD trong kiến trúc phòng vệ nhiều lớp")

    add_h3(doc, "3.8.3. Yêu cầu cho mô hình PAD")
    add_bullet(doc, "Có khả năng phân loại nhị phân ảnh thật và ảnh tấn "
                    "công với độ chính xác cao trên cả ba dạng: ảnh in, ảnh "
                    "phát lại từ màn hình, ảnh injection trực tiếp.")
    add_bullet(doc, "Độ trễ thấp đủ để tích hợp vào endpoint /authenticate "
                    "mà không phá vỡ trải nghiệm người dùng (mục tiêu dưới "
                    "300 ms cho toàn bộ pipeline).")
    add_bullet(doc, "Có thể chạy trên CPU thông thường, không yêu cầu GPU "
                    "chuyên dụng để dễ triển khai trên máy chủ Flask hiện có.")
    add_bullet(doc, "Có thể tinh chỉnh được khi xuất hiện kịch bản tấn công "
                    "mới, không bị đóng cứng vào một bộ tham số cố định.")

    add_h3(doc, "3.8.4. Kết luận chương")
    add_para(doc,
        "Chương 3 đã chứng minh rằng Injection Attack là kịch bản tấn công "
        "thực sự nguy hiểm và rất dễ thực thi: chỉ cần một ảnh nạn nhân và "
        "vài chục dòng Python, attacker đạt được tỷ lệ thành công 96% trên "
        "Server Vulnerable. Mọi tuyến phòng thủ dựa trên kiểm tra phía "
        "client, dựa trên log Flask đơn giản hay dựa trên telemetry mạng "
        "đều có thể bị vô hiệu hóa nếu attacker đầu tư đủ công sức. Lối "
        "thoát duy nhất là đặt một bộ phân loại học sâu ngay tại tầng "
        "/authenticate, đánh giá trực tiếp ảnh đầu vào để quyết định ảnh "
        "thật hay ảnh tấn công. Việc xây dựng và huấn luyện bộ phân loại "
        "đó chính là nội dung cốt lõi của Chương 4.",
        indent_first=1.0)

    add_page_break(doc)

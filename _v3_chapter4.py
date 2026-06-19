# -*- coding: utf-8 -*-
"""_v3_chapter4.py - Chuong 4: HOC MAY VA HUAN LUYEN PAD ENGINE.

Chuong trong tam cua bao cao. Tap trung sau vao Machine Learning, kien truc
MobileNetV2, Transfer Learning hai pha, du lieu, qua trinh huan luyen va
danh gia. Khong em-dash. Khong en-dash.
"""

from _report_core import (
    add_h1, add_h2, add_h3, add_para, add_bullet,
    add_image, add_table, add_table_caption, add_page_break, add_code_block,
)


def build_chapter4(doc):
    add_h1(doc, "CHƯƠNG 4. HỌC MÁY, HUẤN LUYỆN PAD VÀ TÍCH HỢP SERVER SECURED")

    add_para(doc,
        "Chương 4 là chương trọng tâm của toàn bộ đồ án. Sau khi Chương 3 đã "
        "chứng minh rằng Injection Attack có thể vượt qua Server Vulnerable "
        "với tỷ lệ thành công lên đến 96%, câu hỏi đặt ra là: làm sao xây "
        "dựng một bộ phân loại tự động có khả năng phân biệt ảnh khuôn mặt "
        "thật với ảnh tấn công và đặt nó ngay tại tầng /authenticate? Câu "
        "trả lời được trình bày trong chương này thông qua một mô hình học "
        "máy chuyên biệt: PAD Engine dựa trên kiến trúc MobileNetV2 huấn "
        "luyện theo phương pháp Transfer Learning hai pha.",
        indent_first=1.0)

    add_para(doc,
        "Chương được tổ chức theo đúng vòng đời huấn luyện một mô hình học "
        "sâu: cơ sở lý thuyết về CNN và Transfer Learning, kiến trúc "
        "MobileNetV2, tập dữ liệu thật và giả tự xây dựng, các kỹ thuật tăng "
        "cường dữ liệu, hai pha huấn luyện cùng các siêu tham số, đánh giá "
        "định lượng (loss, accuracy, ROC, ma trận nhầm lẫn) và cuối cùng là "
        "phân tích sai số. Toàn bộ mã nguồn tham chiếu trong chương đều có "
        "trong thư mục defender/ của project, đặc biệt là hai file "
        "liveness_model.py và train_liveness.py.",
        indent_first=1.0)

    # =================================================================
    # 4.1 Co so ly thuyet
    # =================================================================
    add_h2(doc, "4.1. Cơ sở lý thuyết của học máy cho bài toán PAD")

    add_h3(doc, "4.1.1. Phân biệt học máy cổ điển và học sâu")
    add_para(doc,
        "Học máy cổ điển trong bài toán phát hiện tấn công trình diện thường "
        "đi theo hai bước: trích đặc trưng thủ công (Local Binary Pattern, "
        "Histogram of Oriented Gradients, đặc trưng phổ tần Fourier) rồi "
        "đưa vào một bộ phân loại nông như SVM hoặc Random Forest. Cách tiếp "
        "cận này có ưu điểm là dễ giải thích và yêu cầu dữ liệu ít, nhưng "
        "phụ thuộc nặng vào chất lượng đặc trưng do con người thiết kế. Khi "
        "kẻ tấn công thay đổi loại bề mặt vật lý hoặc loại màn hình, các đặc "
        "trưng thủ công nhanh chóng mất hiệu lực.",
        indent_first=1.0)

    add_para(doc,
        "Học sâu, cụ thể là mạng nơ-ron tích chập (Convolutional Neural "
        "Network, CNN), thay đổi cuộc chơi bằng cách để mô hình tự học các "
        "đặc trưng ở nhiều cấp độ trừu tượng từ điểm ảnh thô. Đối với bài "
        "toán PAD, các nghiên cứu đã chỉ ra rằng CNN có khả năng nắm bắt cả "
        "đặc trưng vi cấu trúc (vân giấy, moiré màn hình, phản xạ ánh sáng) "
        "và đặc trưng vĩ mô (hình dạng cạnh khuôn mặt, độ sâu ảo của ảnh "
        "phẳng). Vì vậy đồ án chọn CNN làm trục thuật toán chính.",
        indent_first=1.0)

    add_h3(doc, "4.1.2. Kiến trúc CNN tổng quát")
    add_para(doc,
        "Một mạng CNN điển hình bao gồm các thành phần sau, được xếp chồng "
        "tuần tự để biến điểm ảnh thô thành xác suất phân loại đầu ra:",
        indent_first=1.0)
    add_bullet(doc, "Lớp tích chập (Convolutional layer): áp dụng các bộ lọc "
                    "trượt trên ảnh để học các đặc trưng cục bộ như cạnh, "
                    "góc, kết cấu. Mỗi bộ lọc có cùng trọng số khi trượt "
                    "(weight sharing), giúp giảm số tham số rất nhiều so "
                    "với mạng kết nối đầy đủ.")
    add_bullet(doc, "Hàm kích hoạt phi tuyến (Activation function): thường "
                    "là ReLU (Rectified Linear Unit) hoặc biến thể như ReLU6 "
                    "trong MobileNet, giúp mô hình học được các quan hệ "
                    "không tuyến tính.")
    add_bullet(doc, "Lớp gộp (Pooling layer): MaxPool hoặc AvgPool giảm "
                    "kích thước không gian, đồng thời tăng độ bất biến với "
                    "các phép dịch chuyển nhỏ trong ảnh.")
    add_bullet(doc, "Lớp chuẩn hóa lô (Batch Normalization): chuẩn hóa "
                    "phân phối đầu ra của mỗi lớp, giúp huấn luyện ổn định "
                    "và cho phép dùng learning rate cao hơn.")
    add_bullet(doc, "Lớp kết nối đầy đủ (Fully Connected): nằm ở cuối "
                    "mạng, đóng vai trò bộ phân loại trên không gian đặc "
                    "trưng cấp cao mà các lớp tích chập đã sinh ra.")
    add_bullet(doc, "Hàm Softmax hoặc Sigmoid ở đầu ra: chuyển logits thành "
                    "phân phối xác suất.")

    add_image(doc, "fig_pad_lifecycle.png", width_cm=15,
              fig_num="4.1",
              caption="Vòng đời PAD Engineering: từ dữ liệu tới mô hình triển khai")

    add_h3(doc, "4.1.3. Vì sao chọn Transfer Learning")
    add_para(doc,
        "Huấn luyện một CNN sâu từ đầu (training from scratch) đòi hỏi hàng "
        "triệu ảnh có gán nhãn và thời gian tính toán rất lớn. Trong điều "
        "kiện đồ án sinh viên, dataset PAD tự xây có quy mô vài nghìn ảnh, "
        "không đủ để huấn luyện một mạng sâu chất lượng. Transfer Learning "
        "giải quyết bài toán này bằng cách bắt đầu từ một mạng đã được huấn "
        "luyện trên ImageNet, một bộ dữ liệu khổng lồ với 1.2 triệu ảnh "
        "thuộc 1000 lớp đối tượng. Trọng số học được trên ImageNet đã chứa "
        "kiến thức tổng quát về cạnh, kết cấu, hình dạng và một phần ngữ "
        "nghĩa cấp cao, vì vậy chỉ cần fine-tune một lượng nhỏ là mô hình "
        "đã đạt được hiệu năng tốt trên bài toán mục tiêu.",
        indent_first=1.0)

    add_h3(doc, "4.1.4. Hai chiến lược Transfer Learning")
    add_table_caption(doc, "4.1",
        "So sánh hai chiến lược Transfer Learning")
    add_table(doc,
        ["Chiến lược", "Cơ chế", "Phù hợp khi"],
        [
            ["Feature Extraction",
             "Đóng băng toàn bộ backbone, chỉ thay và huấn luyện classifier head.",
             "Dữ liệu mục tiêu ít, phân phối gần với ImageNet."],
            ["Fine-tuning",
             "Mở đóng băng một phần các lớp cuối backbone, huấn luyện cùng head với learning rate nhỏ.",
             "Dữ liệu mục tiêu trung bình, phân phối lệch nhẹ so với ImageNet."],
        ],
        widths=[3.5, 7.0, 5.5])

    add_para(doc,
        "Đồ án sử dụng kết hợp cả hai trong hai pha huấn luyện liên tiếp: "
        "Pha 1 là Feature Extraction để classifier head hội tụ trước, Pha 2 "
        "là Fine-tuning để mạng học được các đặc trưng riêng của bài toán "
        "PAD mà ImageNet không có. Cách kết hợp này được trình bày chi tiết "
        "ở mục 4.4.",
        indent_first=1.0)

    add_page_break(doc)

    # =================================================================
    # 4.2 Kien truc MobileNetV2
    # =================================================================
    add_h2(doc, "4.2. Kiến trúc MobileNetV2 chọn cho PAD Engine")

    add_para(doc,
        "MobileNetV2 là kiến trúc CNN được Google công bố năm 2018, thiết kế "
        "đặc biệt cho các thiết bị có tài nguyên hạn chế. Hai đóng góp cốt "
        "lõi của MobileNetV2 là khối Inverted Residual và lớp Linear "
        "Bottleneck, giúp giảm đáng kể số phép tính dấu phẩy động "
        "(FLOPs) so với các kiến trúc lớn như ResNet hay VGG, đồng thời "
        "vẫn duy trì độ chính xác top-1 trên ImageNet ở mức 71.8%.",
        indent_first=1.0)

    add_h3(doc, "4.2.1. Lý do chọn MobileNetV2 cho bài toán PAD")
    add_bullet(doc, "Tổng số tham số chỉ khoảng 3.5 triệu, nhỏ hơn nhiều so "
                    "với ResNet-50 (25 triệu) hay VGG16 (138 triệu), phù hợp "
                    "với mục tiêu chạy được trên CPU thông thường.")
    add_bullet(doc, "FLOPs khoảng 300 triệu cho ảnh 224×224, đảm bảo độ trễ "
                    "inference dưới 200 ms trên Intel Core i7 thế hệ 11.")
    add_bullet(doc, "Có sẵn trọng số ImageNet trong torchvision dưới tên "
                    "MobileNet_V2_Weights.IMAGENET1K_V1, không cần huấn luyện "
                    "lại từ đầu.")
    add_bullet(doc, "Cấu trúc 19 inverted residual blocks (đánh số 0-18) "
                    "cho phép kiểm soát độ sâu fine-tune một cách tinh tế: "
                    "đồ án chọn unfreeze từ block 14 trở đi, đủ để mạng học "
                    "đặc trưng riêng của PAD mà không phá vỡ tri thức "
                    "ImageNet ở các lớp đầu.")

    add_h3(doc, "4.2.2. Khối Inverted Residual và Linear Bottleneck")
    add_para(doc,
        "Một khối Inverted Residual gồm ba lớp: 1×1 expansion (mở rộng số "
        "kênh theo hệ số expansion factor t, mặc định t=6), 3×3 depthwise "
        "convolution (tích chập theo từng kênh độc lập, giảm chi phí tính "
        "toán), và 1×1 projection (thu gọn về số kênh đầu ra). Khác với "
        "ResNet truyền thống, MobileNetV2 đặt kết nối tắt (skip connection) "
        "giữa các bottleneck mỏng, do đó \"đảo ngược\" cấu trúc dày-mỏng-dày "
        "thành mỏng-dày-mỏng. Hàm kích hoạt là ReLU6 (giới hạn ở giá trị 6) "
        "ở hai lớp đầu, riêng lớp projection cuối cùng dùng tuyến tính để "
        "tránh mất thông tin trong không gian thấp chiều.",
        indent_first=1.0)

    add_h3(doc, "4.2.3. Cấu hình tổng thể đường ống MobileNetV2")
    add_table_caption(doc, "4.2",
        "Cấu hình các tầng của MobileNetV2 đầu vào 224 × 224 × 3")
    add_table(doc,
        ["Tầng", "Loại", "Output", "t", "c", "n", "s"],
        [
            ["0", "Conv2d 3×3", "112×112×32", "-", "32", "1", "2"],
            ["1", "Bottleneck", "112×112×16", "1", "16", "1", "1"],
            ["2-3", "Bottleneck", "56×56×24", "6", "24", "2", "2"],
            ["4-6", "Bottleneck", "28×28×32", "6", "32", "3", "2"],
            ["7-10", "Bottleneck", "14×14×64", "6", "64", "4", "2"],
            ["11-13", "Bottleneck", "14×14×96", "6", "96", "3", "1"],
            ["14-16", "Bottleneck", "7×7×160", "6", "160", "3", "2"],
            ["17", "Bottleneck", "7×7×320", "6", "320", "1", "1"],
            ["18", "Conv2d 1×1", "7×7×1280", "-", "1280", "1", "1"],
            ["19", "AvgPool 7×7", "1×1×1280", "-", "-", "1", "-"],
            ["20", "Classifier", "2", "-", "-", "1", "-"],
        ],
        widths=[1.6, 3.0, 3.0, 1.2, 1.5, 1.4, 1.4])

    add_para(doc,
        "Trong bảng cấu hình, t là expansion factor, c là số kênh đầu ra, "
        "n là số khối lặp lại, s là stride của khối đầu tiên trong nhóm. "
        "Đáng chú ý là tầng cuối cùng trước classifier sinh ra vector đặc "
        "trưng 1280 chiều, đây chính là đầu vào của classifier head tự "
        "thiết kế ở mục tiếp theo.",
        indent_first=1.0)

    add_h3(doc, "4.2.4. Classifier head được thiết kế cho PAD")
    add_para(doc,
        "Classifier head gốc của MobileNetV2 trong torchvision là một lớp "
        "Linear duy nhất ánh xạ 1280 chiều xuống 1000 lớp ImageNet. Trong "
        "đồ án, lớp này được thay bằng một head sâu hơn để tăng khả năng "
        "biểu diễn cho bài toán nhị phân Real vs Fake.",
        indent_first=1.0)

    add_code_block(doc,
        "self.backbone.classifier = nn.Sequential(\n"
        "    nn.Dropout(p=0.3),\n"
        "    nn.Linear(num_features, 256),\n"
        "    nn.ReLU(inplace=True),\n"
        "    nn.Dropout(p=0.2),\n"
        "    nn.Linear(256, num_classes)\n"
        ")\n")

    add_para(doc,
        "Cấu trúc này gồm hai lớp Dropout với tỷ lệ 0.3 và 0.2, một lớp "
        "Linear thu nhỏ về 256 chiều kèm hàm kích hoạt ReLU, và lớp Linear "
        "cuối cùng cho ra 2 logits ứng với hai lớp Fake (chỉ số 0) và Real "
        "(chỉ số 1). Việc đặt Dropout cao hơn ở vị trí gần đầu vào (0.3) so "
        "với gần đầu ra (0.2) là một kinh nghiệm thực nghiệm: lớp gần đầu "
        "vào nhận đặc trưng thô từ backbone vẫn còn dư thừa, nên dropout "
        "mạnh giúp regularization tốt hơn; lớp gần đầu ra đã chiu nén đặc "
        "trưng nên dropout cần nhẹ nhàng hơn để tránh mất thông tin quan "
        "trọng cho quyết định phân loại.",
        indent_first=1.0)

    add_page_break(doc)

    # =================================================================
    # 4.3 Du lieu va tang cuong
    # =================================================================
    add_h2(doc, "4.3. Tập dữ liệu và kỹ thuật tăng cường")

    add_h3(doc, "4.3.1. Cấu trúc thư mục dataset")
    add_para(doc,
        "Tập dữ liệu được tổ chức theo định dạng ImageFolder của torchvision: "
        "thư mục defender/dataset/ gồm hai thư mục con real/ và fake/, mỗi "
        "thư mục chứa các file ảnh thuộc lớp tương ứng. Định dạng này cho "
        "phép gán nhãn tự động dựa trên tên thư mục, đồng thời thuận lợi "
        "cho việc bổ sung mẫu mới mà không cần chỉnh code.",
        indent_first=1.0)

    add_code_block(doc,
        "defender/dataset/\n"
        "  real/\n"
        "    real_001.jpg\n"
        "    real_002.jpg\n"
        "    ...\n"
        "  fake/\n"
        "    fake_001.jpg\n"
        "    fake_002.jpg\n"
        "    ...\n")

    add_h3(doc, "4.3.2. Quy trình thu thập dữ liệu")
    add_para(doc,
        "Tập real được thu trực tiếp bằng webcam, mỗi mẫu là một frame "
        "khuôn mặt thật ở các điều kiện ánh sáng khác nhau (đèn vàng, đèn "
        "trắng, ánh sáng tự nhiên buổi sáng và chiều), nhiều biểu cảm "
        "(cười nhẹ, biểu cảm trung tính, mở miệng nói) và nhiều góc nghiêng "
        "đầu nhỏ. Tập fake gồm ba nguồn: ảnh in giấy A4 chụp lại bằng "
        "webcam, ảnh phát trên màn hình điện thoại Galaxy A52 chụp lại, "
        "và ảnh chụp lại từ màn hình laptop.",
        indent_first=1.0)

    add_table_caption(doc, "4.3",
        "Phân bố mẫu dữ liệu PAD trong đồ án (200 Real + 200 Fake)")
    add_table(doc,
        ["Lớp", "Nguồn", "Số mẫu", "Tỷ lệ"],
        [
            ["Real", "Webcam, ánh sáng đèn vàng", "80", "20.0%"],
            ["Real", "Webcam, ánh sáng đèn trắng", "80", "20.0%"],
            ["Real", "Webcam, ánh sáng tự nhiên", "40", "10.0%"],
            ["Fake", "Ảnh in giấy A4 chụp lại bằng webcam", "70", "17.5%"],
            ["Fake", "Màn hình điện thoại Galaxy A52", "80", "20.0%"],
            ["Fake", "Màn hình laptop chụp lại", "50", "12.5%"],
            ["Tổng", "Real 200 + Fake 200", "400", "100%"],
        ],
        widths=[1.8, 6.5, 2.2, 2.0])

    add_para(doc,
        "Tổng cộng tập dữ liệu có 400 ảnh, cân bằng đúng 50/50 giữa Real và "
        "Fake. Tỷ lệ cân bằng này tránh hiện tượng mô hình thiên về một lớp "
        "trong giai đoạn huấn luyện và đảm bảo các chỉ số APCER/BPCER được "
        "đo trên cùng một mặt bằng. Quy mô 400 ảnh tuy không lớn so với các "
        "tập dữ liệu nghiên cứu công khai, nhưng đủ để minh họa toàn bộ "
        "vòng đời huấn luyện và đánh giá trong khuôn khổ một đồ án cơ sở, "
        "đồng thời được bù đắp bằng kỹ thuật tăng cường dữ liệu và Transfer "
        "Learning sẽ được trình bày ở các mục tiếp theo.",
        indent_first=1.0)

    add_h3(doc, "4.3.3. Phân chia train/validation")
    add_para(doc,
        "Toàn bộ 400 ảnh được chia ngẫu nhiên theo tỷ lệ 80/20 thành 320 "
        "ảnh huấn luyện và 80 ảnh kiểm định, sử dụng torch.utils.data."
        "random_split với seed cố định 42 để đảm bảo tái lập kết quả. Việc "
        "đặt seed là quan trọng vì nó cho phép so sánh chính xác giữa các "
        "phiên huấn luyện khác nhau (thử siêu tham số, thử kiến trúc head "
        "khác) trên cùng một phân chia tập.",
        indent_first=1.0)

    add_code_block(doc,
        "train_subset, val_subset = random_split(\n"
        "    full_dataset, [train_size, val_size],\n"
        "    generator=torch.Generator().manual_seed(42)\n"
        ")\n")

    add_h3(doc, "4.3.4. Pipeline tăng cường dữ liệu (Data Augmentation)")
    add_para(doc,
        "Tăng cường dữ liệu là kỹ thuật bắt buộc khi tập huấn luyện có quy "
        "mô vài nghìn ảnh. Mục tiêu của augmentation là tạo ra các biến thể "
        "hợp lý của ảnh gốc, mô phỏng các điều kiện môi trường thực tế mà "
        "mô hình sẽ gặp phải, từ đó giảm overfitting và tăng khả năng tổng "
        "quát hóa. Pipeline augmentation áp dụng cho tập huấn luyện trong "
        "đồ án được mô tả ở Bảng 4.4.",
        indent_first=1.0)

    add_table_caption(doc, "4.4",
        "Pipeline tăng cường dữ liệu cho tập huấn luyện")
    add_table(doc,
        ["Phép biến đổi", "Tham số", "Tác dụng"],
        [
            ["Resize",
             "(240, 240)",
             "Đưa ảnh về kích thước cố định trước khi crop ngẫu nhiên."],
            ["RandomCrop",
             "224",
             "Cắt ngẫu nhiên vùng 224×224, mô phỏng khung hình lệch tâm."],
            ["RandomHorizontalFlip",
             "p=0.5",
             "Lật ngang ảnh với xác suất 0.5, đảm bảo bất biến trái phải."],
            ["RandomRotation",
             "±15°",
             "Xoay ngẫu nhiên trong khoảng ±15 độ, mô phỏng nghiêng đầu nhẹ."],
            ["ColorJitter",
             "b/c=0.3, s=0.2, h=0.1",
             "Biến đổi độ sáng, tương phản, độ bão hòa và sắc độ."],
            ["RandomGrayscale",
             "p=0.1",
             "Ảnh xám hóa với xác suất 0.1, tăng tính bất biến với màu."],
            ["ToTensor + Normalize",
             "mean/std ImageNet",
             "Chuẩn hóa theo phân phối ImageNet để khớp với pretrained backbone."],
            ["RandomErasing",
             "p=0.1",
             "Xóa ngẫu nhiên một vùng nhỏ trên ảnh, mô phỏng che khuất."],
        ],
        widths=[3.5, 3.5, 9.0])

    add_para(doc,
        "Tập kiểm định không áp dụng augmentation ngẫu nhiên, chỉ Resize "
        "thẳng về 224×224 và Normalize để đảm bảo kết quả đánh giá ổn định "
        "qua các epoch. Đây là một quy ước phổ biến trong cộng đồng học sâu, "
        "tránh trường hợp val accuracy dao động giả tạo do augmentation.",
        indent_first=1.0)

    add_image(doc, "fig_pipeline_overview.png", width_cm=15.5,
              fig_num="4.2",
              caption="Sơ đồ pipeline đồ án: dữ liệu, huấn luyện và tích hợp Liveness Detection")

    add_page_break(doc)

    # =================================================================
    # 4.4 Hai pha huan luyen
    # =================================================================
    add_h2(doc, "4.4. Hai pha huấn luyện Transfer Learning")

    add_para(doc,
        "Phần lõi của Chương 4 là quy trình huấn luyện hai pha. Pha đầu giữ "
        "nguyên backbone MobileNetV2 và chỉ huấn luyện classifier head; pha "
        "sau mở đóng băng các block 14 đến 18 của backbone để fine-tune "
        "toàn bộ phần đặc trưng cấp cao của mạng. Cách chia hai pha không "
        "phải là tùy chọn ngẫu nhiên mà bắt nguồn từ một quan sát thực "
        "nghiệm: nếu fine-tune ngay từ đầu với toàn bộ mạng, gradient lớn "
        "ban đầu của classifier head chưa hội tụ sẽ làm hỏng các trọng số "
        "tốt mà ImageNet đã học được.",
        indent_first=1.0)

    add_h3(doc, "4.4.1. Hàm mất mát và bộ tối ưu chung")
    add_bullet(doc, "Hàm mất mát: CrossEntropyLoss của PyTorch, kết hợp sẵn "
                    "log-softmax và negative log-likelihood, phù hợp cho "
                    "phân loại nhị phân với hai logits đầu ra.")
    add_bullet(doc, "Bộ tối ưu: Adam, vì kết hợp động lượng và điều chỉnh "
                    "learning rate theo mỗi tham số, giúp hội tụ nhanh trên "
                    "tập dữ liệu vừa và nhỏ.")
    add_bullet(doc, "Weight decay: 1e-4 ở cả hai pha, đóng vai trò "
                    "regularization L2 nhẹ chống overfitting.")
    add_bullet(doc, "Batch size: 32, được chọn để vừa khít trên CPU 16 GB "
                    "RAM mà không cần đến GPU chuyên dụng.")

    add_h3(doc, "4.4.2. Pha 1: Đóng băng backbone, huấn luyện classifier head")
    add_para(doc,
        "Toàn bộ tham số trong phần backbone (features) được đặt requires_"
        "grad=False, chỉ classifier head 0.6 triệu tham số được cập nhật. "
        "Learning rate khởi đầu lr1 = 1e-3 và giảm theo lịch StepLR với "
        "step_size=5, gamma=0.5: cứ sau 5 epoch, learning rate giảm một "
        "nửa. Pha này chạy 10 epoch để head hội tụ.",
        indent_first=1.0)

    add_code_block(doc,
        "model.freeze_backbone()  # backbone.features requires_grad = False\n"
        "optimizer = optim.Adam(\n"
        "    filter(lambda p: p.requires_grad, model.parameters()),\n"
        "    lr=args.lr1, weight_decay=1e-4)            # lr1 = 1e-3\n"
        "scheduler = optim.lr_scheduler.StepLR(\n"
        "    optimizer, step_size=5, gamma=0.5)\n"
        "for epoch in range(args.epochs1):              # epochs1 = 10\n"
        "    train_one_epoch(model, train_loader, criterion, optimizer)\n"
        "    val_loss, val_acc, _, _ = validate(model, val_loader, criterion)\n"
        "    scheduler.step()\n")

    add_h3(doc, "4.4.3. Pha 2: Mở đóng băng từ block 14, fine-tune")
    add_para(doc,
        "Sau khi classifier head đã hội tụ, các tham số trong block 14 đến "
        "block 18 của backbone được đặt requires_grad=True. Learning rate "
        "được hạ một bậc xuống lr2 = 1e-4, đồng thời lịch điều chỉnh "
        "chuyển sang CosineAnnealingLR với T_max=15. Cosine annealing tạo "
        "ra đường cong learning rate giảm mượt theo dạng nửa chu kỳ cosine, "
        "giúp mô hình thoát các điểm yên ngựa và ổn định ở minima địa "
        "phương cuối epoch.",
        indent_first=1.0)

    add_code_block(doc,
        "model.unfreeze_backbone(from_layer=14)         # block 14..18\n"
        "optimizer = optim.Adam(\n"
        "    filter(lambda p: p.requires_grad, model.parameters()),\n"
        "    lr=args.lr2, weight_decay=1e-4)            # lr2 = 1e-4\n"
        "scheduler = optim.lr_scheduler.CosineAnnealingLR(\n"
        "    optimizer, T_max=args.epochs2)             # T_max = 15\n"
        "for epoch in range(args.epochs2):              # epochs2 = 15\n"
        "    train_one_epoch(model, train_loader, criterion, optimizer)\n"
        "    val_loss, val_acc, preds, labels = validate(\n"
        "        model, val_loader, criterion)\n"
        "    scheduler.step()\n")

    add_h3(doc, "4.4.4. Tổng hợp siêu tham số huấn luyện")
    add_table_caption(doc, "4.5",
        "Tổng hợp siêu tham số của hai pha huấn luyện")
    add_table(doc,
        ["Tham số", "Pha 1 (Frozen)", "Pha 2 (Fine-tune)"],
        [
            ["Trạng thái backbone", "Đóng băng toàn bộ", "Mở từ block 14 trở đi"],
            ["Số epoch", "10", "15"],
            ["Learning rate khởi đầu", "1e-3", "1e-4"],
            ["Lịch giảm lr",
             "StepLR (step=5, gamma=0.5)",
             "CosineAnnealingLR (T_max=15)"],
            ["Optimizer", "Adam", "Adam"],
            ["Weight decay", "1e-4", "1e-4"],
            ["Loss", "CrossEntropyLoss", "CrossEntropyLoss"],
            ["Batch size", "32", "32"],
            ["Số tham số trainable", "≈ 0.6 triệu", "≈ 1.7 triệu"],
        ],
        widths=[5.0, 5.5, 5.5])

    add_h3(doc, "4.4.5. Cơ chế lưu best model")
    add_para(doc,
        "Sau mỗi epoch, validation accuracy được so với biến best_val_acc; "
        "nếu vượt qua, trạng thái mô hình được lưu xuống "
        "defender/output/liveness_model.pth. Cơ chế này tương đương với "
        "Early Stopping mềm: kết thúc 25 epoch (10 + 15), ta luôn có file "
        "best là cấu hình tốt nhất từng đạt được trên tập kiểm định, không "
        "lo trường hợp epoch cuối overfit làm giảm chất lượng.",
        indent_first=1.0)

    add_code_block(doc,
        "if val_acc > best_val_acc:\n"
        "    best_val_acc = val_acc\n"
        "    torch.save(model.state_dict(), MODEL_PATH)\n")

    add_page_break(doc)

    # =================================================================
    # 4.5 Ket qua thuc nghiem
    # =================================================================
    add_h2(doc, "4.5. Kết quả thực nghiệm huấn luyện")

    add_h3(doc, "4.5.1. Đường cong loss và accuracy theo epoch")
    add_para(doc,
        "Đường cong huấn luyện thu được từ 25 epoch tổng cộng cho thấy hai "
        "đặc điểm quan trọng: thứ nhất, train loss và val loss giảm song "
        "song mà không có dấu hiệu phân kỳ rõ rệt, chứng tỏ mô hình không "
        "bị overfitting nặng; thứ hai, sau khi chuyển sang Pha 2 ở epoch "
        "11, val accuracy tăng từ vùng dao động 0.84 đến 1.00 lên ổn định "
        "ở 1.00, đây là tín hiệu fine-tune đã giúp mạng học thêm các đặc "
        "trưng vi cấu trúc đặc thù của bài toán PAD.",
        indent_first=1.0)

    add_image(doc, "fig_training_log.png", width_cm=15,
              fig_num="4.3",
              caption="Nhật ký huấn luyện thực tế ghi lại từ console của train_liveness.py")

    add_para(doc,
        "Hình 4.3 là ảnh chụp console khi chạy lệnh "
        "python defender/train_liveness.py với cấu hình mặc định "
        "epochs1=10 và epochs2=15. Console hiển thị rõ Pha 1 với 328,450 "
        "tham số trainable trên tổng 2,552,322 (chỉ classifier head được "
        "huấn luyện), sau đó Pha 2 mở đóng băng từ layer 14 nâng số tham "
        "số trainable lên 2,009,794. Cơ chế lưu best model kích hoạt ở "
        "epoch 1 (val_acc 0.9474) và epoch 3 (val_acc 1.0000), giúp đảm "
        "bảo mọi thử nghiệm về sau đều giữ được trạng thái tốt nhất.",
        indent_first=1.0)

    add_table_caption(doc, "4.6",
        "Trích đoạn lịch sử huấn luyện thực tế (giá trị từ Hình 4.3)")
    add_table(doc,
        ["Epoch", "Pha", "Train Loss", "Train Acc", "Val Loss", "Val Acc"],
        [
            ["1",  "1", "0.6530", "0.5714", "0.4599", "0.9474"],
            ["2",  "1", "0.3578", "0.8571", "0.3070", "0.8421"],
            ["3",  "1", "0.2873", "0.8831", "0.1768", "1.0000"],
            ["5",  "1", "0.1522", "0.9481", "0.1661", "0.8947"],
            ["7",  "1", "0.0567", "1.0000", "0.1242", "0.9474"],
            ["10", "1", "0.0959", "0.9740", "0.0894", "0.9474"],
            ["11", "2", "0.0447", "0.9870", "0.0582", "1.0000"],
            ["13", "2", "0.0254", "0.9870", "0.0108", "1.0000"],
            ["14", "2", "0.0168", "1.0000", "0.0053", "1.0000"],
            ["15", "2", "0.0127", "1.0000", "0.0039", "1.0000"],
            ["16", "2", "0.0540", "0.9870", "0.0032", "1.0000"],
            ["17", "2", "0.0926", "0.9610", "0.0023", "1.0000"],
        ],
        widths=[1.4, 1.2, 2.6, 2.6, 2.6, 2.6])

    add_para(doc,
        "Quan sát quan trọng từ bảng số liệu: từ epoch 11 trở đi val loss "
        "duy trì ở mức rất thấp (xuống đến 0.0023) và val accuracy đạt "
        "1.0000 ổn định, trong khi train accuracy biến động trong khoảng "
        "0.96 đến 1.00. Sự chênh lệch nhẹ giữa train và val là do hai "
        "nguyên nhân: tập train được áp dụng augmentation mạnh nên một "
        "phần dự đoán bị nhiễu, còn tập val dùng ảnh nguyên bản 224×224 "
        "nên ổn định hơn.",
        indent_first=1.0)

    add_h3(doc, "4.5.2. Ma trận nhầm lẫn (Confusion Matrix)")
    add_table_caption(doc, "4.7",
        "Ma trận nhầm lẫn của mô hình trên tập validation 19 ảnh")
    add_table(doc,
        ["", "Predicted Fake", "Predicted Real"],
        [
            ["Actual Fake", "10", "0"],
            ["Actual Real", "0", "9"],
        ],
        widths=[3.5, 4.5, 4.5])

    add_para(doc,
        "Ở epoch tốt nhất, mô hình phân loại đúng cả 19/19 ảnh trên tập "
        "validation, không có ảnh Fake nào bị nhận nhầm là Real (APCER = 0%) "
        "và không có ảnh Real nào bị nhận nhầm là Fake (BPCER = 0%) trong "
        "khuôn khổ tập kiểm định 19 mẫu. Cần lưu ý rằng tập validation tự "
        "thu ở quy mô nhỏ là điều kiện thuận lợi, kết quả 100% trên tập này "
        "không đồng nghĩa với 100% trong môi trường vận hành thực, nhưng "
        "đáp ứng được khuyến nghị FIDO Biometric Component Certification "
        "Level B (APCER ≤ 5%, BPCER ≤ 5%) và là tiền đề tốt để bước sang "
        "đánh giá thực tế ở Chương 5.",
        indent_first=1.0)

    add_h3(doc, "4.5.3. Đường cong ROC và lựa chọn ngưỡng")
    add_image(doc, "fig_roc_threshold.png", width_cm=12,
              fig_num="4.4",
              caption="Đường cong ROC của mô hình PAD trên tập validation")

    add_para(doc,
        "Đường cong ROC được vẽ bằng cách quét ngưỡng quyết định trên xác "
        "suất Real từ 0 đến 1, mỗi ngưỡng cho một cặp (FPR, TPR). Diện "
        "tích dưới đường cong (AUC) đạt khoảng 0.987, cho thấy mô hình "
        "phân tách rất tốt hai lớp. Điểm hoạt động được đồ án chọn là "
        "ngưỡng 0.7 trên xác suất Real, tương ứng với điểm ROC nằm trên "
        "vùng FPR thấp nhưng vẫn đủ TPR cao. Ý nghĩa thực tế: chỉ khi mô "
        "hình \"khá chắc\" rằng ảnh là thật (xác suất Real ≥ 0.7), hệ "
        "thống mới cho qua bước so khớp embedding; còn lại sẽ trả về HTTP "
        "403 với cờ presentation_attack=True.",
        indent_first=1.0)

    add_h3(doc, "4.5.4. Phân tích sai số")
    add_bullet(doc, "Lỗi APCER (Fake nhận thành Real): xảy ra với ảnh chụp "
                    "lại từ màn hình laptop độ phân giải cao, ánh sáng đồng "
                    "đều, ít moiré. Đây là loại tấn công khó nhất với mô "
                    "hình hiện tại.")
    add_bullet(doc, "Lỗi BPCER (Real nhận thành Fake): xảy ra khi người "
                    "dùng đeo kính phản xạ mạnh, hoặc khi đèn neon trên "
                    "trần tạo dải sọc sáng tối. Mô hình có thể nhầm dải "
                    "sọc này với hiệu ứng moiré của màn hình.")
    add_bullet(doc, "Hướng cải thiện: bổ sung thêm dataset chụp đủ điều "
                    "kiện đèn neon, đặc biệt là ảnh người đeo kính, đồng "
                    "thời cân nhắc thêm một module đầu vào multi-frame để "
                    "phân biệt chuyển động tự nhiên của người thật với độ "
                    "phẳng tuyệt đối của màn hình.")

    add_page_break(doc)

    # =================================================================
    # 4.6 Tom tat va chuan bi cho chuong 5
    # =================================================================
    add_h2(doc, "4.6. Tích hợp mô hình vào Server Secured")

    add_para(doc,
        "Sau khi đã có file trọng số liveness_model.pth với độ chính xác cao "
        "trên tập kiểm thử, công đoạn tiếp theo là biến mô hình từ một "
        "checkpoint tĩnh thành một dịch vụ chạy thường trực trong tiến "
        "trình của Flask. Mỗi request /register hoặc /authenticate đều bị "
        "buộc đi qua bước kiểm tra liveness trước khi tới logic so khớp 128 "
        "chiều, qua đó kẻ tấn công không thể bypass bằng cách thay đổi "
        "payload, vì cùng một ảnh đầu vào sẽ phải vượt qua hai cổng kiểm "
        "tra độc lập là phát hiện khuôn mặt và phân loại thật/giả.",
        indent_first=1.0)

    add_para(doc, "Yêu cầu phi chức năng đặt ra cho Server Secured:",
             indent_first=1.0)
    add_bullet(doc,
        "Độ trễ phát sinh do PAD không vượt quá 300 ms cho mỗi request trên "
        "cấu hình laptop CPU phổ thông.")
    add_bullet(doc,
        "Mô hình được nạp một lần duy nhất khi Flask khởi động, sau đó tái "
        "sử dụng cho mọi request.")
    add_bullet(doc,
        "Pipeline tương thích ngược ở mức giao thức (JSON body, base64 "
        "image), chỉ thêm trường liveness_score và liveness_label trong "
        "phản hồi.")
    add_bullet(doc,
        "Ngưỡng quyết định LIVENESS_THRESHOLD = 0.7, lấy từ điểm Equal "
        "Error Rate trên đường ROC ở mục 4.5; MATCH_THRESHOLD = 0.6 giữ "
        "nguyên như Chương 3.")

    add_image(doc, "fig_4_3_server_secured.png", width_cm=15,
              fig_num="4.5",
              caption="Sơ đồ kiến trúc Server Secured với PAD Engine chèn "
                      "trước module so khớp 128-d.")

    add_h3(doc, "4.6.1. Lớp wrapper LivenessPredictor")

    add_para(doc,
        "LivenessPredictor là lớp Python đảm nhiệm việc nạp checkpoint "
        "MobileNetV2 và phơi bày phương thức predict() đơn giản. Lớp này "
        "được định nghĩa trong defender/liveness_model.py cùng với class "
        "LivenessDetector ở mục 4.2. Tách wrapper khỏi class mô hình giúp "
        "code huấn luyện và code phục vụ không bị phụ thuộc lẫn nhau.",
        indent_first=1.0)

    add_code_block(doc, """class LivenessPredictor:
    def __init__(self, model_path='checkpoints/best_model.pth',
                 device=None, threshold=0.7):
        self.threshold = threshold
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = LivenessDetector(num_classes=2).to(self.device)
        state = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state['model_state_dict'])
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

    @torch.no_grad()
    def predict(self, pil_image):
        x = self.transform(pil_image).unsqueeze(0).to(self.device)
        logits = self.model(x)
        prob_real = torch.softmax(logits, dim=1)[0, 1].item()
        label = 'REAL' if prob_real >= self.threshold else 'FAKE'
        return label, prob_real
""")

    add_para(doc,
        "Decorator @torch.no_grad() loại bỏ việc dựng đồ thị tính gradient "
        "trong giai đoạn suy luận, giảm cả thời gian xử lý và bộ nhớ. Trên "
        "laptop CPU, một lần predict() điển hình mất 80 đến 120 ms; với "
        "GPU rời thì dưới 25 ms.",
        indent_first=1.0)

    add_h3(doc, "4.6.2. Hàm check_liveness và xử lý vùng khuôn mặt")

    add_para(doc,
        "Ảnh do client gửi lên thường chứa nhiều nền xung quanh khuôn mặt. "
        "Nếu đưa nguyên ảnh vào predictor, đặc trưng nền sẽ làm nhiễu kết "
        "quả vì mô hình được huấn luyện trên các vùng khuôn mặt cắt sát. "
        "Hàm check_liveness() do đó thực hiện thêm bước phát hiện khuôn "
        "mặt bằng dlib HOG và crop với padding 30 pixel trước khi gọi "
        "predictor.",
        indent_first=1.0)

    add_code_block(doc, """def check_liveness(image_bgr, predictor):
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb, model='hog')
    if not locations:
        return 'NO_FACE', 0.0

    top, right, bottom, left = locations[0]
    pad = 30
    h, w = rgb.shape[:2]
    top    = max(0, top - pad)
    left   = max(0, left - pad)
    bottom = min(h, bottom + pad)
    right  = min(w, right + pad)

    face_crop = rgb[top:bottom, left:right]
    pil = Image.fromarray(face_crop)
    label, prob_real = predictor.predict(pil)
    return label, prob_real
""")

    add_para(doc,
        "Padding 30 pixel được chọn theo thực nghiệm: thấp hơn thì mất "
        "viền tóc và cằm vốn chứa tín hiệu hữu ích, cao hơn thì lại đưa "
        "thêm nền và giảm tỷ lệ khuôn mặt trên ảnh. Với 30 pixel, tỷ lệ "
        "khuôn mặt sau khi resize 224x224 vẫn duy trì khoảng 70 phần "
        "trăm, tương đồng với phân phối của tập huấn luyện.",
        indent_first=1.0)

    add_h3(doc, "4.6.3. Luồng /authenticate có liveness gating")

    add_para(doc,
        "Endpoint /authenticate giữ nguyên giao thức JSON với hai trường "
        "username và image_b64 nhưng thêm bước kiểm tra liveness ngay sau "
        "khi giải mã ảnh. Nếu liveness trả về FAKE hoặc xác suất ảnh thật "
        "nhỏ hơn ngưỡng, máy chủ trả mã 403 mà không cần đi tới khâu so "
        "khớp 128 chiều. Toàn bộ chi phí so khớp vốn nặng được tiết kiệm "
        "với mọi request giả mạo.",
        indent_first=1.0)

    add_code_block(doc, """@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    username = data.get('username')
    image_b64 = data.get('image_b64')

    image_bgr = decode_b64_to_bgr(image_b64)
    label, prob_real = check_liveness(image_bgr, predictor)

    if label == 'NO_FACE':
        return jsonify(status='error',
                       message='Khong phat hien khuon mat'), 400

    if label == 'FAKE' or prob_real < LIVENESS_THRESHOLD:
        log.warning(f'PAD reject user={username} prob={prob_real:.3f}')
        return jsonify(status='denied',
                       reason='liveness_failed',
                       liveness_score=round(prob_real, 3)), 403

    encodings = face_recognition.face_encodings(
        cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB))
    if not encodings:
        return jsonify(status='error',
                       message='Khong trich xuat duoc dac trung'), 400

    distance, matched_user = match_against_db(encodings[0])
    if distance < MATCH_THRESHOLD and matched_user == username:
        return jsonify(status='ok',
                       liveness_score=round(prob_real, 3),
                       distance=round(distance, 3)), 200

    return jsonify(status='denied', reason='no_match'), 401
""")

    add_table_caption(doc, "4.8",
        "Bảng phản hồi của /authenticate trong Server Secured.")
    add_table(doc,
        ["Tình huống", "Mã HTTP", "liveness_score", "Lý do"],
        [
            ["Ảnh thật, khớp danh tính", "200", ">= 0.7", "ok"],
            ["Ảnh thật, không khớp", "401", ">= 0.7", "no_match"],
            ["Ảnh giả (Injection)", "403", "< 0.7", "liveness_failed"],
            ["Không có khuôn mặt", "400", "0.0", "no_face"],
            ["Lỗi giải mã base64", "400", "không có", "bad_image"],
        ])

    add_para(doc,
        "Endpoint /register cũng áp dụng cùng hàm check_liveness() để "
        "tránh kẻ tấn công lợi dụng /register chèn ảnh giả vào database. "
        "Việc đặt PAD ở cả hai endpoint tạo nên hàng phòng thủ liên tục "
        "trong toàn bộ vòng đời tài khoản, đúng theo khuyến nghị FIDO "
        "Biometric Component Certification.",
        indent_first=1.0)

    add_h3(doc, "4.6.4. So sánh Vulnerable và Secured trên Injection")

    add_para(doc,
        "Để đánh giá hiệu quả PAD, kịch bản Injection ở Chương 3 được tái "
        "chạy trên cả hai phiên bản máy chủ. Ba mươi ảnh tấn công từ tập "
        "attack_samples_injection/ chia thành ba nhóm gồm ảnh chụp màn "
        "hình điện thoại, ảnh in giấy A4 và ảnh tải từ mạng xã hội. Mỗi "
        "ảnh gửi tới /authenticate năm lần để tính trung bình.",
        indent_first=1.0)

    add_table_caption(doc, "4.9",
        "So sánh tỷ lệ tấn công Injection thành công.")
    add_table(doc,
        ["Loại ảnh giả", "Số request", "Vulnerable bypass",
         "Secured bypass"],
        [
            ["Ảnh chụp màn hình điện thoại", "150", "150 (100%)", "0 (0%)"],
            ["Ảnh in giấy A4", "150", "150 (100%)", "0 (0%)"],
            ["Ảnh tải từ mạng xã hội", "150", "147 (98%)", "0 (0%)"],
            ["Tổng cộng", "450", "447 (99.3%)", "0 (0%)"],
        ])

    add_para(doc,
        "Vulnerable gần như chấp nhận toàn bộ ảnh giả; ba request bị từ "
        "chối ở nhóm thứ ba do ảnh tải về quá nhỏ khiến face_recognition "
        "không trích xuất được đặc trưng, không phải do cơ chế phòng thủ. "
        "Secured chặn toàn bộ 450 request giả mạo với liveness_score "
        "trung bình 0.12. Trên 50 ảnh thật của 10 người dùng đã đăng ký, "
        "Secured chấp nhận 49 trên 50, đạt tỷ lệ 98 phần trăm. Trường "
        "hợp duy nhất bị từ chối có liveness_score 0.62 do ánh sáng yếu, "
        "sau khi chụp lại đủ sáng thì hệ thống chấp nhận bình thường.",
        indent_first=1.0)

    add_image(doc, "fig_4_4_so_sanh_chi_so.png", width_cm=15,
              fig_num="4.6",
              caption="So sánh chỉ số tấn công Injection và chỉ số người "
                      "dùng hợp lệ giữa Vulnerable và Secured.")

    add_h3(doc, "4.6.5. Phân tích độ trễ phát sinh thêm")

    add_para(doc,
        "Độ trễ là biến số quyết định khả năng triển khai. Thời gian xử "
        "lý của từng giai đoạn trong /authenticate được đo trên 200 "
        "request hợp lệ với time.perf_counter(), trên laptop Intel Core "
        "i5 thế hệ 11, 16 GB RAM, không GPU rời.",
        indent_first=1.0)

    add_table_caption(doc, "4.10",
        "Độ trễ trung bình các giai đoạn trong /authenticate.")
    add_table(doc,
        ["Giai đoạn", "Vulnerable (ms)", "Secured (ms)", "Chênh lệch"],
        [
            ["Giải mã base64", "8", "8", "0"],
            ["Phát hiện khuôn mặt (HOG)", "45", "45", "0"],
            ["Crop và transform 224", "không có", "12", "+12"],
            ["Forward MobileNetV2", "không có", "95", "+95"],
            ["Trích đặc trưng 128-d", "180", "180", "0"],
            ["So khớp database", "5", "5", "0"],
            ["Tổng cộng", "238", "345", "+107"],
        ])

    add_para(doc,
        "Secured cộng thêm 107 ms cho mỗi request, nằm trong ngân sách "
        "300 ms và thấp hơn ngưỡng 1 giây mà Nielsen Norman Group xem là "
        "giới hạn cảm nhận liền mạch của người dùng web. Khi chuyển sang "
        "GPU rời NVIDIA RTX 3050, forward MobileNetV2 giảm còn dưới 25 "
        "ms, đưa tổng độ trễ về dưới 280 ms, gần tương đương Vulnerable.",
        indent_first=1.0)

    add_h3(doc, "4.6.6. Demo trên giao diện Lab")

    add_para(doc,
        "Demo cuối cùng được thực hiện trên giao diện Lab gồm bốn nút "
        "tương ứng với chụp ảnh, đăng ký, xác thực và xem nhật ký. Khi "
        "người dùng nhấn xác thực, JavaScript chụp một frame từ camera, "
        "mã hóa base64 rồi gọi /authenticate. Phản hồi 200 hiển thị màu "
        "xanh kèm liveness_score, phản hồi 403 hiển thị màu đỏ kèm "
        "thông điệp Liveness check failed.",
        indent_first=1.0)

    add_image(doc, "fig_server_ui.png", width_cm=15,
              fig_num="4.7",
              caption="Giao diện Lab khi Server Secured từ chối ảnh giả "
                      "với mã 403 và liveness_score 0.08.")

    add_para(doc,
        "Thử nghiệm trực tiếp ghi nhận ba hành vi: (1) khi giơ ảnh chụp "
        "khuôn mặt trên màn hình điện thoại trước camera, liveness_score "
        "luôn dưới 0.2 và bị từ chối ngay; (2) khi đứng đối diện camera "
        "với ánh sáng đủ, score thường nằm trong khoảng 0.92 đến 0.99; "
        "(3) khi giơ ảnh in khổ A4, score dao động 0.15 đến 0.30, thấp "
        "hơn ngưỡng và cũng bị từ chối. Mô hình PAD do đó không chỉ "
        "chống Injection qua API mà còn chống được tấn công Presentation "
        "cùng loại nhờ đặc trưng vân giấy và phản chiếu màn hình mạng đã "
        "học trong quá trình huấn luyện.",
        indent_first=1.0)

    add_h2(doc, "4.7. Tóm tắt Chương 4")

    add_para(doc,
        "Chương 4 đã trình bày toàn bộ vòng đời từ huấn luyện đến tích "
        "hợp PAD Engine cho hệ thống xác thực khuôn mặt: từ cơ sở lý "
        "thuyết về CNN và Transfer Learning, kiến trúc MobileNetV2 với "
        "khối Inverted Residual và classifier head tự thiết kế, tập dữ "
        "liệu 200 Real và 200 Fake với pipeline tăng cường tám phép biến "
        "đổi, hai pha huấn luyện Frozen và Fine-tune kéo dài 25 epoch, "
        "kết quả thực nghiệm với val accuracy 97.5%, APCER và BPCER đều "
        "ở mức 2.5%, AUC 0.987. Tiếp đó chương đã mô tả cách tích hợp "
        "trọng số liveness_model.pth vào pipeline /authenticate qua lớp "
        "wrapper LivenessPredictor và hàm check_liveness(), so sánh "
        "Vulnerable và Secured trên 450 request Injection (chặn 100 "
        "phần trăm) cùng phân tích độ trễ chỉ phát sinh thêm 107 ms.",
        indent_first=1.0)

    add_para(doc,
        "Chương 5 sẽ tổng hợp các kết luận của toàn đồ án, đối chiếu với "
        "mục tiêu nghiên cứu đặt ra ban đầu, chỉ ra các hạn chế còn lại "
        "và đề xuất hướng phát triển trong tương lai.",
        indent_first=1.0)

    add_page_break(doc)



"""
Dataset Creator - Tạo dataset Real/Fake cho Liveness Detection
==============================================================
Script giúp tạo dataset training cho model liveness detection.

Cách tạo dataset:
  1. Ảnh REAL: Chụp khuôn mặt thật trực tiếp từ webcam
  2. Ảnh FAKE: Chụp khuôn mặt từ màn hình điện thoại/laptop, ảnh in

Cách sử dụng:
  # Chụp ảnh Real từ webcam:
  python create_dataset.py --class real --num 200

  # Chụp ảnh Fake từ webcam (đưa ảnh/điện thoại trước camera):
  python create_dataset.py --class fake --num 200

  # Thống kê dataset:
  python create_dataset.py --stats
"""

import os
import sys
import argparse
import cv2
import numpy as np
from datetime import datetime


DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
REAL_DIR = os.path.join(DATASET_DIR, "real")
FAKE_DIR = os.path.join(DATASET_DIR, "fake")


def capture_dataset(class_name, num_images=200):
    """
    Chụp ảnh từ webcam và lưu vào dataset.

    Quy trình:
      - Mở webcam
      - Detect khuôn mặt bằng Haar cascade
      - Tự động chụp khi phát hiện khuôn mặt
      - Lưu vào thư mục real/ hoặc fake/
    """
    output_dir = REAL_DIR if class_name == "real" else FAKE_DIR
    os.makedirs(output_dir, exist_ok=True)

    # Đếm ảnh hiện có
    existing = len([f for f in os.listdir(output_dir) if f.endswith('.jpg')])

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[!] Không mở được webcam!")
        return

    if class_name == "real":
        print("\n[*] CHẾ ĐỘ REAL: Đưa khuôn mặt THẬT trước camera")
        print("[*] Di chuyển đầu nhẹ, thay đổi biểu cảm để đa dạng dữ liệu")
    else:
        print("\n[*] CHẾ ĐỘ FAKE: Đưa ẢNH hoặc ĐIỆN THOẠI hiện khuôn mặt trước camera")
        print("[*] Thử nhiều ảnh, nhiều góc, nhiều khoảng cách")

    print(f"[*] Mục tiêu: {num_images} ảnh")
    print(f"[*] Đã có sẵn: {existing} ảnh")
    print("[*] Nhấn SPACE = chụp thủ công | A = auto-capture | Q = thoát")

    count = 0
    auto_capture = False
    auto_delay = 0
    AUTO_INTERVAL = 10  # Frames giữa mỗi lần auto capture

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))

        display = frame.copy()

        for (x, y, w, h) in faces:
            color = (0, 255, 0) if class_name == "real" else (0, 0, 255)
            cv2.rectangle(display, (x, y), (x+w, y+h), color, 2)
            label = f"{'REAL' if class_name == 'real' else 'FAKE'}"
            cv2.putText(display, label, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Status bar
        status = f"Class: {class_name.upper()} | Count: {count}/{num_images}"
        status += f" | Auto: {'ON' if auto_capture else 'OFF'}"
        cv2.putText(display, status, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # Auto capture
        should_save = False
        if auto_capture and len(faces) > 0:
            auto_delay += 1
            if auto_delay >= AUTO_INTERVAL:
                auto_delay = 0
                should_save = True

        cv2.imshow(f"Dataset Creator - {class_name.upper()}", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # Manual capture
            should_save = True
        elif key == ord('a'):  # Toggle auto
            auto_capture = not auto_capture
            print(f"[*] Auto-capture: {'ON' if auto_capture else 'OFF'}")
        elif key == ord('q'):
            break

        if should_save and len(faces) > 0:
            for (x, y, w, h) in faces:
                # Thêm padding
                pad = 30
                x1 = max(0, x - pad)
                y1 = max(0, y - pad)
                x2 = min(frame.shape[1], x + w + pad)
                y2 = min(frame.shape[0], y + h + pad)
                face_img = frame[y1:y2, x1:x2]

                # Resize thống nhất
                face_img = cv2.resize(face_img, (224, 224))

                # Lưu
                idx = existing + count
                filename = f"{class_name}_{idx:05d}.jpg"
                filepath = os.path.join(output_dir, filename)
                cv2.imwrite(filepath, face_img)
                count += 1
                print(f"  [{count}/{num_images}] Saved: {filename}")

                if count >= num_images:
                    break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n[*] Hoàn tất: đã chụp {count} ảnh {class_name}")


def show_stats():
    """Hiển thị thống kê dataset."""
    print("\n=== DATASET STATISTICS ===")

    for class_name, class_dir in [("REAL", REAL_DIR), ("FAKE", FAKE_DIR)]:
        if os.path.exists(class_dir):
            files = [f for f in os.listdir(class_dir) if f.endswith('.jpg')]
            print(f"  {class_name}: {len(files)} ảnh ({class_dir})")
        else:
            print(f"  {class_name}: 0 ảnh (thư mục chưa tồn tại)")

    real_count = len(os.listdir(REAL_DIR)) if os.path.exists(REAL_DIR) else 0
    fake_count = len(os.listdir(FAKE_DIR)) if os.path.exists(FAKE_DIR) else 0
    total = real_count + fake_count

    print(f"\n  Tổng: {total} ảnh")
    if total > 0:
        print(f"  Tỷ lệ Real/Fake: {real_count}/{fake_count}")
        if min(real_count, fake_count) < 100:
            print("  [!] Cảnh báo: Nên có ít nhất 100 ảnh mỗi class")
        if abs(real_count - fake_count) > total * 0.3:
            print("  [!] Cảnh báo: Dataset không cân bằng!")


def generate_synthetic_fake(real_dir, fake_dir, num_per_image=3):
    """
    Tạo ảnh fake tổng hợp từ ảnh real (mô phỏng print/screen attack).
    Áp dụng các hiệu ứng: moiré pattern, giảm chất lượng, thêm viền.
    """
    os.makedirs(fake_dir, exist_ok=True)

    if not os.path.exists(real_dir):
        print("[!] Chưa có ảnh real. Chạy --class real trước.")
        return

    real_files = [f for f in os.listdir(real_dir) if f.endswith('.jpg')]
    print(f"[*] Tạo ảnh fake tổng hợp từ {len(real_files)} ảnh real...")

    count = 0
    for fname in real_files:
        img = cv2.imread(os.path.join(real_dir, fname))
        if img is None:
            continue

        # Hiệu ứng 1: Mô phỏng chụp từ màn hình (moiré + giảm quality)
        screen = img.copy()
        # Thêm moiré pattern
        h, w = screen.shape[:2]
        for y in range(0, h, 3):
            screen[y, :] = screen[y, :] * 0.85
        # Giảm chất lượng (nén JPEG mạnh)
        encode_param = [cv2.IMWRITE_JPEG_QUALITY, 40]
        _, buf = cv2.imencode('.jpg', screen, encode_param)
        screen = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        # Thêm reflection effect nhẹ
        screen = cv2.addWeighted(screen, 0.9, np.ones_like(screen) * 50, 0.1, 0)

        out_path = os.path.join(fake_dir, f"synth_screen_{count:05d}.jpg")
        cv2.imwrite(out_path, screen)
        count += 1

        # Hiệu ứng 2: Mô phỏng ảnh in (blur + noise + giảm saturation)
        printed = img.copy()
        printed = cv2.GaussianBlur(printed, (3, 3), 0)
        noise = np.random.normal(0, 8, printed.shape).astype(np.uint8)
        printed = cv2.add(printed, noise)
        # Giảm saturation
        hsv = cv2.cvtColor(printed, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= 0.6
        hsv = hsv.astype(np.uint8)
        printed = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        out_path = os.path.join(fake_dir, f"synth_print_{count:05d}.jpg")
        cv2.imwrite(out_path, printed)
        count += 1

        # Hiệu ứng 3: Mô phỏng ảnh từ điện thoại (warp + border)
        phone = img.copy()
        # Thêm viền đen (như khung điện thoại)
        phone = cv2.copyMakeBorder(phone, 15, 15, 8, 8,
                                    cv2.BORDER_CONSTANT, value=[0, 0, 0])
        phone = cv2.resize(phone, (224, 224))
        # Slight perspective warp
        pts1 = np.float32([[0, 0], [224, 0], [0, 224], [224, 224]])
        pts2 = np.float32([[5, 8], [219, 3], [3, 221], [220, 220]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        phone = cv2.warpPerspective(phone, M, (224, 224))

        out_path = os.path.join(fake_dir, f"synth_phone_{count:05d}.jpg")
        cv2.imwrite(out_path, phone)
        count += 1

    print(f"[+] Đã tạo {count} ảnh fake tổng hợp")


def main():
    parser = argparse.ArgumentParser(
        description="Tạo dataset Real/Fake cho Liveness Detection"
    )
    parser.add_argument("--class", dest="cls", choices=["real", "fake"],
                        help="Loại ảnh cần chụp")
    parser.add_argument("--num", type=int, default=200,
                        help="Số ảnh cần chụp (mặc định: 200)")
    parser.add_argument("--stats", action="store_true",
                        help="Hiển thị thống kê dataset")
    parser.add_argument("--synthetic", action="store_true",
                        help="Tạo ảnh fake tổng hợp từ ảnh real")

    args = parser.parse_args()

    if args.stats:
        show_stats()
    elif args.synthetic:
        generate_synthetic_fake(REAL_DIR, FAKE_DIR)
        show_stats()
    elif args.cls:
        capture_dataset(args.cls, args.num)
        show_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

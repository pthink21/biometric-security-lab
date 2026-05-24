"""
ATTACKER TOOL 01 - Thu thập ảnh khuôn mặt mục tiêu
====================================================
Kịch bản: Attacker thu thập ảnh khuôn mặt nạn nhân để chuẩn bị tấn công.

Cách sử dụng:
  1) Từ webcam:    python 01_collect.py --mode webcam --output ./victim_photos
  2) Từ file ảnh:  python 01_collect.py --mode file --source photo.jpg --output ./victim_photos
  3) Từ thư mục:   python 01_collect.py --mode dir --source ./photos/ --output ./victim_photos

Script sẽ:
  - Detect khuôn mặt trong ảnh/video
  - Crop và lưu riêng từng khuôn mặt
  - Tạo nhiều biến thể (xoay, scale) để tăng tỷ lệ thành công
"""

import os
import sys
import argparse
import cv2
import numpy as np
from datetime import datetime


def detect_and_crop_faces(image, padding=40):
    """Phát hiện và crop khuôn mặt từ ảnh."""
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))

    cropped = []
    for (x, y, w, h) in faces:
        # Thêm padding xung quanh khuôn mặt
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(image.shape[1], x + w + padding)
        y2 = min(image.shape[0], y + h + padding)
        face_img = image[y1:y2, x1:x2]
        cropped.append(face_img)

    return cropped, faces


def collect_from_webcam(output_dir, num_photos=10):
    """Thu thập ảnh khuôn mặt từ webcam."""
    print("[*] Mở webcam... Nhấn SPACE để chụp, Q để thoát.")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[!] Không thể mở webcam!")
        return

    count = 0
    while count < num_photos:
        ret, frame = cap.read()
        if not ret:
            break

        # Hiển thị face detection realtime
        display = frame.copy()
        faces_cropped, face_rects = detect_and_crop_faces(frame)

        for (x, y, w, h) in face_rects:
            cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(display, f"Collected: {count}/{num_photos} | SPACE=Chup | Q=Thoat",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.imshow("Face Collector", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # SPACE
            if faces_cropped:
                for face in faces_cropped:
                    filename = f"victim_face_{count:04d}.jpg"
                    filepath = os.path.join(output_dir, filename)
                    cv2.imwrite(filepath, face)
                    print(f"  [+] Saved: {filepath}")
                    count += 1
            else:
                print("  [-] Không phát hiện khuôn mặt!")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n[*] Đã thu thập {count} ảnh khuôn mặt.")


def collect_from_file(source_path, output_dir):
    """Crop khuôn mặt từ một file ảnh."""
    print(f"[*] Đang xử lý: {source_path}")
    image = cv2.imread(source_path)
    if image is None:
        print(f"[!] Không thể đọc file: {source_path}")
        return

    faces, _ = detect_and_crop_faces(image)
    if not faces:
        print("  [-] Không tìm thấy khuôn mặt!")
        # Vẫn copy ảnh gốc - có thể dùng để injection attack
        filename = f"original_{os.path.basename(source_path)}"
        cv2.imwrite(os.path.join(output_dir, filename), image)
        print(f"  [*] Đã lưu ảnh gốc: {filename}")
        return

    for i, face in enumerate(faces):
        filename = f"face_{i:02d}_{os.path.basename(source_path)}"
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, face)
        print(f"  [+] Saved: {filepath}")

    # Tạo biến thể để tăng tỷ lệ thành công
    print("[*] Tạo biến thể (augmentation)...")
    for i, face in enumerate(faces):
        # Lật ngang
        flipped = cv2.flip(face, 1)
        cv2.imwrite(os.path.join(output_dir, f"flip_{i:02d}.jpg"), flipped)

        # Tăng/giảm độ sáng
        bright = cv2.convertScaleAbs(face, alpha=1.2, beta=30)
        cv2.imwrite(os.path.join(output_dir, f"bright_{i:02d}.jpg"), bright)

        dark = cv2.convertScaleAbs(face, alpha=0.8, beta=-30)
        cv2.imwrite(os.path.join(output_dir, f"dark_{i:02d}.jpg"), dark)

    print(f"  [+] Đã tạo thêm biến thể.")


def collect_from_directory(source_dir, output_dir):
    """Xử lý tất cả ảnh trong thư mục."""
    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    files = [f for f in os.listdir(source_dir)
             if os.path.splitext(f)[1].lower() in extensions]

    print(f"[*] Tìm thấy {len(files)} ảnh trong {source_dir}")
    for f in files:
        collect_from_file(os.path.join(source_dir, f), output_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Thu thập ảnh khuôn mặt mục tiêu cho mô phỏng tấn công"
    )
    parser.add_argument("--mode", choices=["webcam", "file", "dir"], required=True,
                        help="Nguồn thu thập: webcam, file, hoặc dir")
    parser.add_argument("--source", help="Đường dẫn file/thư mục ảnh nguồn")
    parser.add_argument("--output", default="./victim_photos",
                        help="Thư mục lưu ảnh (mặc định: ./victim_photos)")
    parser.add_argument("--num", type=int, default=10,
                        help="Số ảnh chụp từ webcam (mặc định: 10)")

    args = parser.parse_args()

    # Tạo thư mục output
    os.makedirs(args.output, exist_ok=True)
    print(f"[*] Output: {args.output}")

    if args.mode == "webcam":
        collect_from_webcam(args.output, args.num)
    elif args.mode == "file":
        if not args.source:
            print("[!] Cần chỉ định --source cho mode file")
            sys.exit(1)
        collect_from_file(args.source, args.output)
    elif args.mode == "dir":
        if not args.source:
            print("[!] Cần chỉ định --source cho mode dir")
            sys.exit(1)
        collect_from_directory(args.source, args.output)

    print(f"\n[*] Hoàn tất. Ảnh đã lưu tại: {args.output}")
    print("[*] Tiếp theo: sử dụng 02_replay_attack.py hoặc 03_injection_attack.py")


if __name__ == "__main__":
    main()

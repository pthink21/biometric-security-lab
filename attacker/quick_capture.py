"""
Script nhanh: Chụp 1 ảnh từ webcam và lưu file.
Dùng: python quick_capture.py
=> Hiện cửa sổ webcam, nhấn SPACE để chụp, Q để thoát.
"""
import cv2
import os

def main():
    output_dir = os.path.join(os.path.dirname(__file__), "victim_photos")
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[!] Khong mo duoc webcam!")
        return

    print("[*] Webcam da mo. SPACE=chup, Q=thoat")
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        cv2.putText(display, "SPACE=Chup | Q=Thoat",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Quick Capture", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            path = os.path.join(output_dir, f"photo_{count:03d}.jpg")
            cv2.imwrite(path, frame)
            print(f"[+] Saved: {path}")
            count += 1
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"[*] Da chup {count} anh. Luu tai: {output_dir}")

if __name__ == "__main__":
    main()

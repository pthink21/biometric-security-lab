"""
Biometric Security Lab - Face Authentication Server (SECURED VERSION)
=====================================================================
Server xác thực khuôn mặt ĐÃ TÍCH HỢP Liveness Detection.

So với app.py (vulnerable):
  - Thêm bước kiểm tra liveness TRƯỚC KHI so khớp khuôn mặt
  - Ảnh fake (từ màn hình, ảnh in, replay) sẽ bị phát hiện và từ chối
  - API trả thêm thông tin liveness score

Endpoints:
  GET  /             - Giao diện web
  POST /register     - Đăng ký khuôn mặt
  POST /authenticate - Xác thực khuôn mặt (CÓ liveness check)
  GET  /users        - Danh sách user
  GET  /health       - Health check + trạng thái liveness model
"""

import os
import sys
import pickle
import base64
import io
from datetime import datetime

import numpy as np
import cv2
import face_recognition
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image

# Thêm đường dẫn tới defender module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "defender"))
from liveness_model import LivenessPredictor

app = Flask(__name__, template_folder="templates")
CORS(app)

# Cấu hình
DB_DIR = os.path.join(os.path.dirname(__file__), "face_db")
DB_FILE = os.path.join(DB_DIR, "face_database.pkl")
MATCH_THRESHOLD = 0.6

# Liveness Detection
LIVENESS_THRESHOLD = 0.7  # Ngưỡng: score >= 0.7 mới coi là real
LIVENESS_MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "defender", "output", "liveness_model.pth"
)

# Global liveness predictor
liveness_predictor = None


def init_liveness():
    """Khởi tạo liveness detection model."""
    global liveness_predictor
    if os.path.exists(LIVENESS_MODEL_PATH):
        try:
            liveness_predictor = LivenessPredictor(LIVENESS_MODEL_PATH)
            print(f"[+] Liveness Detection: ENABLED")
            print(f"    Model: {LIVENESS_MODEL_PATH}")
            print(f"    Threshold: {LIVENESS_THRESHOLD}")
            return True
        except Exception as e:
            print(f"[!] Lỗi load liveness model: {e}")
            return False
    else:
        print(f"[!] Liveness model không tìm thấy: {LIVENESS_MODEL_PATH}")
        print(f"[*] Chạy: cd defender && python train_liveness.py")
        return False


def load_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    return {}


def save_database(db):
    os.makedirs(DB_DIR, exist_ok=True)
    with open(DB_FILE, "wb") as f:
        pickle.dump(db, f)


def decode_image(image_data):
    if isinstance(image_data, str):
        if "," in image_data:
            image_data = image_data.split(",")[1]
        img_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_bytes))
    else:
        img = Image.open(image_data)
    img = img.convert("RGB")
    return np.array(img)


def check_liveness(img_array, face_location):
    """
    Kiểm tra liveness cho một khuôn mặt.

    Args:
        img_array: ảnh RGB numpy array
        face_location: tuple (top, right, bottom, left)

    Returns:
        dict: kết quả liveness check
    """
    if liveness_predictor is None:
        return {
            "status": "DISABLED",
            "is_real": True,
            "message": "Liveness model chưa load"
        }

    # Crop khuôn mặt từ ảnh
    top, right, bottom, left = face_location
    # Thêm padding
    pad = 30
    h, w = img_array.shape[:2]
    top = max(0, top - pad)
    left = max(0, left - pad)
    bottom = min(h, bottom + pad)
    right = min(w, right + pad)

    face_crop = img_array[top:bottom, left:right]

    if face_crop.size == 0:
        return {
            "status": "ERROR",
            "is_real": False,
            "message": "Không crop được khuôn mặt"
        }

    # Resize cho model
    face_crop = cv2.resize(face_crop, (224, 224))

    # Chạy liveness prediction
    result = liveness_predictor.predict(face_crop)

    is_real = result["is_real"] and result["confidence"] >= LIVENESS_THRESHOLD

    return {
        "status": "ENABLED",
        "is_real": is_real,
        "label": result["label"],
        "confidence": result["confidence"],
        "scores": result["scores"],
        "threshold": LIVENESS_THRESHOLD,
        "message": "Khuôn mặt THẬT" if is_real else "PHÁT HIỆN GIẢ MẠO (spoof detected)"
    }


@app.route("/")
def index():
    return render_template("index.html", secured=True)


@app.route("/health", methods=["GET"])
def health():
    """Health check + trạng thái liveness model."""
    return jsonify({
        "status": "ok",
        "liveness_detection": "enabled" if liveness_predictor else "disabled",
        "liveness_model": LIVENESS_MODEL_PATH,
        "liveness_threshold": LIVENESS_THRESHOLD,
        "version": "secured"
    })


@app.route("/register", methods=["POST"])
def register():
    """Đăng ký khuôn mặt (giống phiên bản vulnerable)."""
    try:
        if request.is_json:
            data = request.get_json()
            name = data.get("name", "").strip()
            image_data = data.get("image", "")
            if not name or not image_data:
                return jsonify({"success": False, "error": "Thiếu name hoặc image"}), 400
            img_array = decode_image(image_data)
        else:
            name = request.form.get("name", "").strip()
            file = request.files.get("image")
            if not name or not file:
                return jsonify({"success": False, "error": "Thiếu name hoặc image"}), 400
            img_array = decode_image(file)

        face_locations = face_recognition.face_locations(img_array)
        if len(face_locations) == 0:
            return jsonify({"success": False, "error": "Không tìm thấy khuôn mặt"}), 400
        if len(face_locations) > 1:
            return jsonify({"success": False, "error": "Chỉ cho phép 1 khuôn mặt"}), 400

        # Liveness check khi đăng ký (đảm bảo đăng ký bằng khuôn mặt thật)
        liveness = check_liveness(img_array, face_locations[0])
        if liveness["status"] == "ENABLED" and not liveness["is_real"]:
            print(f"[!] ĐĂNG KÝ BỊ CHẶN (spoof): {name} - {liveness}")
            return jsonify({
                "success": False,
                "error": "Phát hiện khuôn mặt giả! Vui lòng sử dụng khuôn mặt thật.",
                "liveness": liveness
            }), 403

        face_encoding = face_recognition.face_encodings(img_array, face_locations)[0]

        db = load_database()
        db[name] = {
            "encoding": face_encoding,
            "registered_at": datetime.now().isoformat()
        }
        save_database(db)

        print(f"[+] Đã đăng ký: {name} (liveness: {liveness.get('label', 'N/A')})")
        return jsonify({
            "success": True,
            "message": f"Đã đăng ký thành công: {name}",
            "user": name,
            "liveness": liveness
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/authenticate", methods=["POST"])
def authenticate():
    """
    Xác thực khuôn mặt VỚI Liveness Detection.

    Flow:
      1. Nhận ảnh
      2. Detect khuôn mặt
      3. *** LIVENESS CHECK *** → Nếu FAKE → TỪ CHỐI
      4. So khớp với database
      5. Trả kết quả
    """
    try:
        if request.is_json:
            data = request.get_json()
            image_data = data.get("image", "")
            if not image_data:
                return jsonify({"success": False, "error": "Thiếu image"}), 400
            img_array = decode_image(image_data)
        else:
            file = request.files.get("image")
            if not file:
                return jsonify({"success": False, "error": "Thiếu image"}), 400
            img_array = decode_image(file)

        # Step 1: Detect khuôn mặt
        face_locations = face_recognition.face_locations(img_array)
        if len(face_locations) == 0:
            return jsonify({
                "success": False,
                "authenticated": False,
                "error": "Không tìm thấy khuôn mặt"
            }), 400
        if len(face_locations) > 1:
            print(f"[!] Phát hiện {len(face_locations)} khuôn mặt - từ chối")
            return jsonify({
                "success": False,
                "authenticated": False,
                "error": f"Phát hiện {len(face_locations)} khuôn mặt. Vui lòng chỉ một người trước camera.",
                "num_faces": len(face_locations)
            }), 400

        # ============================================
        # Step 2: LIVENESS CHECK (BIỆN PHÁP PHÒNG VỆ)
        # ============================================
        liveness = check_liveness(img_array, face_locations[0])

        if liveness["status"] == "ENABLED" and not liveness["is_real"]:
            # !!! PHÁT HIỆN TẤN CÔNG - TỪ CHỐI !!!
            print(f"[ALERT] SPOOF DETECTED! Liveness: {liveness}")
            print(f"[ALERT] Tấn công đã bị chặn thành công!")
            return jsonify({
                "success": True,
                "authenticated": False,
                "blocked": True,
                "reason": "SPOOF_DETECTED",
                "message": "PHÁT HIỆN GIẢ MẠO! Yêu cầu bị từ chối.",
                "liveness": liveness
            }), 403

        # Step 3: So khớp khuôn mặt (chỉ nếu qua được liveness check)
        unknown_encoding = face_recognition.face_encodings(img_array, face_locations)[0]

        db = load_database()
        if not db:
            return jsonify({
                "success": False,
                "authenticated": False,
                "error": "Database trống"
            }), 400

        best_match = None
        best_distance = float("inf")

        for name, user_data in db.items():
            distance = np.linalg.norm(user_data["encoding"] - unknown_encoding)
            if distance < best_distance:
                best_distance = distance
                best_match = name

        if best_distance <= MATCH_THRESHOLD:
            print(f"[+] Xác thực THÀNH CÔNG: {best_match} "
                  f"(distance: {best_distance:.4f}, liveness: {liveness.get('label', 'N/A')})")
            return jsonify({
                "success": True,
                "authenticated": True,
                "user": best_match,
                "confidence": round(1 - best_distance, 4),
                "distance": round(best_distance, 4),
                "liveness_check": "PASSED",
                "liveness": liveness,
                "message": f"Xin chào, {best_match}! Xác thực thành công."
            })
        else:
            return jsonify({
                "success": True,
                "authenticated": False,
                "message": "Không khớp với bất kỳ ai.",
                "liveness_check": "PASSED",
                "liveness": liveness,
                "best_distance": round(best_distance, 4)
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/users", methods=["GET"])
def list_users():
    db = load_database()
    users = [{"name": n, "registered_at": d.get("registered_at", "N/A")}
             for n, d in db.items()]
    return jsonify({"users": users, "total": len(users)})


if __name__ == "__main__":
    os.makedirs(DB_DIR, exist_ok=True)

    print("=" * 60)
    print("  BIOMETRIC SECURITY LAB - SECURED Face Auth Server")
    print("  [+] LIVENESS DETECTION: ENABLED")
    print("=" * 60)

    liveness_ok = init_liveness()

    if not liveness_ok:
        print("\n[!] Liveness model chưa sẵn sàng.")
        print("[*] Server vẫn chạy nhưng KHÔNG có liveness protection.")
        print("[*] Để bật liveness:")
        print("    1. cd defender")
        print("    2. python create_dataset.py --class real --num 200")
        print("    3. python create_dataset.py --class fake --num 200")
        print("    4. python train_liveness.py")
        print("    5. Restart server này")

    print(f"\n  Database: {DB_FILE}")
    print(f"  Threshold: {MATCH_THRESHOLD}")
    print(f"  Liveness threshold: {LIVENESS_THRESHOLD}")
    print("=" * 60)

    app.run(host="0.0.0.0", port=5000, debug=True)

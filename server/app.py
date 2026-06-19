"""
Biometric Security Lab - Face Authentication Server (VULNERABLE VERSION)
=======================================================================
Server xác thực khuôn mặt cơ bản KHÔNG có Liveness Detection.
Dùng cho mục đích nghiên cứu/học tập bảo mật sinh trắc học.

Endpoints:
  GET  /            - Giao diện web
  POST /register    - Đăng ký khuôn mặt (name + image)
  POST /authenticate - Xác thực khuôn mặt (image)
  GET  /users       - Danh sách user đã đăng ký
"""

import os
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

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
CORS(app)

# Đường dẫn database
DB_DIR = os.path.join(os.path.dirname(__file__), "face_db")
DB_FILE = os.path.join(DB_DIR, "face_database.pkl")

# Ngưỡng so khớp khuôn mặt (euclidean distance)
# Giá trị càng nhỏ → yêu cầu càng giống, mặc định 0.6
MATCH_THRESHOLD = 0.6


def load_database():
    """Load face database từ file pickle."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    return {}


def save_database(db):
    """Lưu face database vào file pickle."""
    os.makedirs(DB_DIR, exist_ok=True)
    with open(DB_FILE, "wb") as f:
        pickle.dump(db, f)


def decode_image(image_data):
    """Decode ảnh từ base64 string hoặc file upload."""
    if isinstance(image_data, str):
        # Base64 encoded image
        if "," in image_data:
            image_data = image_data.split(",")[1]
        img_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(img_bytes))
    else:
        # File upload
        img = Image.open(image_data)

    # Chuyển sang RGB (loại bỏ alpha channel nếu có)
    img = img.convert("RGB")
    img_array = np.array(img)

    # Tự động tăng sáng nếu ảnh quá tối
    brightness = np.mean(img_array)
    if brightness < 80:
        print(f"[*] Ảnh tối (brightness={brightness:.0f}), đang tăng sáng...")
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge([l, a, b])
        img_array = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    return img_array


@app.route("/")
def index():
    return render_template("index.html", secured=False)


@app.route("/register", methods=["POST"])
def register():
    """
    Đăng ký khuôn mặt mới vào hệ thống.

    Input (JSON):  {"name": "Nguyen Van A", "image": "<base64>"}
    Input (Form):  name=... + file=image
    """
    try:
        # Lấy dữ liệu từ request
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

        # Tìm khuôn mặt trong ảnh
        face_locations = face_recognition.face_locations(img_array)
        if len(face_locations) == 0:
            return jsonify({
                "success": False,
                "error": "Không tìm thấy khuôn mặt trong ảnh"
            }), 400

        if len(face_locations) > 1:
            return jsonify({
                "success": False,
                "error": f"Phát hiện {len(face_locations)} khuôn mặt. Chỉ cho phép 1."
            }), 400

        # Tạo face encoding (128-dimensional vector)
        face_encoding = face_recognition.face_encodings(img_array, face_locations)[0]

        # Lưu vào database
        db = load_database()
        db[name] = {
            "encoding": face_encoding,
            "registered_at": datetime.now().isoformat()
        }
        save_database(db)

        print(f"[+] Đã đăng ký: {name}")
        return jsonify({
            "success": True,
            "message": f"Đã đăng ký thành công: {name}",
            "user": name
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/authenticate", methods=["POST"])
def authenticate():
    """
    Xác thực khuôn mặt.
    LƯU Ý: Phiên bản này KHÔNG có Liveness Detection → dễ bị tấn công.

    Input (JSON):  {"image": "<base64>"}
    Input (Form):  file=image
    """
    try:
        # Lấy ảnh từ request
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

        # Tìm khuôn mặt
        face_locations = face_recognition.face_locations(img_array)
        if len(face_locations) == 0:
            return jsonify({
                "success": False,
                "authenticated": False,
                "error": "Không tìm thấy khuôn mặt"
            }), 400

        # Lấy encoding của khuôn mặt cần xác thực
        unknown_encoding = face_recognition.face_encodings(img_array, face_locations)[0]

        # So khớp với database
        db = load_database()
        if not db:
            return jsonify({
                "success": False,
                "authenticated": False,
                "error": "Database trống. Chưa có ai đăng ký."
            }), 400

        best_match = None
        best_distance = float("inf")

        for name, user_data in db.items():
            distance = np.linalg.norm(user_data["encoding"] - unknown_encoding)
            if distance < best_distance:
                best_distance = distance
                best_match = name

        # Kiểm tra ngưỡng
        if best_distance <= MATCH_THRESHOLD:
            print(f"[+] Xác thực THÀNH CÔNG: {best_match} (distance: {best_distance:.4f})")
            return jsonify({
                "success": True,
                "authenticated": True,
                "user": best_match,
                "confidence": round(1 - best_distance, 4),
                "distance": round(best_distance, 4),
                "liveness_check": "DISABLED",  # Cảnh báo: không có liveness
                "message": f"Xin chào, {best_match}! Xác thực thành công."
            })
        else:
            print(f"[-] Xác thực THẤT BẠI (best: {best_match}, distance: {best_distance:.4f})")
            return jsonify({
                "success": True,
                "authenticated": False,
                "message": "Không khớp với bất kỳ ai trong hệ thống.",
                "best_distance": round(best_distance, 4)
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/users", methods=["GET"])
def list_users():
    """Liệt kê danh sách user đã đăng ký."""
    db = load_database()
    users = []
    for name, data in db.items():
        users.append({
            "name": name,
            "registered_at": data.get("registered_at", "N/A")
        })
    return jsonify({"users": users, "total": len(users)})


if __name__ == "__main__":
    os.makedirs(DB_DIR, exist_ok=True)
    print("=" * 60)
    print("  BIOMETRIC SECURITY LAB - Face Authentication Server")
    print("  [!] WARNING: NO LIVENESS DETECTION - VULNERABLE!")
    print("=" * 60)
    print(f"  Database: {DB_FILE}")
    print(f"  Threshold: {MATCH_THRESHOLD}")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)

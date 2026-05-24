# -*- coding: utf-8 -*-
"""Sinh các sơ đồ kiến trúc tiếng Việt cho báo cáo."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.font_manager import FontProperties

OUT = os.path.join(os.path.dirname(__file__), "_report_assets")
os.makedirs(OUT, exist_ok=True)

# Tìm font hỗ trợ tiếng Việt
def get_vn_font():
    candidates = [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
        r"C:\Windows\Fonts\times.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return FontProperties(fname=p)
    return None

VN = get_vn_font()
plt.rcParams["axes.unicode_minus"] = False

# ----------- Helper -----------
def box(ax, x, y, w, h, text, color="#1f77b4", fc=None, fontsize=10, text_color="white"):
    if fc is None:
        fc = color
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                          linewidth=1.5, edgecolor=color, facecolor=fc)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, color=text_color, fontproperties=VN, weight="bold")

def arrow(ax, x1, y1, x2, y2, color="black", text=None, style="->", lw=1.5, text_offset=(0,0.15), fs=9):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=15,
                        linewidth=lw, color=color)
    ax.add_patch(a)
    if text:
        mx = (x1 + x2) / 2 + text_offset[0]
        my = (y1 + y2) / 2 + text_offset[1]
        ax.text(mx, my, text, ha="center", va="center", fontsize=fs,
                color=color, fontproperties=VN)

# ============================================================
# Hình 3.1 - Mô hình client–server tổng thể (giai đoạn 1)
# ============================================================
fig, ax = plt.subplots(figsize=(13, 7.5))
ax.set_xlim(0, 13); ax.set_ylim(0, 8)
ax.axis("off")
ax.set_title("Hình 3.1. Mô hình kiến trúc client–server của hệ thống xác thực sinh trắc học",
             fontproperties=VN, fontsize=13, weight="bold")

# Client side
box(ax, 0.5, 5.2, 3, 1.6, "NGƯỜI DÙNG\n(Trình duyệt + Webcam)", color="#2c7fb8", fc="#41b6c4", fontsize=11)
box(ax, 0.5, 2.8, 3, 1.6, "CLIENT WEB\n(HTML/JS, getUserMedia)", color="#2c7fb8", fc="#7fcdbb", text_color="black", fontsize=11)

# Server side
box(ax, 5.2, 6.0, 3.2, 1.2, "FLASK SERVER\n(Python 3.10)", color="#225ea8", fc="#253494", fontsize=11)
box(ax, 5.2, 4.4, 3.2, 1.2, "API /authenticate\n/register · /users", color="#1d91c0", fc="#1d91c0", fontsize=10)
box(ax, 5.2, 2.8, 3.2, 1.2, "Module nhận diện\nface_recognition + dlib", color="#41b6c4", fc="#41b6c4", fontsize=10)
box(ax, 5.2, 1.2, 3.2, 1.2, "Tiền xử lý ảnh\n(OpenCV + CLAHE)", color="#7fcdbb", fc="#7fcdbb", text_color="black", fontsize=10)

# Database
box(ax, 9.6, 4.0, 3.0, 2.0, "CƠ SỞ DỮ LIỆU\nface_database.pkl\n(vector 128 chiều)", color="#cc4c02", fc="#fe9929", text_color="black", fontsize=11)
box(ax, 9.6, 1.2, 3.0, 1.6, "MÔ HÌNH PAD\nMobileNetV2\n(liveness_model.pth)", color="#cc4c02", fc="#fec44f", text_color="black", fontsize=10)

# Arrows
arrow(ax, 2.0, 5.2, 2.0, 4.4, color="#2c7fb8", text="Webcam stream", text_offset=(0, 0.05))
arrow(ax, 3.5, 3.6, 5.2, 5.0, color="#2c7fb8", text="POST ảnh\nbase64/JSON", text_offset=(-0.2, 0.0))
arrow(ax, 5.2, 4.6, 3.5, 3.6, color="#2c7fb8", style="->", text="JSON kết quả", text_offset=(-0.4, -0.2))
arrow(ax, 6.8, 4.4, 6.8, 4.0, color="#225ea8")
arrow(ax, 6.8, 2.8, 6.8, 2.4, color="#225ea8")
arrow(ax, 8.4, 5.0, 9.6, 5.0, color="#cc4c02", text="đọc/ghi\nencoding", text_offset=(0, 0.2))
arrow(ax, 8.4, 3.4, 9.6, 2.0, color="#cc4c02", text="(secured) load\nmodel .pth", text_offset=(0.0, 0.2))

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_3_1_kien_truc_tong_the.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 3.2 - Phiên bản chưa hoàn thiện (vulnerable)
# ============================================================
fig, ax = plt.subplots(figsize=(13, 5.5))
ax.set_xlim(0, 13); ax.set_ylim(0, 6)
ax.axis("off")
ax.set_title("Hình 3.2. Phiên bản server CHƯA HOÀN THIỆN — không có Liveness Detection",
             fontproperties=VN, fontsize=13, weight="bold", color="#990000")

steps = [
    (0.5, "Ảnh gửi tới\n/authenticate", "#1f78b4"),
    (3.0, "Phát hiện\nkhuôn mặt", "#33a02c"),
    (5.5, "Trích đặc trưng\n128-d", "#33a02c"),
    (8.0, "So khớp\nEuclidean", "#33a02c"),
    (10.5, "Trả Accept\n(authenticated=True)", "#e31a1c"),
]
for x, text, col in steps:
    box(ax, x, 3.0, 2.2, 1.4, text, color=col, fc=col, fontsize=10)

for i in range(len(steps) - 1):
    x1 = steps[i][0] + 2.2
    x2 = steps[i+1][0]
    arrow(ax, x1, 3.7, x2, 3.7, color="black")

# Cảnh báo
box(ax, 1.0, 0.5, 11.0, 1.6,
    "KHÔNG có bước kiểm tra sống (Liveness Detection)\n→ Toàn bộ ảnh in, ảnh điện thoại, replay đều được chấp nhận",
    color="#990000", fc="#fdd0a2", text_color="#990000", fontsize=12)

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_3_2_server_vulnerable.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 3.3 - Quy trình tấn công Replay/Injection
# ============================================================
fig, ax = plt.subplots(figsize=(13, 7.5))
ax.set_xlim(0, 13); ax.set_ylim(0, 8)
ax.axis("off")
ax.set_title("Hình 3.3. Mô hình tấn công Replay và Injection vào API xác thực",
             fontproperties=VN, fontsize=13, weight="bold", color="#990000")

# Attacker
box(ax, 0.5, 5.5, 3.0, 1.5, "KẺ TẤN CÔNG\n(script Python)", color="#a50f15", fc="#cb181d", fontsize=11)
# Stolen data
box(ax, 0.5, 3.2, 3.0, 1.5, "Ảnh nạn nhân\nrò rỉ từ MXH", color="#a50f15", fc="#fb6a4a", fontsize=10)
# Tools
box(ax, 0.5, 1.0, 3.0, 1.5, "curl / Postman\n/ requests.py", color="#a50f15", fc="#fcae91", text_color="black", fontsize=10)

# Network
box(ax, 4.2, 3.5, 2.5, 1.2, "Mạng HTTP/HTTPS\nkhông xác thực\nthiết bị", color="#525252", fc="#969696", fontsize=10)

# Server vulnerable
box(ax, 7.5, 5.5, 3.0, 1.5, "SERVER\nvulnerable", color="#08519c", fc="#2171b5", fontsize=11)
box(ax, 7.5, 3.5, 3.0, 1.2, "POST /authenticate\nimage = base64", color="#08519c", fc="#6baed6", text_color="black", fontsize=10)
box(ax, 7.5, 1.5, 3.0, 1.2, "So khớp 128-d\n(không liveness)", color="#08519c", fc="#bdd7e7", text_color="black", fontsize=10)

# Result
box(ax, 11.0, 3.0, 1.8, 1.6, "200 OK\nAUTH = TRUE", color="#cb181d", fc="#fb6a4a", fontsize=11)

arrow(ax, 3.5, 6.2, 7.5, 6.2, color="#a50f15", text="① gửi ảnh giả", text_offset=(0, 0.2))
arrow(ax, 3.5, 4.0, 4.2, 4.0, color="#a50f15")
arrow(ax, 6.7, 4.0, 7.5, 4.0, color="#a50f15", text="② vượt qua\ntầng mạng", text_offset=(0, 0.5))
arrow(ax, 9.0, 3.5, 9.0, 2.7, color="#08519c")
arrow(ax, 10.5, 2.1, 11.0, 3.5, color="#cb181d", text="③ bypass\nthành công", text_offset=(0.5, 0.1))

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_3_3_attack_replay_injection.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 4.3 - Phiên bản đã gia cố (secured)
# ============================================================
fig, ax = plt.subplots(figsize=(13, 6.5))
ax.set_xlim(0, 13); ax.set_ylim(0, 7)
ax.axis("off")
ax.set_title("Hình 4.3. Phiên bản server ĐÃ GIA CỐ — tích hợp Liveness Detection (MobileNetV2)",
             fontproperties=VN, fontsize=13, weight="bold", color="#006d2c")

# Pipeline secured: input -> face detect -> liveness -> match -> result
boxes = [
    (0.3, "Ảnh gửi tới\n/authenticate", "#1f78b4"),
    (2.4, "Phát hiện\nkhuôn mặt", "#33a02c"),
    (4.5, "LIVENESS CHECK\nMobileNetV2\nngưỡng 0.7", "#006d2c"),
    (7.0, "Trích đặc trưng\n128-d", "#33a02c"),
    (9.1, "So khớp\nEuclidean", "#33a02c"),
    (11.2, "Accept hoặc\nReject", "#08519c"),
]
for x, text, col in boxes:
    box(ax, x, 4.0, 1.9, 1.6, text, color=col, fc=col, fontsize=9)

for i in range(len(boxes) - 1):
    x1 = boxes[i][0] + 1.9
    x2 = boxes[i+1][0]
    arrow(ax, x1, 4.8, x2, 4.8, color="black")

# Reject branch from Liveness
box(ax, 4.8, 1.0, 1.9, 1.4, "HTTP 403\nspoof_detected=true", color="#a50f15", fc="#cb181d", fontsize=9)
arrow(ax, 5.45, 4.0, 5.7, 2.4, color="#a50f15", text="REAL < 0.7", text_offset=(0.5, 0.0))

# Layer note
box(ax, 0.5, 0.1, 12.0, 0.7,
    "Hai lớp phòng vệ: ① Liveness Detection chặn ảnh giả   ② So khớp đặc trưng xác minh danh tính",
    color="#006d2c", fc="#c7e9c0", text_color="#006d2c", fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_4_3_server_secured.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 2.1 - Quy trình xác thực sinh trắc học tổng quát
# ============================================================
fig, ax = plt.subplots(figsize=(13, 5))
ax.set_xlim(0, 13); ax.set_ylim(0, 5)
ax.axis("off")
ax.set_title("Hình 2.1. Quy trình tổng quát của hệ thống xác thực sinh trắc học",
             fontproperties=VN, fontsize=13, weight="bold")
steps = [
    "Thu nhận\ntín hiệu",
    "Tiền xử lý",
    "Kiểm tra\nsống (PAD)",
    "Trích xuất\nđặc trưng",
    "So khớp\nvới CSDL",
    "Quyết định\nAccept/Reject",
]
colors = ["#1d91c0","#7fcdbb","#006d2c","#41b6c4","#225ea8","#e31a1c"]
for i, (text, c) in enumerate(zip(steps, colors)):
    x = 0.3 + i * 2.1
    box(ax, x, 2.0, 1.9, 1.6, text, color=c, fc=c, fontsize=10)
    if i < len(steps) - 1:
        arrow(ax, x+1.9, 2.8, x+2.1, 2.8, color="black")

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_2_1_quy_trinh_bio.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 2.2 - Phân loại tấn công theo ISO/IEC 30107
# ============================================================
fig, ax = plt.subplots(figsize=(13, 7))
ax.set_xlim(0, 13); ax.set_ylim(0, 7)
ax.axis("off")
ax.set_title("Hình 2.2. Phân loại tấn công sinh trắc học theo ISO/IEC 30107",
             fontproperties=VN, fontsize=13, weight="bold")

box(ax, 4.5, 5.5, 4.0, 1.2, "TẤN CÔNG SINH TRẮC HỌC", color="#08306b", fc="#08519c", fontsize=12)
# Two main branches
box(ax, 0.5, 3.5, 5.5, 1.4, "Tấn công trình diện\n(Presentation Attack)", color="#a50f15", fc="#cb181d", fontsize=11)
box(ax, 7.0, 3.5, 5.5, 1.4, "Tấn công kỹ thuật số\n(Digital / Injection)", color="#7a0177", fc="#ae017e", fontsize=11)

arrow(ax, 5.5, 5.5, 3.0, 4.9, color="black")
arrow(ax, 7.5, 5.5, 9.7, 4.9, color="black")

# Sub-branches
pa_subs = [(0.2, "Ảnh in"), (1.6, "Ảnh điện thoại"), (3.2, "Mặt nạ 3D"), (4.7, "Video replay")]
for x, t in pa_subs:
    box(ax, x, 1.5, 1.4, 1.2, t, color="#a50f15", fc="#fb6a4a", fontsize=9)
    arrow(ax, x+0.7, 2.7, x+0.7, 3.5, color="black", lw=1)

inj_subs = [(7.2, "Replay\nbase64"), (8.6, "Bypass API"), (10.0, "Deepfake\nGAN"), (11.4, "Tampering\nfeature vector")]
for x, t in inj_subs:
    box(ax, x, 1.5, 1.4, 1.2, t, color="#7a0177", fc="#df65b0", fontsize=9)
    arrow(ax, x+0.7, 2.7, x+0.7, 3.5, color="black", lw=1)

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_2_2_phan_loai_tan_cong.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 2.4 - Vị trí tấn công Injection trong pipeline ISO/IEC 30107
# ============================================================
fig, ax = plt.subplots(figsize=(13, 6))
ax.set_xlim(0, 13); ax.set_ylim(0, 6)
ax.axis("off")
ax.set_title("Hình 2.4. Vị trí 5 điểm tấn công Injection trong pipeline ISO/IEC 30107",
             fontproperties=VN, fontsize=13, weight="bold")

stages = [
    (0.3, "Cảm biến\n(Camera)"),
    (2.6, "Tiền xử lý"),
    (4.9, "Trích đặc\ntrưng"),
    (7.2, "So khớp"),
    (9.5, "Quyết định"),
    (11.5, "Ứng dụng"),
]
for x, t in stages:
    box(ax, x, 3.0, 1.5, 1.2, t, color="#1f78b4", fc="#1f78b4", fontsize=10)
arrow(ax, 1.8, 3.6, 2.6, 3.6, color="black")
arrow(ax, 4.1, 3.6, 4.9, 3.6, color="black")
arrow(ax, 6.4, 3.6, 7.2, 3.6, color="black")
arrow(ax, 8.7, 3.6, 9.5, 3.6, color="black")
arrow(ax, 11.0, 3.6, 11.5, 3.6, color="black")

# Attack points 1..5
attack_points = [
    (1.05, 5.0, "P1\nĐầu vào\ncảm biến"),
    (3.35, 5.0, "P2\nKênh truyền\ndữ liệu"),
    (5.65, 5.0, "P3\nBộ trích\nđặc trưng"),
    (7.95, 5.0, "P4\nKênh template\n– matcher"),
    (10.25, 5.0, "P5\nKênh kết quả\nmatcher"),
]
for x, y, t in attack_points:
    box(ax, x-0.6, y-0.5, 1.5, 1.0, t, color="#cb181d", fc="#fb6a4a", fontsize=8)
    arrow(ax, x+0.15, y-0.5, x+0.15, 4.2, color="#cb181d", lw=1.2)

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_2_4_injection_pipeline.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 4.4 - Biểu đồ so sánh FAR/FRR/APCER
# ============================================================
import numpy as np
fig, ax = plt.subplots(figsize=(11, 6))
metrics = ["FAR", "FRR", "APCER", "BPCER", "Thời gian (ms/100)"]
vuln = [100, 0, 100, 0, 1.20]
sec = [2, 5, 1.5, 4.8, 1.80]
x = np.arange(len(metrics))
w = 0.36
ax.bar(x - w/2, vuln, width=w, color="#cb181d", label="Server vulnerable")
ax.bar(x + w/2, sec, width=w, color="#006d2c", label="Server secured")
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontproperties=VN, fontsize=11)
ax.set_ylabel("Giá trị (%) hoặc thời gian chuẩn hóa", fontproperties=VN, fontsize=11)
ax.set_title("Hình 4.4. So sánh FAR / FRR / APCER / BPCER trước và sau Liveness Detection",
             fontproperties=VN, fontsize=13, weight="bold")
ax.legend(prop=VN, fontsize=11)
ax.grid(axis="y", alpha=0.3)
for i, v in enumerate(vuln):
    ax.text(i - w/2, v + 1, str(v), ha="center", fontsize=9)
for i, v in enumerate(sec):
    ax.text(i + w/2, v + 1, str(v), ha="center", fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_4_4_so_sanh_chi_so.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 4.5 - Các lớp phòng vệ chống Injection
# ============================================================
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12); ax.set_ylim(0, 7.5)
ax.axis("off")
ax.set_title("Hình 4.5. Các lớp phòng vệ chống Injection Attack trên hệ thống sinh trắc học",
             fontproperties=VN, fontsize=13, weight="bold")
layers = [
    ("L1 — Xác thực thiết bị (device attestation, TLS)", "#08519c"),
    ("L2 — Ký số ảnh tại client + nonce chống replay", "#225ea8"),
    ("L3 — Liveness Detection (MobileNetV2)", "#006d2c"),
    ("L4 — Kiểm tra ngưỡng + log audit", "#cc4c02"),
    ("L5 — Giám sát bất thường + rate-limit", "#a50f15"),
]
for i, (text, c) in enumerate(layers):
    y = 6.0 - i * 1.1
    box(ax, 1.5, y, 9.0, 0.9, text, color=c, fc=c, fontsize=11)

# Attacker arrow
ax.annotate("", xy=(1.0, 5.4), xytext=(1.0, 0.6),
            arrowprops=dict(arrowstyle="->", color="#a50f15", lw=2))
ax.text(0.7, 3.0, "Attacker", fontproperties=VN, fontsize=11, color="#a50f15", rotation=90)

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_4_5_lop_phong_ve.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 2.3 - MobileNetV2 inverted residual
# ============================================================
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_xlim(0, 12); ax.set_ylim(0, 5)
ax.axis("off")
ax.set_title("Hình 2.3. Kiến trúc MobileNetV2 và khối Inverted Residual",
             fontproperties=VN, fontsize=13, weight="bold")
seq = [
    ("Input\n224×224×3", "#1d91c0"),
    ("Conv 3×3\nstride 2", "#41b6c4"),
    ("17 khối\nInverted\nResidual", "#225ea8"),
    ("Conv 1×1\n1280-d", "#41b6c4"),
    ("AvgPool\n+ Dropout", "#7fcdbb"),
    ("FC 1280→256\nReLU", "#fec44f"),
    ("FC 256→2\n(REAL/FAKE)", "#cb181d"),
]
for i, (t, c) in enumerate(seq):
    x = 0.3 + i * 1.7
    box(ax, x, 1.8, 1.55, 1.6, t, color=c, fc=c, fontsize=9, text_color="white" if c not in ["#fec44f","#7fcdbb"] else "black")
    if i < len(seq) - 1:
        arrow(ax, x+1.55, 2.6, x+1.7, 2.6, color="black")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_2_3_mobilenetv2.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 2.5 - PA vs Digital Injection
# ============================================================
fig, ax = plt.subplots(figsize=(13, 6))
ax.set_xlim(0, 13); ax.set_ylim(0, 6)
ax.axis("off")
ax.set_title("Hình 2.5. So sánh Presentation Attack và Digital Injection Attack",
             fontproperties=VN, fontsize=13, weight="bold")
# PA
box(ax, 0.5, 4.5, 5.5, 1.0, "PRESENTATION ATTACK", color="#a50f15", fc="#cb181d", fontsize=12)
box(ax, 0.5, 3.0, 1.5, 1.0, "Attacker", color="#a50f15", fc="#fb6a4a", fontsize=10)
box(ax, 2.3, 3.0, 1.5, 1.0, "Vật chứa giả\n(in/màn hình)", color="#a50f15", fc="#fb6a4a", fontsize=9)
box(ax, 4.1, 3.0, 1.7, 1.0, "Camera\n(cảm biến)", color="#08519c", fc="#6baed6", fontsize=9)
arrow(ax, 2.0, 3.5, 2.3, 3.5, color="black")
arrow(ax, 3.8, 3.5, 4.1, 3.5, color="black")
ax.text(3.25, 1.5, "Tấn công ở phần CỨNG\n(trước cảm biến)", ha="center", fontproperties=VN, fontsize=10, color="#a50f15")

# Injection
box(ax, 7.0, 4.5, 5.5, 1.0, "DIGITAL / INJECTION ATTACK", color="#7a0177", fc="#ae017e", fontsize=12)
box(ax, 7.0, 3.0, 1.5, 1.0, "Attacker", color="#7a0177", fc="#df65b0", fontsize=10)
box(ax, 8.8, 3.0, 1.7, 1.0, "API HTTP\n/authenticate", color="#08519c", fc="#6baed6", fontsize=9)
box(ax, 10.8, 3.0, 1.7, 1.0, "Server\nbackend", color="#08519c", fc="#2171b5", fontsize=9)
arrow(ax, 8.5, 3.5, 8.8, 3.5, color="black")
arrow(ax, 10.5, 3.5, 10.8, 3.5, color="black")
ax.text(9.75, 1.5, "Tấn công ở tầng PHẦN MỀM\n(không cần cảm biến)", ha="center", fontproperties=VN, fontsize=10, color="#7a0177")

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_2_5_pa_vs_injection.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 3.4 - Mô hình tấn công Injection chi tiết
# ============================================================
fig, ax = plt.subplots(figsize=(13, 7))
ax.set_xlim(0, 13); ax.set_ylim(0, 7)
ax.axis("off")
ax.set_title("Hình 3.4. Mô hình tấn công Injection qua API xác thực khuôn mặt",
             fontproperties=VN, fontsize=13, weight="bold", color="#7a0177")

box(ax, 0.5, 5.0, 2.5, 1.5, "Attacker\n(Python/curl)", color="#a50f15", fc="#cb181d", fontsize=11)
box(ax, 0.5, 2.5, 2.5, 1.5, "Kho ảnh giả\nvictim_photos/*.jpg", color="#a50f15", fc="#fb6a4a", fontsize=10)
box(ax, 0.5, 0.5, 2.5, 1.2, "Script\n03_injection_attack.py", color="#a50f15", fc="#fcae91", text_color="black", fontsize=9)

box(ax, 4.0, 4.5, 2.0, 1.2, "JSON payload\n{image: base64}", color="#525252", fc="#969696", fontsize=10)
box(ax, 4.0, 2.5, 2.0, 1.2, "POST /authenticate\nContent-Type: JSON", color="#525252", fc="#bdbdbd", text_color="black", fontsize=10)

box(ax, 7.0, 4.5, 3.0, 1.2, "Server vulnerable\napp.py:150 /authenticate", color="#08519c", fc="#2171b5", fontsize=10)
box(ax, 7.0, 2.5, 3.0, 1.2, "face_recognition\nso khớp 128-d", color="#08519c", fc="#6baed6", text_color="black", fontsize=10)
box(ax, 7.0, 0.5, 3.0, 1.2, "200 OK\nauthenticated=True", color="#cb181d", fc="#fb6a4a", fontsize=10)

box(ax, 10.5, 2.5, 2.2, 1.2, "Database\nface_database.pkl", color="#cc4c02", fc="#fe9929", text_color="black", fontsize=10)

arrow(ax, 3.0, 5.7, 4.0, 5.1, color="#a50f15", text="① đọc ảnh", text_offset=(-0.3, 0.2))
arrow(ax, 3.0, 3.2, 4.0, 3.1, color="#a50f15")
arrow(ax, 6.0, 5.1, 7.0, 5.1, color="#a50f15", text="② POST", text_offset=(0, 0.2))
arrow(ax, 6.0, 3.1, 7.0, 3.1, color="#a50f15")
arrow(ax, 8.5, 4.5, 8.5, 3.7, color="#08519c")
arrow(ax, 8.5, 2.5, 8.5, 1.7, color="#08519c", text="③ match", text_offset=(0.3, 0.0))
arrow(ax, 10.0, 3.1, 10.5, 3.1, color="#cc4c02")
arrow(ax, 10.5, 3.1, 10.0, 3.1, color="#cc4c02", style="<-")

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_3_4_injection_chi_tiet.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 4.1 - Bộ dữ liệu Real/Fake
# ============================================================
fig, ax = plt.subplots(figsize=(11, 5))
ax.set_xlim(0, 11); ax.set_ylim(0, 5)
ax.axis("off")
ax.set_title("Hình 4.1. Bộ dữ liệu Real (200 ảnh) và Fake (200 ảnh) dùng huấn luyện MobileNetV2",
             fontproperties=VN, fontsize=13, weight="bold")
box(ax, 0.5, 1.5, 4.5, 2.5, "DATASET REAL\n200 ảnh khuôn mặt thật\nchụp trực tiếp từ webcam\n(đa dạng góc, ánh sáng)", color="#006d2c", fc="#41ab5d", fontsize=12)
box(ax, 6.0, 1.5, 4.5, 2.5, "DATASET FAKE\n200 ảnh giả mạo: ảnh in,\nảnh điện thoại, ảnh chụp lại\nmàn hình máy tính", color="#a50f15", fc="#cb181d", fontsize=12)
ax.text(5.5, 0.7, "Tỷ lệ chia: 80% train · 10% val · 10% test  (giữ cân bằng REAL/FAKE)",
        ha="center", fontproperties=VN, fontsize=11, weight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_4_1_dataset.png"), dpi=170, bbox_inches="tight")
plt.close()

# ============================================================
# Hình 5.1 - Lộ trình hoàn thiện hệ thống (Roadmap)
# ============================================================
fig, ax = plt.subplots(figsize=(13, 6.5))
ax.set_xlim(0, 13); ax.set_ylim(0, 6.5)
ax.axis("off")
ax.set_title("Hình 5.1. Lộ trình hoàn thiện hệ thống xác thực sinh trắc học",
             fontproperties=VN, fontsize=13, weight="bold")
phases = [
    (0.3, "Giai đoạn 1\nDựng server cơ bản\n(face_recognition)", "#fdae6b"),
    (3.0, "Giai đoạn 2\nThực hiện tấn công\n(spoof, replay, inject)", "#cb181d"),
    (5.7, "Giai đoạn 3\nThu thập dữ liệu\nReal/Fake", "#9e9ac8"),
    (8.4, "Giai đoạn 4\nHuấn luyện MobileNetV2\n(transfer learning)", "#3182bd"),
    (11.1, "Giai đoạn 5\nTích hợp + đo đạc\nFAR/FRR/APCER", "#006d2c"),
]
for x, t, c in phases:
    box(ax, x, 3.5, 2.5, 2.0, t, color=c, fc=c, fontsize=10)
for i in range(len(phases) - 1):
    x1 = phases[i][0] + 2.5
    x2 = phases[i+1][0]
    arrow(ax, x1, 4.5, x2, 4.5, color="black")

box(ax, 0.5, 0.7, 12.0, 1.6,
    "Mỗi giai đoạn đều có deliverable rõ ràng: code commit, dataset .zip, model .pth, biểu đồ kết quả.\n"
    "Chu trình lặp lại: Tấn công → Học từ thất bại → Cải thiện phòng vệ → Đo lại các chỉ số.",
    color="#252525", fc="#f0f0f0", text_color="black", fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_5_1_lo_trinh.png"), dpi=170, bbox_inches="tight")
plt.close()

print("DONE")
print(os.listdir(OUT))

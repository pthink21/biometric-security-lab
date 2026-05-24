# -*- coding: utf-8 -*-
"""Sơ đồ tiến trình hệ thống server: chưa hoàn thiện -> bị tấn công -> đã bảo mật.
Tiếng Việt có dấu, font Segoe UI/Arial Unicode để hiển thị đúng.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.font_manager import FontProperties

OUT = os.path.join(os.path.dirname(__file__), "_report_assets")
os.makedirs(OUT, exist_ok=True)


def vn_font(size=11, bold=False):
    for p in [r"C:\Windows\Fonts\segoeui.ttf",
              r"C:\Windows\Fonts\arial.ttf",
              r"C:\Windows\Fonts\tahoma.ttf"]:
        if os.path.exists(p):
            fp = FontProperties(fname=p, size=size)
            if bold:
                # try bold variant
                bold_path = p.replace(".ttf", "b.ttf")
                if os.path.exists(bold_path):
                    fp = FontProperties(fname=bold_path, size=size, weight="bold")
                else:
                    fp = FontProperties(fname=p, size=size, weight="bold")
            return fp
    return FontProperties(size=size, weight=("bold" if bold else "normal"))


# ======================================================================
# Hình tổng: 3 giai đoạn nằm theo chiều dọc, mỗi giai đoạn 1 mini-sơ đồ
# ======================================================================
fig, ax = plt.subplots(figsize=(15, 18))
ax.set_xlim(0, 15)
ax.set_ylim(0, 18)
ax.axis("off")
ax.set_facecolor("white")

ax.text(7.5, 17.55,
        "Tiến trình phát triển hệ thống xác thực sinh trắc học",
        ha="center", va="center",
        fontproperties=vn_font(17, True), color="#1a1a1a")
ax.text(7.5, 17.15,
        "Giai đoạn 1 — Chưa hoàn thiện   →   Giai đoạn 2 — Bị tấn công   →   Giai đoạn 3 — Đã được bảo mật",
        ha="center", va="center",
        fontproperties=vn_font(11, False), color="#444")


def draw_server(ax, cx, cy, w, h, label, color, edge, sub=None):
    rect = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                          boxstyle="round,pad=0.04,rounding_size=0.1",
                          linewidth=1.6, edgecolor=edge, facecolor=color)
    ax.add_patch(rect)
    ax.text(cx, cy + (h/2 - 0.35), label,
            ha="center", va="center",
            fontproperties=vn_font(11, True), color="white")
    if sub:
        for i, line in enumerate(sub):
            ax.text(cx, cy + (h/2 - 0.85) - i*0.32, line,
                    ha="center", va="center",
                    fontproperties=vn_font(9, False), color="#f5f5f5")


def draw_client(ax, cx, cy, label, color="#3a6ea5", sub=None):
    rect = FancyBboxPatch((cx - 1.0, cy - 0.55), 2.0, 1.1,
                          boxstyle="round,pad=0.04,rounding_size=0.08",
                          linewidth=1.4, edgecolor="#1a3a5e", facecolor=color)
    ax.add_patch(rect)
    ax.text(cx, cy + 0.18, label,
            ha="center", fontproperties=vn_font(10, True), color="white")
    if sub:
        ax.text(cx, cy - 0.22, sub,
                ha="center", fontproperties=vn_font(8.5, False), color="#eaeaea")


def draw_attacker(ax, cx, cy, label="Kẻ tấn công"):
    rect = FancyBboxPatch((cx - 1.0, cy - 0.55), 2.0, 1.1,
                          boxstyle="round,pad=0.04,rounding_size=0.08",
                          linewidth=1.6, edgecolor="#7a0000", facecolor="#cc2222")
    ax.add_patch(rect)
    ax.text(cx, cy + 0.18, label,
            ha="center", fontproperties=vn_font(10, True), color="white")
    ax.text(cx, cy - 0.22, "(attacker)",
            ha="center", fontproperties=vn_font(8.5, False), color="#fff0f0")


def arrow(ax, x1, y1, x2, y2, label="", color="#222", style="-|>", lw=1.6,
          rad=0.0, label_color=None, label_size=9, dash=False):
    ls = (0, (5, 3)) if dash else "-"
    a = FancyArrowPatch((x1, y1), (x2, y2),
                        arrowstyle=style, color=color, linewidth=lw,
                        connectionstyle=f"arc3,rad={rad}",
                        linestyle=ls,
                        mutation_scale=14)
    ax.add_patch(a)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.18, label,
                ha="center", fontproperties=vn_font(label_size, True),
                color=label_color or color,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=1.4))


# --- GIAI ĐOẠN 1: Chưa hoàn thiện ---
y0 = 14.8
ax.add_patch(patches.Rectangle((0.4, y0 - 1.9), 14.2, 2.8,
                               linewidth=1.2, edgecolor="#fdae6b",
                               facecolor="#fff5e6"))
ax.text(0.7, y0 + 0.65,
        "GIAI ĐOẠN 1 — Hệ thống chưa hoàn thiện",
        fontproperties=vn_font(13, True), color="#a3590b")
ax.text(0.7, y0 + 0.30,
        "Chỉ có chức năng đăng ký + so khớp khuôn mặt. Chưa có kiểm tra sống. "
        "Chưa kiểm tra nguồn ảnh.",
        fontproperties=vn_font(9.5, False), color="#6a3f00")

draw_client(ax, 2.2, y0 - 0.6, "Trình duyệt", color="#4a90c8",
            sub="getUserMedia / webcam")
draw_server(ax, 6.5, y0 - 0.6, 3.6, 1.8,
            "Server vulnerable (Flask)",
            "#5a8ab8", "#1a3a5e",
            sub=["/register, /authenticate",
                 "face_recognition (dlib)",
                 "Match khoảng cách Euclidean",
                 "KHÔNG có Liveness"])
db1 = patches.FancyBboxPatch((10.7, y0 - 1.2), 2.6, 1.2,
                             boxstyle="round,pad=0.04,rounding_size=0.06",
                             linewidth=1.4, edgecolor="#3b3b3b",
                             facecolor="#444")
ax.add_patch(db1)
ax.text(12.0, y0 - 0.4, "face_database.pkl",
        ha="center", fontproperties=vn_font(10, True), color="white")
ax.text(12.0, y0 - 0.85, "{name, encoding 128-d}",
        ha="center", fontproperties=vn_font(8.5, False), color="#dcdcdc")

arrow(ax, 3.25, y0 - 0.6, 4.7, y0 - 0.6, "ảnh khuôn mặt", color="#1a3a5e")
arrow(ax, 8.32, y0 - 0.6, 10.7, y0 - 0.6, "encoding", color="#1a3a5e")

# --- GIAI ĐOẠN 2: Bị tấn công ---
y1 = 10.0
ax.add_patch(patches.Rectangle((0.4, y1 - 2.7), 14.2, 3.6,
                               linewidth=1.2, edgecolor="#cb181d",
                               facecolor="#ffecec"))
ax.text(0.7, y1 + 0.65,
        "GIAI ĐOẠN 2 — Hệ thống bị tấn công thực tế",
        fontproperties=vn_font(13, True), color="#a30b0b")
ax.text(0.7, y1 + 0.30,
        "Kẻ tấn công khai thác lỗ hổng: spoofing ảnh in / màn hình điện thoại, "
        "replay & injection trực tiếp qua API.",
        fontproperties=vn_font(9.5, False), color="#6a0000")

draw_attacker(ax, 2.2, y1 - 0.6)
draw_server(ax, 6.5, y1 - 0.6, 3.6, 1.8,
            "Server vulnerable",
            "#a8546a", "#7a0000",
            sub=["Không phân biệt ảnh thật/giả",
                 "Trả về authenticated = True",
                 "liveness_check: DISABLED"])
db2 = patches.FancyBboxPatch((10.7, y1 - 1.2), 2.6, 1.2,
                             boxstyle="round,pad=0.04,rounding_size=0.06",
                             linewidth=1.4, edgecolor="#3b3b3b",
                             facecolor="#3a3a3a")
ax.add_patch(db2)
ax.text(12.0, y1 - 0.4, "face_database.pkl",
        ha="center", fontproperties=vn_font(10, True), color="white")
ax.text(12.0, y1 - 0.85, "(7 user bị lộ qua /users)",
        ha="center", fontproperties=vn_font(8.5, False), color="#ffd0d0")

arrow(ax, 3.25, y1 - 0.4, 4.7, y1 - 0.4, "Ảnh in / điện thoại",
      color="#cb181d", rad=0.15)
arrow(ax, 3.25, y1 - 0.8, 4.7, y1 - 0.8, "POST /authenticate (Injection)",
      color="#cb181d", rad=-0.15)
arrow(ax, 8.32, y1 - 0.6, 10.7, y1 - 0.6, "Match thành công",
      color="#cb181d", label_size=9)

# Vector tấn công liệt kê dưới
attacks = [
    "1. Presentation: ảnh giấy / điện thoại / màn hình",
    "2. Replay: gửi lại ảnh đã chụp lén",
    "3. Injection: bypass camera, gọi thẳng API",
    "4. Threshold abuse: nâng MATCH_THRESHOLD"
]
for i, t in enumerate(attacks):
    ax.text(0.85, y1 - 1.55 - i*0.25, t,
            fontproperties=vn_font(9, False), color="#7a0000")

# --- GIAI ĐOẠN 3: Đã được bảo mật ---
y2 = 4.5
ax.add_patch(patches.Rectangle((0.4, y2 - 2.7), 14.2, 4.5,
                               linewidth=1.2, edgecolor="#006d2c",
                               facecolor="#e8f6ec"))
ax.text(0.7, y2 + 1.55,
        "GIAI ĐOẠN 3 — Hệ thống đã được bảo mật (gia cố)",
        fontproperties=vn_font(13, True), color="#0b5c1f")
ax.text(0.7, y2 + 1.20,
        "Tích hợp Liveness Detection (MobileNetV2) ở đầu pipeline + xác thực thiết bị + log giám sát.",
        fontproperties=vn_font(9.5, False), color="#0b5c1f")

draw_client(ax, 1.7, y2 - 0.2, "Client tin cậy",
            color="#3a8c5c", sub="ảnh từ webcam")
draw_attacker(ax, 1.7, y2 - 1.7)

# pipeline server
def stage(ax, cx, cy, label, color, edge):
    rect = FancyBboxPatch((cx - 0.95, cy - 0.5), 1.9, 1.0,
                          boxstyle="round,pad=0.04,rounding_size=0.08",
                          linewidth=1.4, edgecolor=edge, facecolor=color)
    ax.add_patch(rect)
    ax.text(cx, cy, label, ha="center", va="center",
            fontproperties=vn_font(9.5, True), color="white")

stage(ax, 4.6, y2 - 0.2, "Phát hiện\nkhuôn mặt", "#3182bd", "#0b3666")
stage(ax, 6.8, y2 - 0.2, "Liveness\nDetection\n(MobileNetV2)", "#0b5c1f", "#063612")
stage(ax, 9.0, y2 - 0.2, "Trích đặc trưng\n128-d", "#3182bd", "#0b3666")
stage(ax, 11.2, y2 - 0.2, "Match\n+ ngưỡng", "#3182bd", "#0b3666")

arrow(ax, 2.7, y2 - 0.2, 3.65, y2 - 0.2, color="#0b5c1f")
arrow(ax, 5.55, y2 - 0.2, 5.85, y2 - 0.2, color="#0b5c1f")
arrow(ax, 7.75, y2 - 0.2, 8.05, y2 - 0.2, color="#0b5c1f")
arrow(ax, 9.95, y2 - 0.2, 10.25, y2 - 0.2, color="#0b5c1f")

# DB secured
db3 = patches.FancyBboxPatch((12.6, y2 - 0.7), 2.2, 1.0,
                             boxstyle="round,pad=0.04,rounding_size=0.06",
                             linewidth=1.4, edgecolor="#0b3666",
                             facecolor="#3a3a3a")
ax.add_patch(db3)
ax.text(13.7, y2 - 0.05, "face_database",
        ha="center", fontproperties=vn_font(9.5, True), color="white")
ax.text(13.7, y2 - 0.45, "(read-only check)",
        ha="center", fontproperties=vn_font(8.5, False), color="#dcdcdc")
arrow(ax, 12.15, y2 - 0.2, 12.6, y2 - 0.2, color="#0b5c1f")

# Attacker bị chặn ở Liveness
arrow(ax, 2.7, y2 - 1.7, 6.0, y2 - 0.6, color="#cb181d", rad=-0.15,
      label="ảnh giả", label_size=8.5)
ax.text(6.8, y2 - 1.05, "Bị chặn",
        ha="center", fontproperties=vn_font(10, True), color="#a30b0b")
ax.add_patch(patches.Circle((6.8, y2 - 0.85), 0.18,
                            edgecolor="#a30b0b", facecolor="white", linewidth=1.8))
ax.plot([6.67, 6.93], [y2 - 0.98, y2 - 0.72],
        color="#a30b0b", linewidth=1.8)
ax.plot([6.67, 6.93], [y2 - 0.72, y2 - 0.98],
        color="#a30b0b", linewidth=1.8)

# Ghi chú phòng vệ ở dưới
defenses = [
    "• Kiểm tra sống: ngưỡng xác suất Real ≥ 0.7  → trả HTTP 403 nếu phát hiện tấn công",
    "• Xác thực thiết bị (device attestation) + chữ ký số ảnh tại client",
    "• Mã hóa kênh truyền TLS 1.3, chống MITM",
    "• Logging & cảnh báo bất thường: nhiều request thất bại từ cùng một IP",
    "• Kết hợp xác thực đa yếu tố (MFA): biometric + OTP/PIN cho giao dịch nhạy cảm"
]
for i, d in enumerate(defenses):
    ax.text(0.85, y2 - 1.85 - i*0.28, d,
            fontproperties=vn_font(9, False), color="#0b5c1f")

# --- KẾT QUẢ định lượng ---
yk = 0.6
ax.add_patch(patches.Rectangle((0.4, yk - 0.05), 14.2, 0.95,
                               linewidth=1.2, edgecolor="#525252",
                               facecolor="#f0f0f0"))
ax.text(7.5, yk + 0.65, "Kết quả định lượng (môi trường lab, dataset 200 Real / 200 Fake)",
        ha="center", fontproperties=vn_font(11, True), color="#252525")
ax.text(7.5, yk + 0.25,
        "FAR: ≈ 100% → ≈ 2%   •   FRR: ≈ 0% → ≈ 5%   •   APCER ≈ 1.5%   •   BPCER ≈ 4.8%   •   Latency: 120 → 180 ms",
        ha="center", fontproperties=vn_font(10, False), color="#252525")

plt.tight_layout()
out_path = os.path.join(OUT, "fig_3_5_tien_trinh_3_giai_doan.png")
plt.savefig(out_path, dpi=170, bbox_inches="tight", facecolor="white")
plt.close()
print("OK", out_path)

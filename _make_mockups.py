# -*- coding: utf-8 -*-
"""Tạo các ảnh mô phỏng giao diện và log tấn công."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties

OUT = os.path.join(os.path.dirname(__file__), "_report_assets")
os.makedirs(OUT, exist_ok=True)

def get_vn_font():
    for p in [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf",
              r"C:\Windows\Fonts\tahoma.ttf"]:
        if os.path.exists(p):
            return FontProperties(fname=p)
    return None

def get_mono_font():
    for p in [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"]:
        if os.path.exists(p):
            return FontProperties(fname=p)
    return None

VN = get_vn_font()
MONO = get_mono_font()

# ============================================================
# Hình 4.6 - Giao diện server vulnerable (mô phỏng)
# ============================================================
fig, ax = plt.subplots(figsize=(13, 7.5))
ax.set_xlim(0, 13); ax.set_ylim(0, 8)
ax.set_facecolor("#0a0a2a")
fig.patch.set_facecolor("#0a0a2a")
ax.axis("off")
ax.set_title("Hình 4.6. Giao diện server vulnerable — chưa có Liveness Detection",
             fontproperties=VN, fontsize=13, weight="bold", color="black")

# Header
ax.text(6.5, 7.4, "HE THONG CHAM CONG - NHAN DIEN KHUON MAT",
        ha="center", fontproperties=VN, fontsize=18, weight="bold", color="#33ccff")
ax.text(6.5, 7.05, "Cong ty X - Phong Nhan su",
        ha="center", fontproperties=VN, fontsize=10, color="white")

# Warning banner
warn = FancyBboxPatch((1.0, 6.4), 11.0, 0.45, boxstyle="round,pad=0.02",
                     linewidth=1.5, edgecolor="#ff0000", facecolor="#7a0000")
ax.add_patch(warn)
ax.text(6.5, 6.62, "LAB DEMO - KHONG CO LIVENESS DETECTION - DE BI TAN CONG",
        ha="center", fontproperties=VN, fontsize=11, weight="bold", color="white")

# Tabs
tabs = [("DANG KY", True), ("CHAM CONG", False), ("DS NHAN VIEN", False)]
for i, (t, active) in enumerate(tabs):
    x = 3.0 + i * 2.5
    color = "#1a3a5e" if active else "#0a1a2a"
    edge = "#33ccff" if active else "#3a4a5a"
    rect = FancyBboxPatch((x, 5.5), 2.2, 0.5, boxstyle="round,pad=0.02",
                          linewidth=1.5, edgecolor=edge, facecolor=color)
    ax.add_patch(rect)
    ax.text(x+1.1, 5.75, t, ha="center", fontproperties=VN, fontsize=10,
            color="#33ccff" if active else "#7a8a9a", weight="bold")

# Form container
form = FancyBboxPatch((1.0, 1.0), 11.0, 4.2, boxstyle="round,pad=0.02",
                     linewidth=1.5, edgecolor="#1a2a3a", facecolor="#0a1a2a")
ax.add_patch(form)
ax.text(1.5, 4.85, "Dang ky Khuon mat", fontproperties=VN, fontsize=13,
        weight="bold", color="#33ccff")

# Input
inp = FancyBboxPatch((1.5, 4.3), 10.0, 0.45, boxstyle="round,pad=0.01",
                    linewidth=1.0, edgecolor="#3a5a7a", facecolor="#0a2a4a")
ax.add_patch(inp)
ax.text(1.7, 4.52, "thinh", fontproperties=VN, fontsize=11, color="white")

# Webcam preview area (placeholder)
cam = patches.Rectangle((4.5, 1.7), 4.0, 2.3, linewidth=1.5,
                         edgecolor="#3a5a7a", facecolor="#1a1a1a")
ax.add_patch(cam)
ax.text(6.5, 2.85, "[Webcam preview]",
        ha="center", fontproperties=VN, fontsize=11, color="#5a6a7a", style="italic")

# Capture button
btn = FancyBboxPatch((5.5, 1.15), 2.0, 0.45, boxstyle="round,pad=0.02",
                    linewidth=1.0, edgecolor="#33ccff", facecolor="#22aacc")
ax.add_patch(btn)
ax.text(6.5, 1.37, "CHUP & DANG KY", ha="center", fontproperties=VN,
        fontsize=10, weight="bold", color="white")

# Error banner
err = FancyBboxPatch((1.5, 0.15), 10.0, 0.55, boxstyle="round,pad=0.02",
                    linewidth=1.5, edgecolor="#ff0000", facecolor="#3a0000")
ax.add_patch(err)
ax.text(6.5, 0.42, "LOI: Khong tim thay khuon mat trong anh",
        ha="center", fontproperties=VN, fontsize=11, color="#ff6666")

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_4_6_giao_dien_vulnerable.png"), dpi=170,
            bbox_inches="tight", facecolor="#0a0a2a")
plt.close()

# ============================================================
# Hình 4.7 - Mô phỏng log tấn công Injection
# ============================================================
fig, ax = plt.subplots(figsize=(13, 8))
ax.set_xlim(0, 13); ax.set_ylim(0, 10)
ax.set_facecolor("black")
fig.patch.set_facecolor("white")
ax.axis("off")
ax.set_title("Hình 4.7. Log tấn công Injection vào endpoint /authenticate (mô phỏng từ script tấn công)",
             fontproperties=VN, fontsize=13, weight="bold", color="black")

# Terminal background
term = patches.Rectangle((0.2, 0.3), 12.6, 9.3, linewidth=1.0,
                         edgecolor="#444", facecolor="#000")
ax.add_patch(term)

logs = [
    ("="*68, "#888"),
    ("  INJECTION ATTACK - Tiêm ảnh vào API xác thực", "#fff"),
    ("="*68, "#888"),
    ("  Target: http://localhost:5000", "#33ff33"),
    ("  Thời gian: 2026-05-07T13:40:58.554191", "#33ff33"),
    ("", "#fff"),
    ("[*] === PHASE 1: TRINH SAT ===", "#ffaa00"),
    ("[+] Tìm thấy 7 user:", "#33ff33"),
    ("    - thinh (đăng ký: 2026-04-06T11:51:39.890953)", "#aaaaff"),
    ("    - nhan (đăng ký: 2026-04-06T10:36:40.724865)", "#aaaaff"),
    ("    - tai (đăng ký: 2026-04-06T10:41:11.582885)", "#aaaaff"),
    ("    - hoang (đăng ký: 2026-04-11T17:17:38.728147)", "#aaaaff"),
    ("    - NGUYEN VAN CHUOT (đăng ký: 2026-04-16T11:03:20.169869)", "#aaaaff"),
    ("    - Xxsxcsxc (đăng ký: 2026-04-17T15:45:59.812356)", "#aaaaff"),
    ("    - hihi (đăng ký: 2026-05-07T13:05:16.598337)", "#aaaaff"),
    ("", "#fff"),
    ("[*] Tiêm ảnh: attacker/victim_photos/photo_003.jpg", "#ffaa00"),
    ("    Kích thước payload: 84 KB", "#ffaa00"),
    ("    Gửi POST -> http://localhost:5000/authenticate", "#ffaa00"),
    ("    Response time: 2.59s", "#aaaaff"),
    ("    Status: 200", "#aaaaff"),
    ("", "#fff"),
    ("    [!!!] INJECTION THANH CONG!", "#ff3333"),
    ("    [!!!] Xác thực là: hihi", "#ff3333"),
    ("    [!!!] Confidence: 0.7302", "#ff3333"),
    ("    [!!!] Liveness check: PASSED  (server không kiểm tra)", "#ff3333"),
]
y = 9.2
for line, color in logs:
    ax.text(0.4, y, line, fontproperties=MONO, fontsize=10, color=color)
    y -= 0.32

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_4_7_log_injection.png"), dpi=170,
            bbox_inches="tight", facecolor="white")
plt.close()

# ============================================================
# Hình 4.2-bis - Quá trình train (sẵn có training_history.png)
# Copy training_history.png và confusion_matrix.png ra _report_assets
# ============================================================
import shutil
src1 = os.path.join(os.path.dirname(__file__), "defender", "output", "training_history.png")
src2 = os.path.join(os.path.dirname(__file__), "defender", "output", "confusion_matrix.png")
if os.path.exists(src1):
    shutil.copy(src1, os.path.join(OUT, "fig_4_2_training_history.png"))
if os.path.exists(src2):
    shutil.copy(src2, os.path.join(OUT, "fig_4_2b_confusion_matrix.png"))

# ============================================================
# Hình 4.8 - Sơ đồ workflow tấn công – phòng vệ (chu trình)
# ============================================================
fig, ax = plt.subplots(figsize=(11, 9))
ax.set_xlim(-5, 5); ax.set_ylim(-5, 5)
ax.axis("off")
ax.set_title("Hình 4.8. Chu trình tấn công – phòng vệ – đánh giá",
             fontproperties=VN, fontsize=13, weight="bold")

import math
labels = ["Triển khai\nserver vulnerable",
          "Thực hiện\ntấn công thực tế",
          "Phân tích lỗ hổng,\nthu thập dữ liệu",
          "Huấn luyện\nmô hình PAD",
          "Tích hợp vào\nserver secured",
          "Đo FAR/FRR/APCER\nvà cải tiến"]
colors = ["#fdae6b", "#cb181d", "#9e9ac8", "#3182bd", "#006d2c", "#525252"]
n = len(labels)
R = 3.0
for i, (lab, c) in enumerate(zip(labels, colors)):
    angle = math.pi/2 - i * 2*math.pi/n
    x = R * math.cos(angle)
    y = R * math.sin(angle)
    rect = FancyBboxPatch((x-0.95, y-0.55), 1.9, 1.1, boxstyle="round,pad=0.02,rounding_size=0.1",
                          linewidth=1.5, edgecolor=c, facecolor=c)
    ax.add_patch(rect)
    ax.text(x, y, lab, ha="center", va="center", fontproperties=VN,
            fontsize=10, color="white", weight="bold")

for i in range(n):
    a1 = math.pi/2 - i * 2*math.pi/n
    a2 = math.pi/2 - ((i+1) % n) * 2*math.pi/n
    x1 = R * math.cos(a1) * 0.75
    y1 = R * math.sin(a1) * 0.75
    x2 = R * math.cos(a2) * 0.75
    y2 = R * math.sin(a2) * 0.75
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5,
                                connectionstyle="arc3,rad=0.2"))

ax.text(0, 0, "CHU TRÌNH\nLAB", ha="center", va="center",
        fontproperties=VN, fontsize=14, weight="bold", color="#252525")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig_4_8_chu_trinh.png"), dpi=170, bbox_inches="tight")
plt.close()

print("DONE")
print(sorted(os.listdir(OUT)))

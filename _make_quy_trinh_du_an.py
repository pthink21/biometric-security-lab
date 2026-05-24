# -*- coding: utf-8 -*-
"""
Sinh sơ đồ TỔNG THỂ mô phỏng đầy đủ quy trình của dự án
Biometric Security Lab.

Đầu ra:
  _report_assets/quy_trinh_du_an_tong_the.png
  _report_assets/quy_trinh_giai_doan_1.png ... giai_doan_5.png
"""
import os
import sys

# Ép stdout dùng UTF-8 để in tiếng Việt trên Windows console
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.font_manager import FontProperties

ROOT = os.path.dirname(__file__)
ASSETS = os.path.join(ROOT, "_report_assets")
OUT = ASSETS
os.makedirs(OUT, exist_ok=True)


# --------- Font tiếng Việt có dấu ---------
def get_vn_font(bold=False):
    candidates_regular = [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ]
    candidates_bold = [
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\tahomabd.ttf",
    ]
    pool = candidates_bold if bold else candidates_regular
    for p in pool:
        if os.path.exists(p):
            return FontProperties(fname=p)
    return None


VN = get_vn_font()
VNB = get_vn_font(bold=True) or VN
plt.rcParams["axes.unicode_minus"] = False


# --------- Helpers ---------
def box(ax, x, y, w, h, text,
        fc="#1f77b4", ec=None, text_color="white",
        fontsize=10, bold=True, rounding=0.08):
    if ec is None:
        ec = fc
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.02,rounding_size={rounding}",
        linewidth=1.6, edgecolor=ec, facecolor=fc,
    )
    ax.add_patch(rect)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center",
        fontsize=fontsize, color=text_color,
        fontproperties=(VNB if bold else VN), wrap=True,
    )


def banner(ax, x, y, w, h, text, fc="#0d3b66", text_color="white", fontsize=14):
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        linewidth=0, facecolor=fc,
    )
    ax.add_patch(rect)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center",
        fontsize=fontsize, color=text_color,
        fontproperties=VNB,
    )


def arrow(ax, x1, y1, x2, y2, color="#222", text=None,
          style="->", lw=1.8, fs=9, text_offset=(0, 0.2)):
    a = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=18,
        linewidth=lw, color=color,
    )
    ax.add_patch(a)
    if text:
        mx = (x1 + x2) / 2 + text_offset[0]
        my = (y1 + y2) / 2 + text_offset[1]
        ax.text(mx, my, text, ha="center", va="center",
                fontsize=fs, color=color, fontproperties=VN)


def place_image(ax, path, xy, zoom=0.15, frame_color="#333"):
    """Đặt một ảnh vào sơ đồ tại tọa độ (data coords)."""
    full = os.path.join(ASSETS, path)
    if not os.path.exists(full):
        # Vẽ placeholder nếu thiếu ảnh
        box(ax, xy[0] - 1.0, xy[1] - 0.7, 2.0, 1.4,
            f"[Thiếu ảnh]\n{path}", fc="#cccccc", text_color="#333",
            fontsize=8)
        return
    img = mpimg.imread(full)
    im = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(
        im, xy, frameon=True, pad=0.2,
        bboxprops=dict(edgecolor=frame_color, linewidth=1.2),
    )
    ax.add_artist(ab)


def caption(ax, x, y, text, fontsize=9, color="#333"):
    ax.text(x, y, text, ha="center", va="top",
            fontsize=fontsize, color=color,
            fontproperties=VN, style="italic")


# Bảng màu cho từng giai đoạn
PALETTE = {
    "setup":   "#0d3b66",    # xanh đậm
    "phase1":  "#9b1d20",    # đỏ tía  (vulnerable)
    "phase2":  "#c1440e",    # cam đỏ  (attack)
    "phase3":  "#1b6e3a",    # xanh lá (defense)
    "phase4":  "#274690",    # xanh dương đậm (verify)
    "accent":  "#f4a259",
    "muted":   "#e9ecef",
    "ok":      "#2a9d8f",
    "danger":  "#e63946",
}


# ==========================================================
# SƠ ĐỒ TỔNG THỂ - 1 trang lớn
# ==========================================================
def draw_master():
    fig, ax = plt.subplots(figsize=(20, 28))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 28)
    ax.axis("off")

    # Tiêu đề lớn
    ax.text(10, 27.3,
            "MÔ HÌNH MÔ PHỎNG ĐẦY ĐỦ QUY TRÌNH DỰ ÁN",
            ha="center", va="center",
            fontsize=22, color="#0d3b66",
            fontproperties=VNB)
    ax.text(10, 26.6,
            "Biometric Security Lab — Tấn công & Phòng vệ Sinh trắc học",
            ha="center", va="center",
            fontsize=14, color="#444",
            fontproperties=VN)

    # ----------------------------------------
    # GIAI ĐOẠN 0 - SETUP
    # ----------------------------------------
    y0 = 24.3
    banner(ax, 0.5, y0, 19, 0.9,
           "GIAI ĐOẠN 0 · CHUẨN BỊ MÔI TRƯỜNG (setup.sh)",
           fc=PALETTE["setup"], fontsize=15)

    sx = 0.7; sy = 22.6; sw = 3.5; sh = 1.3
    items = [
        ("Cài Python 3.10\n+ tạo venv",          "#1d3557"),
        ("Cài thư viện hệ thống\n(cmake, dlib, ffmpeg)", "#457b9d"),
        ("Cài gói Python\nserver / attacker / defender", "#457b9d"),
        ("Tạo cấu trúc thư mục\nface_db, dataset, output", "#2a6f97"),
        ("Nạp v4l2loopback\n(webcam ảo, Linux)", "#014f86"),
    ]
    for i, (txt, c) in enumerate(items):
        x = sx + i * (sw + 0.2)
        box(ax, x, sy, sw, sh, txt, fc=c, fontsize=10)
        if i < len(items) - 1:
            arrow(ax, x + sw, sy + sh / 2, x + sw + 0.2, sy + sh / 2,
                  color="#0d3b66", lw=2)

    # ----------------------------------------
    # GIAI ĐOẠN 1 - SERVER VULNERABLE
    # ----------------------------------------
    y1 = 21.3
    banner(ax, 0.5, y1, 19, 0.9,
           "GIAI ĐOẠN 1 · XÂY DỰNG SERVER VULNERABLE (chưa có Liveness)",
           fc=PALETTE["phase1"], fontsize=15)

    # Pipeline 5 bước
    steps_p1 = [
        ("Ảnh gửi tới\n/authenticate",   "#6a040f"),
        ("Phát hiện\nkhuôn mặt",         "#9d0208"),
        ("Trích đặc trưng\nvector 128-d","#d00000"),
        ("So khớp\nEuclidean < 0.6",     "#dc2f02"),
        ("Trả Accept\n(authenticated)",  "#e63946"),
    ]
    py = 19.7; pw = 3.2; ph = 1.2; gap = 0.55
    px0 = 0.7
    for i, (txt, c) in enumerate(steps_p1):
        x = px0 + i * (pw + gap)
        box(ax, x, py, pw, ph, txt, fc=c, fontsize=10)
        if i < len(steps_p1) - 1:
            arrow(ax, x + pw, py + ph / 2,
                  x + pw + gap, py + ph / 2,
                  color="#6a040f", lw=2)

    # Ảnh minh hoạ giao diện + sơ đồ vulnerable
    place_image(ax, "fig_3_2_server_vulnerable.png", (5.0, 18.3), zoom=0.09)
    caption(ax, 5.0, 17.05, "Hình: pipeline server CHƯA có liveness")

    place_image(ax, "fig_4_6_giao_dien_vulnerable.png", (14.5, 18.3), zoom=0.09)
    caption(ax, 14.5, 17.05, "Hình: giao diện web /register & /authenticate")

    # ----------------------------------------
    # GIAI ĐOẠN 2 - TẤN CÔNG
    # ----------------------------------------
    y2 = 15.8
    banner(ax, 0.5, y2, 19, 0.9,
           "GIAI ĐOẠN 2 · MÔ PHỎNG TẤN CÔNG (Replay & Injection)",
           fc=PALETTE["phase2"], fontsize=15)

    # 2a. Replay attack
    box(ax, 0.7, 14.4, 8.8, 1.0,
        "2A · REPLAY ATTACK — chiếu ảnh/video qua webcam ảo",
        fc="#bb3e03", fontsize=11)

    replay_steps = [
        ("Thu thập ảnh\nnạn nhân", "#ae2012"),
        ("Tạo webcam ảo\nv4l2loopback", "#bb3e03"),
        ("Phát ảnh/video\nvào /dev/video20", "#ca6702"),
        ("Server đọc cam\n→ Accept (BAD)", "#ee9b00"),
    ]
    rx = 0.7
    for i, (txt, c) in enumerate(replay_steps):
        x = rx + i * 2.25
        box(ax, x, 13.0, 2.05, 1.2, txt, fc=c, fontsize=9)
        if i < len(replay_steps) - 1:
            arrow(ax, x + 2.05, 13.6, x + 2.25, 13.6,
                  color="#6a040f", lw=1.8)

    # 2b. Injection attack
    box(ax, 10.2, 14.4, 9.3, 1.0,
        "2B · INJECTION ATTACK — gửi HTTP POST trực tiếp, bỏ qua webcam",
        fc="#9d0208", fontsize=11)

    inj_steps = [
        ("Mã hóa ảnh\nbase64 (JSON)", "#6a040f"),
        ("POST tới\n/authenticate", "#9d0208"),
        ("Bypass mọi\nkiểm tra client", "#d00000"),
        ("Server vẫn\ntrả Accept (BAD)", "#dc2f02"),
    ]
    ix = 10.2
    for i, (txt, c) in enumerate(inj_steps):
        x = ix + i * 2.35
        box(ax, x, 13.0, 2.15, 1.2, txt, fc=c, fontsize=9)
        if i < len(inj_steps) - 1:
            arrow(ax, x + 2.15, 13.6, x + 2.35, 13.6,
                  color="#370617", lw=1.8)

    # Ảnh minh hoạ tấn công
    place_image(ax, "fig_3_3_attack_replay_injection.png", (5.0, 11.5), zoom=0.09)
    caption(ax, 5.0, 10.3, "Hình: hai vector tấn công Replay & Injection")

    place_image(ax, "fig_4_7_log_injection.png", (14.5, 11.5), zoom=0.09)
    caption(ax, 14.5, 10.3, "Hình: log thực tế khi bị Injection thành công")

    # ----------------------------------------
    # GIAI ĐOẠN 3 - PHÒNG VỆ (PAD)
    # ----------------------------------------
    y3 = 9.1
    banner(ax, 0.5, y3, 19, 0.9,
           "GIAI ĐOẠN 3 · XÂY DỰNG LỚP PHÒNG VỆ — Liveness Detection (PAD)",
           fc=PALETTE["phase3"], fontsize=15)

    pad_steps = [
        ("Thu thập\ndataset Real/Fake\n(create_dataset.py)", "#1b4332"),
        ("Augment\n(flip, rotate,\ncolor jitter)", "#2d6a4f"),
        ("Phase 1: train\nclassifier head\n(10 epochs)", "#40916c"),
        ("Phase 2:\nfine-tune\n(15 epochs)", "#52b788"),
        ("Đánh giá\n+ xuất\nliveness_model.pth", "#74c69d"),
        ("Tích hợp vào\napp_secured.py\n(điểm ≥ 0.5)", "#1b6e3a"),
    ]
    dx = 0.7; dw = 3.0; dh = 1.6; dgap = 0.13
    dy = 7.3
    for i, (txt, c) in enumerate(pad_steps):
        x = dx + i * (dw + dgap)
        box(ax, x, dy, dw, dh, txt, fc=c, fontsize=9)
        if i < len(pad_steps) - 1:
            arrow(ax, x + dw, dy + dh / 2, x + dw + dgap, dy + dh / 2,
                  color="#1b4332", lw=2)

    # Ảnh minh hoạ phòng vệ
    place_image(ax, "fig_4_1_dataset.png",          (3.3, 5.7), zoom=0.08)
    caption(ax, 3.3, 4.55, "Dataset Real/Fake")

    place_image(ax, "fig_4_2_training_history.png", (8.2, 5.7), zoom=0.08)
    caption(ax, 8.2, 4.55, "Lịch sử huấn luyện")

    place_image(ax, "fig_4_2b_confusion_matrix.png",(12.2, 5.7), zoom=0.08)
    caption(ax, 12.2, 4.55, "Ma trận nhầm lẫn")

    place_image(ax, "fig_4_3_server_secured.png",   (16.7, 5.7), zoom=0.08)
    caption(ax, 16.7, 4.55, "Server SECURED có PAD")

    # ----------------------------------------
    # GIAI ĐOẠN 4 - KIỂM CHỨNG
    # ----------------------------------------
    y4 = 3.7
    banner(ax, 0.5, y4, 19, 0.9,
           "GIAI ĐOẠN 4 · KIỂM CHỨNG & ĐÁNH GIÁ KẾT QUẢ",
           fc=PALETTE["phase4"], fontsize=15)

    # Trước/Sau
    box(ax, 0.7, 1.9, 9.0, 1.6,
        "TRƯỚC PHÒNG VỆ\n• Replay: thành công (BAD)\n• Injection: thành công (BAD)\n• Tỉ lệ chấp nhận giả mạo cao",
        fc="#9d0208", fontsize=11)
    box(ax, 10.3, 1.9, 9.0, 1.6,
        "SAU PHÒNG VỆ (PAD)\n• Replay: BỊ CHẶN (OK)\n• Injection: BỊ CHẶN (OK)\n• Acc ≥ 95% trên test set",
        fc="#1b6e3a", fontsize=11)

    arrow(ax, 9.7, 2.7, 10.3, 2.7,
          color="#0d3b66", lw=3, text="Triển khai\napp_secured.py",
          text_offset=(0, 0.55), fs=10)

    # Footer
    ax.text(10, 0.6,
            "Quy trình khép kín: SETUP → VULNERABLE → ATTACK → DEFEND (PAD) → VERIFY",
            ha="center", va="center",
            fontsize=12, color="#0d3b66",
            fontproperties=VNB)
    ax.text(10, 0.15,
            "Sinh tự động bằng matplotlib · ảnh minh hoạ lấy từ thư mục _report_assets",
            ha="center", va="center",
            fontsize=9, color="#666",
            fontproperties=VN, style="italic")

    out_path = os.path.join(OUT, "quy_trinh_du_an_tong_the.png")
    plt.savefig(out_path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()
    return out_path


# ==========================================================
# SƠ ĐỒ CHI TIẾT TỪNG GIAI ĐOẠN
# ==========================================================
def _phase_canvas(title, subtitle, color):
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis("off")
    banner(ax, 0.3, 8.0, 14.4, 0.85, title, fc=color, fontsize=16)
    ax.text(7.5, 7.55, subtitle,
            ha="center", va="center",
            fontsize=11, color="#444", fontproperties=VN)
    return fig, ax


def draw_phase_1():
    fig, ax = _phase_canvas(
        "GIAI ĐOẠN 1 · SERVER VULNERABLE",
        "Pipeline xác thực khuôn mặt CHƯA có cơ chế Liveness Detection (app.py)",
        PALETTE["phase1"],
    )
    steps = [
        ("Người dùng gửi ảnh\nqua webcam/web", "#6a040f"),
        ("Flask nhận POST\n/authenticate", "#9d0208"),
        ("face_recognition\nphát hiện khuôn mặt", "#d00000"),
        ("Trích vector\nđặc trưng 128-d", "#dc2f02"),
        ("So khớp\nEuclidean < 0.6", "#e85d04"),
        ("Trả về\nauthenticated=True", "#f48c06"),
    ]
    y = 5.6
    w = 2.1; h = 1.3; gap = 0.25
    x0 = 0.5
    for i, (txt, c) in enumerate(steps):
        x = x0 + i * (w + gap)
        box(ax, x, y, w, h, txt, fc=c, fontsize=9)
        if i < len(steps) - 1:
            arrow(ax, x + w, y + h / 2, x + w + gap, y + h / 2,
                  color="#370617", lw=2)

    place_image(ax, "fig_3_2_server_vulnerable.png", (4.2, 3.0), zoom=0.16)
    caption(ax, 4.2, 0.9, "Sơ đồ pipeline VULNERABLE")

    place_image(ax, "fig_4_6_giao_dien_vulnerable.png", (11.0, 3.0), zoom=0.16)
    caption(ax, 11.0, 0.9, "Giao diện web /register & /authenticate")

    out = os.path.join(OUT, "quy_trinh_giai_doan_1.png")
    plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()
    return out


def draw_phase_2():
    fig, ax = _phase_canvas(
        "GIAI ĐOẠN 2 · TẤN CÔNG",
        "Hai vector tấn công: Replay (webcam ảo) & Injection (HTTP POST trực tiếp)",
        PALETTE["phase2"],
    )

    # Replay
    box(ax, 0.4, 6.4, 6.9, 0.7,
        "2A · REPLAY ATTACK", fc="#bb3e03", fontsize=12)
    replay = [
        ("Thu ảnh/video\nnạn nhân", "#ae2012"),
        ("v4l2loopback\n→ /dev/video20", "#bb3e03"),
        ("Phát ảnh vào\nwebcam ảo", "#ca6702"),
        ("Server đọc\n→ Accept (BAD)", "#ee9b00"),
    ]
    for i, (txt, c) in enumerate(replay):
        x = 0.4 + i * 1.78
        box(ax, x, 4.9, 1.65, 1.2, txt, fc=c, fontsize=9)
        if i < len(replay) - 1:
            arrow(ax, x + 1.65, 5.5, x + 1.78, 5.5,
                  color="#6a040f", lw=1.8)

    # Injection
    box(ax, 7.7, 6.4, 6.9, 0.7,
        "2B · INJECTION ATTACK", fc="#9d0208", fontsize=12)
    inj = [
        ("Mã hoá ảnh\nbase64 / JSON", "#6a040f"),
        ("POST trực tiếp\ntới /authenticate", "#9d0208"),
        ("Bypass toàn bộ\nclient-side check", "#d00000"),
        ("Server vẫn\ntrả Accept (BAD)", "#dc2f02"),
    ]
    for i, (txt, c) in enumerate(inj):
        x = 7.7 + i * 1.78
        box(ax, x, 4.9, 1.65, 1.2, txt, fc=c, fontsize=9)
        if i < len(inj) - 1:
            arrow(ax, x + 1.65, 5.5, x + 1.78, 5.5,
                  color="#370617", lw=1.8)

    place_image(ax, "fig_3_3_attack_replay_injection.png", (4.2, 2.6), zoom=0.16)
    caption(ax, 4.2, 0.7, "Mô hình hai vector tấn công")

    place_image(ax, "fig_4_7_log_injection.png", (11.0, 2.6), zoom=0.16)
    caption(ax, 11.0, 0.7, "Log thực tế khi Injection thành công")

    out = os.path.join(OUT, "quy_trinh_giai_doan_2.png")
    plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()
    return out


def draw_phase_3():
    fig, ax = _phase_canvas(
        "GIAI ĐOẠN 3 · LỚP PHÒNG VỆ (Liveness / PAD)",
        "Thu dữ liệu → Huấn luyện MobileNetV2 → Tích hợp vào app_secured.py",
        PALETTE["phase3"],
    )

    steps = [
        ("Thu thập dataset\nReal & Fake", "#1b4332"),
        ("Tăng cường dữ liệu\n(augmentation)", "#2d6a4f"),
        ("Phase 1\nfreeze backbone\ntrain head 10ep", "#40916c"),
        ("Phase 2\nunfreeze + fine-tune\n15 epochs", "#52b788"),
        ("Đánh giá\n+ xuất .pth", "#74c69d"),
        ("Gắn vào server\napp_secured.py", "#1b6e3a"),
    ]
    y = 5.7; w = 2.25; h = 1.4; gap = 0.13
    x0 = 0.4
    for i, (txt, c) in enumerate(steps):
        x = x0 + i * (w + gap)
        box(ax, x, y, w, h, txt, fc=c, fontsize=9)
        if i < len(steps) - 1:
            arrow(ax, x + w, y + h / 2, x + w + gap, y + h / 2,
                  color="#1b4332", lw=2)

    place_image(ax, "fig_4_1_dataset.png",          (2.5, 3.0), zoom=0.10)
    caption(ax, 2.5, 1.5, "Hình: Dataset Real/Fake")

    place_image(ax, "fig_4_2_training_history.png", (6.5, 3.0), zoom=0.10)
    caption(ax, 6.5, 1.5, "Hình: Lịch sử huấn luyện")

    place_image(ax, "fig_4_2b_confusion_matrix.png",(10.0, 3.0), zoom=0.10)
    caption(ax, 10.0, 1.5, "Hình: Ma trận nhầm lẫn")

    place_image(ax, "fig_4_3_server_secured.png",   (13.3, 3.0), zoom=0.10)
    caption(ax, 13.3, 1.5, "Hình: Server SECURED")

    out = os.path.join(OUT, "quy_trinh_giai_doan_3.png")
    plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()
    return out


def draw_phase_4():
    fig, ax = _phase_canvas(
        "GIAI ĐOẠN 4 · KIỂM CHỨNG KẾT QUẢ",
        "So sánh tỷ lệ chấp nhận giả mạo TRƯỚC & SAU khi triển khai PAD",
        PALETTE["phase4"],
    )
    box(ax, 0.4, 5.0, 7.0, 1.8,
        "TRƯỚC PHÒNG VỆ\n• Replay attack: thành công (BAD)\n• Injection attack: thành công (BAD)\n• Hệ thống chấp nhận khuôn mặt giả mạo",
        fc="#9d0208", fontsize=11)
    box(ax, 7.6, 5.0, 7.0, 1.8,
        "SAU PHÒNG VỆ (PAD)\n• Replay attack: BỊ CHẶN (OK)\n• Injection attack: BỊ CHẶN (OK)\n• Độ chính xác PAD ≥ 95% trên test",
        fc="#1b6e3a", fontsize=11)
    arrow(ax, 7.4, 5.9, 7.6, 5.9, color="#0d3b66", lw=3,
          text="Tích hợp\nMobileNetV2", text_offset=(0, 0.4), fs=10)

    place_image(ax, "fig_4_4_so_sanh_chi_so.png", (4.0, 2.5), zoom=0.16)
    caption(ax, 4.0, 0.6, "Biểu đồ so sánh các chỉ số")

    place_image(ax, "fig_4_8_chu_trinh.png",      (11.0, 2.5), zoom=0.16)
    caption(ax, 11.0, 0.6, "Chu trình khép kín tấn công – phòng vệ")

    out = os.path.join(OUT, "quy_trinh_giai_doan_4.png")
    plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()
    return out


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    paths = []
    paths.append(draw_master())
    paths.append(draw_phase_1())
    paths.append(draw_phase_2())
    paths.append(draw_phase_3())
    paths.append(draw_phase_4())
    print("Đã tạo:")
    for p in paths:
        print("  -", p)

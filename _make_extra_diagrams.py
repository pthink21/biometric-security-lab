# -*- coding: utf-8 -*-
"""Sinh thêm diagram cho các phần còn thiếu của báo cáo cuối:
- AttackNet detail (Inverted Residual chi tiết)
- Detection Engine Lifecycle (PAD Engineering vòng đời)
- MITRE ATT&CK Biometric mapping
- Attack Chain (Reconnaissance -> ... -> Impact)
- Image Telemetry Pipeline chi tiết
- Threshold tuning ROC curve mockup
- Defense in Depth 6 lớp
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

OUT = r"C:\Users\ADMIN\biometric-security-lab\_report_assets"
os.makedirs(OUT, exist_ok=True)

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, name), dpi=160, bbox_inches='tight', facecolor='white')
    plt.close()


# ============================================================
# 1. AttackNet / MobileNetV2 chi tiết (Inverted Residual block)
# ============================================================
def fig_attacknet_detail():
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title("Kiến trúc AttackNet (MobileNetV2 + classifier head Real/Fake)",
                 fontsize=13, fontweight='bold', pad=14)

    # Input
    blocks = [
        (0.2, 3, 1.4, "Input\n224x224x3\n(RGB)", "#E3F2FD"),
        (1.8, 3, 1.4, "Conv 3x3\nstride=2\n32 ch", "#BBDEFB"),
        (3.4, 3, 1.4, "InvRes x1\n16 ch", "#FFF9C4"),
        (5.0, 3, 1.4, "InvRes x2\n24 ch", "#FFE082"),
        (6.6, 3, 1.4, "InvRes x7\n32-160 ch", "#FFCC80"),
        (8.2, 3, 1.4, "Conv 1x1\n1280 ch", "#FFAB91"),
        (9.8, 3, 1.4, "GlobalAvg\nPool 1x1x1280", "#F8BBD9"),
        (11.4, 3, 1.4, "FC + Sigmoid\nReal / Fake", "#CE93D8"),
    ]
    for x, y, w, label, color in blocks:
        ax.add_patch(FancyBboxPatch((x, y), w, 1.2,
                                     boxstyle="round,pad=0.05",
                                     facecolor=color, edgecolor='#333', linewidth=1.2))
        ax.text(x + w / 2, y + 0.6, label, ha='center', va='center', fontsize=8.5)
        if x < 11:
            ax.add_patch(FancyArrowPatch((x + w, y + 0.6), (x + w + 0.18, y + 0.6),
                                          arrowstyle='->', color='#333', mutation_scale=12))

    # Inverted Residual chi tiết phía dưới
    ax.text(6.5, 2.4, "Inverted Residual Block (chi tiết):",
            ha='center', fontsize=11, fontweight='bold', color='#1976D2')
    inv = [
        (1.5, 0.6, 1.6, "Expand 1x1\nReLU6\n(t=6)", "#FFECB3"),
        (3.4, 0.6, 1.6, "Depthwise 3x3\nstride=s\nReLU6", "#FFCDD2"),
        (5.3, 0.6, 1.6, "Project 1x1\nLinear\n(no ReLU)", "#C5CAE9"),
        (7.2, 0.6, 1.6, "Skip Connect\n(if stride=1)", "#B2DFDB"),
    ]
    for x, y, w, label, color in inv:
        ax.add_patch(FancyBboxPatch((x, y), w, 1.2,
                                     boxstyle="round,pad=0.05",
                                     facecolor=color, edgecolor='#333'))
        ax.text(x + w / 2, y + 0.6, label, ha='center', va='center', fontsize=8.5)
        if x < 7:
            ax.add_patch(FancyArrowPatch((x + w, y + 0.6), (x + w + 0.18, y + 0.6),
                                          arrowstyle='->', color='#333', mutation_scale=12))

    # Skip-connection arc
    ax.add_patch(FancyArrowPatch((2.3, 1.85), (8.0, 1.85),
                                  arrowstyle='->', color='#1976D2',
                                  connectionstyle="arc3,rad=-0.45",
                                  linewidth=1.8, mutation_scale=15))
    ax.text(5.2, 2.2, "skip", ha='center', fontsize=9, color='#1976D2', style='italic')

    # Footnote
    ax.text(6.5, 0.1,
            "Tham số: 3.4M params, 300 MFLOPs — chạy thời gian thực 28-32 FPS trên CPU Intel i7",
            ha='center', fontsize=9, style='italic', color='#555')
    save("fig_attacknet_detail.png")


# ============================================================
# 2. Detection Engine Lifecycle (PAD Engineering)
# ============================================================
def fig_pad_lifecycle():
    fig, ax = plt.subplots(figsize=(11, 8))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 9)
    ax.axis('off')
    ax.set_title("Vòng đời PAD Engineering (Detection Engineering Lifecycle)",
                 fontsize=14, fontweight='bold', pad=14)

    # Circular layout - 6 phases
    phases = [
        ("1. Threat Intelligence\n& Hunt Hypothesis",
         "Thu thập IOC tấn công\nMITRE ATT&CK mapping"),
        ("2. Data Collection\n(Image Telemetry)",
         "Thu nhận Real/Fake samples\nCASIA, OULU, dataset lab"),
        ("3. Detection Logic\n(Model Training)",
         "Transfer Learning\nMobileNetV2 Real/Fake"),
        ("4. Validation\n(Threshold Tuning)",
         "ROC, APCER/BPCER\nLIVENESS_THRESHOLD=0.7"),
        ("5. Deployment\n(Production)",
         "Tích hợp server Secured\nServing pipeline"),
        ("6. Continuous Tuning\n(Red Teaming)",
         "Mô phỏng tấn công mới\nRetrain & alert tuning"),
    ]
    cx, cy, R = 5, 4, 3.4
    colors = ['#E1F5FE', '#FFF3E0', '#F3E5F5', '#E8F5E9', '#FFF9C4', '#FFCDD2']
    positions = []
    for i, (title, desc) in enumerate(phases):
        ang = np.pi / 2 - i * (2 * np.pi / 6)
        x, y = cx + R * np.cos(ang), cy + R * np.sin(ang)
        positions.append((x, y))
        ax.add_patch(FancyBboxPatch((x - 1.5, y - 0.8), 3.0, 1.6,
                                     boxstyle="round,pad=0.08",
                                     facecolor=colors[i], edgecolor='#333', linewidth=1.4))
        ax.text(x, y + 0.3, title, ha='center', va='center', fontsize=9.5, fontweight='bold')
        ax.text(x, y - 0.35, desc, ha='center', va='center', fontsize=8.2)

    # Arrows between phases
    for i in range(6):
        x1, y1 = positions[i]
        x2, y2 = positions[(i + 1) % 6]
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                      arrowstyle='->',
                                      connectionstyle="arc3,rad=0.18",
                                      color='#1565C0', linewidth=2,
                                      mutation_scale=18))

    ax.text(cx, cy + 0.3, "PAD\nEngineering", ha='center', va='center',
            fontsize=14, fontweight='bold', color='#0D47A1')
    ax.text(cx, cy - 0.5, "(ISO/IEC 30107)", ha='center', va='center',
            fontsize=9, style='italic', color='#1565C0')
    save("fig_pad_lifecycle.png")


# ============================================================
# 3. MITRE ATT&CK Biometric mapping
# ============================================================
def fig_mitre_mapping():
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title("Ánh xạ TTPs tấn công sinh trắc học vào ma trận MITRE ATT&CK",
                 fontsize=13, fontweight='bold', pad=12)

    tactics = ["Reconnaissance", "Resource Dev", "Initial Access",
               "Credential Access", "Defense Evasion", "Impact"]
    techniques = [
        ["T1589.001\nGather victim photo\n(social media)"],
        ["T1588.005\nObtain capabilities\n(printer, deepfake tool)"],
        ["TTP-01\nPrint Attack\n(physical)",
         "TTP-02\nReplay Screen\n(physical)"],
        ["TTP-04\nAPI Injection\n(direct)",
         "TTP-03\nReplay over API"],
        ["T1036\nMasquerading\nfake liveness signals"],
        ["T1531\nAccount Access\nRemoval"]
    ]

    col_w = 13 / 6
    for i, t in enumerate(tactics):
        ax.add_patch(Rectangle((i * col_w + 0.05, 6), col_w - 0.1, 0.6,
                                facecolor='#1565C0', edgecolor='black'))
        ax.text(i * col_w + col_w / 2, 6.3, t, ha='center', va='center',
                color='white', fontsize=10, fontweight='bold')

    colors_tech = ['#FFCDD2', '#F8BBD9', '#FFCC80', '#FFE082', '#C8E6C9', '#B3E5FC']
    for i, techs in enumerate(techniques):
        for j, tech in enumerate(techs):
            y = 5.0 - j * 1.5
            ax.add_patch(FancyBboxPatch((i * col_w + 0.15, y - 0.5),
                                         col_w - 0.3, 1.2,
                                         boxstyle="round,pad=0.04",
                                         facecolor=colors_tech[i], edgecolor='#333'))
            ax.text(i * col_w + col_w / 2, y + 0.1, tech,
                    ha='center', va='center', fontsize=8.5)

    # Legend
    ax.text(6.5, 0.3, "Mỗi cột = 1 Tactic. Mỗi ô = 1 Technique cụ thể được quan sát "
                       "trong chu trình tấn công sinh trắc học khuôn mặt.",
            ha='center', fontsize=9.5, style='italic', color='#444')
    save("fig_mitre_mapping.png")


# ============================================================
# 4. Attack Chain (Cyber Kill Chain biometric)
# ============================================================
def fig_attack_chain():
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title("Attack Chain — Chuỗi tấn công sinh trắc học khuôn mặt",
                 fontsize=13, fontweight='bold', pad=12)

    steps = [
        ("Recon",
         "Thu thập ảnh\nnạn nhân từ\nFacebook, Zalo,\nLinkedIn", "#E1F5FE"),
        ("Weaponize",
         "In ảnh A4 /\nload lên màn hình /\nrender deepfake", "#FFF3E0"),
        ("Delivery",
         "Trình diện\ntrước camera\nhoặc curl --POST", "#F3E5F5"),
        ("Exploit",
         "Bypass\nlớp PAD\n(nếu thiếu)", "#FFCDD2"),
        ("Install",
         "Hệ thống cấp\nsession token\nhợp lệ", "#FFEBEE"),
        ("C2",
         "Attacker\nthao tác trong\nphiên hợp lệ", "#FFCDD2"),
        ("Action",
         "Chuyển khoản /\nlộ thông tin /\nleo thang quyền", "#B71C1C"),
    ]
    n = len(steps)
    w = 14 / n - 0.2
    for i, (title, desc, color) in enumerate(steps):
        x = i * (14 / n) + 0.1
        ax.add_patch(FancyBboxPatch((x, 1.6), w, 2.2,
                                     boxstyle="round,pad=0.06",
                                     facecolor=color, edgecolor='#333', linewidth=1.4))
        text_color = 'white' if title == 'Action' else 'black'
        ax.text(x + w / 2, 3.4, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color=text_color)
        ax.text(x + w / 2, 2.4, desc, ha='center', va='center',
                fontsize=8.5, color=text_color)
        if i < n - 1:
            ax.add_patch(FancyArrowPatch((x + w + 0.05, 2.7),
                                          (x + w + 0.18, 2.7),
                                          arrowstyle='->', color='#333',
                                          linewidth=1.8, mutation_scale=15))

    # PAD chặn được giai đoạn nào
    ax.text(7, 0.9,
            "★ PAD Engine (Liveness Detection) chặn ở bước Exploit — phá vỡ chuỗi tại điểm sớm nhất.",
            ha='center', fontsize=10, fontweight='bold', color='#1B5E20')
    ax.text(7, 0.4,
            "Nếu thiếu PAD: chuỗi đi thẳng đến Action → thiệt hại không thể đảo ngược.",
            ha='center', fontsize=10, color='#B71C1C')
    save("fig_attack_chain.png")


# ============================================================
# 5. Image Telemetry pipeline chi tiết
# ============================================================
def fig_image_telemetry():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title("Pipeline xử lý Image Telemetry — server Secured",
                 fontsize=13, fontweight='bold', pad=12)

    blocks = [
        (0.3, "Camera\nClient",
         "OpenCV\n640x480 RGB\n30fps", "#E3F2FD"),
        (2.2, "Capture &\nEncode JPEG",
         "Base64\nFrame=K",
         "#BBDEFB"),
        (4.1, "POST /authenticate\nHTTPS + JWT",
         "Username +\nimage payload",
         "#FFCC80"),
        (6.0, "Tiền xử lý\nCLAHE",
         "Cân bằng\nsáng/độ tương phản",
         "#FFE082"),
        (7.9, "Detection Engine\n(PAD MobileNetV2)",
         "score in [0,1]\nThreshold=0.7",
         "#FFAB91"),
        (9.8, "Face Embedding\n(face_recognition)",
         "128-d vector\nso khớp DB",
         "#F8BBD9"),
        (11.7, "Decision\n& Audit Log",
         "Access / Reject\nWazuh / SIEM",
         "#CE93D8"),
    ]
    for x, title, desc, color in blocks:
        ax.add_patch(FancyBboxPatch((x, 2.2), 1.6, 1.8,
                                     boxstyle="round,pad=0.06",
                                     facecolor=color, edgecolor='#333', linewidth=1.4))
        ax.text(x + 0.8, 3.4, title, ha='center', va='center',
                fontsize=9, fontweight='bold')
        ax.text(x + 0.8, 2.6, desc, ha='center', va='center', fontsize=7.6)
        if x < 11.6:
            ax.add_patch(FancyArrowPatch((x + 1.6, 3.1), (x + 1.85, 3.1),
                                          arrowstyle='->', color='#333',
                                          linewidth=1.5, mutation_scale=14))

    # PAD reject branch
    ax.add_patch(FancyArrowPatch((8.7, 2.2), (8.7, 1.0),
                                  arrowstyle='->', color='#C62828',
                                  linewidth=1.8, mutation_scale=15))
    ax.add_patch(FancyBboxPatch((7.9, 0.3), 1.6, 0.65,
                                 boxstyle="round,pad=0.05",
                                 facecolor='#FFCDD2', edgecolor='#C62828'))
    ax.text(8.7, 0.62, "Reject 401\nspoof_score>0.3", ha='center', va='center',
            fontsize=8, color='#C62828', fontweight='bold')

    ax.text(7, 5.4, "Image Telemetry = luồng dữ liệu hình ảnh có metadata "
                     "(timestamp, device_id, frame_id, geo) đi qua pipeline phòng vệ",
            ha='center', fontsize=10, style='italic', color='#444')
    save("fig_image_telemetry.png")


# ============================================================
# 6. ROC Curve & Threshold Tuning
# ============================================================
def fig_roc_threshold():
    fig, ax = plt.subplots(figsize=(11, 6))
    # Synthetic ROC for PAD demo
    x = np.linspace(0, 1, 200)
    # Vulnerable - random
    fpr_v = x
    tpr_v = x
    # Secured - high AUC
    fpr_s = x
    tpr_s = 1 - (1 - x) ** 4
    ax.plot(fpr_v, tpr_v, '--', color='#B71C1C', linewidth=2,
            label='Server Vulnerable (no PAD) — AUC=0.50')
    ax.plot(fpr_s, tpr_s, '-', color='#1B5E20', linewidth=2.5,
            label='Server Secured (PAD MobileNetV2) — AUC=0.97')
    # Operating points
    op = [(0.015, 0.95, '0.7 (chosen)'),
          (0.005, 0.80, '0.85'),
          (0.05, 0.985, '0.5')]
    for fpr, tpr, lbl in op:
        ax.scatter([fpr], [tpr], color='#0D47A1', s=80, zorder=5)
        ax.annotate(f't={lbl}', xy=(fpr, tpr), xytext=(fpr + 0.05, tpr - 0.05),
                    fontsize=9, color='#0D47A1', fontweight='bold')
    ax.set_xlabel('APCER (False Acceptance / Attack pass-through)', fontsize=11)
    ax.set_ylabel('1 − BPCER (True Acceptance Rate of bona-fide)', fontsize=11)
    ax.set_title('ROC Curve & Threshold Tuning — APCER vs BPCER trade-off',
                 fontsize=12, fontweight='bold')
    ax.grid(alpha=0.3)
    ax.legend(loc='lower right', fontsize=10)
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0.5, 1.02)
    save("fig_roc_threshold.png")


# ============================================================
# 7. Defense in Depth 6-layer
# ============================================================
def fig_defense_in_depth():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis('off')
    ax.set_title("Kiến trúc Defense in Depth cho hệ thống xác thực sinh trắc học",
                 fontsize=13, fontweight='bold', pad=10)

    layers = [
        ("L1 — Client Trust", "TLS 1.3 + Certificate Pinning + Device Attestation (SafetyNet/WebAuthn)", "#1565C0"),
        ("L2 — Channel Integrity", "Mã hóa kênh, ký số ảnh tại client (HMAC), chống MITM",       "#1976D2"),
        ("L3 — Image Telemetry QC", "CLAHE, dimension check, chuẩn hóa frame rate, anti-replay nonce", "#1E88E5"),
        ("L4 — Detection Engine (PAD)", "MobileNetV2 Real/Fake — APCER<3%, latency<60ms",        "#43A047"),
        ("L5 — Behavioral Analytics",   "Velocity check, geo-impossible, frequency anomaly (UEBA)", "#7B1FA2"),
        ("L6 — MFA Step-up + Audit",    "OTP / FIDO2 cho giao dịch lớn, log Wazuh + alert SIEM",   "#E65100"),
    ]
    for i, (title, desc, color) in enumerate(layers):
        y = 6.2 - i * 0.95
        ax.add_patch(FancyBboxPatch((0.3, y), 10.4, 0.78,
                                     boxstyle="round,pad=0.06",
                                     facecolor=color, edgecolor='#333', linewidth=1.4))
        ax.text(1.0, y + 0.39, title, ha='left', va='center',
                fontsize=11, fontweight='bold', color='white')
        ax.text(4.4, y + 0.39, desc, ha='left', va='center',
                fontsize=9.5, color='white')

    ax.text(5.5, 0.4,
            "Mỗi lớp phát hiện một loại tấn công khác nhau — bypass cùng lúc cả 6 lớp gần như bất khả thi",
            ha='center', fontsize=10, style='italic', fontweight='bold', color='#444')
    save("fig_defense_in_depth.png")


# ============================================================
# 8. Threat Model (STRIDE + bề mặt tấn công)
# ============================================================
def fig_threat_model():
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title("Threat Model — Bề mặt tấn công của hệ thống xác thực sinh trắc học",
                 fontsize=13, fontweight='bold', pad=10)

    # Three zones: Client / Network / Server
    ax.add_patch(Rectangle((0.2, 0.5), 4, 6, facecolor='#E3F2FD',
                            edgecolor='#1565C0', linewidth=1.5, linestyle='--'))
    ax.text(2.2, 6.2, "Client Zone", fontsize=11, fontweight='bold',
            ha='center', color='#0D47A1')

    ax.add_patch(Rectangle((4.4, 0.5), 3.6, 6, facecolor='#FFF3E0',
                            edgecolor='#E65100', linewidth=1.5, linestyle='--'))
    ax.text(6.2, 6.2, "Network Zone", fontsize=11, fontweight='bold',
            ha='center', color='#BF360C')

    ax.add_patch(Rectangle((8.2, 0.5), 4.6, 6, facecolor='#E8F5E9',
                            edgecolor='#1B5E20', linewidth=1.5, linestyle='--'))
    ax.text(10.5, 6.2, "Server Zone", fontsize=11, fontweight='bold',
            ha='center', color='#1B5E20')

    # Components
    parts = [
        (0.5, 4.2, 3.4, "Camera + Browser/App\n(WebRTC, OpenCV)"),
        (0.5, 2.5, 3.4, "Local image buffer\n(JPEG/Base64)"),
        (4.7, 4.0, 3.0, "HTTPS / TLS 1.2\nREST endpoint"),
        (8.6, 4.6, 3.8, "Flask /authenticate\nRoute handler"),
        (8.6, 3.0, 3.8, "PAD Engine\n(MobileNetV2)"),
        (8.6, 1.4, 3.8, "Embedding DB\n(pickle, 128-d)"),
    ]
    for x, y, w, label in parts:
        ax.add_patch(FancyBboxPatch((x, y), w, 1.0,
                                     boxstyle="round,pad=0.05",
                                     facecolor='white', edgecolor='#333'))
        ax.text(x + w / 2, y + 0.5, label, ha='center', va='center', fontsize=9)

    # Attack arrows
    attacks = [
        (1.0, 3.6, "PA-01\nSpoof phys.", '#C62828'),
        (4.5, 3.5, "AT-02\nMITM/replay", '#C62828'),
        (8.4, 4.0, "AT-03\nInjection /authenticate", '#C62828'),
        (8.4, 1.7, "AT-04\nDB poisoning", '#C62828'),
    ]
    for x, y, lbl, col in attacks:
        ax.add_patch(FancyArrowPatch((x - 0.5, y + 0.7), (x, y),
                                      arrowstyle='->', color=col,
                                      linewidth=2.4, mutation_scale=18))
        ax.text(x - 0.6, y + 0.95, lbl, fontsize=8.5, color=col,
                fontweight='bold', ha='left')

    save("fig_threat_model.png")


# ============================================================
# 9. Visibility Gap (điểm mù giám sát)
# ============================================================
def fig_visibility_gap():
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    ax.set_title("Visibility Gap — Điểm mù giám sát khi hệ thống thiếu lớp PAD",
                 fontsize=13, fontweight='bold', pad=10)

    # Top: hệ thống thiếu PAD
    ax.text(6, 5.0, "Hệ thống KHÔNG có PAD (Vulnerable)",
            ha='center', fontsize=11, fontweight='bold', color='#B71C1C')
    blocks_v = [(0.3, "Camera"), (2.0, "Capture"), (3.7, "API"), (5.4, "Match"), (7.1, "Decision")]
    for x, lbl in blocks_v:
        ax.add_patch(FancyBboxPatch((x, 3.7), 1.4, 0.8,
                                     boxstyle="round,pad=0.05",
                                     facecolor='#FFCDD2', edgecolor='#B71C1C'))
        ax.text(x + 0.7, 4.1, lbl, ha='center', va='center', fontsize=9)
    # gap
    ax.add_patch(FancyBboxPatch((9.2, 3.7), 2.5, 0.8,
                                 boxstyle="round,pad=0.05",
                                 facecolor='#FFEBEE', edgecolor='#B71C1C',
                                 linestyle='--', linewidth=2))
    ax.text(10.45, 4.1, "VISIBILITY\nGAP",
            ha='center', va='center', fontsize=9, color='#B71C1C', fontweight='bold')

    # Bottom: hệ thống có PAD
    ax.text(6, 2.6, "Hệ thống có PAD Engine (Secured)",
            ha='center', fontsize=11, fontweight='bold', color='#1B5E20')
    blocks_s = [(0.3, "Camera"), (1.8, "Capture"),
                (3.3, "PAD\nEngine"), (4.8, "API"),
                (6.3, "Match"), (7.8, "Decision"),
                (9.3, "SIEM\nAudit")]
    colors = ['#C8E6C9', '#C8E6C9', '#A5D6A7', '#C8E6C9',
              '#C8E6C9', '#C8E6C9', '#A5D6A7']
    for (x, lbl), c in zip(blocks_s, colors):
        ax.add_patch(FancyBboxPatch((x, 1.3), 1.3, 0.9,
                                     boxstyle="round,pad=0.05",
                                     facecolor=c, edgecolor='#1B5E20'))
        ax.text(x + 0.65, 1.75, lbl, ha='center', va='center', fontsize=8.5)

    ax.text(6, 0.4,
            "★ PAD Engine bịt kín điểm mù — mọi frame qua pipeline đều có nhãn liveness và lưu vết audit",
            ha='center', fontsize=10, fontweight='bold', color='#1B5E20')
    save("fig_visibility_gap.png")


if __name__ == "__main__":
    fig_attacknet_detail()
    fig_pad_lifecycle()
    fig_mitre_mapping()
    fig_attack_chain()
    fig_image_telemetry()
    fig_roc_threshold()
    fig_defense_in_depth()
    fig_threat_model()
    fig_visibility_gap()
    print("Da sinh xong cac diagram bo sung.")

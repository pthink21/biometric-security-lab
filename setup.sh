#!/bin/bash
# ================================================================
# Biometric Security Lab - Setup Script
# ================================================================
# Script cài đặt tự động cho hệ thống lab bảo mật sinh trắc học.
#
# Hỗ trợ:
#   - Kali Linux / Ubuntu / Debian
#   - Windows (WSL) - cần chạy trong WSL terminal
#
# Cách dùng:
#   chmod +x setup.sh && ./setup.sh
# ================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "================================================================"
echo "  BIOMETRIC SECURITY LAB - SETUP"
echo "  Mo phong Tan cong & Phong ve Sinh trac hoc"
echo "================================================================"
echo -e "${NC}"

# --- 1. Kiểm tra Python ---
echo -e "${YELLOW}[1/6] Kiểm tra Python...${NC}"
if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 --version)
    echo -e "${GREEN}  [+] $PY_VERSION${NC}"
else
    echo -e "${RED}  [!] Python3 chưa cài! Đang cài...${NC}"
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv
fi

# --- 2. Tạo virtual environment ---
echo -e "${YELLOW}[2/6] Tạo virtual environment...${NC}"
VENV_DIR="./venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}  [+] Tạo venv: $VENV_DIR${NC}"
else
    echo -e "${GREEN}  [+] Venv đã tồn tại${NC}"
fi
source "$VENV_DIR/bin/activate"

# --- 3. Cài system dependencies ---
echo -e "${YELLOW}[3/6] Cài system dependencies...${NC}"
if command -v apt &>/dev/null; then
    sudo apt update
    sudo apt install -y \
        cmake \
        build-essential \
        libopenblas-dev \
        liblapack-dev \
        libx11-dev \
        libgtk-3-dev \
        v4l2loopback-dkms \
        ffmpeg \
        libsm6 \
        libxext6

    echo -e "${GREEN}  [+] System dependencies installed${NC}"
else
    echo -e "${YELLOW}  [*] Không phải Debian/Ubuntu - bỏ qua apt${NC}"
fi

# --- 4. Cài Python packages ---
echo -e "${YELLOW}[4/6] Cài Python packages...${NC}"
pip install --upgrade pip

echo "  Installing server packages..."
pip install -r server/requirements.txt

echo "  Installing attacker packages..."
pip install -r attacker/requirements.txt

echo "  Installing defender (ML) packages..."
pip install -r defender/requirements.txt

echo -e "${GREEN}  [+] Tất cả packages đã cài${NC}"

# --- 5. Tạo cấu trúc thư mục ---
echo -e "${YELLOW}[5/6] Tạo thư mục...${NC}"
mkdir -p server/face_db
mkdir -p server/templates
mkdir -p attacker
mkdir -p defender/dataset/real
mkdir -p defender/dataset/fake
mkdir -p defender/output
echo -e "${GREEN}  [+] Thư mục đã tạo${NC}"

# --- 6. Setup virtual webcam (Linux only) ---
echo -e "${YELLOW}[6/6] Setup virtual webcam...${NC}"
if [ -f /etc/os-release ]; then
    if lsmod | grep -q v4l2loopback; then
        echo -e "${GREEN}  [+] v4l2loopback đã load${NC}"
    else
        echo "  Đang load v4l2loopback..."
        sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="FakeWebcam" exclusive_caps=1 2>/dev/null || true
        if [ -e /dev/video20 ]; then
            echo -e "${GREEN}  [+] Virtual webcam ready: /dev/video20${NC}"
        else
            echo -e "${YELLOW}  [*] Không thể tạo virtual webcam (có thể cần reboot)${NC}"
        fi
    fi
else
    echo -e "${YELLOW}  [*] Không phải Linux - bỏ qua virtual webcam${NC}"
fi

# --- Done ---
echo ""
echo -e "${CYAN}================================================================${NC}"
echo -e "${GREEN}  SETUP HOÀN TẤT!${NC}"
echo -e "${CYAN}================================================================${NC}"
echo ""
echo -e "${YELLOW}HƯỚNG DẪN SỬ DỤNG:${NC}"
echo ""
echo "  1. Kích hoạt venv:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Chạy server (VULNERABLE - không có liveness):"
echo "     cd server && python app.py"
echo "     => Mở http://localhost:5000"
echo ""
echo "  3. Đăng ký khuôn mặt qua giao diện web"
echo ""
echo "  4. Chạy tấn công INJECTION:"
echo "     cd attacker"
echo "     python 03_injection_attack.py --target http://localhost:5000 --image <ảnh_nạn_nhân>"
echo ""
echo "  5. Chạy tấn công REPLAY (Linux):"
echo "     sudo modprobe v4l2loopback devices=1 video_nr=20 card_label=\"FakeWebcam\""
echo "     cd attacker"
echo "     python 02_replay_attack.py --mode image --source <ảnh_nạn_nhân>"
echo ""
echo "  6. Tạo dataset liveness:"
echo "     cd defender"
echo "     python create_dataset.py --class real --num 200"
echo "     python create_dataset.py --class fake --num 200"
echo "     python create_dataset.py --synthetic   # tạo thêm ảnh fake tổng hợp"
echo ""
echo "  7. Train liveness model:"
echo "     cd defender"
echo "     python train_liveness.py"
echo ""
echo "  8. Chạy server SECURED (có liveness detection):"
echo "     cd server && python app_secured.py"
echo "     => Thử lại injection attack => BỊ CHẶN!"
echo ""
echo -e "${CYAN}================================================================${NC}"

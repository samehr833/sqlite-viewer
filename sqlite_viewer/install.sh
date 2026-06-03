#!/bin/bash
# SQLite Viewer - Termux Installer
# Created By CommandO | In Collaboration With XR Studio

echo "══════════════════════════════════════════════════════════════"
echo "  SQLite Viewer - Termux Installation"
echo "  Created By CommandO | In Collaboration With XR Studio"
echo "══════════════════════════════════════════════════════════════"

# تحديث الحزم
echo "[1/5] Updating packages..."
pkg update -y && pkg upgrade -y

# تثبيت المتطلبات
echo "[2/5] Installing requirements..."
pkg install python git -y

# تحميل المشروع
echo "[3/5] Downloading SQLite Viewer..."
git clone https://github.com/yourusername/sqlite-viewer.git
cd sqlite-viewer

# تثبيت المكتبات
echo "[4/5] Installing Python libraries..."
pip install tabulate colorama

# تشغيل البرنامج
echo "[5/5] Starting SQLite Viewer..."
echo "══════════════════════════════════════════════════════════════"
python main.py
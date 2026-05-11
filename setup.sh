#!/bin/bash

# OmniCloudRun Pro Termux Setup
echo "[*] Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing required packages..."
pkg install -y python git wget curl

echo "[*] Installing Python dependencies..."
pip install --upgrade pip
pip install rich textual google-cloud google-auth google-auth-oauthlib google-cloud-run

# Check if gcloud exists
if ! command -v gcloud &> /dev/null
then
    echo "[*] Installing Google Cloud SDK..."
    # Download Google Cloud SDK
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-431.0.0-linux-x86_64.tar.gz
    tar -xzf google-cloud-sdk-431.0.0-linux-x86_64.tar.gz
    ./google-cloud-sdk/install.sh --quiet
    source ./google-cloud-sdk/path.bash.inc
fi

# Authenticate gcloud
echo "[*] Authenticating Google Cloud..."
gcloud auth login
gcloud config set project $(gcloud projects list | awk 'NR==2{print $1}')

# Ensure directories exist
mkdir -p logs config assets

# Copy default config if missing
if [ ! -f config/config.json ]; then
    echo "[*] Copying default config..."
    cp config/config.json.default config/config.json
fi

# Launch OmniCloudRun Pro
echo "[*] Launching OmniCloudRun Pro..."
python main.py
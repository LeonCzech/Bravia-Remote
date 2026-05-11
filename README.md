# BraviaRemote: Multi-Platform Sony Control

A lightweight, high-performance Python-based remote control system for Sony Bravia TVs. This project allows you to control your TV directly from your computer keyboard using Sony's internal IP Control API, bypassing the need for the official mobile app or a physical remote.

---

## 📺 TV Setup

Before running the scripts, you must enable remote access on your Sony Bravia TV:

1.  **Enable IP Control:**
    *   Navigate to **Settings** → **Network & Internet** → **Home network setup** → **IP control**.
2.  **Set Authentication:**
    *   Change **Authentication** to **Pre-Shared Key**.
3.  **Set the PSK:**
    *   Select **Pre-Shared Key** and enter your desired code (e.g., `1234`).
4.  **Simple IP Control:**
    *   (Optional) Enable **Simple IP Control** for faster response times.
5.  **Identify TV IP:**
    *   Go to **Settings** → **Network & Internet** → **Network status** and note down the **IPv4 Address** (e.g., `192.168.2.31`).

---

## 🚀 Installation & Usage

### Prerequisites
Both versions require the `requests` library. Open your terminal/command prompt and run:
```bash
pip install requests

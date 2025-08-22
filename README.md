# 🖥️ TungDiag - System Diagnostics App

Tungdiag is a **Python-based desktop application** that collects and displays detailed hardware and system information through a modern graphical interface.  
It also logs diagnostic data into a **PostgreSQL database** and allows exporting reports in multiple formats.  
For end-users, Tungdiag can also be packaged into a **standalone Windows executable (.exe)** for quick installation and usage without requiring Python.

---

## ✨ Essential Key Features:
- 📊 **System Diagnostics**;
  - CPU, GPU, RAM, Motherboard, Audio Devices, Network, and Operating System details
- 🗄️ **Database Logging**;
  - Automatically stores diagnostic data into PostgreSQL (`jsonb` format)
- 💾 **Report Export**;
  - Save full reports as **JSON, CSV, TXT, or PDF**
- 🎨 **Modern GUI**;
  - Built with **Tkinter + ttkbootstrap**  
  - Light theme & Dark theme toggle
- 🔄 **Real-time Updates**;
  - Refresh buttons for each tab
- 💻 **Cross-platform**;
  - Runs on Linux (source code) and Windows (source code & executable build)

---

## 📦 Installation Tips:

### Requirements:
- **Python 3.8+**
- **IDE**
- **PostgreSQL** (for database logging)
- Dependencies listed in `requirements.txt`

### Install dependencies:
- pip install -r requirements.txt

---

## İmportant Reminder:
- 💥 The ** .idea/ ** folder has been deleted from the repository because it contains IDE settings.

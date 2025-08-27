# 🖥️ TungDiag - System Diagnostics App

Tungdiag is a **Python-based desktop application** that collects and displays detailed hardware and system information through a modern graphical interface.  
It also logs diagnostic data into a **PostgreSQL database** and allows exporting reports in multiple formats.  
For end-users, Tungdiag can also be packaged into a **standalone Windows executable (.exe)** for quick installation and usage without requiring Python. (Check **Releases** section)

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

## 📁 Project Structure:

```
├── build/
├── dist/
├── tungDiag.py
├── tundiag_sql.sql
├── requirements.txt
├── tungDiag.spec
└── .gitignore
```
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-brightgreen?logo=windows)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📦 Installation Tips:

### Requirements:
- **Python 3.10+**
- **PostgreSQL 17+** (for database logging)
- Dependencies listed in `requirements.txt`

### Install dependencies:
    pip install -r requirements.txt

---

## 💥 İmportant Reminder:

- Don't forget to change the database information in the code!

---

## 👑 Author:

        Tunç KUL
    Computer Engineer

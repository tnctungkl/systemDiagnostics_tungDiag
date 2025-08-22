import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkbootstrap import Style
import platform
import socket
import psutil
import cpuinfo
import locale
import json
import csv
import threading
import sounddevice as sd
import requests
import speedtest
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TUNDIAG_DB = {
    "dbname": os.getenv("TUNDIAG_DB_NAME", ":) Your DB Name Here :)"),
    "user": os.getenv("TUNDIAG_DB_USER", ":) Your DB User Name Here :)"),
    "password": os.getenv("TUNDIAG_DB_PASSWORD", ":) Your Password Here :)"),
    "host": os.getenv("TUNDIAG_DB_HOST", ":) Your DC Host Here :)"),
    "port": os.getenv("TUNDIAG_DB_PORT", "5432 (default but you can write your db port)")
}

try:
    import GPUtil
    gputil_available = True
except ImportError:
    gputil_available = False
try:
    import wmi
    wmi_available = True
except ImportError:
    wmi_available = False

def get_cname():
    return f"Computer Name: {socket.gethostname()}"

def get_cmodel():
    if not wmi_available:
        return "Model Info: WMI not available"
    try:
        w = wmi.WMI()
        for sys in w.Win32_ComputerSystem():
            return f"Manufacturer: {sys.Manufacturer}\nModel: {sys.Model}"
    except:
        return "Model Info: Error accessing WMI"

def get_gpu():
    if not gputil_available:
        return "GPU Info: GPUtil not installed"
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "GPU Info: No GPU Found"
    info = ""
    for i, gpu in enumerate(gpus):
        info += (
            f"GPU {i+1}: {gpu.name}\n"
            f"  Memory Total: {gpu.memoryTotal}MB\n"
            f"  Memory Free: {gpu.memoryFree}MB\n"
            f"  Driver: {gpu.driver}\n"
            f"  Temperature: {gpu.temperature}°C\n\n"
        )
    return info.strip()

def get_cpu():
    try:
        info = cpuinfo.get_cpu_info()
        return (
            f"Brand: {info['brand_raw']}\n"
            f"Arch: {info['arch']}\n"
            f"Cores: {psutil.cpu_count(logical=False)}\n"
            f"Threads: {psutil.cpu_count()}\n"
            f"Frequency: {psutil.cpu_freq().current:.2f} MHz"
        )
    except:
        return "CPU Info: Unavailable"

def get_rams():
    try:
        ram = psutil.virtual_memory()
        return (
            f"Total RAM: {round(ram.total / (1024 ** 3), 2)} GB\n"
            f"Available: {round(ram.available / (1024 ** 3), 2)} GB\n"
            f"Used: {round(ram.used / (1024 ** 3), 2)} GB ({ram.percent}%)"
        )
    except:
        return "RAM Info: Unavailable"

def get_motherboard():
    if not wmi_available:
        return "Motherboard Info: WMI not available"
    try:
        w = wmi.WMI()
        for board in w.Win32_BaseBoard():
            return (
                f"Manufacturer: {board.Manufacturer}\n"
                f"Product: {board.Product}\n"
                f"Serial: {board.SerialNumber}"
            )
    except:
        return "Motherboard Info: Unavailable"

def get_system():
    return (
        f"OS: {platform.system()} {platform.release()}\n"
        f"Version: {platform.version()}\n"
        f"Machine: {platform.machine()}\n"
        f"Processor: {platform.processor()}"
    )

def get_language():
    try:
        lang = locale.getlocale()
        encoding = locale.getpreferredencoding(False)
        return f"System Language: {lang[0]}\nEncoding: {encoding}"
    except:
        return "Language Info: Unavailable"

def get_audio_devices():
    try:
        comp_devices = sd.query_devices()
        default_input = sd.default.device[0]
        default_output = sd.default.device[1]
        input_devices = []
        output_devices = []
        for i, device in enumerate(comp_devices):
            dvc_name = device['name']
            if device['max_input_channels'] > 0:
                star = " ★" if i == default_input else ""
                input_devices.append(f"{len(input_devices)+1}. {star} {dvc_name}")
            if device['max_output_channels'] > 0:
                star = " ★" if i == default_output else ""
                output_devices.append(f"{len(output_devices)+1}. {star} {dvc_name}")
        result = ""
        if input_devices:
            result += "**Input Devices:**\n" + "\n".join(input_devices) + "\n\n"
        else:
            result += "No input devices found.\n\n"
        if output_devices:
            result += "**Output Devices:**\n" + "\n".join(output_devices)
        else:
            result += "No output devices found."
        return result.strip()
    except Exception as e:
        return f"Audio Info: Error - {e}"

def get_cnetwork():
    data = {}
    try:
        d_hostname = socket.gethostname()
        data["Hostname"] = d_hostname
        data["Internal IP"] = socket.gethostbyname(d_hostname)
    except:
        data["Internal IP"] = "Unavailable"
    try:
        external_ip = requests.get('https://api.ipify.org').text
        data["External IP"] = external_ip
    except:
        data["External IP"] = "Unavailable"
    try:
        spdtst = speedtest.Speedtest()
        spdtst.get_best_server()
        download_speed = spdtst.download() / 1_000_000
        upload_speed = spdtst.upload() / 1_000_000
        data["Download Mbps"] = f"{download_speed:.2f} Mbps"
        data["Upload Mbps"] = f"{upload_speed:.2f} Mbps"
    except:
        data["Download Mbps"] = "Unavailable"
        data["Upload Mbps"] = "Unavailable"
    try:
        respond = requests.get(f"https://ipinfo.io/{data.get('External IP', '')}/json").json()
        data["Operator"] = respond.get("org", "Unavailable")
    except:
        data["Operator"] = "Unavailable"
    result = ""
    for k, v in data.items():
        result += f"{k}: {v}\n"
    return result.strip()

def insert_log():
    try:
        data = {
            "Computer Name": get_cname(),
            "Model": get_cmodel(),
            "GPU": get_gpu(),
            "CPU": get_cpu(),
            "RAM": get_rams(),
            "Motherboard": get_motherboard(),
            "Operating System": get_system(),
            "Language": get_language(),
            "Audio Devices": get_audio_devices(),
            "Network": get_cnetwork()
        }

        pos_conn = psycopg2.connect(**TUNDIAG_DB)
        print("PostgreSQL.. connected!✅")
        pos_curs = pos_conn.cursor()
        pos_curs.execute(
            "INSERT INTO system_logs (log_time, data) VALUES (%s, %s::jsonb)",
            (datetime.now(), json.dumps(data, ensure_ascii=False))
        )
        pos_conn.commit()
        pos_curs.close()
        pos_conn.close()

        print(f"[LOGGED] {datetime.now()} -> Log succesfully saved to PostgreSQL.")

    except Exception as e:
        print(f"❌PostgreSQL Log Issue: {e}")

tabs = {
    "Computer Name": get_cname,
    "Model": get_cmodel,
    "GPU": get_gpu,
    "CPU": get_cpu,
    "RAM": get_rams,
    "Motherboard": get_motherboard,
    "Operating System": get_system,
    "Language": get_language,
    "Audio Devices": get_audio_devices,
    "Network": get_cnetwork,
}

root = tk.Tk()
root.title("Tundiag - System Diagnostics")
root.geometry("960x700")
current_theme = "darkly"
style = Style(current_theme)

top_frame = tk.Frame(root, bg=style.colors.bg)
top_frame.pack(side="top", fill="x")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)
tab_frames = {}

for title, func in tabs.items():
    frame = tk.Frame(notebook, bg=style.colors.bg)
    notebook.add(frame, text=title)
    tab_frames[title] = (frame, func)

def threaded_network_load(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    loading_label = tk.Label(frame, text="Loading, please wait...", font=("Consolas", 12),
                             bg=style.colors.bg, fg=style.colors.fg)
    loading_label.pack(padx=30, pady=30, anchor="w")

    def worker():
        info = get_cnetwork()

        def update_ui():
            loading_label.destroy()
            label = tk.Label(frame, text=info, font=("Consolas", 12), wraplength=900,
                             justify="left", bg=style.colors.bg, fg=style.colors.fg)
            label.pack(padx=30, pady=30, anchor="w")
            refresh_btn = ttk.Button(frame, text="🔄 Refresh",
                                     command=lambda: [load_tab_content("Network"), insert_log()])
            refresh_btn.pack(anchor="se", padx=20, pady=10)

        root.after(0, update_ui)

    threading.Thread(target=worker, daemon=True).start()

def load_tab_content(title):
    frame, func = tab_frames[title]
    for widget in frame.winfo_children():
        widget.destroy()
    if title == "Network":
        threaded_network_load(frame)
    else:
        try:
            info = func()
        except Exception as e:
            info = f"Error: {str(e)}"
        label = tk.Label(frame, text=info, font=("Consolas", 12), wraplength=900,
                         justify="left", bg=style.colors.bg, fg=style.colors.fg)
        label.pack(padx=30, pady=30, anchor="w")

        refresh_btn = ttk.Button(
            frame,
            text="🔄 Refresh",
            command=lambda: [load_tab_content(title), insert_log()]  # LOG EKLENDİ
        )
        refresh_btn.pack(anchor="se", padx=20, pady=10)

    if title == list(tabs.keys())[0]:
        insert_log()

def on_tab_change(event):
    selected_tab_index = notebook.index("current")
    selected_title = notebook.tab(selected_tab_index, "text")
    load_tab_content(selected_title)

notebook.bind("<<NotebookTabChanged>>", on_tab_change)
load_tab_content(list(tabs.keys())[0])

def toggle_theme():
    global current_theme, style
    current_theme = "flatly" if current_theme == "darkly" else "darkly"
    style.theme_use(current_theme)
    if current_theme == "flatly":
        bg_color = "#f5f7fa"
        fg_color = "#2e2e2e"
        frame_border_color = "#d1d9e6"
        font_family = "Segoe UI Semibold"
        icon = "☀️"
    else:
        bg_color = style.colors.bg
        fg_color = style.colors.fg
        frame_border_color = None
        font_family = "Consolas"
        icon = "🌙"
    notebook.configure(style="TNotebook")
    root.configure(bg=bg_color)
    toggle_bttn.configure(style="TButton", text=f"{icon} Toggle Theme")
    for title, (frame, _) in tab_frames.items():
        frame.configure(bg=bg_color, highlightbackground=frame_border_color,
                        highlightthickness=1 if current_theme == "flatly" else 0, bd=0, relief="flat")
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=bg_color, fg=fg_color,
                                 font=(font_family, 12, "bold" if current_theme == "flatly" else "normal"))


toggle_bttn = ttk.Button(top_frame, text="🌙  Toggle Theme", command=toggle_theme)
toggle_bttn.pack(side="right", padx=10, pady=10)
root.configure(bg=style.colors.bg)

bttm_fr = tk.Frame(root, bg=style.colors.bg)
bttm_fr.pack(side="bottom", fill="x", pady=5)

def all_save():
    wins = tk.Toplevel(root)
    wins.title("Save All System Info")
    wins.geometry("350x250")
    wins.configure(bg=style.colors.bg)

    def save_as(format):
        data = {}
        for title, func in tabs.items():
            try:
                data[title] = func()
            except Exception as e:
                data[title] = f"Error: {e}"
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{format}",
            filetypes=[(f"{format.upper()} files", f"*.{format}"), ("All files", "*.*")]
        )
        if not filename:
            return
        try:
            if format == "json":
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            elif format == "csv":
                with open(filename, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Section", "Info"])
                    for section, info in data.items():
                        clean_info = info.replace("\n", " | ").replace("\r", "")
                        writer.writerow([section, clean_info])
            elif format == "txt":
                with open(filename, "w", encoding="utf-8") as f:
                    for section, info in data.items():
                        f.write(f"--- {section} ---\n{info}\n\n")
            elif format == "pdf":
                from fpdf import FPDF
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=10)
                pdf.add_page()
                pdf.set_font("Courier", size=11)
                for section, info in data.items():
                    pdf.set_font("Courier", "B", 12)
                    pdf.cell(0, 10, f"--- {section} ---", ln=True)
                    pdf.set_font("Courier", size=11)
                    for line in info.splitlines():
                        pdf.multi_cell(0, 6, line)
                    pdf.ln(4)
                pdf.output(filename)
            messagebox.showinfo("Success", f"File saved as:\n{filename}")
            wins.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

    ttk.Button(wins, text="Save as JSON", command=lambda: save_as("json")).pack(pady=5, fill="x", padx=20)
    ttk.Button(wins, text="Save as CSV", command=lambda: save_as("csv")).pack(pady=5, fill="x", padx=20)
    ttk.Button(wins, text="Save as PDF", command=lambda: save_as("pdf")).pack(pady=5, fill="x", padx=20)
    ttk.Button(wins, text="Save as TXT", command=lambda: save_as("txt")).pack(pady=5, fill="x", padx=20)


ttk.Button(bttm_fr, text="Save", command=all_save).pack(pady=10)

root.mainloop()

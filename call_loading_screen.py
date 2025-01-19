# loading_screen.py
import tkinter as tk
from tkinter import ttk

def loading_window():
    load_win = tk.Toplevel()
    load_win.title("กำลังโหลด...")

    # ตั้งค่าให้หน้าต่างอยู่กลางจอ
    window_width = 300
    window_height = 100
    screen_width = load_win.winfo_screenwidth()
    screen_height = load_win.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    load_win.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    
    label = tk.Label(load_win, text="กำลังประมวลผล โปรดรอสักครู่...")
    label.pack(pady=10)

    # ใช้ determinate mode เพื่อแสดงความคืบหน้า
    progress_bar = ttk.Progressbar(load_win, orient="horizontal", mode="determinate", length=250)
    progress_bar.pack(pady=10)
    progress_bar["maximum"] = 100  # กำหนดค่าเต็มที่ 100%

    return load_win, progress_bar

def update_progress(progress_bar, value):
    progress_bar["value"] = value  # อัปเดตค่า Progress bar

def close_loading_window(load_win):
    load_win.destroy()
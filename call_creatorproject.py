import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import data_storage
def createprojectname(text_info):
    ROOT = tk.Tk()
    ROOT.resizable(False, False)
    ROOT.withdraw()

    while True:
        USER_INP = simpledialog.askstring(title=" ", prompt="What's your project Name?")
        if USER_INP is None:
            ROOT.destroy()
            print("User cancelled the project creation.")
            return None
        elif len(USER_INP) < 6:
            messagebox.showerror("Error", "Project name must be at least 6 characters long.")
            continue

        data_storage.projectname = USER_INP
        print(data_storage.selected_customer)
        
        # สร้างเส้นทางโฟลเดอร์ที่ต้องการ โดยใช้ค่าจาก selected_customer
        project_path = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname)
        
        if os.path.exists(project_path):
            messagebox.showerror("Error", "Project name already exists. Please choose a different name.")
        else:
            try:
                # สร้างโฟลเดอร์ในเส้นทางที่ระบุ
                os.makedirs(project_path)
                # messagebox.showinfo("Info", "Project created successfully.")
                
                # # อัปเดตข้อความใน text_widget
                text_info.configure(state="normal")
                text_info.delete("1.0", "end")
                text_info.insert(tk.END, f"{USER_INP} created successfully\n")
                text_info.configure(state="disabled")
                
                ROOT.destroy()
                return project_path, data_storage.Main_folder  # ส่งคืนค่าเส้นทางที่สร้างใหม่
            except Exception as e:
                print(f"An error occurred during project creation: {e}")
                ROOT.destroy()
                return None

    ROOT.destroy()
    return None
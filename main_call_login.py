import tkinter as tk
from tkinter import ttk, messagebox
import data_storage  # นำเข้าโมดูล data_storage

# ฟังก์ชันหลักในการจัดการระบบล็อกอิน
def main_login(root_window, user_text):
    # ฟังก์ชันตรวจสอบการล็อกอิน
    def login_system(credentials, username_input, password_input, window, user_text):
        username = username_input.get()
        password = password_input.get()

        # ตรวจสอบ username และ password จาก credentials
        if username in credentials and password == credentials.get(username):
            data_storage.logged_in_user = username  
            user_text.config(state='normal')  # ปลดล็อค Text widget ก่อนใส่ค่าใหม่
            user_text.delete("1.0", tk.END)  # ลบข้อความเดิมใน user_text
            user_text.insert("1.0",username, 'center')  # ใส่ username ลงใน Text widget พร้อม tag 'center'
            user_text.tag_configure('center', justify='center')  # กำหนดค่าให้ tag 'center' จัดข้อความให้อยู่กึ่งกลาง
            user_text.config(state='disabled')  # ล็อค Text widget ไม่ให้แก้ไข
            window.destroy()  # ปิดหน้าต่างล็อกอินเมื่อสำเร็จ
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    # ฟังก์ชันสำหรับปิดโปรแกรมเมื่อปิดหน้าต่างล็อกอิน
    def on_close():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root_window.quit()
            root_window.destroy()
    root_window.protocol("WM_DELETE_WINDOW", on_close)

    # ฟังก์ชันสร้างหน้าต่างล็อกอิน
    def create_login_window(credentials):
        window = tk.Toplevel(root_window)  # สร้างหน้าต่างใหม่จาก Toplevel
        window.title("Login")
        window.geometry("400x500")
        window.resizable(False, False)

        # ทำให้หน้าต่างล็อกอินขึ้นตรงกลางหน้าจอด้วยการคำนวณตำแหน่งเอง
        window.update_idletasks()  # อัปเดตขนาดหน้าต่าง
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = 400
        window_height = 300
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        window.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        snow_color = '#FFFAFA'
        frame_bg_color = '#DCDCDC'
        text_color = '#2C3E50'

        background_frame = tk.Frame(window, bg=snow_color)
        background_frame.place(relwidth=1, relheight=1)

        login_frame = tk.Frame(background_frame, bg=frame_bg_color, bd=5)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(login_frame, text="Username:", bg=frame_bg_color, fg=text_color, font=('Helvetica', 14)).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(login_frame, text="Password:", bg=frame_bg_color, fg=text_color, font=('Helvetica', 14)).grid(row=1, column=0, padx=10, pady=10)
        
        # ช่องกรอก username และ password
        username_input = ttk.Entry(login_frame, width=25)
        password_input = ttk.Entry(login_frame, show="*", width=25)
        username_input.grid(row=0, column=1, padx=10, pady=10)
        password_input.grid(row=1, column=1, padx=10, pady=10)

        # ปุ่มล็อกอินที่เรียกใช้ login_system
        login_button = ttk.Button(login_frame, text="Login", command=lambda: login_system(credentials, username_input, password_input, window, user_text))
        login_button.grid(row=2, column=0, columnspan=2, pady=20)

        # ทำให้ปุ่ม Enter ทำหน้าที่เหมือนการกดปุ่ม Login
        window.bind('<Return>', lambda event: login_system(credentials, username_input, password_input, window, user_text))

        window.transient(root_window)  # ทำให้หน้าต่าง Toplevel อยู่ด้านหน้าของ root_window
        window.grab_set()  # ป้องกันการใช้งานหน้าต่างอื่นในขณะที่ Toplevel เปิดอยู่
        window.protocol("WM_DELETE_WINDOW", on_close)  # ปิดโปรแกรมเมื่อปิดหน้าต่าง

    # เรียกใช้ฟังก์ชันสร้างหน้าต่างล็อกอินโดยส่ง credentials จาก data_storage
    create_login_window(data_storage.credentials)
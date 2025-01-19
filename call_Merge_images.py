# import os
# import tkinter as tk
# from tkinter import filedialog, messagebox, simpledialog
# from PIL import Image
# import data_storage
# def create_gui(on_complete=None):
#     """
#     สร้าง GUI สำหรับเลือกไฟล์ PNG และส่งค่ากลับผ่าน callback function
#     """
#     root = tk.Toplevel()
#     root.title("File Selector with Preview")
#     root.geometry("340x450")
#     root.configure(bg="#f0f8ff")

#     # ทำให้หน้าต่างอยู่ด้านบนสุดเสมอ
#     root.attributes('-topmost', True)
#     root.lift()  # ยกหน้าต่างขึ้นด้านบนสุด
#     root.focus_force()  # บังคับให้หน้าต่างรับโฟกัส

#     file_checkboxes = {}
#     folder_path = ""

#     # ฟังก์ชันสำหรับแสดงโฟลเดอร์ที่เลือกใน Textbox
#     def update_folder_display():
#         folder_display.config(state="normal")
#         folder_display.delete(1.0, tk.END)  # ล้างข้อมูลใน Textbox
#         folder_name = os.path.basename(folder_path)  # ดึงชื่อโฟลเดอร์
#         folder_display.insert(tk.END, folder_name)  # ใส่ชื่อโฟลเดอร์ใน Textbox
#         folder_display.tag_add("center", "1.0", "end")  # จัดข้อความให้อยู่ตรงกลาง
#         folder_display.config(state="disabled")  # ปิดการแก้ไข

#     def select_and_preview_folder():
#         nonlocal folder_path
#         initial_path = os.path.join(data_storage.Main_folder, data_storage.selected_customer)
#         # สร้างหน้าต่าง dialog สำหรับเลือกโฟลเดอร์ และตั้งให้อยู่ด้านบน
#         root.attributes('-topmost', False)  # ปิดสถานะ "topmost" ชั่วคราว
#         folder_path = filedialog.askdirectory(initialdir=initial_path, parent=root)
#         root.attributes('-topmost', True)  # เปิดสถานะ "topmost" อีกครั้ง

#         if not folder_path:  # หากผู้ใช้กดยกเลิก
#             return

#         try:
#             files = [file for file in os.listdir(folder_path) if file.lower().endswith('.png')]
#             if not files:
#                 messagebox.showinfo("No PNG Files Found", "No PNG files found in the selected folder.", parent=root)
#                 return

#             # อัปเดต Textbox แสดงชื่อโฟลเดอร์ที่เลือก
#             update_folder_display()

#             # ล้างเนื้อหาในกรอบก่อนหน้า
#             for widget in file_frame.winfo_children():
#                 widget.destroy()
#             file_checkboxes.clear()

#             # สร้าง Checkbutton สำหรับแต่ละไฟล์
#             for file in files:
#                 var = tk.BooleanVar()
#                 checkbox = tk.Checkbutton(file_frame, text=file, variable=var, font=("Arial", 10), bg="white")
#                 checkbox.pack(anchor="w", pady=2, padx=10)
#                 file_checkboxes[file] = var
#         except Exception as e:
#             messagebox.showerror("Error", f"Unable to preview files: {e}", parent=root)

#     def process_files():
#         """
#         ดำเนินการลบพื้นหลังและรวมรูปภาพ
#         """
#         selected_files = [file for file, var in file_checkboxes.items() if var.get()]
#         if not selected_files:
#             messagebox.showinfo("No Files Selected", "Please select at least one file.", parent=root)
#             return

#         # ขอชื่อไฟล์จากผู้ใช้
#         file_name = simpledialog.askstring("File Name", "Enter the name for the combined image:", parent=root)
#         if not file_name:
#             messagebox.showinfo("Error", "Please provide a valid file name.", parent=root)
#             return

#         result_filename = f"{file_name}.png"
#         images = []

#         try:
#             # ลบพื้นหลังสำหรับแต่ละไฟล์
#             for file in selected_files:
#                 file_path = os.path.join(folder_path, file)
#                 img = Image.open(file_path).convert("RGBA")
#                 img_no_bg = remove_black_background(file_path)
#                 images.append(img_no_bg)

#             # รวมรูปภาพและเพิ่มพื้นหลังสีขาว
#             output_path = os.path.join(folder_path, result_filename)
#             combine_images_with_white_background(images, output_path)

#             # แจ้งผู้ใช้สำเร็จ
#             messagebox.showinfo("Success", f"Combined image saved to: {output_path}", parent=root)
#         except Exception as e:
#             messagebox.showerror("Error", f"Error processing files: {e}", parent=root)

#     # ปุ่มเลือกโฟลเดอร์
#     select_preview_button = tk.Button(
#         root, text="Select & Preview Folder", command=select_and_preview_folder,
#         bg="#007bff", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5
#     )
#     select_preview_button.pack(pady=10)

#     # Textbox แสดงชื่อโฟลเดอร์ที่เลือก
#     folder_display = tk.Text(root, height=1, font=("Arial", 12), wrap="none", bg="white", state="disabled")
#     folder_display.tag_configure("center", justify="center")  # จัดข้อความให้อยู่ตรงกลาง
#     folder_display.pack(pady=5, padx=10, fill="x")

#     # กรอบแสดง Checkbutton
#     file_frame = tk.Frame(root, bg="white", bd=2, relief="solid", height=200, width=500)
#     file_frame.pack(pady=10, padx=10, fill="both", expand=True)

#     # ปุ่ม Process
#     process_button = tk.Button(
#         root, text="Process Files", command=process_files,
#         bg="#4caf50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5
#     )
#     process_button.pack(pady=10)

#     root.mainloop()

# def remove_black_background(image_path):
#     """
#     ลบพื้นหลังสีดำและทำให้โปร่งใส
#     """
#     img = Image.open(image_path).convert("RGBA")
#     datas = img.getdata()
#     new_data = [(255, 255, 255, 0) if item[:3] == (0, 0, 0) else item for item in datas]
#     img.putdata(new_data)
#     return img

# def combine_images_with_white_background(images, output_path):
#     """
#     รวมรูปภาพและเพิ่มพื้นหลังสีขาว
#     """
#     base_image = images[0]
#     width, height = base_image.size

#     for img in images[1:]:
#         img_resized = img.resize((width, height), Image.LANCZOS)
#         base_image = Image.alpha_composite(base_image, img_resized)

#     white_background = Image.new("RGBA", (width, height), (255, 255, 255, 255))
#     final_image = Image.alpha_composite(white_background, base_image)

#     final_image.save(output_path, "PNG")
#     print(f"Combined image saved to: {output_path}")

import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import data_storage

def create_gui(on_complete=None):
    """
    สร้าง GUI สำหรับเลือกไฟล์ PNG และส่งค่ากลับผ่าน callback function
    """
    root = tk.Toplevel()
    root.title("File Selector with Preview")
    root.geometry("340x500")
    root.configure(bg="#f0f8ff")

    # ทำให้หน้าต่างอยู่ด้านบนสุดเสมอ
    root.attributes('-topmost', True)
    root.lift()  # ยกหน้าต่างขึ้นด้านบนสุด
    root.focus_force()  # บังคับให้หน้าต่างรับโฟกัส

    file_checkboxes = {}
    folder_path = ""

    # ฟังก์ชันสำหรับแสดงโฟลเดอร์ที่เลือกใน Textbox
    def update_folder_display():
        folder_display.config(state="normal")
        folder_display.delete(1.0, tk.END)  # ล้างข้อมูลใน Textbox
        folder_name = os.path.basename(folder_path)  # ดึงชื่อโฟลเดอร์
        folder_display.insert(tk.END, folder_name)  # ใส่ชื่อโฟลเดอร์ใน Textbox
        folder_display.tag_add("center", "1.0", "end")  # จัดข้อความให้อยู่ตรงกลาง
        folder_display.config(state="disabled")  # ปิดการแก้ไข

    def select_and_preview_folder():
        nonlocal folder_path
        initial_path = os.path.join(data_storage.Main_folder, data_storage.selected_customer)
        # สร้างหน้าต่าง dialog สำหรับเลือกโฟลเดอร์ และตั้งให้อยู่ด้านบน
        root.attributes('-topmost', False)  # ปิดสถานะ "topmost" ชั่วคราว
        folder_path = filedialog.askdirectory(initialdir=initial_path, parent=root)
        root.attributes('-topmost', True)  # เปิดสถานะ "topmost" อีกครั้ง

        if not folder_path:  # หากผู้ใช้กดยกเลิก
            return

        try:
            files = [file for file in os.listdir(folder_path) if file.lower().endswith('.BMP')]
            if not files:
                messagebox.showinfo("No PNG Files Found", "No PNG files found in the selected folder.", parent=root)
                return

            # อัปเดต Textbox แสดงชื่อโฟลเดอร์ที่เลือก
            update_folder_display()

            # ล้างเนื้อหาในกรอบก่อนหน้า
            for widget in file_frame.winfo_children():
                widget.destroy()
            file_checkboxes.clear()

            # สร้าง Checkbutton สำหรับแต่ละไฟล์
            for file in files:
                var = tk.BooleanVar()
                checkbox = tk.Checkbutton(file_frame, text=file, variable=var, font=("Arial", 10), bg="white")
                checkbox.pack(anchor="w", pady=2, padx=10)
                file_checkboxes[file] = var
        except Exception as e:
            messagebox.showerror("Error", f"Unable to preview files: {e}", parent=root)

    def process_files():
        """
        ดำเนินการลบพื้นหลังและรวมรูปภาพ
        """
        selected_files = [file for file, var in file_checkboxes.items() if var.get()]
        if not selected_files:
            messagebox.showinfo("No Files Selected", "Please select at least one file.", parent=root)
            return

        # ขอชื่อไฟล์จากผู้ใช้
        file_name = simpledialog.askstring("File Name", "Enter the name for the combined image:", parent=root)
        if not file_name:
            messagebox.showinfo("Error", "Please provide a valid file name.", parent=root)
            return

        result_filename = f"{file_name}.png"
        images = []

        try:
            # ลบพื้นหลังสำหรับแต่ละไฟล์
            for file in selected_files:
                file_path = os.path.join(folder_path, file)
                img = Image.open(file_path).convert("RGBA")
                img_no_bg = remove_black_background(file_path)
                images.append(img_no_bg)

            # รวมรูปภาพและเพิ่มพื้นหลังสีขาว
            output_path = os.path.join(folder_path, result_filename)
            combine_images_with_white_background(images, output_path)

            # แจ้งผู้ใช้สำเร็จ
            messagebox.showinfo("Success", f"Combined image saved to: {output_path}", parent=root)
        except Exception as e:
            messagebox.showerror("Error", f"Error processing files: {e}", parent=root)

    # Label สำหรับข้อความด้านบน
    header_label = tk.Label(
        root, text="Combining pictures of cad files",
        bg="#f0f8ff", font=("Arial", 14, "bold"), fg="#333"
    )
    header_label.pack(pady=10)

    # Label สำหรับ Project Name
    project_label = tk.Label(
        root, text="Project Name", 
        bg="#f0f8ff", font=("Arial", 12, "bold"), fg="#333"
    )
    project_label.pack(pady=5)

    # Textbox แสดงชื่อโฟลเดอร์ที่เลือก
    folder_display = tk.Text(root, height=1, font=("Arial", 12), wrap="none", bg="white", state="disabled")
    folder_display.tag_configure("center", justify="center")  # จัดข้อความให้อยู่ตรงกลาง
    folder_display.pack(pady=5, padx=10, fill="x")

    # ปุ่มเลือกโฟลเดอร์
    select_preview_button = tk.Button(
        root, text="Select & Preview Folder", command=select_and_preview_folder,
        bg="#007bff", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5
    )
    select_preview_button.pack(pady=10)

    # Label สำหรับ Input Combine
    input_combine_label = tk.Label(
        root, text="Input combine",
        bg="#f0f8ff", font=("Arial", 12, "bold"), fg="#333"
    )
    input_combine_label.pack(pady=5)

    # กรอบแสดง Checkbutton
    file_frame = tk.Frame(root, bg="white", bd=2, relief="solid", height=200, width=500)
    file_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # ปุ่ม Process
    process_button = tk.Button(
        root, text="Process Files", command=process_files,
        bg="#4caf50", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5
    )
    process_button.pack(pady=10)

    root.mainloop()

def remove_black_background(image_path):
    """
    ลบพื้นหลังสีดำและทำให้โปร่งใส
    """
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()
    new_data = [(255, 255, 255, 0) if item[:3] == (0, 0, 0) else item for item in datas]
    img.putdata(new_data)
    return img

def combine_images_with_white_background(images, output_path):
    """
    รวมรูปภาพและเพิ่มพื้นหลังสีขาว
    """
    base_image = images[0]
    width, height = base_image.size

    for img in images[1:]:
        img_resized = img.resize((width, height), Image.LANCZOS)
        base_image = Image.alpha_composite(base_image, img_resized)

    white_background = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    final_image = Image.alpha_composite(white_background, base_image)

    final_image.save(output_path, "PNG")
    print(f"Combined image saved to: {output_path}")

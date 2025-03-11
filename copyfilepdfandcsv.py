# import shutil
# import os
# import data_storage

# def copy_files():
#     # โฟลเดอร์ปลายทาง
#     destination_folder = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname)

#     # ตรวจสอบและสร้างโฟลเดอร์ปลายทางหากไม่มีอยู่
#     if not os.path.exists(destination_folder):
#         os.makedirs(destination_folder)

#     # ตรวจสอบว่ามี `pdf_path_top` หรือ `pdf_path_bot` หรือไม่
#     if data_storage.pdf_path_top or data_storage.pdf_path_bot:
#         pdf_files = [data_storage.pdf_path_top, data_storage.pdf_path_bot]  # ไม่ใช้ pdf_path
#     else:
#         pdf_files = [data_storage.pdf_path]  # ใช้ pdf_path แทน

#     # คัดลอกไฟล์ที่มีอยู่เท่านั้น
#     for file in pdf_files:
#         if file and os.path.exists(file):  # เช็คว่าไฟล์มีอยู่จริง
#             file_name = os.path.basename(file)  # ดึงชื่อไฟล์
#             destination_path = os.path.join(destination_folder, file_name)  # สร้างพาธปลายทาง

#             try:
#                 shutil.copy2(file, destination_path)
#                 print(f"✅ คัดลอกไฟล์ไปที่: {destination_path}")
#             except Exception as e:
#                 print(f"❌ Error: ไม่สามารถคัดลอกไฟล์ {file} ได้ -> {e}")
#         else:
#             print(f"⚠️ ข้ามไฟล์: {file} (ไม่มีอยู่จริง)")

import shutil
import os
import data_storage

def copy_files():
    """ ฟังก์ชันคัดลอกไฟล์ PDF และ CSV ไปยังโฟลเดอร์ปลายทาง """

    # โฟลเดอร์ปลายทาง
    destination_folder = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname)

    # ตรวจสอบและสร้างโฟลเดอร์ปลายทางหากไม่มีอยู่
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # ตรวจสอบว่ามี `pdf_path_top` หรือ `pdf_path_bot` หรือไม่
    if data_storage.pdf_path_top or data_storage.pdf_path_bot:
        pdf_files = [data_storage.pdf_path_top, data_storage.pdf_path_bot, data_storage.filepathcsv]  # ใช้ไฟล์ Top & Bottom
    else:
        pdf_files = [data_storage.pdf_path, data_storage.filepathcsv]  # ใช้ pdf_path แทน

    # คัดลอกไฟล์ที่มีอยู่เท่านั้น
    for file in pdf_files:
        if file and os.path.exists(file):  # เช็คว่าไฟล์มีอยู่จริง
            file_name = os.path.basename(file)  # ดึงชื่อไฟล์
            destination_path = os.path.join(destination_folder, file_name)  # สร้างพาธปลายทาง

            try:
                shutil.copy2(file, destination_path)
                print(f"✅ คัดลอกไฟล์ไปที่: {destination_path}")
            except Exception as e:
                print(f"❌ Error: ไม่สามารถคัดลอกไฟล์ {file} ได้ -> {e}")
        else:
            print(f"⚠️ ข้ามไฟล์: {file} (ไม่มีอยู่จริง)")

    print("✅ คัดลอกไฟล์เสร็จสิ้น")
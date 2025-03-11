
# import pandas as pd
# import tkinter as tk

# def check_ref_des(df, df_name, mismatch_entries):
#     for x in range(df.shape[0]):
#         ref_des = df.iat[x, 3]  # ดึงค่าจากคอลัมน์ที่ 3
#         qty = df.iat[x, 1]  # ดึงค่าจากคอลัมน์ที่ 1

#         if pd.isna(ref_des):
#             continue  # ข้ามถ้าข้อมูลเป็น NaN

#         ref_des_list = str(ref_des).split(",")

#         if len(ref_des_list) != qty:
#             mismatch_entries.append(f"❌ ค่าของ {ref_des_list} {len(ref_des_list)} ไม่ตรงกับ QTY = {qty} ")

# def check_all_data(data_storage, text_info):
#     mismatch_entries = []  # เก็บเฉพาะรายการที่ผิดพลาด

#     # ตรวจสอบข้อมูล
#     check_ref_des(data_storage.data_top, "data_top", mismatch_entries)
#     check_ref_des(data_storage.data_buttom, "data_buttom", mismatch_entries)
#     check_ref_des(data_storage.data_hl_top, "data_hl_top", mismatch_entries)

#     # อัปเดตข้อความลงใน text_info
#     text_info.configure(state="normal")  # เปิดให้แก้ไขได้

#     if mismatch_entries:
#         text_info.insert(tk.END, "\n".join(mismatch_entries) + "\n")  # แสดงเฉพาะข้อมูลที่ผิดพลาด
#     else:
#         text_info.insert(tk.END, "✅ ไฟล์ CSV ไม่มีข้อผิดพลาด\n")  # แสดงแค่ครั้งเดียวถ้าทุกอย่างถูกต้อง

#     text_info.configure(state="disabled")  # ปิดการแก้ไข
import pandas as pd
import tkinter as tk

def check_ref_des(df, df_name, mismatch_entries, text_info):
    for x in range(df.shape[0]):
        ref_des = df.iat[x, 3]  # ดึงค่าจากคอลัมน์ที่ 3
        qty = df.iat[x, 1]  # ดึงค่าจากคอลัมน์ที่ 1

        if pd.isna(ref_des):
            continue  # ข้ามถ้าข้อมูลเป็น NaN

        ref_des_list = str(ref_des).split(",")

        if len(ref_des_list) != qty:
            error_message = f"❌ ในไฟล์ CSV ค่าของ {ref_des_list} = {len(ref_des_list)} ไม่ตรงกับ QTY = {qty} กรุณาตรวจสอบ\n"
            mismatch_entries.append(error_message)

            # แสดงข้อความผิดพลาดเป็น **สีแดง และตัวหนา**
            text_info.insert(tk.END, error_message, "error_bold")

def check_all_data(data_storage, text_info):
    mismatch_entries = []  # เก็บเฉพาะรายการที่ผิดพลาด

    # ตั้งค่าสไตล์ให้ข้อความผิดพลาด (สีแดง + ตัวหนา)
    text_info.tag_configure("error_bold", foreground="red", font=("Arial", 10, "bold"))  
    text_info.configure(state="normal")  # เปิดให้แก้ไขได้

    # ตรวจสอบข้อมูล
    check_ref_des(data_storage.data_top, "data_top", mismatch_entries, text_info)
    check_ref_des(data_storage.data_buttom, "data_buttom", mismatch_entries, text_info)
    check_ref_des(data_storage.data_hl_top, "data_hl_top", mismatch_entries, text_info)

    if not mismatch_entries:
        text_info.insert(tk.END, "✅ ไฟล์ CSV ไม่มีข้อผิดพลาด\n")  # ถ้าไม่มีข้อผิดพลาด แสดงข้อความปกติ

    text_info.configure(state="disabled")  # ปิดการแก้ไข




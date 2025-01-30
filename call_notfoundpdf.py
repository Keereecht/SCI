# import fitz 
# import numpy as np
# import pandas as pd
# from tkinter import filedialog 
# import tkinter as tk
# import data_storage
# def notfoundh(text_info):
#     # docf = data_storage.pdf_path  # ระบุชื่อไฟล์ PDF ที่ต้องการ
#     if isinstance(data_storage.pdf_path, BytesIO):
#         docf = fitz.Document(stream=data_storage.pdf_path)
#     else:
#         docf = fitz.open(data_storage.pdf_path)
#     doc = fitz.open(docf)
#     all_words = []
#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)  # โหลดแต่ละหน้า
#         words = page.get_text("words")  # ดึงคำในรูปแบบ "words"
#         page_words = [word[4] for word in words]  # แยกเฉพาะคำ
#         all_words.extend(page_words)  # เพิ่มคำในรายการรวม
#     doc.close()
#     check = data_storage.df["Ref_Des"].str.split(',').explode().tolist()
#     notfound = set(check) - set(all_words)
#     data_storage.notfountlist = len(notfound)

#     checknotfound = data_storage.df[["Ref_Des", "Op_Seq"]].to_numpy()
#     expanded_data = []
#     for row in checknotfound:
#         ref_des_list = row[0].split(",")  # แยก Ref_Des ด้วย ","
#         for ref_des in ref_des_list:
#             expanded_data.append({"Ref_Des": ref_des.strip(), "Op_Seq": row[1]})
#     expanded_df = pd.DataFrame(expanded_data)
#     filtered_df = expanded_df[expanded_df["Ref_Des"].isin(notfound)]
#     filtered_array = filtered_df.to_numpy()
#         # แก้ไขค่าตามเงื่อนไข
#     filtered_array[:, 1] = np.where(filtered_array[:, 1].astype(int) == 150, "TOP", 
#                             np.where(filtered_array[:, 1].astype(int) == 50, "BOTTOM", 
#                             np.where(filtered_array[:, 1].astype(int) > 200, "HANDLOAD", filtered_array[:, 1])))
#     sorted_filtered_array = filtered_array[
#     np.lexsort((
#             filtered_array[:, 1],  # จัดเรียงตาม layer
#             np.where(filtered_array[:, 1] == "TOP", 0,  # TOP ได้ลำดับแรก
#                     np.where(filtered_array[:, 1] == "BOTTOM", 1, 2))  # BOTTOM ได้ลำดับสอง
#         ))]
#     total_count_not = 0
#     count_width = 10
#     value_width = 15
#     result_width = 15
#     count_layer = 15
#     header = f"{'Item'.ljust(count_width)}{'Layer'.ljust(count_layer)}{'Device'.ljust(value_width)}{'actual result'.ljust(result_width)}\n"
#     text_info.insert(tk.END, "-" * len(header) + "\n")
#     text_info.insert(tk.END, header)
#     text_info.insert(tk.END, "-" * len(header) + "\n")
#     for notf in sorted_filtered_array:
#             devicenf = notf [0]  # ตัวแรก (Device)
#             layernf = notf [1]   # ตัวที่สอง (Layer)
#             # count = alldf.count(notf)
#             total_count_not += 1
#             formatted_text = (
#                 f"{str(total_count_not).ljust(count_width)}"
#                 f"{layernf.ljust(count_layer)}"
#                 f"{devicenf.ljust(value_width)}"
#                 f"{'Not found'.ljust(result_width)}\n"
#             )
#             text_info.insert(tk.END,formatted_text)
#     text_info.configure(state="disabled")

import fitz
import numpy as np
import pandas as pd
from io import BytesIO  # เพิ่มการ import
from tkinter import filedialog 
import tkinter as tk
import data_storage

def notfoundh(text_info):
    docf = data_storage.pdf_path  # ไฟล์ PDF ที่ต้องการเปิด

    # ตรวจสอบประเภทของไฟล์
    if isinstance(docf, BytesIO):  
        doc = fitz.open("pdf", docf.getvalue())  # เปิดจาก memory (BytesIO)
    else:
        doc = fitz.open(docf)  # เปิดจาก path

    all_words = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # โหลดแต่ละหน้า
        words = page.get_text("words")  # ดึงคำในรูปแบบ "words"
        page_words = [word[4] for word in words]  # แยกเฉพาะคำ
        all_words.extend(page_words)  # เพิ่มคำในรายการรวม
    doc.close()

    check = data_storage.df["Ref_Des"].str.split(',').explode().tolist()
    notfound = set(check) - set(all_words)
    data_storage.notfountlist = len(notfound)

    checknotfound = data_storage.df[["Ref_Des", "Op_Seq"]].to_numpy()
    expanded_data = []
    for row in checknotfound:
        ref_des_list = row[0].split(",")  # แยก Ref_Des ด้วย ","
        for ref_des in ref_des_list:
            expanded_data.append({"Ref_Des": ref_des.strip(), "Op_Seq": row[1]})
    expanded_df = pd.DataFrame(expanded_data)
    filtered_df = expanded_df[expanded_df["Ref_Des"].isin(notfound)]
    filtered_array = filtered_df.to_numpy()

    # แก้ไขค่าตามเงื่อนไข
    filtered_array[:, 1] = np.where(
        filtered_array[:, 1].astype(int) == 150, "TOP", 
        np.where(filtered_array[:, 1].astype(int) == 50, "BOTTOM", 
        np.where(filtered_array[:, 1].astype(int) > 200, "HANDLOAD", filtered_array[:, 1]))
    )

    sorted_filtered_array = filtered_array[
        np.lexsort((
            filtered_array[:, 1],  # จัดเรียงตาม layer
            np.where(filtered_array[:, 1] == "TOP", 0,  
                     np.where(filtered_array[:, 1] == "BOTTOM", 1, 2))  
        ))
    ]

    total_count_not = 0
    count_width = 10
    value_width = 15
    result_width = 15
    count_layer = 15
    header = f"{'Item'.ljust(count_width)}{'Layer'.ljust(count_layer)}{'Device'.ljust(value_width)}{'actual result'.ljust(result_width)}\n"
    
    text_info.insert(tk.END, "-" * len(header) + "\n")
    text_info.insert(tk.END, header)
    text_info.insert(tk.END, "-" * len(header) + "\n")

    for notf in sorted_filtered_array:
        devicenf = notf[0]  
        layernf = notf[1]   
        total_count_not += 1
        formatted_text = (
            f"{str(total_count_not).ljust(count_width)}"
            f"{layernf.ljust(count_layer)}"
            f"{devicenf.ljust(value_width)}"
            f"{'Not found'.ljust(result_width)}\n"
        )
        text_info.insert(tk.END, formatted_text)
    
    text_info.configure(state="disabled")

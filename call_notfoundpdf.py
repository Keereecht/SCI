# import fitz
# import numpy as np
# import pandas as pd
# from io import BytesIO  # เพิ่มการ import
# from tkinter import filedialog 
# import tkinter as tk
# import data_storage

# def notfoundh(text_info):
#     docf = data_storage.pdf_path  # ไฟล์ PDF ที่ต้องการเปิด

#     # ตรวจสอบประเภทของไฟล์
#     if isinstance(docf, BytesIO):  
#         doc = fitz.open("pdf", docf.getvalue())  # เปิดจาก memory (BytesIO)
#     else:
#         doc = fitz.open(docf)  # เปิดจาก path

#     all_words_top = []
#     for page_num in range(len(doc)):
#         page = doc.load_page(data_storage.page_top)  # โหลดแต่ละหน้า
#         words = page.get_text("words")  # ดึงคำในรูปแบบ "words"
#         page_words = [word[4] for word in words]  # แยกเฉพาะคำ
#         all_words_top.extend(page_words)  # เพิ่มคำในรายการรวม
#     doc.close()

#     all_words_bot = []
#     for page_num in range(len(doc)):
#         page = doc.load_page(data_storage.page_bot)  # โหลดแต่ละหน้า
#         words = page.get_text("words")  # ดึงคำในรูปแบบ "words"
#         page_words = [word[4] for word in words]  # แยกเฉพาะคำ
#         all_words_bot.extend(page_words)  # เพิ่มคำในรายการรวม
#     doc.close()

#     checktop = data_storage.data_top["Ref_Des"].str.split(',').explode().tolist()
#     checkbot = data_storage.data_buttom["Ref_Des"].str.split(',').explode().tolist()
#     checkhl = data_storage.data_hl_top["Ref_Des"].str.split(',').explode().tolist()

#     all_words = []
#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)  # โหลดแต่ละหน้า
#         words = page.get_text("words")  # ดึงคำในรูปแบบ "words"
#         page_words = [word[4] for word in words]  # แยกเฉพาะคำ
#         all_words_bot.extend(page_words)  # เพิ่มคำในรายการรวม
#     doc.close()

#     checktop = data_storage.data_top["Ref_Des"].str.split(',').explode().tolist()
#     checkbot = data_storage.data_buttom["Ref_Des"].str.split(',').explode().tolist()
#     checkhl = data_storage.data_hl_top["Ref_Des"].str.split(',').explode().tolist()


#     notfoundtop = set(map(lambda x: x.strip().upper(), set(checktop))) - set(map(lambda x: x.strip().upper(), all_words_top))
#     notfoundbot = set(map(lambda x: x.strip().upper(), set(checkbot))) - set(map(lambda x: x.strip().upper(), all_words_bot))
#     notfoundhl = set(map(lambda x: x.strip().upper(), set(checkhl))) - set(map(lambda x: x.strip().upper(), all_words_bot))

#     print(notfound)

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


#     # แก้ไขค่าตามเงื่อนไข
#     filtered_array[:, 1] = np.where(
#         filtered_array[:, 1].astype(int) == 150, "TOP", 
#         np.where(filtered_array[:, 1].astype(int) == 50, "BOTTOM", 
#         np.where(filtered_array[:, 1].astype(int) > 200, "HANDLOAD", filtered_array[:, 1]))
#     )

#     sorted_filtered_array = filtered_array[
#         np.lexsort((
#             filtered_array[:, 1],  # จัดเรียงตาม layer
#             np.where(filtered_array[:, 1] == "TOP", 0,  
#                      np.where(filtered_array[:, 1] == "BOTTOM", 1, 2))  
#         ))
#     ]

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
#         devicenf = notf[0]  
#         layernf = notf[1]   
#         total_count_not += 1
#         formatted_text = (
#             f"{str(total_count_not).ljust(count_width)}"
#             f"{layernf.ljust(count_layer)}"
#             f"{devicenf.ljust(value_width)}"
#             f"{'Not found'.ljust(result_width)}\n"
#         )
#         text_info.insert(tk.END, formatted_text)
    
#     text_info.configure(state="disabled")
import fitz
import numpy as np
import pandas as pd
from io import BytesIO  
import tkinter as tk
import data_storage

def notfoundh(text_info):
    docf = data_storage.pdf_path  # ไฟล์ PDF ที่ต้องการเปิด

    # 🔹 เปิด PDF ครั้งเดียว
    if isinstance(docf, BytesIO):  
        doc = fitz.open("pdf", docf.getvalue())  
    else:
        doc = fitz.open(docf)  

    # 🔹 อ่านข้อความจากหน้า TOP
    all_words_top = []
    page_top = doc.load_page(data_storage.page_top)
    words_top = page_top.get_text("words")
    all_words_top = [word[4].strip() for word in words_top]  

    # 🔹 อ่านข้อความจากหน้า BOT
    all_words_bot = []
    page_bot = doc.load_page(data_storage.page_bot)
    words_bot = page_bot.get_text("words")
    all_words_bot = [word[4].strip() for word in words_bot]  
    all_words_hl = all_words_top + all_words_bot
    doc.close()  # 🔹 ปิด PDF เมื่อดึงข้อมูลครบแล้ว
    # 🔹 ดึงค่า Ref_Des จาก DataFrame
    checktop = data_storage.data_top["Ref_Des"].str.split(',').explode().tolist()
    checkbot = data_storage.data_buttom["Ref_Des"].str.split(',').explode().tolist()
    checkhl = data_storage.data_hl_top["Ref_Des"].str.split(',').explode().tolist()

    # 🔹 ค้นหาค่าที่ไม่พบ
    notfoundtop = set(map(str.upper, map(str.strip, checktop))) - set(map(str.upper, all_words_top))
    notfoundbot = set(map(str.upper, map(str.strip, checkbot))) - set(map(str.upper, all_words_bot))
    notfoundhl = set(map(str.upper, map(str.strip, checkhl))) - set(map(str.upper, all_words_hl))

    print("🔎 Not Found (TOP):", notfoundtop)
    print("🔎 Not Found (BOTTOM):", notfoundbot)
    print("🔎 Not Found (HANDLOAD):", notfoundhl)

    # 🔹 รวมค่าที่ไม่พบทั้งหมด
    notfound = notfoundtop | notfoundbot | notfoundhl  
    data_storage.notfountlist = len(notfound)

    # 🔹 กรองค่าที่ไม่พบจาก DataFrame
    checknotfound = data_storage.df[["Ref_Des", "Op_Seq"]].to_numpy()
    expanded_data = [
        {"Ref_Des": ref.strip(), "Op_Seq": row[1]}
        for row in checknotfound for ref in row[0].split(",")
    ]

    expanded_df = pd.DataFrame(expanded_data)
    filtered_df = expanded_df[expanded_df["Ref_Des"].isin(notfound)]
    filtered_array = filtered_df.to_numpy()

    # 🔹 กำหนดค่าตาม Layer
    filtered_array[:, 1] = np.where(
        filtered_array[:, 1].astype(int) == 150, "TOP", 
        np.where(filtered_array[:, 1].astype(int) == 50, "BOTTOM", 
        np.where(filtered_array[:, 1].astype(int) > 200, "HANDLOAD", filtered_array[:, 1]))
    )

    # 🔹 จัดเรียงตาม Layer
    sorted_filtered_array = filtered_array[
        np.lexsort((
            filtered_array[:, 1],  
            np.where(filtered_array[:, 1] == "TOP", 0,  
                     np.where(filtered_array[:, 1] == "BOTTOM", 1, 2))  
        ))
    ]

    # 🔹 แสดงผลใน Tkinter
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
        devicenf, layernf = notf[0], notf[1]   
        total_count_not += 1
        formatted_text = (
            f"{str(total_count_not).ljust(count_width)}"
            f"{layernf.ljust(count_layer)}"
            f"{devicenf.ljust(value_width)}"
            f"{'Not found'.ljust(result_width)}\n"
        )
        text_info.insert(tk.END, formatted_text)
    
    text_info.configure(state="disabled")

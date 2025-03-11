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

    # print("🔎 Not Found (TOP):", notfoundtop)
    # print("🔎 Not Found (BOTTOM):", notfoundbot)
    # print("🔎 Not Found (HANDLOAD):", notfoundhl)

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

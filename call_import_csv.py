import pandas as pd
from io import StringIO
import os
from tkinter import filedialog 
import tkinter as tk
from tkinter import messagebox
import addcustumerlistemail
# -----------------------------
import data_storage
import lenagile

def open_file_csv(text_info, Textboxtotal, red_frame_importpdf, red_frame_importcsv, red_frame_run):
    filepathcsv = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    data_storage.filepathcsv = filepathcsv
    if not filepathcsv:
        return
    filenamecsv = os.path.basename(filepathcsv)
    data_storage.filenamecsv = filenamecsv
    addcustumerlistemail.sync_customer_with_listemail() #เรียกใช้เช็คsheet
    if filenamecsv:
        red_frame_run.config(highlightthickness=0)
        red_frame_importcsv.config(highlightthickness=0)
        red_frame_importpdf.config(highlightthickness=2)
  
    with open(filepathcsv, "r", encoding='ISO-8859-1') as myfile:
        start_collecting = False
        text = ""
        for line in myfile:
            if "BOM Notes" in line:
                start_collecting = True  # เริ่มเก็บข้อมูลหลังจากเจอ "BOM Notes"
                text += line.replace("BOM.", "")
            elif start_collecting:  # บันทึกเฉพาะหลังจากเจอบรรทัดที่ต้องการแล้ว
                if "true" in line or "True" in line or "Active" in line or "active" in line:
                    text += line
        if not text.strip():  # ตรวจสอบว่าไม่มีข้อมูลใน text
            messagebox.showerror("Error", "ไฟล์ agile มีปัญหาโปรดตรวจสอบไฟล์ของคุณ")
            text_info.configure(state="normal")
            text_info.insert(tk.END, filenamecsv + " Imported ERROR\n")
            text_info.configure(state="disabled")
            filepathcsv =""
            data_storage.filenamecsv = ""  # รีเซ็ตค่าใน data_storage ด้วย
            red_frame_run.config(highlightthickness=0)
            red_frame_importcsv.config(highlightthickness=2)
            red_frame_importpdf.config(highlightthickness=0)
            return  # หยุดการทำงานของฟังก์ชันทันที

    text_info.configure(state="normal")
    text_info.insert(tk.END, filenamecsv + " Imported successfully\n")
    text_info.configure(state="disabled")

    data_io = StringIO(text)
    df = pd.read_csv(data_io)
    columns_to_keep = ['Op Seq', 'Qty', 'Item Description', 'Ref Des']
    if any('BOM.' in col for col in df.columns):
        df.columns = df.columns.str.replace('BOM.', '', regex=False)
    # เก็บเฉพาะคอลัมน์ที่เราต้องการ
    df = df[[col for col in df.columns if col in columns_to_keep]]
    df.columns = [column.replace(" ", "_") for column in df.columns] 
    df = df.dropna()
    df = df[~df["Ref_Des"].str.contains("SOLDER|PCB")]
    df = df.rename(columns={"Qty": "BOM_Target(EA)"})  # เปลี่ยนชื่อคอลัมน์ 'Qty' เป็น 'BOM_Target(EA)'
    df.insert(4, column="PDF_Actual(EA)", value="")
    df.insert(5, column="Actual_fond(EA)", value="")
    df.insert(6, column="Not_found(EA)", value="")
    df.insert(7, column="Result", value="")
    # print(df)
    data_storage.df = df

    # total_sum = df['BOM_Target(EA)'].sum()
    # print(total_sum,"--------")
    # Textboxtotal.configure(state="normal")
    # Textboxtotal.delete("1.0", "end")
    # Textboxtotal.insert(tk.END, int(total_sum))
    # Textboxtotal.configure(state="disabled")

    data_top = df[df['Op_Seq'] == 150].copy()
    data_buttom = df[df['Op_Seq'] == 50].copy()
    data_ic_top = df[(df['Op_Seq'] == 150) & (df['Item_Description'].str.startswith("IC"))].copy()
    data_ic_bot = df[(df['Op_Seq'] == 50) & (df['Item_Description'].str.startswith("IC"))].copy()

    data_hl_top = df[(df['Op_Seq'] > 160) & (df['Op_Seq'] <= 600)].copy()
    data_hl_bot = data_hl_top.copy()

    t = data_top['BOM_Target(EA)'].sum()
    b = data_buttom['BOM_Target(EA)'].sum()
    h = data_hl_top['BOM_Target(EA)'].sum()
    total_sum = t + b + h
    print(t,b,h)
    Textboxtotal.configure(state="normal")
    Textboxtotal.delete("1.0", "end")
    Textboxtotal.insert(tk.END, int(total_sum))
    Textboxtotal.configure(state="disabled")

    noload_top_h = pd.concat([data_top, data_hl_top], ignore_index=True).copy()
    noload_bot_h = pd.concat([data_buttom, data_hl_bot], ignore_index=True).copy()
    
    data_top_CAP = data_top[data_top['Item_Description'].str.startswith("CAP")]
    data_top_RES = data_top[data_top['Item_Description'].str.startswith("RES")]
    data_bot_CAP = data_buttom[data_buttom['Item_Description'].str.startswith("CAP")]
    data_bot_RES = data_buttom[data_buttom['Item_Description'].str.startswith("RES")]
    # new use cad
    data_top_not_CAP_RES = data_top[~data_top['Item_Description'].str.startswith("CAP") & 
    ~data_top['Item_Description'].str.startswith("RES") & 
    ~data_top['Item_Description'].str.startswith("IC")]

    data_bot_not_CAP_RES = data_buttom[~data_buttom['Item_Description'].str.startswith("CAP") & 
    ~data_buttom['Item_Description'].str.startswith("RES")& 
    ~data_buttom['Item_Description'].str.startswith("IC")]

    other_top = data_top_not_CAP_RES["Ref_Des"].str.split(',').explode().tolist()
    other_bot = data_bot_not_CAP_RES["Ref_Des"].str.split(',').explode().tolist()

    capa_top =  data_top_CAP["Ref_Des"].str.split(',').explode().tolist()
    capa_bot =  data_bot_CAP["Ref_Des"].str.split(',').explode().tolist()

    res_top = data_top_RES["Ref_Des"].str.split(',').explode().tolist()
    res_bot = data_bot_RES["Ref_Des"].str.split(',').explode().tolist()

    ic_top = data_ic_top["Ref_Des"].str.split(',').explode().tolist()
    ic_bot = data_ic_bot["Ref_Des"].str.split(',').explode().tolist()

    hl_top = data_hl_top["Ref_Des"].str.split(',').explode().tolist()
    hl_bot = data_hl_top["Ref_Des"].str.split(',').explode().tolist()

    data_storage.data_top = data_top
    data_storage.data_buttom = data_buttom
    data_storage.data_ic_top = data_ic_top
    data_storage.data_ic_bot = data_ic_bot
    data_storage.data_hl_top = data_hl_top
    data_storage.data_hl_bot = data_hl_bot
    data_storage.noload_top_h = noload_top_h
    data_storage.noload_bot_h = noload_bot_h
    data_storage.data_top_CAP = data_top_CAP
    data_storage.data_top_RES = data_top_RES
    data_storage.data_bot_CAP = data_bot_CAP
    data_storage.data_bot_RES = data_bot_RES

    data_storage.capa_top = capa_top
    data_storage.res_top = res_top
    data_storage.ic_top = ic_top
    data_storage.hl_top = hl_top
    data_storage.other_top = other_top

    data_storage.capa_bot = capa_bot
    data_storage.res_bot = res_bot
    data_storage.ic_bot = ic_bot
    data_storage.hl_bot = hl_bot
    data_storage.other_bot = other_bot
    print("เช็คความถูกต้อง")
    lenagile.check_all_data(data_storage,text_info)
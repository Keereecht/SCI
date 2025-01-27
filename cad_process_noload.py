import data_storage
import pandas as pd
from io import StringIO
import numpy as np
import os
import tkinter as tk
import time
global input_file_path
input_file_path = "parts_cadprocess/com.cad"

# print(component_values)
def extract_component_values():
    # global component_values
    # global alldf
    # # สร้างลิสต์เพื่อเก็บคำที่อยู่หลัง COMPONENT
    # alldf = data_storage.df["Ref_Des"].str.split(',').explode().tolist()
    # component_values = []
    
    # with open(input_file_path, 'r') as file:
    #     for line in file:
    #         if line.startswith("COMPONENT"):  # ตรวจสอบว่าแถวเริ่มต้นด้วย COMPONENT
    #             # แยกคำและดึงคำหลัง COMPONENT
    #             value = line.split(' ', 1)[1].strip()  # ตัด 'COMPONENT ' ออก และลบช่องว่าง
    #             component_values.append(value)
    # print("=================================================================")
    # print(component_values)
    # print("=================================================================")
    global component_layer_values
    global component_values
    global combined_values
    global checknotfound
    global expanded_df
    global alldf

    alldf = data_storage.df["Ref_Des"].str.split(',').explode().tolist()
    print(alldf)
    checknotfound = data_storage.df[["Ref_Des", "Op_Seq"]].to_numpy()
    expanded_data = []
    for row in checknotfound:
        ref_des_list = row[0].split(",")  # แยก Ref_Des ด้วย ","
        for ref_des in ref_des_list:
            expanded_data.append({"Ref_Des": ref_des.strip(), "Op_Seq": row[1]})

    # สร้าง DataFrame ใหม่จากข้อมูลที่ขยายแล้ว
    expanded_df = pd.DataFrame(expanded_data)

    component_values = []
    layer_values = []
    combined_values = []  # ลิสต์สำหรับเก็บค่าแบบรวม

    with open(input_file_path, 'r') as file:
        for line in file:
            if line.startswith("COMPONENT"):  # ตรวจสอบว่าแถวเริ่มต้นด้วย COMPONENT
                value = line.split(' ', 1)[1].strip()  # ตัด 'COMPONENT ' ออก และลบช่องว่าง
                component_values.append(value)
            elif line.startswith("LAYER"):  # ตรวจสอบว่าแถวเริ่มต้นด้วย LAYER
                value = line.split(' ', 1)[1].strip()  # ตัด 'LAYER ' ออก และลบช่องว่าง
                layer_values.append(value)

    # รวมค่าจาก component_values และ layer_values
    for component, layer in zip(component_values, layer_values):
        combined_values.append(f"{component} {layer}")

    # เก็บค่าที่รวมไว้ใน global variable
    component_layer_values = combined_values
    # print("Combined Values:", combined_values)
def Filter_values(text_info):
    start_time = time.time()
    samevalue = set(alldf) & set(component_values)
    noload_cad = set(component_values) - set(alldf)
    notfound = set(alldf) - set(component_values)
    filtered_df = expanded_df[expanded_df["Ref_Des"].isin(notfound)]
    print(filtered_df)
    filtered_array = filtered_df.to_numpy()
    # แก้ไขค่าตามเงื่อนไข
    filtered_array[:, 1] = np.where(filtered_array[:, 1].astype(int) == 150, "TOP", 
                        np.where(filtered_array[:, 1].astype(int) == 50, "BOTTOM", 
                        np.where(filtered_array[:, 1].astype(int) > 200, "HANDLOAD", filtered_array[:, 1])))
    # แสดงผลลัพธ์
    # print(filtered_array)
    # แยก filtered_combined_values ออกเป็นส่วนหน้า (value) และส่วนหลัง (layer)
    filtered_combined_values = [
        value.split(' ', 1) for value in combined_values if value.split()[0] in samevalue
    ]  # ได้เป็นลิสต์ของ [ส่วนหน้า, ส่วนหลัง]
    data_storage.noload_cad_len = len(noload_cad)
    total_count = 0
    total_count_not = 0
    text_info.configure(state="normal")
    
    # กำหนดความกว้างของแต่ละคอลัมน์
    count_width = 10
    value_width = 15
    result_width = 15
    count_layer = 15
    
    # เพิ่มหัวข้อ
    header = f"{'Item'.ljust(count_width)}{'Layer'.ljust(count_layer)}{'Device'.ljust(value_width)}{'actual result'.ljust(result_width)}\n"
    text_info.insert(tk.END, "-" * len(header) + "\n")
    text_info.insert(tk.END, header)
    text_info.insert(tk.END, "-" * len(header) + "\n")

    for value, layer in filtered_combined_values:  # แยก value และ layer
        count = alldf.count(value)
        total_count += count  # บวกจำนวนสะสม
        formatted_text = (
            f"{str(total_count).ljust(count_width)}"
            f"{layer.ljust(count_layer)}"
            f"{value.ljust(value_width)}"
            f"{'Found'.ljust(result_width)}\n"
        )
        text_info.insert(tk.END, formatted_text)
        # print(f"{value}: Total count so far: {total_count}")
    # text_info.configure(state="disabled")
    header = f"{'Item'.ljust(count_width)}{'Layer'.ljust(count_layer)}{'Device'.ljust(value_width)}{'actual result'.ljust(result_width)}\n"
    text_info.insert(tk.END, "-" * len(header) + "\n")
    text_info.insert(tk.END, header)
    text_info.insert(tk.END, "-" * len(header) + "\n")
    for notf in filtered_array:
        devicenf = notf [0]  # ตัวแรก (Device)
        layernf = notf [1]   # ตัวที่สอง (Layer)
        # count = alldf.count(notf)
        total_count_not += 1
        formatted_text = (
            f"{str(total_count_not).ljust(count_width)}"
            f"{layernf.ljust(count_layer)}"
            f"{devicenf.ljust(value_width)}"
            f"{'Not found'.ljust(result_width)}\n"
        )
        text_info.insert(tk.END,formatted_text)
    text_info.configure(state="disabled")
    data_storage.notfountlist = len(notfound)
    # Prepare data for CSV
    noload_cad_list = list(noload_cad)
    noload_cad_counts = [alldf.count(value) for value in noload_cad_list]

    # Create a DataFrame for the data
    df = pd.DataFrame({
        'Ref_Des': noload_cad_list,
        'Count': noload_cad_counts
    })

    # Construct the file path
    folder_path = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname)
    os.makedirs(folder_path, exist_ok=True)  # Create the directory if it doesn't exist
    file_path = os.path.join(folder_path, data_storage.projectname + '_NOLOAD.csv')

    # Save to CSV
    df.to_csv(file_path, index=False)
    print(f"noload_cad data saved to '{file_path}'")
    end_time = time.time()
    data_storage.noloadtime = round(end_time - start_time,2)
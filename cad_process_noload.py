import data_storage
import pandas as pd
from io import StringIO
import os
import tkinter as tk
import time
global input_file_path
input_file_path = "parts_cadprocess/com.cad"

# print(component_values)
def extract_component_values():
    global component_values
    global alldf
    # สร้างลิสต์เพื่อเก็บคำที่อยู่หลัง COMPONENT
    alldf = data_storage.df["Ref_Des"].str.split(',').explode().tolist()
    component_values = []
    
    with open(input_file_path, 'r') as file:
        for line in file:
            if line.startswith("COMPONENT"):  # ตรวจสอบว่าแถวเริ่มต้นด้วย COMPONENT
                # แยกคำและดึงคำหลัง COMPONENT
                value = line.split(' ', 1)[1].strip()  # ตัด 'COMPONENT ' ออก และลบช่องว่าง
                component_values.append(value)

    return component_values
def Filter_values(text_info):
    start_time = time.time()
    samevalue = set(alldf) & set(component_values)
    # noload_cad = set(alldf) - set(component_values)
    noload_cad = set(component_values) - set(alldf)
    notfount =  set(alldf) - set(component_values)
    data_storage.noload_cad_len = len(noload_cad)
    total_count = 0
    text_info.configure(state="normal")
    for value in samevalue:
        count = alldf.count(value)
        total_count += count  # บวกจำนวนสะสม
        text_info.insert(tk.END, f"{value} Actual_fond {total_count} (EA)\n")
        print(f"{value}: Total count so far: {total_count}")
    # text_info.configure(state="disabled")
    for notf in notfount:
        print("============เข้ามาแล้ว")
        count = alldf.count(notf)
        print(notf)
        total_count += count
        text_info.insert(tk.END, f"{notf} Not_fond {total_count}(EA)\n")
        print(f"{notfount}: Total count so far: ")
    text_info.configure(state="disabled")
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
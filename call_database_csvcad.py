import os
import pandas as pd
import data_storage
import tkinter as tk
def save_database_to_csv_cad():
    # กำหนดเส้นทางโฟลเดอร์ที่จะเก็บไฟล์ CSV
    main_folder = data_storage.Main_folder  # เช่น C:\Drive_Test
    output_folder = os.path.join(main_folder, "outputdatabase")
    
    # ตรวจสอบและสร้างโฟลเดอร์ถ้ายังไม่มี
    os.makedirs(output_folder, exist_ok=True)
    
    # กำหนดเส้นทางไฟล์ CSV ที่จะบันทึก
    csv_file = os.path.join(output_folder, "database.csv")

    # ตรวจสอบว่าไฟล์ CSV มีอยู่แล้วหรือไม่
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        # print("ข้อมูลที่อ่านจากไฟล์ CSV:")
        # print(df.head())  # แสดงข้อมูลที่อ่านมา
        if "Project_id" in df.columns and not df.empty:
            last_project_id = df['Project_id'].max()
            next_project_id = last_project_id + 1
        else:
            next_project_id = 1
    else:
        next_project_id = 1

    # pdfname = data_storage.pdfname if data_storage.pdfname else ""
    # pdf_top_filename = data_storage.pdf_top_filename if data_storage.pdf_top_filename else ""
    # pdf_bot_filename = data_storage.pdf_bot_filename if data_storage.pdf_bot_filename else ""
    cadname = data_storage.cadfilename if data_storage.cadfilename else ""
    outpathdata = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname)
    percent_handload = (
        int((int(data_storage.sum_find_hltop + data_storage.sum_find_hlbot) / int(data_storage.sum_qty_hltop)) * 100)
        if data_storage.sum_qty_hltop != 0 else 0
    )
    # สร้างข้อมูลใหม่ที่จะบันทึกลงใน CSV
  
    customer_values = [
            [next_project_id, data_storage.selected_customer, data_storage.projectname + "_CAD", data_storage.filenamecsv, cadname + '_cad_top_filename','None',data_storage.projectname + "_TOP_SMT", int(data_storage.sum_qty_top), int(data_storage.sum_find_top), data_storage.Not_found_top, int(data_storage.percent_top_smt), data_storage.time_top, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname + "_CAD", data_storage.filenamecsv, cadname + '_cad_bot_filename','None',data_storage.projectname + "_BOT_SMT",int(data_storage.sum_qty_bot), int(data_storage.sum_find_bot), data_storage.Not_found_bot, int(data_storage.percent_bot_smt), data_storage.time_bot, data_storage.logged_in_user,data_storage.date_time,outpathdata],

            [next_project_id, data_storage.selected_customer, data_storage.projectname + "_CAD", data_storage.filenamecsv, cadname + '_cad_top_filename','None',data_storage.projectname + "_Handload",int(data_storage.sum_qty_hltop), int(data_storage.sum_find_hltop + data_storage.sum_find_hlbot), int(data_storage.sum_qty_hltop) - int(data_storage.sum_find_hltop + data_storage.sum_find_hlbot), int((int(data_storage.sum_find_hltop + data_storage.sum_find_hlbot)/int(data_storage.sum_qty_hltop))*100), data_storage.time_hl_top, data_storage.logged_in_user, data_storage.date_time,outpathdata],

            [next_project_id, data_storage.selected_customer, data_storage.projectname + "_CAD", data_storage.filenamecsv, cadname + '_cad_top_filename','None',data_storage.projectname + "***TOP_Handload",int(data_storage.sum_qty_hltop), int(data_storage.sum_find_hltop), data_storage.Not_found_hltop, int(data_storage.percent_top_hltop), data_storage.time_hl_top, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname + "_CAD", data_storage.filenamecsv, cadname + '_cad_bot_filename','None',data_storage.projectname + "***BOT_Handload",int(data_storage.sum_qty_hlbot), int(data_storage.sum_find_hlbot), data_storage.Not_found_hlbot, int(data_storage.percent_bot_hlbot), data_storage.time_hl_bot, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname + "_CAD", data_storage.filenamecsv, cadname + '_cad_top_filename','None',data_storage.projectname + "_TOP_Noload",int(data_storage.noload_cad_len),int(data_storage.noload_cad_len), 0, 100, data_storage.noloadtime, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname + "_CAD", data_storage.filenamecsv, cadname + '_cad_bot_filename','None',data_storage.projectname + "_BOT_Noload",int(data_storage.noload_cad_len),int(data_storage.noload_cad_len), 0, 100, data_storage.noloadtime, data_storage.logged_in_user,data_storage.date_time,outpathdata]
        ]

    # เพิ่มข้อมูลใหม่ลงใน DataFrame
    df_new = pd.DataFrame(customer_values, columns=df.columns)
    # กรองคอลัมน์ที่เป็น NaN ทั้งหมดออกจาก df_new
    df_new = df_new.dropna(how='all', axis=1)
    # ทำการ concat ข้อมูลใหม่
    df = pd.concat([df, df_new], ignore_index=True)
    # บันทึกข้อมูลลงในไฟล์ CSV
    df.to_csv(csv_file, index=False)
    print(f"บันทึกข้อมูลลงในไฟล์ CSV ที่: {csv_file} เรียบร้อยแล้ว")
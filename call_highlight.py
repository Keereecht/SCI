from datetime import datetime
import time
import random
import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

import highlight_compound_ic
import highlight_separate_ic
import cad_process_top
import cad_process_bot
import call_data_base
import call_data_base_cad
from call_coversheet import info_over_all
from call_coversheet import info_over_all_ic
from call_database_csv import save_database_to_csv
import data_storage
from io import BytesIO
import compound_countcad
import combinefile
import pluscadname
import cad_process_noload
from call_loading_screen import loading_window, update_progress, close_loading_window

def runfile(text_info, Textboxfind):

    current_datetime = datetime.now()
    date_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    data_storage.date_time = date_time
    print(f"Current date and time: {date_time}")

    load_win, progress_bar = loading_window()
    total_steps = 100

    # นับจำนวนครั้งที่เรียกใช้ฟังก์ชัน runfile
    if not hasattr(runfile, "call_count"):
        runfile.call_count = 0
    runfile.call_count += 1
    
    global text_widget_global  # กำหนด text_widget เป็น global
    text_widget_global = text_info
    Textboxfind.configure(state="normal")
    Textboxfind.delete("1.0", "end")
    Textboxfind.configure(state="disabled")
    text_info.configure(state="normal")
    lines = text_info.get("1.0", tk.END).split('\n')
    filtered_lines = [line for line in lines if 'imported' in line]
    text_info.delete("1.0", tk.END)
    text_info.insert(tk.END, data_storage.projectname + " create successfully\n")
    for line in filtered_lines:
        text_info.insert(tk.END, line + '\n')
    text_info.insert(tk.END, "Waiting for highlight... \n")
    text_info.configure(state="disabled")
    text_info.update()

    if not data_storage.iccall_value:
        for step in range(total_steps):
            if step == 0:
                highlight_separate_ic.run_top(text_info)
            elif step == 1:
                highlight_separate_ic.run_bot(text_info)
            elif step == 2:
                highlight_separate_ic.run_top_hl(text_info)
            elif step == 3:
                highlight_separate_ic.run_bot_hl(text_info, Textboxfind)
            elif step == 4:
                highlight_separate_ic.noload_top()
            elif step == 5:
                highlight_separate_ic.noload_bot()
                
            # อัปเดต Progress bar
            progress = (step + 1) / total_steps * 100
            update_progress(progress_bar, progress)

            # เพิ่มการอัปเดตหน้าต่าง Tkinter เพื่อแสดงผลทันที
            load_win.update_idletasks()

        highlight_separate_ic.timework()
        
        # ปิดหน้าโหลดเมื่อประมวลผลเสร็จ
        # close_loading_window(load_win)

        data_top_no_ic = data_storage.data_top[~data_storage.data_top['Item_Description'].str.startswith('IC')]
        data_bot_no_ic = data_storage.data_buttom[~data_storage.data_buttom['Item_Description'].str.startswith('IC')]
        data_top_ic = data_storage.data_top[data_storage.data_top['Item_Description'].str.startswith('IC')]
        data_bot_ic = data_storage.data_buttom[data_storage.data_buttom['Item_Description'].str.startswith('IC')]
        data_storage.sum_qty_hltop = data_storage.data_hl_top['BOM_Target(EA)'].sum()
        data_storage.sum_qty_hlbot = data_storage.data_hl_bot['BOM_Target(EA)'].sum()

        data_storage.sum_qty_top = data_top_no_ic['BOM_Target(EA)'].sum()
        data_storage.sum_qty_top_ic = data_top_ic['BOM_Target(EA)'].sum()
        data_storage.sum_qty_bot = data_bot_no_ic['BOM_Target(EA)'].sum()
        data_storage.sum_qty_bot_ic = data_bot_ic['BOM_Target(EA)'].sum()

        data_storage.sum_find_top = data_top_no_ic['PDF_Actual(EA)'].sum()
        data_storage.sum_find_top_ic = data_top_ic['PDF_Actual(EA)'].sum()
        data_storage.sum_find_bot = data_bot_no_ic['PDF_Actual(EA)'].sum()
        data_storage.sum_find_bot_ic = data_bot_ic['PDF_Actual(EA)'].sum()

        data_storage.Not_found_top = max(int(data_storage.sum_qty_top) - int(data_storage.sum_find_top), 0)
        data_storage.Not_found_top_ic = max(int(data_storage.sum_qty_top_ic) - int(data_storage.sum_find_top_ic), 0)
        data_storage.Not_found_bot = max(int(data_storage.sum_qty_bot) - int(data_storage.sum_find_bot), 0)
        data_storage.Not_found_bot_ic = max(int(data_storage.sum_qty_bot_ic) - int(data_storage.sum_find_bot_ic), 0)
        data_storage.Not_found_hltop = max(int(data_storage.sum_qty_hltop) - int(data_storage.sum_find_hltop), 0)
        data_storage.Not_found_hlbot = max(int(data_storage.sum_qty_hlbot) - int(data_storage.sum_find_hlbot), 0)

        data_storage.percent_top_smt = (data_storage.sum_find_top / data_storage.sum_qty_top * 100) if data_storage.sum_qty_top != 0 else 0
        data_storage.percent_top_ic = (data_storage.sum_find_top_ic / data_storage.sum_qty_top_ic * 100) if data_storage.sum_qty_top_ic != 0 else 0
        data_storage.percent_bot_smt = (data_storage.sum_find_bot / data_storage.sum_qty_bot * 100) if data_storage.sum_qty_bot != 0 else 0
        data_storage.percent_bot_ic = (data_storage.sum_find_bot_ic / data_storage.sum_qty_bot_ic * 100) if data_storage.sum_qty_bot_ic != 0 else 0
        data_storage.percent_top_hltop = (data_storage.sum_find_hltop / data_storage.sum_qty_hltop * 100) if data_storage.sum_qty_hltop != 0 else 0
        data_storage.percent_bot_hlbot = (data_storage.sum_find_hlbot / data_storage.sum_qty_hlbot * 100) if data_storage.sum_qty_hlbot != 0 else 0

        info_over_all_ic()
        if not data_storage.selected_customer =="Test_product":
            call_data_base.data_base_sheet()
            save_database_to_csv(text_info)
        close_loading_window(load_win)
        time.sleep(1)
        messagebox.showinfo("สถานะ", "เสร็จสิ้น")
    if data_storage.iccall_value:
    # กำหนดจำนวนขั้นตอนเพื่อใช้กับ Progress bar
        total_steps = 6
        for step in range(total_steps):
            if step == 0:
                highlight_compound_ic.run_top(text_info) 
            elif step == 1:
                highlight_compound_ic.run_bot(text_info)
            elif step == 2:
                highlight_compound_ic.run_top_hl(text_info)
            elif step == 3:
                highlight_compound_ic.run_bot_hl(text_info, Textboxfind)
            elif step == 4:
                highlight_compound_ic.noload_top()
            elif step == 5:
                highlight_compound_ic.noload_bot()

            # อัปเดต Progress bar
            progress = (step + 1) / total_steps * 100
            update_progress(progress_bar, progress)
            
            # เพิ่มการอัปเดตหน้าต่าง Tkinter เพื่อแสดงผลทันที
            load_win.update_idletasks()

        # เรียกใช้ฟังก์ชันอื่นหลังจากการประมวลผลเสร็จสิ้น
        highlight_compound_ic.timework()
        
        # ปิดหน้าโหลดเมื่อประมวลผลเสร็จ
        # close_loading_window(load_win)

        # คำนวณและจัดการข้อมูลหลังการประมวลผล
        data_storage.sum_qty_top = data_storage.data_top['BOM_Target(EA)'].sum()
        data_storage.sum_qty_hltop = data_storage.data_hl_top['BOM_Target(EA)'].sum()
        data_storage.sum_qty_bot = data_storage.data_buttom['BOM_Target(EA)'].sum()
        data_storage.sum_qty_hlbot = data_storage.data_hl_bot['BOM_Target(EA)'].sum()
        
        data_storage.sum_find_top = data_storage.data_top['PDF_Actual(EA)'].sum()
        data_storage.sum_find_hltop = data_storage.data_hl_top['PDF_Actual(EA)'].sum()
        data_storage.sum_find_bot = data_storage.data_buttom['PDF_Actual(EA)'].sum()
        data_storage.sum_find_hlbot = data_storage.data_hl_bot['PDF_Actual(EA)'].sum()

        data_storage.Not_found_top = max(int(data_storage.sum_qty_top) - int(data_storage.sum_find_top), 0)
        data_storage.Not_found_hltop = max(int(data_storage.sum_qty_hltop) - int(data_storage.sum_find_hltop), 0)
        data_storage.Not_found_bot = max(int(data_storage.sum_qty_bot) - int(data_storage.sum_find_bot), 0)
        data_storage.Not_found_hlbot = max(int(data_storage.sum_qty_hlbot) - int(data_storage.sum_find_hlbot), 0)

        data_storage.percent_top_smt = (data_storage.sum_find_top / data_storage.sum_qty_top * 100) if data_storage.sum_qty_top != 0 else 0
        data_storage.percent_top_hltop = (data_storage.sum_find_hltop / data_storage.sum_qty_hltop * 100) if data_storage.sum_qty_hltop != 0 else 0
        data_storage.percent_bot_smt = (data_storage.sum_find_bot / data_storage.sum_qty_bot * 100) if data_storage.sum_qty_bot != 0 else 0
        data_storage.percent_bot_hlbot = (data_storage.sum_find_hlbot / data_storage.sum_qty_hlbot * 100) if data_storage.sum_qty_hlbot != 0 else 0

        # แสดงผลข้อมูลสรุป
        info_over_all()
        if not data_storage.selected_customer == "Test_product":
            call_data_base.data_base_sheet()
            save_database_to_csv(text_info)
        close_loading_window(load_win)
        time.sleep(1)
        messagebox.showinfo("สถานะ", "เสร็จสิ้น")

# def call_runcad(Textboxfind,text_info):
#     current_datetime = datetime.now()
#     date_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     data_storage.date_time = date_time

#     Textboxfind.configure(state="normal")
#     Textboxfind.delete("1.0", "end")
#     Textboxfind.configure(state="disabled")
#     text_info.configure(state="normal")
#     text_info.insert(tk.END, "Processing...\n")
#     text_info.configure(state="disabled")
#     input_file_path = "parts_cadprocess/com.cad"

#     cad_process_noload.extract_component_values()
#     cad_process_noload.Filter_values(text_info)
    
#     # สร้างหน้าต่าง loading screen
#     load_win, progress_bar = loading_window()
#     total_steps = 10

#     try:
#         for step in range(total_steps):
#             start_time_cadtop = time.time()
#             if step == 0:
#                 output_file_path = "cadprocess/top_capa.cad"
#                 components_to_keep = data_storage.capa_top
#                 cad_process_top.components_capatop(input_file_path, output_file_path, components_to_keep)
#             elif step == 1:
#                 output_file_path = "cadprocess/top_res.cad"
#                 components_to_keep = data_storage.res_top
#                 cad_process_top.components_restop(input_file_path, output_file_path, components_to_keep)
#             elif step == 2:
#                 output_file_path = "cadprocess/top_ic.cad"
#                 components_to_keep = data_storage.ic_top
#                 cad_process_top.components_ictop(input_file_path, output_file_path, components_to_keep)
#             elif step == 3:
#                 output_file_path = "cadprocess/top_other.cad"
#                 components_to_keep = data_storage.other_top
#                 cad_process_top.components_othertop(input_file_path, output_file_path, components_to_keep)
#             elif step == 4:
#                 output_file_path = "cadprocess/top_hl.cad"
#                 components_to_keep = data_storage.hl_top
#                 cad_process_top.components_hltop(input_file_path, output_file_path, components_to_keep)

#             elif step == 5:
#                 output_file_path = "cadprocess/bot_capa.cad"
#                 components_to_keep = data_storage.capa_bot
#                 cad_process_bot.components_capabot(input_file_path, output_file_path, components_to_keep)
#             elif step == 6:
#                 output_file_path = "cadprocess/bot_res.cad"
#                 components_to_keep = data_storage.res_bot
#                 cad_process_bot.components_resbot(input_file_path, output_file_path, components_to_keep)
#             elif step == 7:
#                 output_file_path = "cadprocess/bot_ic.cad"
#                 components_to_keep = data_storage.ic_bot
#                 cad_process_bot.components_icbot(input_file_path, output_file_path, components_to_keep)
#             elif step == 8:
#                 output_file_path = "cadprocess/bot_other.cad"
#                 components_to_keep = data_storage.other_bot
#                 cad_process_bot.components_otherbot(input_file_path, output_file_path, components_to_keep)
#             elif step == 9:
#                 output_file_path = "cadprocess/bot_hl.cad"
#                 components_to_keep = data_storage.hl_bot
#                 cad_process_bot.components_hlbot(input_file_path, output_file_path, components_to_keep) 
#             # อัปเดต progress bar
#             progress_value = (step + 1) * (100 / total_steps)
#             update_progress(progress_bar, progress_value)
#             load_win.update()  # อัปเดตหน้าต่าง GUI
#             time.sleep(0.1)   # จำลองเวลาการประมวลผล

#         # การดำเนินการเพิ่มเติมนอกลูป
#         cad_process_top.compoundcad()
#         cad_process_top.saveoutput_capatop()
#         cad_process_top.saveoutput_hltop()

#         cad_process_bot.compoundcad()
#         cad_process_bot.saveoutput_capabot()
#         cad_process_bot.saveoutput_hlbot()
  

#         compound_countcad.use_component_count_top(Textboxfind)
#         output_file_path = "cadprocess/top_hl.cad"
#         cad_process_top.components_hltop_use(input_file_path, output_file_path)
#         output_file_path = "cadprocess/bot_hl.cad"
#         cad_process_bot.components_hlbot_use(input_file_path, output_file_path)
#         combinefile.process_and_combine_files_for_project()
#         pluscadname.rename_project_folder()

#         # การคำนวณสถิติ
#         data_storage.sum_qty_top = data_storage.data_top['BOM_Target(EA)'].sum()
#         data_storage.sum_qty_hltop = data_storage.data_hl_top['BOM_Target(EA)'].sum()
#         data_storage.sum_qty_bot = data_storage.data_buttom['BOM_Target(EA)'].sum()
#         data_storage.sum_qty_hlbot = data_storage.data_hl_bot['BOM_Target(EA)'].sum()
#         data_storage.sum_find_top = data_storage.data_top['PDF_Actual(EA)'].sum()
#         data_storage.sum_find_hltop = data_storage.data_hl_top['PDF_Actual(EA)'].sum()
#         data_storage.sum_find_bot = data_storage.data_buttom['PDF_Actual(EA)'].sum()
#         data_storage.sum_find_hlbot = data_storage.data_hl_bot['PDF_Actual(EA)'].sum()

#         data_storage.Not_found_top = max(int(data_storage.sum_qty_top) - int(data_storage.sum_find_top), 0)
#         data_storage.Not_found_hltop = max(int(data_storage.sum_qty_hltop) - int(data_storage.sum_find_hltop), 0)
#         data_storage.Not_found_bot = max(int(data_storage.sum_qty_bot) - int(data_storage.sum_find_bot), 0)
#         data_storage.Not_found_hlbot = max(int(data_storage.sum_qty_hlbot) - int(data_storage.sum_find_hlbot), 0)

#         data_storage.percent_top_smt = round(data_storage.sum_find_top / data_storage.sum_qty_top * 100) if data_storage.sum_qty_top != 0 else 0
#         data_storage.percent_top_hltop = round(data_storage.sum_find_hltop / data_storage.sum_qty_hltop * 100) if data_storage.sum_qty_hltop != 0 else 0
#         data_storage.percent_bot_smt = round(data_storage.sum_find_bot / data_storage.sum_qty_bot * 100) if data_storage.sum_qty_bot != 0 else 0
#         data_storage.percent_bot_hlbot = round(data_storage.sum_find_hlbot / data_storage.sum_qty_hlbot * 100) if data_storage.sum_qty_hlbot != 0 else 0

#         if not data_storage.selected_customer == "Test_product":
#             call_data_base_cad.data_base_sheet()

#     finally:
#         close_loading_window(load_win)
#         print('--------save----------')
def call_runcad(Textboxfind,text_info):
    current_datetime = datetime.now()
    date_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    data_storage.date_time = date_time

    Textboxfind.configure(state="normal")
    Textboxfind.delete("1.0", "end")
    Textboxfind.configure(state="disabled")
    text_info.configure(state="normal")
    text_info.insert(tk.END, "Processing...\n")
    text_info.configure(state="disabled")
    input_file_path = "parts_cadprocess/com.cad"

    cad_process_noload.extract_component_values()
    cad_process_noload.Filter_values(text_info)
    
    # สร้างหน้าต่าง loading screen
    load_win, progress_bar = loading_window()
    total_steps = 10

    try:
        for step in range(total_steps):
            # จับเวลา step 0 ถึง 3
            if step in range(0, 4):  # step 0 ถึง 3
                if step == 0:
                    start_time_steps_0_3 = time.time()  # เริ่มจับเวลา

                output_file_path = ""
                if step == 0:
                    output_file_path = "cadprocess/top_capa.cad"
                    components_to_keep = data_storage.capa_top
                    cad_process_top.components_capatop(input_file_path, output_file_path, components_to_keep)
                elif step == 1:
                    output_file_path = "cadprocess/top_res.cad"
                    components_to_keep = data_storage.res_top
                    cad_process_top.components_restop(input_file_path, output_file_path, components_to_keep)
                elif step == 2:
                    output_file_path = "cadprocess/top_ic.cad"
                    components_to_keep = data_storage.ic_top
                    cad_process_top.components_ictop(input_file_path, output_file_path, components_to_keep)
                elif step == 3:
                    output_file_path = "cadprocess/top_other.cad"
                    components_to_keep = data_storage.other_top
                    cad_process_top.components_othertop(input_file_path, output_file_path, components_to_keep)
                    end_time_steps_0_3 = time.time()  # จับเวลาเมื่อสิ้นสุด step 3
                    elapsed_time_steps_0_3 = end_time_steps_0_3 - start_time_steps_0_3
                    data_storage.time_top = round(elapsed_time_steps_0_3,2)
                    print(f"Steps 0 to 3 completed in {elapsed_time_steps_0_3:.2f} seconds.")

            # จับเวลาเฉพาะ step 4
            elif step == 4:
                start_time_step_4 = time.time()  # เริ่มจับเวลา
                output_file_path = "cadprocess/top_hl.cad"
                components_to_keep = data_storage.hl_top
                cad_process_top.components_hltop(input_file_path, output_file_path, components_to_keep)
                end_time_step_4 = time.time()  # สิ้นสุดจับเวลา
                elapsed_time_step_4 = end_time_step_4 - start_time_step_4
                data_storage.time_hl_top = round(elapsed_time_step_4,2)
                print(f"Step 4 completed in {elapsed_time_step_4:.2f} seconds.")

            # จับเวลา step 5 ถึง 8
            elif step in range(5, 9):  # step 5 ถึง 8
                if step == 5:
                    start_time_steps_5_8 = time.time()  # เริ่มจับเวลา
                output_file_path = ""
                if step == 5:
                    output_file_path = "cadprocess/bot_capa.cad"
                    components_to_keep = data_storage.capa_bot
                    cad_process_bot.components_capabot(input_file_path, output_file_path, components_to_keep)
                elif step == 6:
                    output_file_path = "cadprocess/bot_res.cad"
                    components_to_keep = data_storage.res_bot
                    cad_process_bot.components_resbot(input_file_path, output_file_path, components_to_keep)
                elif step == 7:
                    output_file_path = "cadprocess/bot_ic.cad"
                    components_to_keep = data_storage.ic_bot
                    cad_process_bot.components_icbot(input_file_path, output_file_path, components_to_keep)
                elif step == 8:
                    output_file_path = "cadprocess/bot_other.cad"
                    components_to_keep = data_storage.other_bot
                    cad_process_bot.components_otherbot(input_file_path, output_file_path, components_to_keep)
                    end_time_steps_5_8 = time.time()  # สิ้นสุดจับเวลา
                    elapsed_time_steps_5_8 = end_time_steps_5_8 - start_time_steps_5_8
                    data_storage.time_bot = round(elapsed_time_steps_5_8,2)
                    print(f"Steps 5 to 8 completed in {elapsed_time_steps_5_8:.2f} seconds.")

            # จับเวลาเฉพาะ step 9
            elif step == 9:
                start_time_step_9 = time.time()  # เริ่มจับเวลา
                output_file_path = "cadprocess/bot_hl.cad"
                components_to_keep = data_storage.hl_bot
                cad_process_bot.components_hlbot(input_file_path, output_file_path, components_to_keep)
                end_time_step_9 = time.time()  # สิ้นสุดจับเวลา
                elapsed_time_step_9 = end_time_step_9 - start_time_step_9
                data_storage.time_hl_bot = round(elapsed_time_step_9,2)
                print(f"Step 9 completed in {elapsed_time_step_9:.2f} seconds.")

            # อัปเดต progress bar
            progress_value = (step + 1) * (100 / total_steps)
            update_progress(progress_bar, progress_value)
            load_win.update()  # อัปเดตหน้าต่าง GUI
            # time.sleep(0.1)   # จำลองเวลาการประมวลผล

        # การดำเนินการเพิ่มเติมนอกลูป
        cad_process_top.compoundcad()
        cad_process_top.saveoutput_capatop()
        cad_process_top.saveoutput_hltop()

        cad_process_bot.compoundcad()
        cad_process_bot.saveoutput_capabot()
        cad_process_bot.saveoutput_hlbot()
  

        compound_countcad.use_component_count_top(Textboxfind)
        output_file_path = "cadprocess/top_hl.cad"
        cad_process_top.components_hltop_use(input_file_path, output_file_path)
        output_file_path = "cadprocess/bot_hl.cad"
        cad_process_bot.components_hlbot_use(input_file_path, output_file_path)
        combinefile.process_and_combine_files_for_project()
        pluscadname.rename_project_folder()

        # การคำนวณสถิติ
        data_storage.sum_qty_top = data_storage.data_top['BOM_Target(EA)'].sum()
        data_storage.sum_qty_hltop = data_storage.data_hl_top['BOM_Target(EA)'].sum()
        data_storage.sum_qty_bot = data_storage.data_buttom['BOM_Target(EA)'].sum()
        data_storage.sum_qty_hlbot = data_storage.data_hl_bot['BOM_Target(EA)'].sum()

        data_storage.sum_find_top = data_storage.data_top['PDF_Actual(EA)'].sum()
        data_storage.sum_find_hltop = data_storage.data_hl_top['PDF_Actual(EA)'].sum()
        data_storage.sum_find_bot = data_storage.data_buttom['PDF_Actual(EA)'].sum()
        data_storage.sum_find_hlbot = data_storage.data_hl_bot['PDF_Actual(EA)'].sum()

        data_storage.Not_found_top = max(int(data_storage.sum_qty_top) - int(data_storage.sum_find_top), 0)
        data_storage.Not_found_hltop = max(int(data_storage.sum_qty_hltop) - int(data_storage.sum_find_hltop), 0)
        data_storage.Not_found_bot = max(int(data_storage.sum_qty_bot) - int(data_storage.sum_find_bot), 0)
        data_storage.Not_found_hlbot = max(int(data_storage.sum_qty_hlbot) - int(data_storage.sum_find_hlbot), 0)

        data_storage.percent_top_smt = round(data_storage.sum_find_top / data_storage.sum_qty_top * 100) if data_storage.sum_qty_top != 0 else 0
        data_storage.percent_top_hltop = round(data_storage.sum_find_hltop / data_storage.sum_qty_hltop * 100) if data_storage.sum_qty_hltop != 0 else 0
        data_storage.percent_bot_smt = round(data_storage.sum_find_bot / data_storage.sum_qty_bot * 100) if data_storage.sum_qty_bot != 0 else 0
        data_storage.percent_bot_hlbot = round(data_storage.sum_find_hlbot / data_storage.sum_qty_hlbot * 100) if data_storage.sum_qty_hlbot != 0 else 0

        if not data_storage.selected_customer == "Test_product":
            call_data_base_cad.data_base_sheet()

    finally:
        close_loading_window(load_win)
   

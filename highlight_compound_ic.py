import csv
from array import *
import numpy as np
from numpy import loadtxt
import pandas as pd
from tkinter import *
from tkinter import filedialog 
from io import StringIO
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import fitz
import os
import random
from tkinter import simpledialog
from datetime import datetime
import time
import re
import data_storage
from io import BytesIO
# --------------call-all-pass-----------
def run_top(text_info): # ใช้ text_widget จาก global
    global loop_counter
    global elapsed_time_top
    if data_storage.df is None:
        messagebox.showerror("Error", "Data frame 'df' is not initialized.")
        return
    start_time_top = time.time()
    text_info.configure(state="normal")
    text_info.insert(tk.END, "TOP_SMT\n")
    top = data_storage.data_top.shape
    output_path_top = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_TOP_SMT.pdf')
    os.makedirs(os.path.dirname(output_path_top), exist_ok=True)
    # ตรวจสอบประเภทของ pdf_path
    if isinstance(data_storage.pdf_path, BytesIO):
        doc = fitz.Document(stream=data_storage.pdf_path)
    else:
        doc = fitz.open(data_storage.pdf_path)
    page = doc.load_page(data_storage.page_top)
    words = page.get_text("words")
    collected_values_list = []
    count_list = []
    loop_counter = 0
    for x in range(top[0]):
        ref_des = data_storage.data_top.iat[x, 3]
        des = data_storage.data_top.iat[x, 2].strip().upper()
        ref_des_list = ref_des.split(",")
        filtered_words = [word for word in words if word[4] in ref_des_list]
        collected_values = []
        count = 0
        is_cap = des.startswith('CAP') or des.startswith('SMD CAP')
        is_res = des.startswith('RES') or des.startswith('SMD RES')
        for word in filtered_words:
            loop_counter += 1
            count += 1
            original_rect = fitz.Rect(word[:4])
            
            # การเช็คขนาดของสี่เหลี่ยม
            rect_width = original_rect.width
            rect_height = original_rect.height
            
            # กำหนดเกณฑ์ขนาดที่ต้องการจะขยาย
            threshold_width = 1  
            threshold_height = 1  

            if rect_width < threshold_width or rect_height < threshold_height:
                # ขยายขนาดสำหรับสี่เหลี่ยมที่มีขนาดเล็กกว่าเกณฑ์
                reduced_rect = fitz.Rect(
                    original_rect.x0 - 0.9 * original_rect.width,
                    original_rect.y0 - 0.9 * original_rect.height,
                    original_rect.x1 + 0.9 * original_rect.width,
                    original_rect.y1 + 0.9 * original_rect.height
                )
            else:
                # คงขนาดเดิมสำหรับสี่เหลี่ยมที่มีขนาดใหญ่กว่าเกณฑ์
                reduced_rect = original_rect
            highlight = page.add_highlight_annot(reduced_rect)
            color = (1, 0.65, 0.9)  # Default color pink
            if word[4].startswith('C') and is_cap or word[4].startswith('XC') and is_cap:
                color = (0, 1, 0)  # Green for capacitors
            if word[4].startswith('R') and is_res or word[4].startswith('XR') and is_res:
                color = (1, 0.5, 0)  # Orange for resistors
            highlight.set_colors(stroke=color)
            highlight.update()
            collected_values.append(word[4])
            print(word[4], "Actual_fond(EA)", loop_counter)
            text_info.configure(state="normal")
            text_info.insert(tk.END, f"{word[4]} Actual_fond {loop_counter} (EA)\n")
        collected_values_list.append(",".join(collected_values))
        count_list.append(count)
    doc.save(output_path_top)
    data_storage.data_top['Actual_fond(EA)'] = collected_values_list
    data_storage.data_top['PDF_Actual(EA)'] = count_list
    data_storage.df.loc[data_storage.df['Op_Seq'] == 150, 'Actual_fond(EA)'] = data_storage.data_top['Actual_fond(EA)'].values
    data_storage.df.loc[data_storage.df['Op_Seq'] == 150, 'PDF_Actual(EA)'] = data_storage.data_top['PDF_Actual(EA)'].values
    diff_list = []
    for index, row in data_storage.data_top.iterrows():
        ref_des_set = set(row['Ref_Des'].split(','))
        collected_values_set = set(row['Actual_fond(EA)'].split(','))
        diff = ref_des_set.symmetric_difference(collected_values_set)
        diff_list.append(",".join(diff))
    data_storage.data_top['Not_found(EA)'] = diff_list
    data_storage.data_top['Result'] = data_storage.data_top.apply(lambda row: 'accepted' if row['PDF_Actual(EA)'] == row['BOM_Target(EA)'] else 'rejected', axis=1)
    file_path_top = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_TOP_SMT.csv')
    os.makedirs(os.path.dirname(file_path_top), exist_ok=True)
    data_storage.data_top.to_csv(file_path_top, index=False)
    end_time_top = time.time()
    elapsed_time_top = end_time_top - start_time_top
        
def run_bot(text_info):
    global loop_counter
    global elapsed_time_bot
    start_time_bot = time.time()
    text_info.configure(state="normal")
    text_info.insert(tk.END, "BOT_SMT\n")
    bot = data_storage.data_buttom.shape
    output_path_bot = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_BOT_SMT.pdf')
    os.makedirs(os.path.dirname(output_path_bot), exist_ok=True)
        # ตรวจสอบประเภทของ pdf_path
    if isinstance(data_storage.pdf_path, BytesIO):
        doc = fitz.Document(stream=data_storage.pdf_path)
    else:
        doc = fitz.open(data_storage.pdf_path)
    page = doc.load_page(data_storage.page_bot)
    words = page.get_text("words")
    collected_values_list = []
    count_list = []
    for x in range(bot[0]):
        ref_des = data_storage.data_buttom.iat[x, 3]
        des = data_storage.data_buttom.iat[x, 2].strip().upper()
        ref_des_list = ref_des.split(",")
        filtered_words = [word for word in words if word[4] in ref_des_list]
        collected_values = []
        count = 0
        is_cap = des.startswith('CAP') or des.startswith('SMD CAP')
        is_res = des.startswith('RES') or des.startswith('SMD RES')
        is_ic = des.startswith('IC')
        for word in filtered_words:
            if is_ic and not data_storage.iccall_value:
                continue  # ข้ามการไฮไลท์ถ้าเป็น IC
            loop_counter += 1
            count += 1
            original_rect = fitz.Rect(word[:4])
            
            # การเช็คขนาดของสี่เหลี่ยม
            rect_width = original_rect.width
            rect_height = original_rect.height
            
            # กำหนดเกณฑ์ขนาดที่ต้องการจะขยาย
            threshold_width = 1  # คุณสามารถปรับค่าเกณฑ์นี้ตามที่ต้องการ
            threshold_height = 1  # คุณสามารถปรับค่าเกณฑ์นี้ตามที่ต้องการ

            if rect_width < threshold_width or rect_height < threshold_height:
                # ขยายขนาดสำหรับสี่เหลี่ยมที่มีขนาดเล็กกว่าเกณฑ์
                reduced_rect = fitz.Rect(
                    original_rect.x0 - 0.9 * original_rect.width,
                    original_rect.y0 - 0.9 * original_rect.height,
                    original_rect.x1 + 0.9 * original_rect.width,
                    original_rect.y1 + 0.9 * original_rect.height
                )
            else:
                # คงขนาดเดิมสำหรับสี่เหลี่ยมที่มีขนาดใหญ่กว่าเกณฑ์
                reduced_rect = original_rect

            highlight = page.add_highlight_annot(reduced_rect)
            color = (1, 0.65, 0.9)  # Default color pink
            if word[4].startswith('C') and is_cap or word[4].startswith('YC') and is_cap:
                color = (0, 1, 0)  # Green for capacitors
            if word[4].startswith('R') and is_res or word[4].startswith('YR') and is_res:
                color = (1, 0.5, 0)  # Orange for resistors
            highlight.set_colors(stroke=color)
            highlight.update()
            collected_values.append(word[4])
            # print(word[4], "Actual_fond(EA)", loop_counter)
            text_info.configure(state="normal")
            text_info.insert(tk.END, f"{word[4]} Actual_fond {loop_counter} (EA)\n")
        collected_values_list.append(",".join(collected_values))
        count_list.append(count)
    doc.save(output_path_bot)
    data_storage.data_buttom['Actual_fond(EA)'] = collected_values_list
    data_storage.data_buttom['PDF_Actual(EA)'] = count_list
    data_storage.df.loc[data_storage.df['Op_Seq'] == 50, 'Actual_fond(EA)'] = data_storage.data_buttom['Actual_fond(EA)'].values
    data_storage.df.loc[data_storage.df['Op_Seq'] == 50, 'PDF_Actual(EA)'] = data_storage.data_buttom['PDF_Actual(EA)'].values
    diff_list = []
    for index, row in data_storage.data_buttom.iterrows():
        ref_des_set = set(row['Ref_Des'].split(','))
        collected_values_set = set(row['Actual_fond(EA)'].split(','))
        diff = ref_des_set.symmetric_difference(collected_values_set)
        diff_list.append(",".join(diff))
    data_storage.data_buttom['Not_found(EA)'] = diff_list
    data_storage.data_buttom['Result'] = data_storage.data_buttom.apply(lambda row: 'accepted' if row['PDF_Actual(EA)'] == row['BOM_Target(EA)'] else 'rejected', axis=1)
    file_path_bot = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_BOT_SMT.csv')
    os.makedirs(os.path.dirname(file_path_bot), exist_ok=True)
    data_storage.data_buttom.to_csv(file_path_bot, index=False)
    end_time_bot = time.time()
    elapsed_time_bot = end_time_bot - start_time_bot

def run_top_hl(text_info):
    global loop_counter
    global elapsed_time_top_hl
    start_time_top_hl = time.time()
    text_info.configure(state="normal")
    text_info.insert(tk.END, "TOP_HANDLOAD\n")
    hl_top = data_storage.data_hl_top.shape
    output_path_hl_top = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_TOP_HANDLOAD.pdf')
    os.makedirs(os.path.dirname(output_path_hl_top), exist_ok=True)
        # ตรวจสอบประเภทของ pdf_path
    if isinstance(data_storage.pdf_path, BytesIO):
        doc = fitz.Document(stream=data_storage.pdf_path)
    else:
        doc = fitz.open(data_storage.pdf_path)
    page = doc.load_page(data_storage.page_top)
    words = page.get_text("words")
    collected_values_list = []
    count_list = []
    for x in range(hl_top[0]):
        ref_des = data_storage.data_hl_top.iat[x, 3]
        ref_des_list = ref_des.split(",")
        filtered_words = [word for word in words if word[4] in ref_des_list]
        collected_values = []
        count = 0
        for word in filtered_words:
            loop_counter += 1
            count += 1
            rect = fitz.Rect(word[:4])
            highlight = page.add_highlight_annot(rect)
            color = (135/255, 206/255, 235/255)  # Default color light blue
            highlight.set_colors(stroke=color)
            highlight.update()
            # print(word[4], "Actual_fond(EA)", loop_counter)
            text_info.configure(state="normal")
            text_info.insert(tk.END, f"{word[4]} Actual_fond {loop_counter} (EA)\n")
            collected_values.append(word[4])
        collected_values_list.append(",".join(collected_values))
        count_list.append(count)
    doc.save(output_path_hl_top)
    data_storage.data_hl_top['Actual_fond(EA)'] = collected_values_list
    data_storage.data_hl_top['PDF_Actual(EA)'] = count_list
    data_storage.df.loc[(data_storage.df['Op_Seq'] > 190) & (data_storage.df['Op_Seq'] <= 600), 
    ['Actual_fond(EA)', 'PDF_Actual(EA)']] = data_storage.data_hl_top[['Actual_fond(EA)', 'PDF_Actual(EA)']].values
    diff_list = []
    for index, row in data_storage.data_hl_top.iterrows():
        ref_des_set = set(row['Ref_Des'].split(','))
        collected_values_set = set(row['Actual_fond(EA)'].split(','))
        diff = ref_des_set.symmetric_difference(collected_values_set)
        diff_list.append(",".join(diff))
    data_storage.data_hl_top['Not_found(EA)'] = diff_list
    data_storage.data_hl_top['Result'] = data_storage.data_hl_top.apply(lambda row: 'accepted' if row['PDF_Actual(EA)'] == row['BOM_Target(EA)'] else 'rejected', axis=1)
    file_path_top_hl = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_TOP_HANDLOAD.csv')
    os.makedirs(os.path.dirname(file_path_top_hl), exist_ok=True)
    data_storage.data_hl_top.to_csv(file_path_top_hl, index=False)
    end_time_top_hl = time.time()
    elapsed_time_top_hl = end_time_top_hl - start_time_top_hl
    
def run_bot_hl(text_info, Textboxfind):
    global loop_counter
    global elapsed_time_bot_hl
    start_time_bot_hl = time.time()
    text_info.configure(state="normal")
    text_info.insert(tk.END, "BOT_HANDLOAD\n")
    text_info.configure(state="disabled")
    hl_bot = data_storage.data_hl_bot.shape
    output_path_hl_bot = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_BOT_HANDLOAD.pdf')
    os.makedirs(os.path.dirname(output_path_hl_bot), exist_ok=True)
        # ตรวจสอบประเภทของ pdf_path
    if isinstance(data_storage.pdf_path, BytesIO):
        doc = fitz.Document(stream=data_storage.pdf_path)
    else:
        doc = fitz.open(data_storage.pdf_path)
    page = doc.load_page(data_storage.page_bot)
    words = page.get_text("words")
    collected_values_list = []
    count_list = []
    for x in range(hl_bot[0]):
        ref_des = data_storage.data_hl_bot.iat[x, 3]
        ref_des_list = ref_des.split(",")
        filtered_words = [word for word in words if word[4] in ref_des_list]
        collected_values = []
        count = 0
        for word in filtered_words:
            loop_counter += 1
            count += 1
            rect = fitz.Rect(word[:4])
            highlight = page.add_highlight_annot(rect)
            color = (135/255, 206/255, 235/255)  # Default color light blue
            highlight.set_colors(stroke=color)
            highlight.update()
            print(word[4], "Actual_fond(EA)", loop_counter)
            text_info.configure(state="normal")
            text_info.insert(tk.END, f"{word[4]} Actual_fond {loop_counter} (EA)\n")
            text_info.configure(state="disabled")
            collected_values.append(word[4])
        collected_values_list.append(",".join(collected_values))
        count_list.append(count)
    doc.save(output_path_hl_bot)
    data_storage.data_hl_bot['Actual_fond(EA)'] = collected_values_list
    data_storage.data_hl_bot['PDF_Actual(EA)'] = count_list
    data_storage.df.loc[(data_storage.df['Op_Seq'] > 190) & (data_storage.df['Op_Seq'] <= 600), 
    ['Actual_fond(EA)', 'PDF_Actual(EA)']] = data_storage.data_hl_bot[['Actual_fond(EA)', 'PDF_Actual(EA)']].values
    diff_list = []
    for index, row in data_storage.data_hl_bot.iterrows():
        ref_des_set = set(row['Ref_Des'].split(','))
        collected_values_set = set(row['Actual_fond(EA)'].split(','))
        diff = ref_des_set.symmetric_difference(collected_values_set)
        diff_list.append(",".join(diff))
    data_storage.data_hl_bot['Not_found(EA)'] = diff_list
    data_storage.data_hl_bot['Result'] = data_storage.data_hl_bot.apply(lambda row: 'accepted' if row['PDF_Actual(EA)'] == row['BOM_Target(EA)'] else 'rejected', axis=1)
    file_path_bot_hl = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_BOT_HANDLOAD.csv')
    os.makedirs(os.path.dirname(file_path_bot_hl), exist_ok=True)
    data_storage.data_hl_bot.to_csv(file_path_bot_hl, index=False)
    end_time_bot_hl = time.time()
    elapsed_time_bot_hl = end_time_bot_hl - start_time_bot_hl
    Textboxfind.configure(state="normal")
    Textboxfind.insert(tk.END, loop_counter)
    Textboxfind.configure(state="disabled")

def noload_top():
    global loop_counter
    global elapsed_time_noload_top
    start_time_noload_top = time.time()
    ref_des_list_flat = []
    for ref_des_l in data_storage.noload_top_h["Ref_Des"]:
        ref_des_list = ref_des_l.split(",")
        ref_des_list_flat.extend(ref_des_list)
        # ตรวจสอบประเภทของ pdf_path
    if isinstance(data_storage.pdf_path, BytesIO):
        doc = fitz.Document(stream=data_storage.pdf_path)
    else:
        doc = fitz.open(data_storage.pdf_path)
    page = doc.load_page(data_storage.page_top)
    words = page.get_text("words")
    text_content = [word[4] for word in words]
    ref_des_set = set(ref_des_list_flat)
    text_content_set = set(text_content)
    difference = list(text_content_set - ref_des_set)
    output_path_noload_top = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_TOP_NOLOAD.pdf')
    csv_output_path = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_TOP_NOLOAD.csv')
    collected_values_list = []
    count_list = []
    pattern = re.compile(r'^[A-Z]\d+$')
    total_count_top = 0
    with open(csv_output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Ref_Des', 'Count'])  # เขียนหัวตาราง
 
        for word in difference:
            if pattern.match(word):
                count = 0
                for word_item in words:
                    if word == word_item[4]:
                        count += 1
                        loop_counter += 1
                        # Create a rectangle for highlighting
                        original_rect = fitz.Rect(word_item[:4])
                        if original_rect.width <= 0 or original_rect.height <= 0:
                            continue
                        # Reduce the size of the rectangle
                        reduced_rect = fitz.Rect(
                            # original_rect.x0 + 0.15 * original_rect.width,
                            # original_rect.y0 + 0.15 * original_rect.height,
                            # original_rect.x1 - 0.15 * original_rect.width,
                            # original_rect.y1 - 0.15 * original_rect.height

                            original_rect.x0,
                            original_rect.y0,
                            original_rect.x1,
                            original_rect.y1 
                        )
                        # Add highlight annotation
                        highlight = page.add_highlight_annot(reduced_rect)
                        # Set custom color for the highlight
                        color = (1, 1, 0)  # Yellow
                        highlight.set_colors(stroke=color)
                        highlight.update()
                        print(word_item[4], "Actual_fond",loop_counter, "(EA)")
                        collected_values_list.append(word_item[4])
                        count_list.append(count)
                        writer.writerow([word_item[4], count])  # เขียนค่า word_item[4] และ count ลงในไฟล์ CSV
                total_count_top += count
                print(total_count_top,"")
    data_storage.total_count_top = total_count_top
    doc.save(output_path_noload_top)
    end_time_noload_top = time.time()
    elapsed_time_noload_top = end_time_noload_top - start_time_noload_top
def noload_bot():
    global loop_counter
    global elapsed_time_noload_bot
    start_time_noload_bot = time.time()
    ref_des_list_flat = []
    for ref_des_l in data_storage.noload_bot_h["Ref_Des"]:
        ref_des_list = ref_des_l.split(",")
        ref_des_list_flat.extend(ref_des_list)
        # ตรวจสอบประเภทของ pdf_path
    if isinstance(data_storage.pdf_path, BytesIO):
        doc = fitz.Document(stream=data_storage.pdf_path)
    else:
        doc = fitz.open(data_storage.pdf_path)
    # doc = fitz.open(data_storage.pdf_path)
    page = doc.load_page(data_storage.page_bot)
    words = page.get_text("words")
    text_content = [word[4] for word in words]
    ref_des_set = set(ref_des_list_flat)
    text_content_set = set(text_content)
    difference = list(text_content_set - ref_des_set)
    output_path_noload_top = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_BOT_NOLOAD.pdf')
    csv_output_path = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, data_storage.projectname+'_BOT_NOLOAD.csv')
    collected_values_list = []
    count_list = []
    pattern = re.compile(r'^[A-Z]\d+$')
    total_count_bot = 0
    with open(csv_output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Ref_Des', 'Count'])  # เขียนหัวตาราง

        for word in difference:
            if pattern.match(word):
                count = 0
                for word_item in words:
                    if word == word_item[4]:
                        count += 1
                        loop_counter += 1
                        # Create a rectangle for highlighting
                        original_rect = fitz.Rect(word_item[:4])
                        if original_rect.width <= 0 or original_rect.height <= 0:
                            continue
                        # Reduce the size of the rectangle
                        reduced_rect = fitz.Rect(
                            # original_rect.x0 + 0.15 * original_rect.width,
                            # original_rect.y0 + 0.15 * original_rect.height,
                            # original_rect.x1 - 0.15 * original_rect.width,
                            # original_rect.y1 - 0.15 * original_rect.height

                            original_rect.x0,
                            original_rect.y0,
                            original_rect.x1, 
                            original_rect.y1 
                        )
                        # Add highlight annotation
                        highlight = page.add_highlight_annot(reduced_rect)
                        # Set custom color for the highlight
                        color = (1, 1, 0)  # Yellow
                        highlight.set_colors(stroke=color)
                        highlight.update()
                        print(word_item[4], "Actual_fond(EA)",loop_counter,"(EA)")
                        collected_values_list.append(word_item[4])
                        count_list.append(count)
                        writer.writerow([word_item[4], count])  # เขียนค่า word_item[4] และ count ลงในไฟล์ CSV
                total_count_bot += count
    data_storage.total_count_bot = total_count_bot
    end_time_noload_bot = time.time()
    elapsed_time_noload_bot = end_time_noload_bot - start_time_noload_bot
    doc.save(output_path_noload_top)

def timework():
    global all_time
    all_time = (elapsed_time_bot_hl + elapsed_time_top_hl + elapsed_time_bot + elapsed_time_top+elapsed_time_noload_bot+elapsed_time_noload_top)
    data_storage.time_top = round(elapsed_time_top, 2)
    data_storage.time_bot = round(elapsed_time_bot, 2)
    data_storage.time_hl_top = round(elapsed_time_top_hl, 2)
    data_storage.time_hl_bot = round(elapsed_time_bot_hl, 2)
    data_storage.time_no_top = round(elapsed_time_noload_top, 2)
    data_storage.time_no_bot = round(elapsed_time_noload_bot, 2)
    all_time = round(all_time, 2)
    data_storage.all_time = all_time
    print(all_time)
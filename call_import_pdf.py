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
import time
import re
import shutil
import data_storage

from io import BytesIO

def showfile_pdf(root, text_info,red_frame_run,red_frame_importpdf):
    option = IntVar()
    option.set(0)
    data_storage.option = option
    print("-------------op-------------")
    print(option.get())
    # คำนวณตำแหน่งตรงกลางของหน้าจอ
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 320
    window_height = 250
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    
    # กำหนดตำแหน่งและขนาดก่อนสร้าง mywindow
    mywindow = Toplevel(root)
    mywindow.title("Import PDF file")
    mywindow.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    mywindow.resizable(False, False)

    mywindow.transient(root)
    mywindow.grab_set()
    mywindow.focus()
    global pdf_path_top, pdf_path_bot
    pdf_path_top = None
    pdf_path_bot = None

    def p():
        if option.get() == 1:
            print("Button 1 selected")
            button_two.configure(state="normal")
            button_onepagetop.configure(state="disabled")
            button_onepagebot.configure(state="disabled")
            data_storage.option.set(1)
    def p2():
        if option.get() == 2:
            print("Button 2 selected")
            button_onepagetop.configure(state="normal")
            button_onepagebot.configure(state="normal")
            button_two.configure(state="disabled")
            data_storage.option.set(2)
    def p3():
        if option.get() == 3:
            print("Button 3 selected")
            button_cad.configure(state="normal")
            button_two.configure(state="disabled")
            button_onepagetop.configure(state="disabled")
            button_onepagebot.configure(state="disabled")
            data_storage.option.set(3)
    def import_pdf_twopage():
        clear_import_onepage()
        global pdf_path, pdfname
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        data_storage.pdf_path = pdf_path
        if not pdf_path:
            messagebox.showerror("Error", "No file selected")
        else:
            pdfname = os.path.basename(pdf_path)
            data_storage.pdfname = pdfname
            if pdfname:
                red_frame_importpdf.config(highlightthickness=0)
                red_frame_run.config(highlightthickness=2)
            mywindow.destroy()

            # เก็บไฟล์หลัก
            # save_path = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, pdfname)
            # os.makedirs(os.path.dirname(save_path), exist_ok=True)
            # shutil.copy(pdf_path, save_path)
    
            text_info.configure(state="normal")
            text_info.insert(tk.END, pdfname + " imported successfully\n")
            text_info.configure(state="disabled")
            print(pdf_path)
            find_page_top()
            find_page_bot()

    def import_pdf_onepage_top():
        clear_import_twopage()
        global pdf_path_top
        pdf_path_top = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        pdf_top_filename = os.path.basename(pdf_path_top)
        data_storage.pdf_top_filename = pdf_top_filename

        # save_path = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, pdf_top_filename)
        # os.makedirs(os.path.dirname(save_path), exist_ok=True)
        # shutil.copy(pdf_path_top, save_path)

        print(pdf_path_top)
        if pdf_path_top:
            text_info.configure(state="normal")
            text_info.insert(tk.END,"TOP SIDE " + pdf_top_filename + " imported successfully\n")
            text_info.configure(state="disabled")
        check_merge()

    def import_pdf_onepage_bot():
        clear_import_twopage()
        global pdf_path_bot
        pdf_path_bot = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        pdf_bot_filename = os.path.basename(pdf_path_bot)
        data_storage.pdf_bot_filename = pdf_bot_filename

        # save_path = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname, pdf_bot_filename)
        # os.makedirs(os.path.dirname(save_path), exist_ok=True)
        # shutil.copy(pdf_path_bot, save_path)
        if pdf_path_bot:
            text_info.configure(state="normal")
            text_info.insert(tk.END,"BOT SIDE " + pdf_bot_filename + " imported successfully\n")
            text_info.configure(state="disabled")
        print(pdf_path_bot)
        check_merge()

    def check_merge():
        if pdf_path_top and pdf_path_bot:
            merged_pdf_memory = merge_pdfs_with_fitz_to_memory()
            if merged_pdf_memory:
                red_frame_importpdf.config(highlightthickness=0)
                red_frame_run.config(highlightthickness=2)
                # messagebox.showinfo("Info", "PDFs have been merged successfully.")
                find_page_top()
                find_page_bot()
                mywindow.destroy()

    def merge_pdfs_with_fitz_to_memory():
        global pdf_path
        if pdf_path_top and pdf_path_bot:
            merged_pdf = fitz.open()

            pdf_top = fitz.open(pdf_path_top)
            for page in range(pdf_top.page_count):
                merged_pdf.insert_pdf(pdf_top, from_page=page, to_page=page)

            pdf_bot = fitz.open(pdf_path_bot)
            for page in range(pdf_bot.page_count):
                merged_pdf.insert_pdf(pdf_bot, from_page=page, to_page=page)

            merged_pdf_memory = BytesIO()
            merged_pdf.save(merged_pdf_memory)
            merged_pdf.close()

            merged_pdf_memory.seek(0)
            pdf_path = merged_pdf_memory
            data_storage.pdf_path = pdf_path
            return merged_pdf_memory
        else:
            print("Please import both PDFs first.")
            return None
    def importcad():
        global cadfile
        cadfile = filedialog.askopenfilename(filetypes=[("CAD files", "*.cad")])
        cadfilename = os.path.basename(cadfile)

        # text_info.configure(state="normal")
        # text_info.insert(tk.END, cadfilename + " imported successfully\n")
        # text_info.configure(state="disabled")

        print("======",cadfilename,"======")
        data_storage.cadfilename = cadfilename
        data_storage.cadfile = cadfile
        if not cadfile:
            print(cadfile)
        else:
            mywindow.destroy()
            if cadfile:
                red_frame_importpdf.config(highlightthickness=0)
                red_frame_run.config(highlightthickness=2)
                text_info.configure(state="normal")
                text_info.insert(tk.END, cadfilename + " imported successfully\n")
                text_info.configure(state="disabled")
            
            cutfilecad()


    left_frame = tk.Frame(mywindow, bg="#D9D9D9", padx=5, pady=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    b_label = ttk.Label(mywindow, text="Select import", background="#EBEBEB", foreground="black")
    b_label.grid(row=0, column=0, padx=5, pady=20)
    frame = tk.Frame(mywindow, bg="#D9D9D9", padx=5, pady=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    frame2 = tk.Frame(mywindow, bg="#D9D9D9", padx=5, pady=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    frame2.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
    frame2.grid_rowconfigure(0, weight=0)
    frame2.grid_columnconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)
    frame2.grid_columnconfigure(1, weight=1)
    frame2.grid_columnconfigure(2, weight=1)

    R1 = Radiobutton(frame, text="Import 1 file", variable=option, value=1, bg="#EBEBEB", command=p)
    R1.grid(row=1, column=0, padx=20, pady=10)

    R2 = Radiobutton(frame, text="Import 2 files", variable=option, value=2, bg="#EBEBEB", command=p2)
    R2.grid(row=2, column=0, padx=20, pady=2)

    R3 = Radiobutton(frame2, text="Import CAD file", variable=option, value=3, bg="#EBEBEB", command=p3)
    R3.grid(row=1, column=0, padx=0, pady=10)

    button_two = Button(frame, text="TOP&BOTTOM", state="disabled", command=import_pdf_twopage)
    button_two.grid(row=1, column=1, padx=5, pady=10, sticky=W)

    button_onepagetop = Button(frame, text="TOP", state="disabled", command=import_pdf_onepage_top)
    button_onepagetop.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    button_onepagebot = Button(frame, text="BOTTOM", state="disabled", command=import_pdf_onepage_bot)
    button_onepagebot.grid(row=2, column=2, padx=0, pady=5, sticky=W)

    button_cad = Button(frame2, text="CAD", state="disabled",command= importcad)
    button_cad.grid(row=1, column=1, padx=0, pady=5, sticky=W)

def find_page_top():
    global page_top
    attempts = 0
    max_attempts = 2
    page_top = None

    # ตรวจสอบว่าถ้าเป็น BytesIO หรือไม่
    if isinstance(pdf_path, BytesIO):
        doc = fitz.Document(stream=pdf_path)
    else:
        doc = fitz.open(pdf_path)  # เปิดแบบไฟล์ปกติ

    total_pages = len(doc)
    while attempts < max_attempts:
        ref_des_values = []
        for ref_des in data_storage.data_top_CAP['Ref_Des']:
            ref_des_values.extend(ref_des.split(','))
        random_CAP = random.sample(ref_des_values, 5)
        for ref_des in data_storage.data_top_RES['Ref_Des']:
            ref_des_values.extend(ref_des.split(','))
        random_RES = random.sample(ref_des_values, 5)
        random_value = random_CAP + random_RES
        found_pages = {value: [] for value in random_value}
        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            words = page.get_text("words")
            for word in words:
                for value in random_value:
                    if word[4] == value:
                        found_pages[value].append(page_num)
            all_pages = [page for pages in found_pages.values() for page in pages]
            if len(all_pages) > 1 and len(set(all_pages)) < len(all_pages):
                page_top = all_pages[0]
                data_storage.page_top = page_top
                break
        if page_top is not None:
            break
        attempts += 1 
    print("Page_Top", page_top)

def find_page_bot():
    global page_bot
    attempts = 0
    max_attempts = 2
    page_bot = None

    # ตรวจสอบว่าถ้าเป็น BytesIO หรือไม่
    if isinstance(pdf_path, BytesIO):
        doc = fitz.Document(stream=pdf_path)
    else:
        doc = fitz.open(pdf_path)  # เปิดแบบไฟล์ปกติ

    total_pages = len(doc)
    while attempts < max_attempts:
        ref_des_values = []
        for ref_des in data_storage.data_bot_CAP['Ref_Des']:
            ref_des_values.extend(ref_des.split(','))
        random_CAP = random.sample(ref_des_values, 5)
        for ref_des in data_storage.data_bot_RES['Ref_Des']:
            ref_des_values.extend(ref_des.split(','))
        random_RES = random.sample(ref_des_values, 5)
        random_value = random_CAP + random_RES
        found_pages = {value: [] for value in random_value}
        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            words = page.get_text("words")
            for word in words:
                for value in random_value:
                    if word[4] == value:
                        found_pages[value].append(page_num)
            all_pages = [page for pages in found_pages.values() for page in pages]
            if len(all_pages) > 1 and len(set(all_pages)) < len(all_pages):
                page_bot = all_pages[0]
                data_storage.page_bot = page_bot
                break
        if page_bot is not None:
            break
        attempts += 1
    print("Page_bot", page_bot)

def clear_import_twopage():
    global pdf_path, pdfname
    pdf_path = None
    pdfname = None
    data_storage.pdf_path = None
    data_storage.pdfname = None

def clear_import_onepage():
    global pdf_path_top, pdf_path_bot,pdf_top_filename,pdf_bot_filename
    pdf_path_top = None
    pdf_path_bot = None
    pdf_top_filename = None
    pdf_bot_filename = None
    data_storage.pdf_top_filename = None
    data_storage.pdf_bot_filename = None

def cutfilecad():
    cad = open(cadfile, "r")
    
    # cadfile use did file
    capturing = False
    capturing_2 = False 
    capturing_3 = False
    header_lines_top = []
    header_lines_com = []
    header_lines_bot = []
    for line in cad:
            if line.startswith("$HEADER"):
                capturing = True  
            if capturing:
                header_lines_top.append(line)  #get line
            if line.startswith("$ENDSHAPES"):
                capturing = False  #stop
                header_lines_top.append("\n") 

            if line.startswith("$COMPONENTS"):
                capturing_2 = True  
            if capturing_2:
                header_lines_com.append(line)  #get line
            if line.startswith("$ENDCOMPONENTS"):
                capturing_2 = False  #stop
                header_lines_com.append("\n")  #get line

            if line.startswith("$DEVICES"):
                capturing_3 = True  
            if capturing_3:
                header_lines_bot.append(line)  #get line

    cadpath= "parts_cadprocess"
    # file_path_header = os.path.join(cadpath,"head_cad.cad")
    file_path_com = os.path.join(cadpath,"com.cad")
    # file_path_bot = os.path.join(cadpath,"bottom_cad.cad")

    # with open(file_path_header, "w") as output_file:
    #     output_file.writelines(header_lines_top)
    # print("complete_top")
    with open(file_path_com, "w") as output_file_com:
        output_file_com.writelines(header_lines_com)
    # print("complete_com")
    # with open(file_path_bot, "w") as output_file_bot:
    #     output_file_bot.writelines(header_lines_bot)
    # print("complete_bot")

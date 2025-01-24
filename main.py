# import numpy as np
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import os
from tkinter import simpledialog

import data_storage
import call_config
import main_call_login
import call_highlight
from call_createcustomer import createcustomer, create_folders_from_csv,load_csv_data
from call_creatorproject import createprojectname
from call_import_csv import open_file_csv
from call_import_pdf import showfile_pdf
import resetfile
import call_Merge_images


display = tk.Tk()
display.title("Program highlights")
display.state('zoomed')
display.configure(bg="#DCDCDC")
display.geometry("1200x660")
# ---------------------
display.update_idletasks()
# screen_width = display.winfo_screenwidth()
# screen_height = display.winfo_screenheight()
# size = tuple(int(_) for _ in display.geometry().split('+')[0].split('x'))
# x = (screen_width - size[0]) // 2
# y = (screen_height - size[1]) // 2
# display.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
# ---------------------
# display.resizable(False, False)
load_csv_data()
# ฟังก์ชันโหลดโลโก้ในพื้นหลัง
def load_logo_image():
    logo_image_path = "image/minisanmina.png"
    logo_image = Image.open(logo_image_path)
    new_size = (144, 144)  # ลดขนาดลงเพื่อความรวดเร็ว
    resized_logo_image = logo_image.resize(new_size, Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(resized_logo_image)
    display.iconphoto(False, logo_photo)

# ฟังก์ชันโหลดข้อมูล Banner Image
def load_banner_image():
    global banner_image
    image_path = "image/Sanminalogo.png"
    original_image = Image.open(image_path)
    resized_image = original_image.resize((120, 70), Image.Resampling.LANCZOS)
    banner_image = ImageTk.PhotoImage(resized_image)
    image_label.config(image=banner_image)

# เรียกใช้ Thread ในการโหลดรูปภาพ
threading.Thread(target=load_logo_image, daemon=True).start()
# -----------------------------
option = tk.IntVar()
option.set(0)
fil_capa = tk.IntVar()
fil_capa.set(0)
fil_res = tk.IntVar()
fil_res.set(0)
fil_other = tk.IntVar()
fil_other.set(0)
fil_ic = tk.IntVar()
fil_ic.set(0)
iccall_var = tk.BooleanVar()

# สร้างพื้นหลัง UI ทันทีเพื่อความรวดเร็ว
# -----ส่วนหัว------
rows_display = 3
columns_display = 3
banner_height = 110
footer_height = 50

# Configure rows and columns
display.grid_rowconfigure(0, minsize=banner_height)
display.grid_rowconfigure(1, weight=1)
display.grid_rowconfigure(2, minsize=footer_height)
for i in range(columns_display):
    display.grid_columnconfigure(i, weight=1)

# Banner Frame
banner_frame = tk.Frame(display, bg="#FFFAFA")
banner_frame.grid(row=0, column=0, columnspan=columns_display, sticky='nsew', padx=2, pady=0)
image_label = tk.Label(banner_frame, bg="#FFFAFA")  # กำหนด Label แต่ยังไม่ใส่รูปภาพ
image_label.pack(side='left', padx=5, pady=5)

# เรียกใช้ Thread ในการโหลด Banner Image
threading.Thread(target=load_banner_image, daemon=True).start()

# Right Frame for User Entry
right_frame = tk.Frame(banner_frame, bg="#FFFAFA")
right_frame.pack(side='right', padx=10, pady=5)

# Banner Label and User Entry
banner_label = ttk.Label(right_frame, text=data_storage.versions, background="#FFFAFA", font=("Arial", 10), foreground="black")
banner_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
user_text = tk.Text(right_frame, height=1, width=15, font=("Arial", 10), fg="blue", highlightbackground="black", highlightthickness=1)
user_text.grid(row=1, column=0, sticky='e', padx=5, pady=5)

# กำหนดค่าเริ่มต้นให้กับ Combobox
customer_names = data_storage.customer_data['Customer_name'].tolist() if hasattr(data_storage, 'customer_data') else []
combobox_customer = ttk.Combobox(display, state="readonly", values=customer_names)
combobox_customer.grid(row=1, column=0, padx=5, pady=5, sticky='w')

# ฟังก์ชันสร้างโฟลเดอร์ CSV ในพื้นหลัง
def create_folders_background():
    create_folders_from_csv()
# เรียกใช้ Thread ในการสร้างโฟลเดอร์
threading.Thread(target=create_folders_background, daemon=True).start()

# -----ฟังก์ชันเพิ่มเติม---------
def createcustomerwindows():
    createcustomer(display, update_combobox_values)  # ส่งฟังก์ชัน update_combobox_values ไปให้ createcustomer

def update_combobox_values(values):
    """อัปเดตค่าใน Combobox ของ main.py"""
    combobox_customer['values'] = values  # อัปเดตค่าของ Combobox

def on_select(event):
    selection = combobox_customer.get()
    data_storage.selected_customer = selection
    if selection:
        red_frame_combobox_customer.config(highlightthickness=0)
        red_frame_button_createprojectname.config(highlightthickness=2)
    print(f"Selected Customer is: {selection}")

def create_pn():

    if not data_storage.selected_customer:
        messagebox.showerror("ERROR", "Please select a customer first.")
    else:
        createprojectname(text_info)
        if data_storage.projectname:
            red_frame_button_createprojectname.config(highlightthickness=0)
            red_frame_importcsv.config(highlightthickness=2)
            red_frame_importpdf.config(highlightthickness=0)

def import_csv_data():

    if data_storage.projectname is None:
        messagebox.showerror("ERROR", "Please create project name first.")
    else:
        open_file_csv(text_info,Textboxtotal)
        if data_storage.filenamecsv:
            red_frame_importcsv.config(highlightthickness=0)
            red_frame_importpdf.config(highlightthickness=2)
            red_frame_run.config(highlightthickness=0)
            
def open_pdf_window():
    
    if not data_storage.filenamecsv:
        messagebox.showerror("ERROR", "Please import a BOM file first")
    else:
        showfile_pdf(display,text_info,red_frame_run,red_frame_importpdf)

def cmd_find_components():
    dg1=0
    dg2=0
    dg8=0
    dg4=0
    if fil_capa.get()==1:   #1
       dg1=1
    else:
        dg1=0
    if fil_res.get()==1:    #2
        dg2=2
    else:
        dg2=0
    if fil_other.get()==1:  #8
        dg8=8
    else:
        dg8=0
    if fil_ic.get()==1:     #4
        dg4 =4
    else:
        dg4=0
    index_cmd = dg1+dg2+dg8+dg4
    print('index_cmd')
    print(index_cmd)
    cmd_query =['Item_Description.str.contains("0000000000000")',
                'Item_Description.str.contains("CAP")',
                'Item_Description.str.contains("RES")',
                'Item_Description.str.contains("CAP") or Item_Description.str.contains("RES")',
                'Item_Description.str.startswith("IC")',
                'Item_Description.str.contains("CAP") or Item_Description.str.startswith("IC")',
                'Item_Description.str.contains("RES") or Item_Description.str.startswith("IC")',
                'Item_Description.str.contains("RES") or Item_Description.str.contains("CAP") or Item_Description.str.startswith("IC")',
                'Item_Description.str.contains("RES") == False and Item_Description.str.contains("CAP") == False and Item_Description.str.startswith("IC") == False',
                'Item_Description.str.contains("CAP") or Item_Description.str.contains("RES") == False and Item_Description.str.startswith("IC") == False',
                'Item_Description.str.contains("RES") or Item_Description.str.contains("CAP") == False and Item_Description.str.startswith("IC") == False',
                'Item_Description.str.contains("RES") or Item_Description.str.contains("CAP") or Item_Description.str.startswith("IC") == False',
                'Item_Description.str.contains("RES") == False and Item_Description.str.contains("CAP") == False and Item_Description.str.startswith("IC")',
                'Item_Description.str.contains("RES") or Item_Description.str.contains("CAP") and Item_Description.str.startswith("IC") == False',
                'Item_Description.str.contains("RES") == False and Item_Description.str.contains("CAP") or Item_Description.str.startswith("IC")',
                'Item_Description.str.contains("RES") == False or Item_Description.str.contains("CAP") == False or Item_Description.str.startswith("IC") == False or Item_Description.str.contains("RES") or Item_Description.str.contains("CAP") or Item_Description.str.startswith("IC")',
                'Item_Description.str.contains("RES") or Item_Description.str.startswith("IC") and Item_Description.str.contains("CAP") == False'
                ]
    return cmd_query[index_cmd]
def filters():
    global layer_choice
    global data_filter
    layer_choice = option.get()
    print(layer_choice )
    match layer_choice:
        case 1:
            C1.config(state=tk.NORMAL)
            C2.config(state=tk.NORMAL)
            C3.config(state=tk.NORMAL)
            C4.config(state=tk.NORMAL)
            data_filter=data_storage.data_top
        case 2:
            C1.config(state=tk.NORMAL)
            C2.config(state=tk.NORMAL)
            C3.config(state=tk.NORMAL)
            C4.config(state=tk.NORMAL)
            data_filter=data_storage.data_buttom
        case 3:
            C1.config(state=tk.DISABLED)
            C2.config(state=tk.DISABLED)
            C3.config(state=tk.DISABLED)
            C4.config(state=tk.DISABLED)
            data_filter=data_storage.data_hl_top
            fil_capa.set(0),fil_res.set(0),fil_other.set(0),fil_ic.set(0)
        case 4:
            C1.config(state=tk.DISABLED)
            C2.config(state=tk.DISABLED)
            C3.config(state=tk.DISABLED)
            C4.config(state=tk.DISABLED)
            data_filter=data_storage.data_hl_bot
            fil_capa.set(0),fil_res.set(0),fil_other.set(0),fil_ic.set(0)
        case _:
            messagebox.showinfo("Data Table", "No Data")
            fil_capa.set(0),fil_res.set(0),fil_other.set(0)
    if layer_choice <3:
         find_row = cmd_find_components()
         newdata_filter = data_filter.query(find_row)
    else:
        newdata_filter=data_filter      
    update_table(newdata_filter)
selected_value = tk.StringVar()
def check_status():
    data_storage.iccall_value = iccall_var.get()
def update_table(data):
    # Create a style for the Treeview
    style = ttk.Style()
    style.configure("Custom.Treeview.Heading", font=("Arial", 10, "bold"), foreground="black")
    style.configure("Custom.Treeview", rowheight=25, borderwidth=1, relief="solid", highlightthickness=1)

    displaytable.delete(*displaytable.get_children())
    displaytable['column'] = list(data.columns)
    displaytable['show'] = "headings"
    
    # Set custom style for the table headings
    displaytable.configure(style="Custom.Treeview")

    for col in displaytable['column']:
        displaytable.heading(col, text=col)
    
    df_row = data.to_numpy().tolist()
    for row in df_row:
        # Ensure 'Result' column exists and handle empty values
        result_index = data.columns.get_loc('Result')
        result_value = row[result_index] if row[result_index] else 'pending'
        if not row[result_index]:  # Check if the value is empty or None
            tags = ()
        else:
            tags = ('accepted',) if result_value == 'accepted' else ('rejected',)
        displaytable.insert("", "end", values=row, tags=tags)
    
    # Configure tags for coloring
    displaytable.tag_configure('accepted', background='#7FFF00')
    displaytable.tag_configure('rejected', background='#FF4444')
    displaytable.tag_configure('pending', background='#FFDD44')

def Run_highlight():

    option_selected = data_storage.option.get()
    # print(option_selected)
    if  option_selected == 1:
        if not data_storage.filenamecsv:
            messagebox.showerror("ERROR","Please import a CSV file before proceeding.")
        if not data_storage.pdf_path:
            messagebox.showerror("ERROR","Please import a PDF file before proceeding.")
        if not data_storage.projectname:
            messagebox.showerror("ERROR","Please create project name before proceeding.")
        if data_storage.pdf_path:
            call_highlight.runfile(text_info, Textboxfind)
            red_frame_run.config(highlightthickness=0)
            red_frame_button_createprojectname.config(highlightthickness=2)
            resetfile.reset_files()

    elif  option_selected == 2:
        if not data_storage.filenamecsv:
            messagebox.showerror("ERROR","Please import a CSV file before proceeding.")
        if not data_storage.pdf_top_filename:
            messagebox.showerror("ERROR","Please import a PDF TOP file before proceeding.")
        if not data_storage.pdf_bot_filename:
            messagebox.showerror("ERROR","Please import a PDF BOT file before proceeding.")
        else:
            call_highlight.runfile(text_info, Textboxfind)
            red_frame_run.config(highlightthickness=0)
            red_frame_button_createprojectname.config(highlightthickness=2)
            resetfile.reset_files()

    elif option_selected == 3:
        if not data_storage.cadfile:
            messagebox.showerror("ERROR","Please import a CAD file before proceeding.")
        if data_storage.cadfile:
            call_highlight.call_runcad(Textboxfind,text_info,Textboxnotfound)
            red_frame_run.config(highlightthickness=0) 
            red_frame_button_createprojectname.config(highlightthickness=2)
            resetfile.reset_files()
# รวมรูป
def on_files_selected(selected_files, folder_path):
    """
    Callback function สำหรับรับค่าที่เลือกจาก GUI และดำเนินการ
    """
    print("Selected Files:", selected_files)
    print("Folder Path:", folder_path)

    # สร้างหน้าต่าง dialog เพื่อขอชื่อไฟล์
    root = tk.Tk()
    root.withdraw()  # ซ่อนหน้าต่างหลัก
    root.attributes('-topmost', True)  # ทำให้หน้าต่างอยู่ด้านบนเสมอ
    root.focus_force()  # ดึงหน้าต่างขึ้นมา
    file_name = simpledialog.askstring("File Name", "Enter the name for the combined image:", parent=root)


    if not file_name:
        print("No file name provided. Operation cancelled.")
        messagebox.showinfo("Operation Cancelled", "No file name provided. Please try again.")
        return

    # เพิ่ม .png เป็นนามสกุลไฟล์
    output_file = f"{file_name}.png"

    # สร้างเส้นทางไฟล์เต็ม
    full_paths = [os.path.join(folder_path, file) for file in selected_files]

    try:
        # ลบพื้นหลัง
        images_without_bg = [call_Merge_images.remove_black_background(path) for path in full_paths]

        # รวมรูปภาพและเพิ่มพื้นหลังสีขาว
        output_path = os.path.join(folder_path, output_file)
        call_Merge_images.combine_images_with_white_background(images_without_bg, output_path)

        # แจ้งผลลัพธ์สำเร็จ
        messagebox.showinfo("Success", f"Combined image saved to: {output_path}")
        print(f"Combined image saved to: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error processing files: {e}")
        print(f"Error: {e}")

def run_merge_gui():
    """
    เรียกใช้งาน GUI จาก call_Merge_images
    """
    call_Merge_images.create_gui(on_files_selected)

left_frame = tk.Frame(display, bg="#D9D9D9", padx=5, pady=5, highlightbackground="black", highlightcolor="black", highlightthickness=1)
left_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
left_frame.grid_rowconfigure(0, weight=0)
left_frame.grid_columnconfigure(0, weight=1)
left_frame.grid_columnconfigure(1, weight=1)
left_frame.grid_columnconfigure(2, weight=1)

# Textboxreadfilecsv = Text(left_frame, height=1, width=55, state="disabled")
# Textboxreadfilecsv.grid(row=0, column=0, columnspan=3, padx=0, pady=5, sticky='ew')
lable_c = ttk.Label(left_frame, text=" Customer                      Project name                                      Import files", background="#D9D9D9", font=("Arial", 12), foreground="black")
lable_c.grid(row=0, column=0, columnspan=3, padx=0, pady=5, sticky='ew')

red_frame_button_createprojectname = tk.Frame(left_frame, highlightbackground="red", highlightthickness=0, bd=0)
red_frame_button_createprojectname.grid(row=1, column=0, padx=(100, 0), pady=0, sticky='e')
button_createprojectname = tk.Button(red_frame_button_createprojectname, text="Create project name", command=create_pn)
button_createprojectname.grid(row=1, column=0, padx=(0, 0), pady=0, sticky='e')

red_frame_importcsv = tk.Frame(left_frame, highlightbackground="red", highlightthickness=0, bd=0)
red_frame_importcsv.grid(row=1, column=1, padx=(90, 0), pady=5, sticky='w')
button_importcsv = tk.Button(red_frame_importcsv, text="Import csv", command=import_csv_data)
button_importcsv.grid(row=1, column=1, padx=0, pady=0, sticky='w')

red_frame_importpdf = tk.Frame(left_frame, highlightbackground="red", highlightthickness=0, bd=0)
red_frame_importpdf.grid(row=1, column=1, padx=(105, 0), pady=5, sticky='e')
button_importpdf = tk.Button(red_frame_importpdf, text="Import pdf",command=open_pdf_window)
button_importpdf.grid(row=1, column=1, padx=0, pady=0, sticky='e')
# กำหนด Combobox
red_frame_combobox_customer = tk.Frame(left_frame, highlightbackground="red", highlightthickness=2, bd=0)  
red_frame_combobox_customer.grid(row=1, column=0, padx=5, pady=5, sticky='w')
combobox_customer = ttk.Combobox(red_frame_combobox_customer, state="readonly", values=customer_names)

combobox_customer.set("Select Customer")
combobox_customer.bind("<<ComboboxSelected>>", on_select)
combobox_customer.grid(row=1, column=0, padx=0, pady=0, sticky='w')
# Radio buttons
redio_frame = tk.Frame(left_frame, bg="#EBEBEB", padx=5, pady=0)
redio_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5, columnspan=3)
for i in range(3):
    redio_frame.grid_columnconfigure(i, weight=1)
redio_frame.grid_rowconfigure(0, weight=0)
R1 = Radiobutton(redio_frame, text="Top", bg="#EBEBEB",variable=option,value=1,command=filters)
R1.grid(row=0, column=0, padx=(0, 20), pady=5)
R2 = Radiobutton(redio_frame, text="Button", bg="#EBEBEB",variable=option,value=2,command=filters)
R2.grid(row=0, column=1, padx=(20, 20), pady=5)
R3 = Radiobutton(redio_frame, text="Handload_TOP", bg="#EBEBEB",variable=option,value=3,command=filters)
R3.grid(row=0, column=2, padx=(20, 20), pady=5)
R4 = Radiobutton(redio_frame, text="Handload_BOT", bg="#EBEBEB",variable=option,value=4,command=filters)
R4.grid(row=0, column=3, padx=(20, 40), pady=5)

iccall = Checkbutton(left_frame, text="Run with IC separation.",bg="#D9D9D9",variable=iccall_var,command=check_status)
iccall.grid(row=6, column=1, padx=(10,20), pady=5,sticky='e')

red_frame_run = tk.Frame(left_frame, highlightbackground="red", highlightthickness=0, bd=0)
red_frame_run.grid(row=6, column=2, padx=10, pady=5, sticky='w')
button_run = tk.Button(red_frame_run, text="RUN",command=Run_highlight)
button_run.grid(row=6, column=2, padx=0, pady=0, sticky='w')
# Checkboxes
checkbox_frame = tk.Frame(left_frame, bg="#EBEBEB", padx=5, pady=0)
checkbox_frame.grid(row=3, column=0, sticky='nsew', padx=5, pady=5, columnspan=3)
for i in range(3):
    checkbox_frame.grid_columnconfigure(i, weight=1)
checkbox_frame.grid_rowconfigure(0, weight=0)
C1 = Checkbutton(checkbox_frame, text="RES", bg="#EBEBEB",variable=fil_res, onvalue=1, offvalue=0, command=filters)
C1.grid(row=0, column=0, padx=(0,40), pady=5)
C2 = Checkbutton(checkbox_frame, text="CAPA", bg="#EBEBEB",variable=fil_capa, onvalue=1, offvalue=0, command=filters)
C2.grid(row=0, column=1, padx=(0,50), pady=5)
C3 = Checkbutton(checkbox_frame, text="OTHER", bg="#EBEBEB",variable=fil_other, onvalue=1, offvalue=0, command=filters)
C3.grid(row=0, column=2, padx=(0,80), pady=5)
C4 = Checkbutton(checkbox_frame, text="IC", bg="#EBEBEB",variable=fil_ic, onvalue=1, offvalue=0, command=filters)
C4.grid(row=0, column=3, padx=(0,105), pady=5)
# -------------------------------------------------
total_frame = tk.Frame(left_frame, bg="#D9D9D9")
total_frame.grid(row=6, column=0, columnspan=3, padx=2, pady=2, sticky='w')

data_label_total = ttk.Label(total_frame, text="Total", background="#D9D9D9", font=("Arial", 8), foreground="black")
data_label_total.pack(side='left', padx=(2, 5), pady=5)
Textboxtotal = Text(total_frame, height=1, width=6, state="disabled")
Textboxtotal.pack(side='left', padx=(2, 0), pady=5)

# data_label_total = ttk.Label(total_frame, text="Total", background="#D9D9D9", font=("Arial", 8), foreground="black")
# data_label_total.pack(side='left', padx=(2, 5), pady=5)

data_label_find = ttk.Label(total_frame, text="Found", background="#D9D9D9", font=("Arial", 8), foreground="black")
data_label_find.pack(side='left', padx=(3, 5), pady=5)
Textboxfind = Text(total_frame, height=1, width=6, state="disabled")
Textboxfind.pack(side='left', padx=(3, 0), pady=5)

# data_label_find = ttk.Label(total_frame, text="Found", background="#D9D9D9", font=("Arial", 8), foreground="black")
# data_label_find.pack(side='left', padx=(3, 5), pady=5)

data_label_notfound = ttk.Label(total_frame, text="Not found", background="#D9D9D9", font=("Arial", 8), foreground="black")
data_label_notfound.pack(side='left', padx=(3, 5), pady=5)
Textboxnotfound = Text(total_frame, height=1, width=6, state="disabled")
Textboxnotfound.pack(side='left', padx=(3, 0), pady=5)

# data_label_notfound = ttk.Label(total_frame, text="Found", background="#D9D9D9", font=("Arial", 8), foreground="black")
# data_label_notfound.pack(side='left', padx=(3, 5), pady=5)
# -------------------------------------------------
# f_merge = tk.Frame(left_frame, bg="#D9D9D9")
# f_merge.grid(row=7, column=0, columnspan=3, padx=2, pady=2, sticky='w')
# merge = tk.Button(f_merge, text="Merge")
# merge.grid(row=7, column=2, padx=0, pady=0, sticky='w')
# -------------------------------------------------
# Information text box

show_info_all = tk.Frame(left_frame)
show_info_all.grid(row=5, column=0, columnspan=3, sticky='nsew', padx=5, pady=10)

vscrollbar_text_widget = tk.Scrollbar(show_info_all, orient="vertical")
vscrollbar_text_widget.grid(row=0, column=1, sticky='ns')
text_info = tk.Text(show_info_all, height=2, width=40, wrap='none', state="disabled", yscrollcommand=vscrollbar_text_widget.set)
text_info.grid(row=0, column=0, sticky='nsew')
show_info_all.grid_rowconfigure(0, weight=1)
show_info_all.grid_columnconfigure(0, weight=1)
vscrollbar_text_widget.config(command=text_info.yview)
left_frame.grid_rowconfigure(5, minsize=150)

# R Table Frame
table_frame = tk.Frame(display, bg="#DCDCDC")
table_frame.grid(row=1, column=1, columnspan=2, sticky='nsew', padx=5, pady=5)
table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)
vscrollbar = tk.Scrollbar(table_frame, orient="vertical")
vscrollbar.grid(row=0, column=1, sticky='ns')
hscrollbar = tk.Scrollbar(table_frame, orient="horizontal")
hscrollbar.grid(row=1, column=0, sticky='ew')
displaytable = ttk.Treeview(table_frame, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
displaytable.grid(row=0, column=0, sticky='nsew')
vscrollbar.config(command=displaytable.yview)
hscrollbar.config(command=displaytable.xview)
display.grid_columnconfigure(1, weight=2)
display.grid_columnconfigure(2, weight=3)
display.grid_rowconfigure(1, weight=1)
table_frame.grid_propagate(False)
# Footer Frame
footer_frame = tk.Frame(display, bg="#FFFAFA")
footer_frame.grid(row=2, column=0, columnspan=columns_display, sticky='nsew', padx=2, pady=0)
# เพิ่มปุ่ม Add Customer ใน footer_frame
add_customer_button = ttk.Button(footer_frame, text="Add Customer", command=createcustomerwindows)
add_customer_button.pack(side='left', padx=10, pady=10)

merge_button = ttk.Button(footer_frame, text="Merge picture", command=run_merge_gui)
merge_button.pack(side='left', padx=10, pady=10)
# เรียกใช้งาน main_login ในพื้นหลัง
threading.Thread(target=lambda: main_call_login.main_login(display, user_text), daemon=True).start()
# แสดงหน้าต่างหลัก

display.mainloop()

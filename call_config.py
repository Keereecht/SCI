import os
import data_storage
import pandas as pd
from call_data_base import readapikey
from call_data_base_cad import readapikey_cad
import tkinter as tk
filepath = 'Config/Config.text'
config_lines = None  # ใช้ตัวแปรเก็บค่าที่อ่านแล้ว
readapikey()
readapikey_cad()
# ฟังก์ชันในการอ่านไฟล์ config เพียงครั้งเดียว
def read_config_file(filepath):
    global config_lines
    if config_lines is None:
        if not os.path.exists(filepath):
            print(f"Error: File '{filepath}' not found.")
            return []
        with open(filepath, 'r', encoding='utf-8') as file:
            config_lines = file.readlines()
    return config_lines

# ฟังก์ชันในการอ่าน version update จาก config
def read_version_update(lines):
    if not hasattr(data_storage, 'versions') or not data_storage.versions:
        versions = ""
        for line in lines:
            if line.startswith('Version'):
                ver = line.split(',')[1].strip()
                versions += ver + "\n"
        data_storage.versions = versions.strip()
    print(data_storage.versions)
    return data_storage.versions

# ฟังก์ชันในการอ่าน main folder
def read_name_main_folder(lines):
    if not hasattr(data_storage, 'Main_folder') or not data_storage.Main_folder:
        for line in lines:
            if line.startswith('Outpath'):
                Main_folder = line.split(',')[1].strip()
                data_storage.Main_folder = Main_folder
                print(Main_folder)
    return data_storage.Main_folder

def read_name_main_folder_cad(lines):
    if not hasattr(data_storage, 'Main_folder_cad') or not data_storage.Main_folder_cad:
        for line in lines:
            if line.startswith('Outcad'):
                Main_folder_cad = line.split(',')[1].strip()
                data_storage.Main_folder_cad = Main_folder_cad
                print("cadmain",Main_folder_cad)
    return data_storage.Main_folder_cad   

def read_name_worksheet(lines):
    if not hasattr(data_storage, 'worksheet') or not data_storage.worksheet:
        for line in lines:
            if line.startswith('worksheet'):
                worksheet = line.split(',')[1].strip()  # Define 'worksheet'
                data_storage.worksheet = worksheet     # Assign the value to data_storage
                print(worksheet)  # Optional debug print statement
                return data_storage.worksheet  # Return the value

# ฟังก์ชันในการสร้างไฟล์ CSV ถ้ายังไม่มี
def create_empty_database_csv():
    main_folder = data_storage.Main_folder
    output_folder = os.path.join(main_folder, "outputdatabase")
    os.makedirs(output_folder, exist_ok=True)
    csv_file = os.path.join(output_folder, "database.csv")
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=["Project_id", "Customer", "Pn_project", "Bom_file_name", "Pdf_file", "Page", "Output", "BOM_Target", "PDF_Actual", "Not_found", "Percent", "Time(sec)", "Who", "Date", "Filepath"])
        df.to_csv(csv_file, index=False)
        print(f"สร้างไฟล์ database.csv เปล่าในโฟลเดอร์ {output_folder} เรียบร้อยแล้ว\n")
    else:
        print(f"ไฟล์ database.csv มีอยู่แล้วในโฟลเดอร์ {output_folder}\n")

def create_empty_Customer():
    main_folder = data_storage.Main_folder
    output_folder = os.path.join(main_folder, "customer_config")
    os.makedirs(output_folder, exist_ok=True)
    csv_file = os.path.join(output_folder, "Customer.csv")
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=["Customer_name"])
        df.to_csv(csv_file, index=False)
        print(f"สร้างไฟล์ database.csv เปล่าในโฟลเดอร์ {output_folder} เรียบร้อยแล้ว\n")
    else:
        print(f"ไฟล์ database.csv มีอยู่แล้วในโฟลเดอร์ {output_folder}\n")

def read_config():
    # ตรวจสอบว่า config_lines ถูกอ่านและมีข้อมูลหรือไม่
    if not config_lines:
        print("Error: Config file has not been read yet or is empty.")
        return {}

    credentials = {}
    current_user = None
    for line in config_lines:
        if line.strip() == '' or '---' in line:
            continue
        parts = line.strip().split(',', 1)
        if len(parts) == 2:
            key, value = parts
            key = key.strip().lower()
            if key == 'user':
                current_user = value.strip()
                credentials[current_user] = ''
            elif key == 'pass' and current_user:
                credentials[current_user] = value.strip()
    data_storage.credentials = credentials
    print(credentials)
    return credentials

def read_combinefile(config_lines):
    if not hasattr(data_storage, 'combinefile') or not data_storage.combinefile:
        for line in config_lines:
            if line.startswith('combinefile'):
                combinefile_value = line.split('=')[1].strip()
                data_storage.combinefile_value = combinefile_value
                print(f"combinefile: {combinefile_value}")  # Debug print
                
# เรียกใช้ฟังก์ชันเพียงครั้งเดียว
config_lines = read_config_file(filepath)
if config_lines:  # ตรวจสอบว่ามีการอ่านไฟล์ได้สำเร็จหรือไม่
    versions = read_version_update(config_lines)
    main_outpath = read_name_main_folder(config_lines)
    main_outpath_cad = read_name_main_folder_cad(config_lines)
    read_combinefile(config_lines)
    worksheet = read_name_worksheet(config_lines)
    credentials = read_config() 
    create_empty_database_csv()
    create_empty_Customer()
else:
    print("Error: Unable to read config file. Please check the file path or content.")

import os
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from tkinter import messagebox
import data_storage

def readapikey():
    """ อ่านค่า database_value และ filesheet จากไฟล์ Config.text """
    global database_value, filesheet
    with open('Config/Config.text', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    database_value, filesheet = None, None
    for line in lines:
        line = line.strip()
        if line.startswith('database'):
            database_value = line.split(',')[1].strip('"')
        elif line.startswith('filesheetname'):
            filesheet = line.split(',')[1].strip('"')

def load_csv_data():
    """ โหลดข้อมูลจาก Customer.csv เข้า data_storage """
    global csv_file_path
    csv_file_path = os.path.join(data_storage.Main_folder, "customer_config", "Customer.csv")

    if not os.path.exists(csv_file_path):
        messagebox.showerror("Error", f"ไม่พบไฟล์ CSV: {csv_file_path}")
        return

    try:
        if 'customer_data' not in data_storage.__dict__:
            data_storage.customer_data = pd.read_csv(csv_file_path)
    except pd.errors.EmptyDataError:
        messagebox.showerror("Error", "CSV file is empty!")
    except pd.errors.ParserError:
        messagebox.showerror("Error", "CSV file format is incorrect!")

def get_listemail_data():
    """ ดึงข้อมูลจากคอลัมน์ A ของชีต 'listemail' ใน Google Sheets """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(database_value, scopes=scope)
    client = gspread.authorize(creds)

    try:
        sheet = client.open(filesheet).worksheet("listemail")
        return sheet.col_values(1)[1:]  # ตัด Header ออก
    except gspread.exceptions.WorksheetNotFound:
        print("❌ ไม่พบชีต 'listemail'")
        return []

# def sync_customer_with_listemail():
#     """ เช็คข้อมูล Customer.csv กับ listemail และเพิ่มข้อมูลที่ขาดหาย """
#     readapikey()  # โหลดค่า database_value และ filesheet
#     load_csv_data()  # โหลดข้อมูล CSV

#     if not hasattr(data_storage, 'customer_data'):
#         messagebox.showerror("Error", "ไม่สามารถโหลดข้อมูลจาก CSV ได้!")
#         return

#     csv_customers = data_storage.customer_data['Customer_name'].dropna().astype(str).tolist()
#     listemail_customers = get_listemail_data()

#     # เปลี่ยนเป็นตัวพิมพ์เล็กทั้งหมดเพื่อให้เปรียบเทียบได้ง่าย
#     csv_customers_lower = {name.lower(): name for name in csv_customers}
#     listemail_customers_lower = {name.lower() for name in listemail_customers}

#     # หา Customer ที่อยู่ใน CSV แต่ไม่มีใน listemail และไม่ใช่ "TEST_PRODUCT"
#     missing_customers = [
#         csv_customers_lower[name] for name in csv_customers_lower
#         if name not in listemail_customers_lower and name.lower() != "test_product"
#     ]

#     if missing_customers:
#         print("🔄 กำลังเพิ่มรายชื่อลูกค้าที่ขาดหายลงใน listemail...")
#         scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#         creds = Credentials.from_service_account_file(database_value, scopes=scope)
#         client = gspread.authorize(creds)

#         sheet = client.open(filesheet).worksheet("listemail")
#         for name in missing_customers:
#             sheet.append_row([name])
#             print(f"✅ เพิ่ม '{name}' ลงใน listemail")

#         messagebox.showinfo("สำเร็จ", f"เพิ่ม {len(missing_customers)} ชื่อลูกค้าใหม่ลงใน listemail แล้ว!")
#     else:
#         messagebox.showinfo("สำเร็จ", "✅ ข้อมูลตรงกันแล้ว ไม่ต้องอัปเดต")
def sync_customer_with_listemail():
    """ เช็คข้อมูล Customer.csv กับ listemail และเพิ่มข้อมูลที่ขาดหาย """
    readapikey()  # โหลดค่า database_value และ filesheet
    load_csv_data()  # โหลดข้อมูล CSV

    if not hasattr(data_storage, 'customer_data'):
        messagebox.showerror("Error", "ไม่สามารถโหลดข้อมูลจาก CSV ได้!")
        return

    csv_customers = data_storage.customer_data['Customer_name'].dropna().astype(str).tolist()
    listemail_customers = get_listemail_data()

    # เปลี่ยนเป็นตัวพิมพ์เล็กทั้งหมดเพื่อให้เปรียบเทียบได้ง่าย
    csv_customers_lower = {name.lower(): name for name in csv_customers}
    listemail_customers_lower = {name.lower() for name in listemail_customers}

    # หา Customer ที่อยู่ใน CSV แต่ไม่มีใน listemail และไม่ใช่ "TEST_PRODUCT"
    missing_customers = [
        csv_customers_lower[name] for name in csv_customers_lower
        if name not in listemail_customers_lower and name.lower() != "test_product"
    ]

    # รายชื่ออีเมลที่ต้องใส่ในคอลัมน์ B
    email_list = "Anusit.B@sanmina.com, putamongkol@gmail.com, keereechlit@gmail.com, netsara.w@sanmina.com, nichaya.th@sanmina.com, sawanee.s@sanmina.com, tassanee.j@sanmina.com, wijit.s@sanmina.com"
    if missing_customers:
        print("🔄 กำลังเพิ่มรายชื่อลูกค้าที่ขาดหายลงใน listemail...")
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(database_value, scopes=scope)
        client = gspread.authorize(creds)

        sheet = client.open(filesheet).worksheet("listemail")
        for name in missing_customers:
            sheet.append_row([name, email_list])  # เพิ่มชื่อในคอลัมน์ A และอีเมลในคอลัมน์ B
            print(f"✅ เพิ่ม '{name}' และอีเมลลงใน listemail")

# 🔹 เรียกใช้ฟังก์ชันหลัก
# sync_customer_with_listemail()


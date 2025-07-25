import os
import gspread
from google.oauth2.service_account import Credentials
import data_storage

def readapikey():
    global database_value
    global filesheet
    # เปิดไฟล์ Config.Config.text เพื่ออ่านข้อมูล
    with open('Config/Config.text', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # สร้างตัวแปรเพื่อเก็บค่าของ 'database'
    database_value = None
    filesheet = None
    # วนลูปตรวจสอบแต่ละบรรทัดในไฟล์
    for line in lines:
        # ลบช่องว่างหรือช่องว่างพิเศษออกจากบรรทัด
        line = line.strip()
        # ตรวจสอบว่า 'database' อยู่ในบรรทัดหรือไม่
        if line.startswith('database'):
            # แยกค่าด้วยเครื่องหมายจุลภาค
            key, value = line.split(',')
            # เก็บค่าในตัวแปร database_value
            database_value = value.strip('"')  # ลบเครื่องหมายคำพูดหากมี
        if line.startswith('filesheetname'):
            # แยกค่าด้วยเครื่องหมายจุลภาค
            key, value = line.split(',')
            # เก็บค่าในตัวแปร filesheet
            filesheet = value.strip('"')  # ลบเครื่องหมายคำพูดหากมี

def update_sheet_headers(sheet):
    # สร้างหัวเรื่องที่ต้องการ
    headers = ["Project_id", "Customer", "Pn_project", "Bom_file_name", "Pdf_file", "Page", "Output", 
               "BOM_Target", "PDF_Atcual", "Not_found", "Percent", "Time(sec)", "Who", "Date", "Filepath"]
    
    # ตรวจสอบว่าแถวแรกมีข้อมูลหัวเรื่องหรือยัง
    existing_headers = sheet.row_values(1)
    
    # ตรวจสอบว่าหัวเรื่องตรงกับที่เราต้องการหรือไม่
    if existing_headers == headers:
        print("หัวเรื่องมีอยู่แล้ว ไม่จำเป็นต้องสร้างใหม่")
    else:
        # อัปเดตหัวเรื่องใหม่ถ้าไม่ตรงกัน
        header_range = f"A1:{chr(64 + len(headers))}1"
        sheet.update(header_range, [headers])
        print("สร้างหรืออัปเดตหัวเรื่องเรียบร้อยแล้ว")

def data_base_sheet():
    # กำหนด scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # โหลด Service Account Credentials จากไฟล์ JSON
    creds = Credentials.from_service_account_file(database_value, scopes=scope)
    client = gspread.authorize(creds)
    
    # เปิด Google Sheets โดยใช้ชื่อหรือ URL ของสเปรดชีต
    sheet = client.open(filesheet).worksheet(data_storage.worksheet)
    update_sheet_headers(sheet)

    # ตรวจสอบแถวสุดท้ายที่มีข้อมูลในคอลัมน์ 'project_id'
    col_values = sheet.col_values(1)  # คอลัมน์ A คือคอลัมน์ที่ 1

    # คำนวณค่า project_id ถัดไป
    if len(col_values) == 1:  # ถ้ามีแค่หัวเรื่อง
        next_project_id = 1
    else:
        last_project_id = int(col_values[-1])
        next_project_id = last_project_id + 1
    # กำหนดค่าเริ่มต้นสำหรับค่าที่อาจเป็น None
    pdfname = data_storage.pdfname if data_storage.pdfname else ""
    pdf_top_filename = data_storage.pdf_top_filename if data_storage.pdf_top_filename else ""
    pdf_bot_filename = data_storage.pdf_bot_filename if data_storage.pdf_bot_filename else ""
    outpathdata = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname)
    percent_handload = (
        int((int(data_storage.sum_find_hltop + data_storage.sum_find_hlbot) / int(data_storage.sum_qty_hltop)) * 100)
        if data_storage.sum_qty_hltop != 0 else 0
    )

    # เพิ่ม project_id และ customer ในแถวถัดไป
    if not data_storage.iccall_value:
        customer_values = [
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_top_filename, data_storage.page_top +1, data_storage.projectname + "_TOP_SMT", int(data_storage.sum_qty_top), int(data_storage.sum_find_top), data_storage.Not_found_top, int(data_storage.percent_top_smt), data_storage.time_top, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_top_filename, data_storage.page_top +1, data_storage.projectname + "_TOP_IC", int(data_storage.sum_qty_top_ic), int(data_storage.sum_find_top_ic), data_storage.Not_found_top_ic, int(data_storage.percent_top_ic), data_storage.time_top, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_bot_filename, data_storage.page_bot +1, data_storage.projectname + "_BOT_SMT",int(data_storage.sum_qty_bot), int(data_storage.sum_find_bot), data_storage.Not_found_bot, int(data_storage.percent_bot_smt), data_storage.time_bot, data_storage.logged_in_user, data_storage.date_time,outpathdata],  
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_bot_filename, data_storage.page_bot +1, data_storage.projectname + "_BOT_IC", int(data_storage.sum_qty_bot_ic), int(data_storage.sum_find_bot_ic), data_storage.Not_found_bot_ic, int(data_storage.percent_bot_ic), data_storage.time_bot, data_storage.logged_in_user, data_storage.date_time,outpathdata],

            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_top_filename,"-", data_storage.projectname + "_Handload",int(data_storage.sum_qty_hltop), int(data_storage.sum_find_hltop + data_storage.sum_find_hlbot),int(data_storage.sum_qty_hltop) - int(data_storage.sum_find_hltop + data_storage.sum_find_hlbot), percent_handload, data_storage.time_hl_top + data_storage.time_hl_bot, data_storage.logged_in_user, data_storage.date_time,outpathdata],

            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_top_filename, data_storage.page_top +1, data_storage.projectname + "***TOP_Handload",int(data_storage.sum_qty_hltop), int(data_storage.sum_find_hltop), data_storage.Not_found_hltop, int(data_storage.percent_top_hltop), data_storage.time_hl_top, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_bot_filename, data_storage.page_bot +1, data_storage.projectname + "***BOT_Handload",int(data_storage.sum_qty_hlbot), int(data_storage.sum_find_hlbot), data_storage.Not_found_hlbot, int(data_storage.percent_bot_hlbot), data_storage.time_hl_bot, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_top_filename, data_storage.page_top +1, data_storage.projectname + "_TOP_Noload",int(data_storage.total_count_top),int(data_storage.total_count_top), 0, 100, data_storage.time_no_top, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_bot_filename, data_storage.page_bot +1, data_storage.projectname + "_BOT_Noload",int(data_storage.total_count_bot),int(data_storage.total_count_bot), 0, 100, data_storage.time_no_bot, data_storage.logged_in_user, data_storage.date_time,outpathdata]
        ]
    else:
        customer_values = [
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_top_filename, data_storage.page_top +1,data_storage.projectname + "_TOP_SMT", int(data_storage.sum_qty_top), int(data_storage.sum_find_top), data_storage.Not_found_top, int(data_storage.percent_top_smt), data_storage.time_top, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_bot_filename, data_storage.page_bot +1,data_storage.projectname + "_BOT_SMT",int(data_storage.sum_qty_bot), int(data_storage.sum_find_bot), data_storage.Not_found_bot, int(data_storage.percent_bot_smt), data_storage.time_bot, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_top_filename,"-", data_storage.projectname + "_Handload",int(data_storage.sum_qty_hltop), int(data_storage.sum_find_hltop + data_storage.sum_find_hlbot),int(data_storage.sum_qty_hltop) - int(data_storage.sum_find_hltop + data_storage.sum_find_hlbot), int((int(data_storage.sum_find_hltop + data_storage.sum_find_hlbot)/int(data_storage.sum_qty_hltop))*100), data_storage.time_hl_top + data_storage.time_hl_bot, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_top_filename, data_storage.page_top +1,data_storage.projectname + "***TOP_Handload",int(data_storage.sum_qty_hltop), int(data_storage.sum_find_hltop), data_storage.Not_found_hltop, int(data_storage.percent_top_hltop), data_storage.time_hl_top, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_bot_filename, data_storage.page_bot +1,data_storage.projectname + "***BOT_Handload",int(data_storage.sum_qty_hlbot), int(data_storage.sum_find_hlbot), data_storage.Not_found_hlbot, int(data_storage.percent_bot_hlbot), data_storage.time_hl_bot, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_top_filename, data_storage.page_top +1,data_storage.projectname + "***TOP_Noload",int(data_storage.total_count_top),int(data_storage.total_count_top), 0, 100, data_storage.time_no_top, data_storage.logged_in_user, data_storage.date_time,outpathdata],
            [next_project_id, data_storage.selected_customer, data_storage.projectname, data_storage.filenamecsv, pdfname + pdf_bot_filename, data_storage.page_bot +1,data_storage.projectname + "***BOT_Noload",int(data_storage.total_count_bot),int(data_storage.total_count_bot), 0, 100, data_storage.time_no_bot, data_storage.logged_in_user, data_storage.date_time,outpathdata]
        ]
    last_row = len(col_values) + 1
    # ปรับช่วงการอัปเดตให้สอดคล้องกับจำนวนแถวของข้อมูล
    sheet.update(f'A{last_row}:O{last_row + len(customer_values) - 1}', customer_values)
    increment_countemail(client)

def increment_countemail(client):
    try:
        # เปิด worksheet ที่ชื่อว่า "countemail"
        count_sheet = client.open(filesheet).worksheet("countemail")

        # อ่านค่าปัจจุบันจากเซลล์ A1 (หรือเซลล์อื่นที่ใช้เก็บค่า count)
        current_count = count_sheet.acell("A2").value

        # ถ้าค่าปัจจุบันเป็น None หรือว่าง ให้เริ่มจาก 0
        if current_count is None or current_count == "":
            new_count = 1
        else:
            new_count = int(current_count) + 1  # บวกค่า +1
        count_sheet.update("A2", [[new_count]])

        print(f"ค่า countemail ถูกเพิ่มเป็น {new_count}")
    
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอัปเดต countemail: {e}")

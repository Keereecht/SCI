import data_storage
import os

def process_and_combine_files_for_project():
    # ตรวจสอบค่า combinefile_value และพิมพ์ออกมาเพื่อตรวจสอบ
    print(f"🔍 Debug: data_storage.combinefile_value = {repr(data_storage.combinefile_value)}")

    # ใช้ strip() และ lower() เพื่อลดปัญหา case-sensitive และช่องว่างที่อาจเกิดขึ้น
    combinefile_mode = data_storage.combinefile_value.strip().lower()

    if combinefile_mode == "long":
        print("✅ Processing LONG format")
        suffix = f"{data_storage.projectname}_TOP"
        bot_suffix = f"{data_storage.projectname}_BOT"
    elif combinefile_mode == "short":
        print("✅ Processing SHORT format")
        suffix = "TOP"
        bot_suffix = "BOT"
    else:
        print(f"❌ Error: Unknown value in data_storage.combinefile_value -> {repr(data_storage.combinefile_value)}")
        return

    # สร้าง file paths โดยเพิ่มชื่อโปรเจคในไฟล์
    file_types = ["CAPA", "IC", "OTHER", "RES", "HL"]
    
    top_files = {ftype: os.path.join(data_storage.Main_folder_cad, data_storage.selected_customer,
                                     data_storage.projectname, f"{suffix}_{ftype}.cad") for ftype in file_types}

    bot_files = {ftype: os.path.join(data_storage.Main_folder_cad, data_storage.selected_customer,
                                     data_storage.projectname, f"{bot_suffix}_{ftype}.cad") for ftype in file_types}

    # รวมไฟล์ทั้งหมดเข้าด้วยกัน
    file_pairs = [(f"cadprocess/top_{ftype.lower()}.cad", top_files[ftype]) for ftype in file_types] + \
                 [(f"cadprocess/bot_{ftype.lower()}.cad", bot_files[ftype]) for ftype in file_types]

    # เรียกใช้ฟังก์ชัน process_and_combine_files
    for source, destination in file_pairs:
        process_and_combine_files(data_storage.cadfile, source, destination)


def process_and_combine_files(input_file1, input_file2, output_file):
    # ตรวจสอบว่าไฟล์ที่ต้องอ่านมีอยู่จริงหรือไม่
    if not os.path.exists(input_file1):
        print(f"❌ Error: {input_file1} does not exist.")
        return
    if not os.path.exists(input_file2):
        print(f"❌ Error: {input_file2} does not exist.")
        return

    capturing = False
    capturing_2 = False
    capturing_3 = False
    header_lines_top = []
    header_lines_com = []
    header_lines_bot = []

    # เปิดไฟล์แรกและอ่านข้อมูล
    with open(input_file1, "r") as f:
        for line in f:
            if line.startswith("$HEADER"):
                capturing = True  
            if capturing:
                header_lines_top.append(line)
            if line.startswith("$ENDSHAPES"):
                capturing = False
                header_lines_top.append("\n") 

            if line.startswith("$COMPONENTS"):
                capturing_2 = True  
            if capturing_2:
                header_lines_com.append(line)
            if line.startswith("$ENDCOMPONENTS"):
                capturing_2 = False
                header_lines_com.append("\n")

            if line.startswith("$DEVICES"):
                capturing_3 = True  
            if capturing_3:
                header_lines_bot.append(line)

    # เปิดไฟล์ที่สองและอ่านข้อมูลทั้งหมด
    with open(input_file2, "r") as g:
        filtered_lines = g.readlines()

    # รวมข้อมูลจากไฟล์ทั้งสอง
    combined_lines = header_lines_top + filtered_lines + header_lines_bot

    # เขียนข้อมูลที่รวมแล้วลงในไฟล์ผลลัพธ์
    with open(output_file, "w") as output_file_m:
        output_file_m.writelines(combined_lines)

    print(f"✅ Successfully created {output_file}")

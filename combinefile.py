import data_storage
import os

def process_and_combine_files_for_project():
    # Construct file paths
    topcapause = os.path.join(
        data_storage.Main_folder_cad ,
        data_storage.selected_customer,
        data_storage.projectname,
        data_storage.projectname + '_TOP_CAPA.cad'
    )

    topicuse = os.path.join(
        data_storage.Main_folder_cad,
        data_storage.selected_customer,
        data_storage.projectname,
        data_storage.projectname + '_TOP_IC.cad'
    )

    topotheruse = os.path.join(
        data_storage.Main_folder_cad,
        data_storage.selected_customer,
        data_storage.projectname,
        data_storage.projectname + '_TOP_OTHER.cad'
    )

    topresuse = os.path.join(
        data_storage.Main_folder_cad,
        data_storage.selected_customer,
        data_storage.projectname,
        data_storage.projectname + '_TOP_RES.cad'
    )

    tophluse = os.path.join(
        data_storage.Main_folder_cad,
        data_storage.selected_customer,
        data_storage.projectname,
        data_storage.projectname + '_TOP_HL.cad'
    )
    # Buttom-----
    botcapause = os.path.join(
        data_storage.Main_folder_cad,
        data_storage.selected_customer,
        data_storage.projectname,
        data_storage.projectname + '_BOT_CAPA.cad'
    )

    boticuse = os.path.join(
        data_storage.Main_folder_cad,
        data_storage.selected_customer,
        data_storage.projectname,
        data_storage.projectname + '_BOT_IC.cad'
    )

    bototheruse = os.path.join(
        data_storage.Main_folder_cad,
        data_storage.selected_customer,
        data_storage.projectname,
        data_storage.projectname + '_BOT_OTHER.cad'
    )

    botresuse = os.path.join(
        data_storage.Main_folder_cad,
        data_storage.selected_customer,
        data_storage.projectname,
        data_storage.projectname + '_BOT_RES.cad'
    )

    bothluse = os.path.join(
        data_storage.Main_folder_cad,
        data_storage.selected_customer,
        data_storage.projectname,
        data_storage.projectname + '_BOT_HL.cad'
    )

    # Define the file pairs (source, destination)
    file_pairs = [
        ("cadprocess/top_capa.cad", topcapause),
        ("cadprocess/top_ic.cad", topicuse),
        ("cadprocess/top_other.cad", topotheruse),
        ("cadprocess/top_res.cad", topresuse),
        ("cadprocess/top_hl.cad", tophluse),
        ("cadprocess/bot_capa.cad", botcapause),
        ("cadprocess/bot_ic.cad", boticuse),
        ("cadprocess/bot_other.cad", bototheruse),
        ("cadprocess/bot_res.cad", botresuse),
        ("cadprocess/bot_hl.cad", bothluse),
    ]

    # Process and combine files
    for source, destination in file_pairs:
        process_and_combine_files(data_storage.cadfile, source, destination)

def process_and_combine_files(input_file1, input_file2, output_file):

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


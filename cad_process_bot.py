import data_storage
import pandas as pd
import tkinter as tk
import os

def components_capabot(input_file_path, output_file_path, components_to_keep):
    print("t1")
    with open(input_file_path, "r") as f:
        lines = f.readlines()
    keep = False
    filtered_lines = []
    in_component_section = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "$COMPONENTS":
            in_component_section = True
            filtered_lines.append(line)
        elif stripped_line == "$ENDCOMPONENTS":
            in_component_section = False
            # Do not append $ENDCOMPONENTS here to avoid duplicates
        elif in_component_section and line.startswith("COMPONENT"):
            component_name = line.split()[1]
            # print(component_name,"-------------")
            keep = component_name in components_to_keep
        if not in_component_section or keep:
            filtered_lines.append(line)
    # Ensure $ENDCOMPONENTS is at the end if it was present in the original file
    if "$ENDCOMPONENTS" in lines:
        filtered_lines.append("$ENDCOMPONENTS\n")
        print(filtered_lines)
    # Write the filtered lines to a new file
    with open(output_file_path, "w") as f:
        f.writelines(filtered_lines)

        print("Filtering complete. Filtered components written to:", output_file_path)
        return(filtered_lines)
 
def components_resbot(input_file_path, output_file_path, components_to_keep):
    print("t2")
    with open(input_file_path, "r") as f:
        lines = f.readlines()
    keep = False
    filtered_lines = []
    in_component_section = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "$COMPONENTS":
            in_component_section = True
            filtered_lines.append(line)
        elif stripped_line == "$ENDCOMPONENTS":
            in_component_section = False
            # Do not append $ENDCOMPONENTS here to avoid duplicates
        elif in_component_section and line.startswith("COMPONENT"):
            component_name = line.split()[1]
            # print(component_name,"-------------")
            keep = component_name in components_to_keep
        if not in_component_section or keep:
            filtered_lines.append(line)
    # Ensure $ENDCOMPONENTS is at the end if it was present in the original file
    if "$ENDCOMPONENTS" in lines:
        filtered_lines.append("$ENDCOMPONENTS\n")
        print(filtered_lines)
    # Write the filtered lines to a new file
    with open(output_file_path, "w") as f:
        f.writelines(filtered_lines)
        return(filtered_lines)

def components_icbot(input_file_path, output_file_path, components_to_keep):
    print("t3")
    with open(input_file_path, "r") as f:
        lines = f.readlines()
    keep = False
    filtered_lines = []
    in_component_section = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "$COMPONENTS":
            in_component_section = True
            filtered_lines.append(line)
        elif stripped_line == "$ENDCOMPONENTS":
            in_component_section = False
            # Do not append $ENDCOMPONENTS here to avoid duplicates
        elif in_component_section and line.startswith("COMPONENT"):
            component_name = line.split()[1]
            # print(component_name,"-------------")
            keep = component_name in components_to_keep
        if not in_component_section or keep:
            filtered_lines.append(line)
    # Ensure $ENDCOMPONENTS is at the end if it was present in the original file
    if "$ENDCOMPONENTS" in lines:
        filtered_lines.append("$ENDCOMPONENTS\n")
        print(filtered_lines)
    # Write the filtered lines to a new file
    with open(output_file_path, "w") as f:
        f.writelines(filtered_lines)
        return(filtered_lines)

def components_hlbot(input_file_path, output_file_path, components_to_keep):
    print("t4")
    with open(input_file_path, "r") as f:
        lines = f.readlines()
    keep = False
    filtered_lines = []
    in_component_section = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "$COMPONENTS":
            in_component_section = True
            filtered_lines.append(line)
        elif stripped_line == "$ENDCOMPONENTS":
            in_component_section = False
            # Do not append $ENDCOMPONENTS here to avoid duplicates
        elif in_component_section and line.startswith("COMPONENT"):
            component_name = line.split()[1]
            # print(component_name,"-------------")
            keep = component_name in components_to_keep
        if not in_component_section or keep:
            filtered_lines.append(line)
    # Ensure $ENDCOMPONENTS is at the end if it was present in the original file
    if "$ENDCOMPONENTS" in lines:
        filtered_lines.append("$ENDCOMPONENTS\n")
        print(filtered_lines)
    # Write the filtered lines to a new file
    with open(output_file_path, "w") as f:
        f.writelines(filtered_lines)
        return(filtered_lines)

def components_otherbot(input_file_path, output_file_path, components_to_keep):
    print("t5")
    with open(input_file_path, "r") as f:
        lines = f.readlines()
    keep = False
    filtered_lines = []
    in_component_section = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "$COMPONENTS":
            in_component_section = True
            filtered_lines.append(line)
        elif stripped_line == "$ENDCOMPONENTS":
            in_component_section = False
            # Do not append $ENDCOMPONENTS here to avoid duplicates
        elif in_component_section and line.startswith("COMPONENT"):
            component_name = line.split()[1]
            # print(component_name,"-------------")
            keep = component_name in components_to_keep
        if not in_component_section or keep:
            filtered_lines.append(line)
    # Ensure $ENDCOMPONENTS is at the end if it was present in the original file
    if "$ENDCOMPONENTS" in lines:
        filtered_lines.append("$ENDCOMPONENTS\n")
        print(filtered_lines)
    # Write the filtered lines to a new file
    with open(output_file_path, "w") as f:
        f.writelines(filtered_lines)
        return(filtered_lines)
# -----------------------------------------------------------
def saveoutput_capabot():
    print("on")
    # อ่านข้อมูลจากไฟล์ .cad และเก็บ Component
    cad_components = []

    with open("cadprocess/bot.cad", "r") as f:
        for line in f:
            if line.startswith('COMPONENT'):
                parts = line.split()
                component_name = parts[1]
                cad_components.append(component_name)
    actual_counts = []

    # for index, row in data_storage.data_top_CAP.iterrows():
    for index, row in data_storage.data_buttom.iterrows():
        # แยกค่า Ref_Des ออกเป็นชุดข้อมูล
        ref_des_list = set(row['Ref_Des'].split(',')) if pd.notnull(row['Ref_Des']) else set()

        # ค้นหา Component ที่ตรงกัน
        matched_components = {comp for comp in ref_des_list if comp in cad_components}

        # ใส่ค่า Actual_fond(EA)
        actual_fond = ','.join(matched_components) if matched_components else ""
        not_found = ref_des_list - matched_components
        not_found_value = ','.join(not_found) if not_found else ""

        # เก็บค่าที่จะอัปเดตใน DataFrame
        actual_counts.append(len(matched_components))

        data_storage.data_buttom.loc[index, 'Actual_fond(EA)'] = actual_fond
        data_storage.df.loc[index, 'Actual_fond(EA)'] = actual_fond
        data_storage.data_buttom.loc[index, 'Not_found(EA)'] = not_found_value
        data_storage.df.loc[index, 'Not_found(EA)'] = not_found_value

    total_actual_counts_bot = sum(actual_counts)
    data_storage.total_actual_counts_bot = sum(actual_counts)

    print(total_actual_counts_bot,"===bot")
    # อัปเดตคอลัมน์ PDF_Actual(EA) และ Result
    data_storage.data_buttom['PDF_Actual(EA)'] = actual_counts
    data_storage.data_buttom['Result'] = data_storage.data_buttom.apply(
        lambda row: 'accepted' if row['PDF_Actual(EA)'] == row['BOM_Target(EA)'] else 'rejected', axis=1
    )
    botsmt = os.path.join(
    data_storage.Main_folder,
    data_storage.selected_customer,
    data_storage.projectname,
    data_storage.projectname +"_BOT_SMT.csv")
    data_storage.data_buttom.to_csv(botsmt, index=False)
    print("Processing complete.")

def compoundcad():
    print("รวมไฟล์แล้ว")
    # รายชื่อไฟล์ที่ต้องการรวม
    file_list = ["cadprocess/bot_capa.cad", "cadprocess/bot_ic.cad", "cadprocess/bot_res.cad", "cadprocess/bot_other.cad"]
    # ชื่อไฟล์ผลลัพธ์
    output_file = "cadprocess/bot.cad"
    # อ่านและเขียนเนื้อหาจากทุกไฟล์ลงในไฟล์ผลลัพธ์
    with open(output_file, "w", encoding="utf-8") as outfile:
        for file_name in file_list:
            with open(file_name, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())  # เขียนเนื้อหาลงไฟล์

def saveoutput_hlbot():
    global cad_hlbot_as_list
    print("on lh")
    # อ่านข้อมูลจากไฟล์ .cad และเก็บข้อมูลในรูปแบบ 2D array
    cad_components = {"COMPONENTS": [], "LAYERS": []}
    with open("cadprocess/bot_hl.cad", "r") as f:
        for line in f:
            if line.startswith('COMPONENT'):
                parts = line.split()
                component_name = parts[1]
                cad_components["COMPONENTS"].append(component_name)
            elif line.startswith('LAYER'):
                parts = line.split()
                layer_name = parts[1]
                cad_components["LAYERS"].append(layer_name)
    cad_2d_array = [cad_components["COMPONENTS"], cad_components["LAYERS"]]
    # print(cad_2d_array)
    hl = pd.DataFrame({
        "Component": cad_2d_array[0],
        "Layer": cad_2d_array[1]
    })
    filtered_df = hl[hl["Layer"] == "BOTTOM"]
    cad_hlbot = filtered_df["Component"].to_numpy()
    cad_hlbot_as_list = cad_hlbot.tolist()
    # data_storage.cad_hlbot_as_list = cad_hlbot_as_list
    print(cad_hlbot,"-----------Bot-----------")

    actual_counts = []

    # for index, row in data_storage.data_top_CAP.iterrows():
    for index, row in data_storage.data_hl_bot.iterrows():
        # แยกค่า Ref_Des ออกเป็นชุดข้อมูล
        ref_des_list = set(row['Ref_Des'].split(',')) if pd.notnull(row['Ref_Des']) else set()

        # ค้นหา Component ที่ตรงกัน
        matched_components = {comp for comp in ref_des_list if comp in cad_hlbot}
        
    
        # ใส่ค่า Actual_fond(EA)
        actual_fond = ','.join(matched_components) if matched_components else ""
        not_found = ref_des_list - matched_components
        not_found_value = ','.join(not_found) if not_found else ""

        # เก็บค่าที่จะอัปเดตใน DataFrame
        actual_counts.append(len(matched_components))

        data_storage.data_hl_bot.loc[index, 'Actual_fond(EA)'] = actual_fond
        data_storage.df.loc[index, 'Actual_fond(EA)'] = actual_fond
        data_storage.data_hl_bot.loc[index, 'Not_found(EA)'] = not_found_value
        data_storage.df.loc[index, 'Not_found(EA)'] = not_found_value

    # อัปเดตคอลัมน์ PDF_Actual(EA) และ Result
    total_actual_counts_bothl = sum(actual_counts)
    data_storage.total_actual_counts_bothl = sum(actual_counts)
    bothl = os.path.join(
    data_storage.Main_folder,
    data_storage.selected_customer,
    data_storage.projectname,
    data_storage.projectname +"_BOT_HANDLOAD.csv")
    data_storage.data_hl_bot.to_csv(bothl, index=False)

    print(total_actual_counts_bothl,"======bothl")
    data_storage.data_hl_bot['PDF_Actual(EA)'] = actual_counts
    data_storage.data_hl_bot['Result'] = data_storage.data_hl_bot.apply(
        lambda row: 'accepted' if row['PDF_Actual(EA)'] == row['BOM_Target(EA)'] else 'rejected', axis=1
    )
   
    print("Processing complete_bot.")

def components_hlbot_use(input_file_path, output_file_path):
    print(cad_hlbot_as_list)
    with open(input_file_path, "r") as f:
        lines = f.readlines()
    keep = False
    filtered_lines = []
    in_component_section = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "$COMPONENTS":
            in_component_section = True
            filtered_lines.append(line)
        elif stripped_line == "$ENDCOMPONENTS":
            in_component_section = False
            # Do not append $ENDCOMPONENTS here to avoid duplicates
        elif in_component_section and line.startswith("COMPONENT"):
            component_name = line.split()[1]
            # print(component_name,"-------------")
            keep = component_name in cad_hlbot_as_list
        if not in_component_section or keep:
            filtered_lines.append(line)
    # Ensure $ENDCOMPONENTS is at the end if it was present in the original file
    if "$ENDCOMPONENTS" in lines:
        filtered_lines.append("$ENDCOMPONENTS\n")
        print(filtered_lines)
    # Write the filtered lines to a new file
    with open(output_file_path, "w") as f:
        f.writelines(filtered_lines)
        return(filtered_lines)


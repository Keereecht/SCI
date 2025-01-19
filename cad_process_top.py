import data_storage
import pandas as pd
import tkinter as tk
import os

def components_capatop(input_file_path, output_file_path, components_to_keep):
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
 
def components_restop(input_file_path, output_file_path, components_to_keep):
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

def components_ictop(input_file_path, output_file_path, components_to_keep):
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

def components_hltop(input_file_path, output_file_path, components_to_keep):
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

def components_othertop(input_file_path, output_file_path, components_to_keep):
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
def saveoutput_capatop():
    print("on")
    # ใช้ตัวเลขสำหรับนับอย่างเดียว
    cad_components = []
    # อ่านไฟล์ .cad และเก็บข้อมูล
    with open("cadprocess/top.cad", "r") as f:
        for line in f:
            if line.startswith('COMPONENT'):
                parts = line.split()
                component_name = parts[1]
                cad_components.append(component_name)
    actual_counts = []
    # for index, row in data_storage.data_top_CAP.iterrows():
    for index, row in data_storage.data_top.iterrows():
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

        data_storage.data_top.loc[index, 'Actual_fond(EA)'] = actual_fond
        data_storage.df.loc[index, 'Actual_fond(EA)'] = actual_fond
        data_storage.data_top.loc[index, 'Not_found(EA)'] = not_found_value
        data_storage.df.loc[index, 'Not_found(EA)'] = not_found_value

    # อัปเดตคอลัมน์ PDF_Actual(EA) และ Result
    total_actual_counts_top = sum(actual_counts)
    data_storage.total_actual_counts_top = sum(actual_counts)
    print(total_actual_counts_top,"===top")
    
    data_storage.data_top['PDF_Actual(EA)'] = actual_counts
    data_storage.data_top['Result'] = data_storage.data_top.apply(
        lambda row: 'accepted' if row['PDF_Actual(EA)'] == row['BOM_Target(EA)'] else 'rejected', axis=1
    )
    topsmt = os.path.join(
    data_storage.Main_folder,
    data_storage.selected_customer,
    data_storage.projectname,
    data_storage.projectname +"_TOP_SMT.csv")
    data_storage.data_top.to_csv(topsmt, index=False)
    print("Processing complete----------------------------------.")

def  compoundcad():
    print("รวมไฟล์แล้ว")
    # รายชื่อไฟล์ที่ต้องการรวม
    file_list = ["cadprocess/top_capa.cad", "cadprocess/top_ic.cad", "cadprocess/top_res.cad", "cadprocess/top_other.cad"]
    # ชื่อไฟล์ผลลัพธ์
    output_file = "cadprocess/top.cad"
    # อ่านและเขียนเนื้อหาจากทุกไฟล์ลงในไฟล์ผลลัพธ์
    with open(output_file, "w", encoding="utf-8") as outfile:
        for file_name in file_list:
            with open(file_name, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())  # เขียนเนื้อหาลงไฟล์

def saveoutput_hltop():
    global cad_hltop_as_list
    # อ่านข้อมูลจากไฟล์ .cad และเก็บข้อมูลในรูปแบบ 2D array
    cad_components = {"COMPONENTS": [], "LAYERS": []}
    
    with open("cadprocess/top_hl.cad", "r") as f:
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
    filtered_df = hl[hl["Layer"] == "TOP"]
    cad_hltop = filtered_df["Component"].to_numpy()
    cad_hltop_as_list = cad_hltop.tolist()
    # data_storage.cad_hltop_as_list = cad_hltop_as_list
    # print(cad_hltop_as_list,"---=--")

    actual_counts = []
    # for index, row in data_storage.data_top_CAP.iterrows():
    for index, row in data_storage.data_hl_top.iterrows():
        # แยกค่า Ref_Des ออกเป็นชุดข้อมูล
        ref_des_list = set(row['Ref_Des'].split(',')) if pd.notnull(row['Ref_Des']) else set()

        # ค้นหา Component ที่ตรงกัน
        matched_components = {comp for comp in ref_des_list if comp in cad_hltop}

        # ใส่ค่า Actual_fond(EA)
        actual_fond = ','.join(matched_components) if matched_components else ""
        not_found = ref_des_list - matched_components
        not_found_value = ','.join(not_found) if not_found else ""

        # เก็บค่าที่จะอัปเดตใน DataFrame
        actual_counts.append(len(matched_components))
        data_storage.data_hl_top.loc[index, 'Actual_fond(EA)'] = actual_fond
        data_storage.df.loc[index, 'Actual_fond(EA)'] = actual_fond
        data_storage.data_hl_top.loc[index, 'Not_found(EA)'] = not_found_value
        data_storage.df.loc[index, 'Not_found(EA)'] = not_found_value

    # อัปเดตคอลัมน์ PDF_Actual(EA) และ Result
    total_actual_counts_tophl = sum(actual_counts)
    data_storage.total_actual_counts_tophl = sum(actual_counts)
    print(total_actual_counts_tophl,"====tophl")
    data_storage.data_hl_top['PDF_Actual(EA)'] = actual_counts
    data_storage.data_hl_top['Result'] = data_storage.data_hl_top.apply(
        lambda row: 'accepted' if row['PDF_Actual(EA)'] == row['BOM_Target(EA)'] else 'rejected', axis=1
    )
    tophl = os.path.join(
    data_storage.Main_folder,
    data_storage.selected_customer,
    data_storage.projectname,
    data_storage.projectname +"_TOP_HANDLOAD.csv")
    data_storage.data_hl_top.to_csv(tophl, index=False)
    print("Processing complete.=============")

def components_hltop_use(input_file_path, output_file_path):
    print(cad_hltop_as_list)
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
            keep = component_name in cad_hltop_as_list
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















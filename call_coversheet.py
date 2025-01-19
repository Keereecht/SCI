import csv
import data_storage
import os

def info_over_all():

    info = [
        ["Project_name :" + data_storage.projectname],
        ["file_csv_name :" + data_storage.filenamecsv],
        # ["file_PDF_name :" + data_storage.pdfname],
        ["file_PDF_name :" + (data_storage.pdfname or "") + (data_storage.pdf_top_filename or "") + (data_storage.pdf_bot_filename or "")],
        ["location file", os.path.join(data_storage.Main_folder, data_storage.projectname)],
        ["TOP SIZE", "","Page", "BOM_Target(EA)", "PDF_Actual(EA)","Not_Found(EA)","Percent(%)"],
        [data_storage.projectname + "_TOP_SMT", "",   data_storage.page_top + 1,int(data_storage.sum_qty_top),int(data_storage.sum_find_top), data_storage.Not_found_top, round(data_storage.percent_top_smt, 2)],
        [data_storage.projectname + "_TOP_HANDLOAD", "",   data_storage.page_top + 1,int(data_storage.sum_qty_hltop),int(data_storage.sum_find_hltop),data_storage.Not_found_hltop,round(data_storage.percent_top_hltop, 2)],
        [data_storage.projectname + "_TOP_NOLOAD", "",  data_storage.page_top + 1,int(data_storage.total_count_top),int(data_storage.total_count_top),0,100],
        ["BOT SIZE", "","Page", "BOM_Target(EA)", "PDF_Actual(EA)","Not_Found(EA)","Percent(%)"],
        [data_storage.projectname + "_BOT_SMT", "",  data_storage.page_bot + 1,int(data_storage.sum_qty_bot),int(data_storage.sum_find_bot),data_storage.Not_found_bot,round(data_storage.percent_bot_smt, 2)],
        [data_storage.projectname + "_TOP_HANDLOAD", "",  data_storage.page_bot + 1,int(data_storage.sum_qty_hlbot),int(data_storage.sum_find_hlbot),data_storage.Not_found_hlbot,round(data_storage.percent_bot_hlbot, 2)],
        [data_storage.projectname + "_TOP_NOLOAD", "",  data_storage.page_bot + 1,int(data_storage.total_count_bot),int(data_storage.total_count_bot),0,100],
        ["Time use:",data_storage.all_time]
    ]

    csv_file_path = os.path.join(data_storage.Main_folder,data_storage.selected_customer, data_storage.projectname, data_storage.projectname + '_cover_sheet.csv')
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, mode='w') as file:
        for row in info:
            file.write(','.join(map(str, row)) + '\n')  # writing data row by row
    print(f"CSV file '{csv_file_path}' created successfully!!!")

def info_over_all_ic():
    info = [
        ["Project_name :" + data_storage.projectname],
        ["file_csv_name :" + (data_storage.filenamecsv or "")],
        ["file_PDF_name :" + (data_storage.pdfname or "") + (data_storage.pdf_top_filename or "") + (data_storage.pdf_bot_filename or "")],
        ["location file", os.path.join(data_storage.Main_folder, data_storage.projectname)],
        ["TOP SIZE", "","Page", "BOM_Target(EA)", "PDF_Actual(EA)","Not_Found(EA)","Percent(%)"],
        [data_storage.projectname + "_TOP_SMT", "",   data_storage.page_top + 1,int(data_storage.sum_qty_top),int(data_storage.sum_find_top), data_storage.Not_found_top, round(data_storage.percent_top_smt, 2)],
        [data_storage.projectname + "_TOP_IC", "",   data_storage.page_top + 1,int(data_storage.sum_qty_top_ic),int(data_storage.sum_find_top_ic), data_storage.Not_found_top_ic, round(data_storage.percent_top_ic, 2)],
        [data_storage.projectname + "_TOP_HANDLOAD", "",   data_storage.page_top + 1,int(data_storage.sum_qty_hltop),int(data_storage.sum_find_hltop),data_storage.Not_found_hltop,round(data_storage.percent_top_hltop, 2)],
        [data_storage.projectname + "_TOP_NOLOAD", "",  data_storage.page_top + 1,int(data_storage.total_count_top),int(data_storage.total_count_top),0,100],
        ["BOT SIZE", "","Page", "BOM_Target(EA)", "PDF_Actual(EA)","Not_Found(EA)","Percent(%)"],
        [data_storage.projectname + "_BOT_SMT", "",  data_storage.page_bot + 1,int(data_storage.sum_qty_bot),int(data_storage.sum_find_bot),data_storage.Not_found_bot,round(data_storage.percent_bot_smt, 2)],
        [data_storage.projectname + "_BOT_IC", "",  data_storage.page_bot + 1,int(data_storage.sum_qty_bot_ic),int(data_storage.sum_find_bot_ic),data_storage.Not_found_bot_ic,round(data_storage.percent_bot_ic, 2)],
        [data_storage.projectname + "_TOP_HANDLOAD", "",  data_storage.page_bot + 1,int(data_storage.sum_qty_hlbot),int(data_storage.sum_find_hlbot),data_storage.Not_found_hlbot,round(data_storage.percent_bot_hlbot, 2)],
        [data_storage.projectname + "_TOP_NOLOAD", "",  data_storage.page_bot + 1,int(data_storage.total_count_bot),int(data_storage.total_count_bot),0,100],
        ["Time use:",data_storage.all_time]
    ]
    csv_file_path = os.path.join(data_storage.Main_folder,data_storage.selected_customer, data_storage.projectname, data_storage.projectname + '_cover_sheet.csv')
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    with open(csv_file_path, mode='w') as file:
        for row in info:
            file.write(','.join(map(str, row)) + '\n')  # writing data row by row
    print(f"CSV file '{csv_file_path}' created successfully!!!")

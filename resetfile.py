import data_storage
# def savefile():
#     print(data_storage.pdf_path)
def reset_files():
    data_storage.pdf_path = ""
    data_storage.pdf_top_filename = ""
    data_storage.pdf_bot_filename = ""
    data_storage.cadfile = ""
    data_storage.projectname = None
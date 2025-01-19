import os
import data_storage

def rename_project_folder():
    old_folder_name = os.path.join(data_storage.Main_folder, data_storage.selected_customer, data_storage.projectname)
    new_folder_name = os.path.join(data_storage.Main_folder, data_storage.selected_customer, f"{data_storage.projectname}_CAD")
    # os.rename(old_folder_name, new_folder_name)
    print(f"เปลี่ยนชื่อโฟลเดอร์จาก '{old_folder_name}' เป็น '{new_folder_name}' สำเร็จ")
    try:
        # เปลี่ยนชื่อโฟลเดอร์
        os.rename(old_folder_name, new_folder_name)
        print(f"เปลี่ยนชื่อโฟลเดอร์จาก '{old_folder_name}' เป็น '{new_folder_name}' สำเร็จ")

        # สร้างโฟลเดอร์ 'test' ในโฟลเดอร์ที่เปลี่ยนชื่อแล้ว
        test_folder_path = os.path.join(new_folder_name, "Outputimage")
        os.makedirs(test_folder_path, exist_ok=True)
        print(f"สร้างโฟลเดอร์ 'test' ที่ '{test_folder_path}' สำเร็จ")
    except FileNotFoundError as e:
        print(f"ไม่พบโฟลเดอร์เดิม: {e}")
    except FileExistsError as e:
        print(f"โฟลเดอร์เป้าหมายมีอยู่แล้ว: {e}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")





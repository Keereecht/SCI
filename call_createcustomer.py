import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pandas as pd
import data_storage
import os
import shutil

# ประกาศตัวแปร
mywindow = None
csv_file_path = None

# ฟังก์ชันสำหรับโหลดข้อมูล CSV
def load_csv_data():
    global csv_file_path
    csv_file_path = os.path.join(data_storage.Main_folder, "customer_config", "Customer.csv")
    if not os.path.exists(csv_file_path):
        messagebox.showerror("Error", f"ไม่พบไฟล์ CSV: {csv_file_path}")
        return
    try:
        if 'customer_data' not in data_storage.__dict__:
            data_storage.customer_data = pd.read_csv(csv_file_path)
            print( data_storage.customer_data)
    except pd.errors.EmptyDataError:
        messagebox.showerror("Error", "CSV file is empty!")
    except pd.errors.ParserError:
        messagebox.showerror("Error", "CSV file format is incorrect!")

# ฟังก์ชันสำหรับสร้างโฟลเดอร์จากข้อมูล CSV
def create_folders_from_csv():
    load_csv_data()
    if not hasattr(data_storage, 'customer_data'):
        return
    base_directory = os.path.join(data_storage.Main_folder)
    
    # ตรวจสอบว่าโฟลเดอร์หลักมีอยู่หรือไม่ หากไม่มี ให้สร้างขึ้นมาก่อน
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
    
    for customer_name in data_storage.customer_data['Customer_name']:
        folder_path = os.path.join(base_directory, customer_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"สร้างโฟลเดอร์: {folder_path}")
        else:
            print(f"โฟลเดอร์ {folder_path} มีอยู่แล้ว")

# ฟังก์ชันสำหรับสร้างหน้าต่างแสดงข้อมูล Customer
def createcustomer(display, update_combobox_callback):
    global mywindow, df
    if not hasattr(data_storage, 'customer_data'):
        load_csv_data()
    df = data_storage.customer_data

    if mywindow is not None and mywindow.winfo_exists():
        mywindow.destroy()
    mywindow = tk.Toplevel(display)
    mywindow.title("Customer Data Window")
    mywindow.geometry("400x400")
    screen_width = mywindow.winfo_screenwidth()
    screen_height = mywindow.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (400 / 2))
    y_cordinate = int((screen_height / 2) - (400 / 2))
    mywindow.geometry(f"400x400+{x_cordinate}+{y_cordinate}")
    mywindow.transient(display)
    mywindow.grab_set()

    if not hasattr(data_storage, 'customer_data'):
        label = ttk.Label(mywindow, text="Error: CSV data not loaded!", font=("Arial", 12), foreground="red")
        label.pack(pady=20)
        return

    # สร้าง Treeview สำหรับแสดงข้อมูล
    tree_frame = ttk.Frame(mywindow)
    tree_frame.pack(pady=20, padx=20, fill='both', expand=True)
    tree = ttk.Treeview(tree_frame, columns=['Customer_name'], show='headings')
    tree.heading('Customer_name', text='Customer_name')
    tree.column('Customer_name', width=200)
    for index, row in df.iterrows():
        tree.insert('', 'end', values=[row['Customer_name']])
    tree.pack(pady=20, padx=20, fill='both', expand=True)

    def add_customer_name():
        global df
        new_customer_name = simpledialog.askstring("เพิ่มลูกค้า", "กรุณากรอกชื่อลูกค้า:", parent=mywindow)
        
        # ตรวจสอบว่าผู้ใช้ป้อนข้อมูลหรือไม่
        if not new_customer_name:
            messagebox.showwarning("ข้อผิดพลาด", "กรุณากรอกชื่อลูกค้า!")
            return
        
        # ตรวจสอบห้ามมีช่องว่าง
        if " " in new_customer_name:
            messagebox.showwarning("ข้อผิดพลาด", "ห้ามมีช่องว่างในชื่อลูกค้า!")
            return

        # ตรวจสอบว่าชื่อนี้มีอยู่แล้วหรือไม่ (ไม่สนตัวพิมพ์เล็ก-ใหญ่)
        existing_names = [name.lower() for name in df['Customer_name'].values]
        if new_customer_name.lower() in existing_names:
            messagebox.showwarning("ข้อผิดพลาด", f"ชื่อลูกค้า '{new_customer_name}' มีอยู่แล้ว!")
            return

        # เพิ่มข้อมูลใหม่
        new_data = pd.DataFrame([[new_customer_name]], columns=['Customer_name'])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(csv_file_path, index=False)
        data_storage.customer_data = df
        tree.insert('', 'end', values=[new_customer_name])
        
        # สร้างโฟลเดอร์ใหม่ตาม Customer_name
        folder_path = os.path.join(data_storage.Main_folder, new_customer_name)
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                messagebox.showinfo("สำเร็จ", f"สร้างโฟลเดอร์ '{new_customer_name}' เรียบร้อยแล้ว!")
            else:
                messagebox.showwarning("แจ้งเตือน", f"โฟลเดอร์ '{folder_path}' มีอยู่แล้ว!")
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการสร้างโฟลเดอร์: {str(e)}")
            return

        # อัปเดตค่าใน Combobox
        update_combobox_callback(df['Customer_name'].tolist())



    def delete_customer_name():
        global df
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Error", "Please select a customer to delete.")
            return
        selected_customer_name = tree.item(selected_item, 'values')[0]
        folder_path = os.path.join(data_storage.Main_folder, selected_customer_name)
        if os.path.exists(folder_path):
            if os.listdir(folder_path):
                confirm = messagebox.askyesno("Confirm Delete", f"โฟลเดอร์ '{folder_path}' มีไฟล์หรือโฟลเดอร์ย่อยอยู่ภายใน\nคุณต้องการลบทั้งหมดหรือไม่?")
                if not confirm:
                    messagebox.showinfo("Cancelled", "ยกเลิกการลบโฟลเดอร์")
                    return
                shutil.rmtree(folder_path)
            else:
                os.rmdir(folder_path)
        df = df[df['Customer_name'] != selected_customer_name]
        df.to_csv(csv_file_path, index=False)
        data_storage.customer_data = df
        tree.delete(selected_item)
        update_combobox_callback(df['Customer_name'].tolist())
        messagebox.showinfo("Success", f"ลบ Customer '{selected_customer_name}' และโฟลเดอร์ '{folder_path}' เรียบร้อยแล้ว!")

    button_frame = ttk.Frame(mywindow)
    button_frame.pack(pady=10)
    add_button = ttk.Button(button_frame, text="Add Customer", command=add_customer_name)
    add_button.pack(side='left', padx=10)
    delete_button = ttk.Button(button_frame, text="Delete Customer", command=delete_customer_name)
    delete_button.pack(side='left', padx=10)
    close_button = ttk.Button(button_frame, text="Close", command=mywindow.destroy)
    close_button.pack(side='left', padx=10)

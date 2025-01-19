import data_storage
import tkinter as tk
def use_component_count_top(Textboxfind):
    print("Component Count top:",data_storage.total_actual_counts_top)
    print("Component Count tophl:",data_storage.total_actual_counts_tophl)
    print("Component Count bot:",data_storage.total_actual_counts_bot)
    print("Component Count bot:",data_storage.total_actual_counts_bothl)
    sumall = data_storage.total_actual_counts_top + data_storage.total_actual_counts_tophl + data_storage.total_actual_counts_bot + data_storage.total_actual_counts_bothl
    print("Sum_all",sumall)
    Textboxfind.configure(state="normal")
    Textboxfind.insert(tk.END, sumall)
    Textboxfind.configure(state="disabled")
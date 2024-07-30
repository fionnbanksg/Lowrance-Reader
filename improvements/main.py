
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reader import read_sl, read_bin
import numpy as np
import os
import processData

dataframe = None
primary_np = None
df_primary = None
def open_sl_file():
    global primary_np
    global dataframe
    global df_primary
    file_path = filedialog.askopenfile(filetypes=[("SL files", "*.sl3"), ("SL files", "*.sl2")])
    if file_path:
        print("Selected Filepath", file_path)
        sl_bin_data = read_bin(file_path.name)
        df = read_sl(file_path.name)
        dataframe = df 
        df_primary = df.query("survey_label == 'primary'") 
        primary_list = [
            item for f, p in zip(df_primary["first_byte"], df_primary["frame_size"])
            if (item := np.frombuffer(sl_bin_data[(f+168):(f+(p-168))], dtype="uint8")[:2904]).size == 2904
        ]

 # Check dimensions of each item in primary_list
        for index, item in enumerate(primary_list):
            print(f"Item {index}: shape {item.shape}")
        
       
        primary_np = np.stack(primary_list)

        update_image(primary_np)
        export_menu.entryconfig("Export Sonar Data", state="normal")
        export_menu.entryconfig("Export Other Data", state="normal")
        export_menu.entryconfig("Process Data", state="normal")
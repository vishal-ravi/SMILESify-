import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from rdkit import Chem
from rdkit.Chem import SDMolSupplier
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter import ttk

# Function to extract SMILES from SDF files
def extract_smiles(folder_path):
    smiles_data = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".sdf"):
            file_path = os.path.join(folder_path, file_name)
            supplier = SDMolSupplier(file_path)

            for mol in supplier:
                if mol is not None:
                    smiles = Chem.MolToSmiles(mol)
                    smiles_data.append([file_name, smiles])

    return smiles_data

# Function to handle folder selection
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder_selected)
        load_smiles()

# Function to load SMILES and display in table
def load_smiles():
    folder_path = entry_folder.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder containing SDF files.")
        return

    progress_var.set(0)
    progress_bar.start()

    smiles_data = extract_smiles(folder_path)

    if not smiles_data:
        messagebox.showwarning("No Data", "No valid SMILES found in the selected folder.")
        progress_bar.stop()
        return

    for i in tree.get_children():
        tree.delete(i)

    for idx, (file_name, smiles) in enumerate(smiles_data):
        tree.insert("", "end", values=(idx + 1, file_name, smiles))

    progress_var.set(100)
    progress_bar.stop()
    btn_save.config(state=NORMAL)

# Function to save data as CSV
def save_csv():
    folder_path = entry_folder.get()
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if save_path:
        smiles_data = extract_smiles(folder_path)
        df = pd.DataFrame(smiles_data, columns=["File Name", "SMILES"])
        df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", "SMILES data saved successfully!")

# Function to exit the application
def exit_app():
    root.destroy()

# Create main window
root = tk.Tk()
root.title("ChemSMILE Extractor")
root.geometry("800x600")
style = Style(theme="darkly")

# UI Elements
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=BOTH, expand=True)

title_frame = ttk.Frame(main_frame)
title_frame.pack(fill=X, pady=10)

lbl_title = ttk.Label(title_frame, text="ChemSMILE Extractor", font=("Helvetica", 18, "bold"), foreground="white")
lbl_title.pack(pady=10)

folder_frame = ttk.Frame(main_frame)
folder_frame.pack(fill=X, pady=10)

entry_folder = ttk.Entry(folder_frame, width=50)
entry_folder.pack(side=LEFT, padx=10, pady=10)
btn_browse = ttk.Button(folder_frame, text="Browse Folder", command=browse_folder)
btn_browse.pack(side=LEFT, padx=5)

progress_frame = ttk.Frame(main_frame)
progress_frame.pack(fill=X, pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
progress_bar.pack(fill=X, pady=10)

# Table to display extracted SMILES
tree_frame = ttk.Frame(main_frame)
tree_frame.pack(fill=BOTH, expand=True, pady=20)

tree = ttk.Treeview(tree_frame, columns=("ID", "File Name", "SMILES"), show="headings")
tree.heading("ID", text="ID")
tree.heading("File Name", text="File Name")
tree.heading("SMILES", text="SMILES")
tree.column("ID", width=50)
tree.column("File Name", width=200)
tree.column("SMILES", width=400)
tree.pack(fill=BOTH, expand=True)

# Button Frame
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=X, pady=10)

btn_save = ttk.Button(button_frame, text="Save as CSV", command=save_csv, state=DISABLED)
btn_save.pack(side=LEFT, padx=10)

btn_exit = ttk.Button(button_frame, text="Exit", command=exit_app, bootstyle=(DANGER, OUTLINE))
btn_exit.pack(side=LEFT, padx=10)

root.mainloop()

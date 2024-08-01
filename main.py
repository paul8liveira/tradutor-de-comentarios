import tkinter as tk
from tkinter import Scrollbar, Listbox, messagebox, END
from threading import Thread
    
from helpers import select_files, delete_selected, process_listbox
from resources import get_resource_path

env_path = get_resource_path('.env')

from dotenv import load_dotenv
load_dotenv(env_path)

def on_translate_button_click():
    files = file_listbox.get(0, END)
    if(len(files) == 0):
        messagebox.showerror(title="Erro", message="Selecione ao menos um arquivo para traduzir")
        return
    
    translate_button.config(state=tk.DISABLED)
    loading_label.pack(pady=10)
    
    def task():
        try:
            process_listbox(file_listbox, 'en')
            process_listbox(file_listbox, 'es')
        finally:
            translate_button.config(state=tk.NORMAL)
            file_listbox.delete(0, END)
            loading_label.pack_forget()
            messagebox.showinfo(title="Sucesso", message="Arquivos traduzidos com sucesso! Ambos foram copiados ao mesmo local dos arquivos originais")
    
    thread = Thread(target=task)
    thread.start()

root = tk.Tk() 
root.title("Tradutor de comentários")

select_button = tk.Button(root, text="Selecionar Arquivos", command=lambda: select_files(file_listbox))
select_button.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

file_listbox = Listbox(frame, width=150, height=20, yscrollcommand=scrollbar.set, selectmode=tk.MULTIPLE)
file_listbox.pack(side="left", fill="both")
file_listbox.bind("<Delete>", lambda event: delete_selected(file_listbox, event))

scrollbar.config(command=file_listbox.yview)

loading_label = tk.Label(root, text="Traduzindo...", font=("Arial", 16), fg="blue")

translate_button = tk.Button(root, text="Traduzir Arquivos", command=on_translate_button_click)
translate_button.pack(pady=10)

root.mainloop()
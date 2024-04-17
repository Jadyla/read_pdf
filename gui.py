import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os


class GUI:
    def __init__(self):
        self.config_from_user = None
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)

    def gui(self):
        # GUI config
        self.root.title("Seleção de Arquivos e Diretórios")
        self.frame.pack(padx=50, pady=50)

        # All inputs
        # Select 'plano' to be used
        tk.Label(self.frame, text="Plano: ").grid(row=0, column=0, pady=5, sticky="E")
        entry_file = tk.Entry(self.frame, width=40)
        entry_file.grid(row=0, column=1, pady=5)
        btn_file = tk.Button(self.frame, text="Selecionar...", command=lambda:self.select_file(entry_file))
        btn_file.grid(row=0, column=2, padx=10)

        # Select directory to save FUNASA spreadsheet
        tk.Label(self.frame, text="Diretório planilha FUNASA: ").grid(row=1, column=0, pady=5, sticky="E")
        entry_dict = tk.Entry(self.frame, width=40)
        entry_dict.grid(row=1, column=1, pady=5)
        btn_dict = tk.Button(self.frame, text="Selecionar...", command=lambda:self.select_dict(entry_dict))
        btn_dict.grid(row=1, column=2, padx=10)

        # Input to add more options to search on summary (default: 'keywords_to_search_on_summary')
        lbl_texto = tk.Label(self.frame, text="Personalizar busca (opcional): ")
        lbl_texto.grid(row=2, column=0, pady=10, sticky="E")
        entry_keywords = tk.Entry(self.frame, width=40)
        entry_keywords.grid(row=2, column=1)

        # Input to add more options to search on summary (default: 'keywords_to_search_on_summary')
        lbl_texto = tk.Label(self.frame, text="Ajuste de páginas do sumário (caso necessário):")
        lbl_texto.grid(row=3, column=0, pady=10, sticky="E")
        entry_sum_ajust = tk.Entry(self.frame, width=5, justify=tk.LEFT)
        entry_sum_ajust.grid(row=3, column=1, sticky=tk.W)
        # /All inputs

        # TODO: it will be necssary to think about select dict or to select the sheet path.
        # For now it is defined as the atual directory
        def process_config():
            self.config_from_user = {'pdf_file_name': entry_file.get(),
                                'funasa_dict': os.getcwd(), # entry_dict.get(),
                                'keywords_': entry_keywords.get().split(),
                                'summary_pages_ajustment': entry_sum_ajust.get(),
                            }
            self.root.destroy()

        btn_ok = tk.Button(self.frame, text="OK", command=process_config)
        btn_ok.grid(row=4, column=1, pady=20)

        self.root.mainloop()
        return self.config_from_user
    
    def select_file(self, entry_file):
        filepath = filedialog.askopenfilename(title="Selecione o plano", filetypes=[('PDF files', '*.pdf')])
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filepath)

    def select_dict(self, entry_dict):
        folderpath = filedialog.askdirectory(title="Selecione um diretório para salvar planilha FUNASA")
        entry_dict.delete(0, tk.END)
        entry_dict.insert(0, folderpath)    


def erro_popup(error_message):
    messagebox.showerror(title="Erro", message=error_message)
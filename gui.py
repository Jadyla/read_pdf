import tkinter as tk
from tkinter import filedialog


def gui():
    config_from_user = None
    root = tk.Tk()
    root.title("Seleção de Arquivos e Diretórios")

    # GUI config
    frame = tk.Frame(root)
    frame.pack(padx=50, pady=50)

    def select_file():
        filepath = filedialog.askopenfilename(title="Selecione o plano", filetypes=[('PDF files', '*.pdf')])
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filepath)

    def select_dict():
        folderpath = filedialog.askdirectory(title="Selecione um diretório para salvar planilha FUNASA")
        entry_dict.delete(0, tk.END)
        entry_dict.insert(0, folderpath)

    # All inputs
    # Select 'plano' to be used
    tk.Label(frame, text="Plano: ").grid(row=0, column=0, pady=5, sticky="E")
    entry_file = tk.Entry(frame, width=40)
    entry_file.grid(row=0, column=1, pady=5)
    btn_file = tk.Button(frame, text="Selecionar...", command=select_file)
    btn_file.grid(row=0, column=2, padx=10)

    # Select directory to save FUNASA spreadsheet
    tk.Label(frame, text="Diretório planilha FUNASA: ").grid(row=1, column=0, pady=5, sticky="E")
    entry_dict = tk.Entry(frame, width=40)
    entry_dict.grid(row=1, column=1, pady=5)
    btn_dict = tk.Button(frame, text="Selecionar...", command=select_dict)
    btn_dict.grid(row=1, column=2, padx=10)

    # Input to add more options to search on summary (default: 'keywords_to_search_on_summary')
    lbl_texto = tk.Label(frame, text="Personalizar busca (opcional): ")
    lbl_texto.grid(row=2, column=0, pady=10, sticky="E")
    entry_keywords = tk.Entry(frame, width=40)
    entry_keywords.grid(row=2, column=1)

    # Input to add more options to search on summary (default: 'keywords_to_search_on_summary')
    lbl_texto = tk.Label(frame, text="Ajuste de páginas do sumário (caso necessário):")
    lbl_texto.grid(row=3, column=0, pady=10, sticky="E")
    entry_sum_ajust = tk.Entry(frame, width=5, justify=tk.LEFT)
    entry_sum_ajust.grid(row=3, column=1, sticky=tk.W)
    # /All inputs

    def process_config():
        nonlocal config_from_user
        config_from_user = {'pdf_file_name': entry_file.get(),
                            'funasa_dict': entry_dict.get(),
                            'keywords_': entry_keywords.get().split(),
                            'summary_pages_ajustment': entry_sum_ajust.get(),
                           }
        root.destroy()

    btn_ok = tk.Button(frame, text="OK", command=process_config)
    btn_ok.grid(row=4, column=1, pady=20)

    root.mainloop()
    return config_from_user

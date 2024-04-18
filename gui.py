from utils import open_option, update_option, close_option
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os


models_ia = ('ft:gpt-3.5-turbo-0613:personal:teste-pablo:8xFa0aLd', 
             'gpt-3.5-turbo-1106',
             'gpt-4-turbo',
             'gpt-4-32k',
            )

models_tokens = {'ft:gpt-3.5-turbo-0613:personal:teste-pablo:8xFa0aLd': 4096,
                 'gpt-3.5-turbo-1106': 16385,
                 'gpt-4-turbo': 128000,
                 'gpt-4-1106': 32768,
                }


main_menu = [
    ('Identificar os objetivos do componente', 1),
    ('Identificar o prazo de um objetivo específico', 2),
    ('Identificar o investimento de um objetivo específico', 3),
    ('Identificar as ações de um objetivo específico', 4),
]

components_menu = [
    ('Todos os componentes', 1),
    ('Apenas o componente de abastecimento de água', 2),
    ('Apenas o componente de esgotamento sanitário', 3),
    ('Apenas o componente de manejo das águas pluviais', 4),
    ('Apenas o componente de manejo de resíduos sólidos', 5),
]

fields = [{'id':'plano', 'type': 'file', 'label': 'Plano: ', 'button_label': 'Selecionar...'},
          #{'id':'funasa', 'type': 'dir', 'label': 'Diretório planilha FUNASA: ', 'button_label': 'Selecionar...'},
          {'id':'sum_ajust', 'type': 'input', 'label': 'Ajuste de páginas do sumário (caso necessário): '},
          {'id':'keywords_obj', 'type': 'input', 'label': 'Personalizar busca de objetivos (opcional): '},
          {'id':'keywords_actions', 'type': 'input', 'label': 'Personalizar busca de ações (opcional): '},
          {'id':'year', 'type': 'input', 'label': 'Digite o ano do plano: '},
          {'id':'menu', 'type': 'radio', 'label': 'Escolha uma opção: ', 'op': main_menu, 'col':0 },
          {'id':'components_menu', 'type': 'radio', 'label': 'Escolha uma opção: ', 'op': components_menu, 'col':1 },
          {'id':'model', 'type': 'dropdown', 'label': 'Escolha um modelo de IA: ', 'op': models_ia, 'col':1},
        ]


class GUI:
    def __init__(self):
        self.config_from_user = None
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.entries = []

    def gui(self):
        # GUI config
        self.root.title("Seleção de Arquivos e Diretórios")
        self.frame.pack(padx=50, pady=50)

        # All inputs
        for field in fields:
            self.entries.append(self.config_field(field, fields.index(field)))
        # /All inputs

        tk.Button(self.frame, text="GERAR", command=self.process_config).grid(row=len(fields)+15, columnspan=3, pady=5)
        tk.Button(self.frame, text="VER", command=lambda:self.process_config(event=open_option)).grid(row=len(fields)+16, columnspan=3, pady=5)
        tk.Button(self.frame, text="ATUALIZAR ALTERAÇÂO", command=lambda:self.process_config(event=update_option)).grid(row=len(fields)+17, columnspan=3, pady=5)
        tk.Button(self.frame, text="SAIR", command=lambda:self.process_config(event=close_option)).grid(row=len(fields)+18, columnspan=3, pady=5)

        self.root.mainloop()
        return self.config_from_user
    
    # TODO: it will be necssary to think about select dict or to select the sheet path.
    # For now it is defined as the atual directory
    def process_config(self, event=None):
        if not event:
            #TODO: upgrade how the entry is gotten, not by position, but by id (create a new function to get the entry by id)
            self.config_from_user = {'pdf_file_name': self.entries[0].get(),
                                    'funasa_dict': os.getcwd(), # entry_dict.get(),
                                    'summary_pages_ajustment': self.entries[1].get(),
                                    'keywords_obj': self.entries[2].get().split(),
                                    'keywords_actions': self.entries[3].get().split(),
                                    'year': self.entries[4].get(),
                                    'menu': self.entries[5].get(),
                                    'components_menu': self.entries[6].get(),
                                    'model': self.entries[7].get(),
                                    'model_tokens': models_tokens[self.entries[7].get()],
                                    }
            self.print_user_config()
        else:
            self.config_from_user = event
        self.root.destroy()

    def select_file(self, entry_file):
        filepath = filedialog.askopenfilename(title="Selecione o plano", filetypes=[('PDF files', '*.pdf')])
        entry_file.delete(0, tk.END)
        entry_file.insert(0, filepath)

    def select_dict(self, entry_dict):
        folderpath = filedialog.askdirectory(title="Selecione um diretório para salvar planilha FUNASA")
        entry_dict.delete(0, tk.END)
        entry_dict.insert(0, folderpath)    

    def config_field(self, config_field, row):
        tk.Label(self.frame, text=config_field['label']).grid(row=row, column=0, pady=10, sticky="E")
        entry = tk.Entry(self.frame, width=40)
    
        if config_field['type'] == 'input':
            entry.grid(row=row, column=1, pady=5)
        elif config_field['type'] == 'file':
            entry.grid(row=row, column=1, pady=5)
            btn = tk.Button(self.frame, text=config_field['button_label'], command=lambda:self.select_file(entry))
            btn.grid(row=row, column=2, padx=10)
        elif config_field['type'] == 'dir':
            entry.grid(row=row, column=1, pady=5)            
            btn = tk.Button(self.frame, text=config_field['button_label'], command=lambda:self.select_dict(entry))
            btn.grid(row=row, column=2, padx=10)
        elif config_field['type'] == 'radio':
            selected = tk.IntVar()
            for index, (text, value) in enumerate(config_field['op']):
                tk.Radiobutton(self.frame, text=text, variable=selected, value=value).grid(row=row+(index+6-config_field['col']), column=config_field['col'], sticky="w", padx=10)
            selected.set(config_field['op'][0][1])
            return selected
        elif config_field['type'] == 'dropdown':
            selected = tk.StringVar()
            dropdown = ttk.Combobox(self.frame, textvariable=selected)
            dropdown['values'] = config_field['op']
            dropdown.grid(row=row, column=config_field['col'], pady=5)
            dropdown.set(config_field['op'][0])
            return selected

        return entry

    def print_user_config(self):
        for key, value in self.config_from_user.items():
            print(key, ": ", value)



def erro_popup(error_message):
    messagebox.showerror(title="Erro", message=error_message)
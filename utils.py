import tkinter as tk
from tkinter import filedialog
import os


margin_bottom = 50
margin_top = 50
keywords_default=['objetivos', 'metas']
keywords_actions_default=['ações']
keywords_approched_or_not = {'Município': ['caracterização', 'características', 'aspectos'],
                             'Política': ['política']}

# Regex and string to remove from pdf text
sumario_id = '...'
summary_identifiers = ['....', '___']
figures_regex = r'Figura\s+\d+\.\d+\s-.*'
font_regex = r'Fonte:\s.*'
quadros_regex = r'QUADRO\s\d+\.\d+\s–.*'
tables_regex = r'Tabela\s+\d+\.\d+\s-.*'
# /Regex and string to remove from pdf text

obj_text_filename = 'plan_obj_ddl_inv'
actions_text_filename = 'plan_actions'
#obj_text_path = os.path.dirname(os.getcwd()) + '/data'
#actions_text_path = os.path.dirname(os.getcwd()) + '/data'

open_option = 5
update_option = 6
close_option = 7


def replace_table_for_text(full_text, tables_extracted_text, tables_correct_text):
    full_text = full_text.replace('\n', ' ')
    for index, table_extracted in enumerate(tables_extracted_text):
        table_extracted = table_extracted.replace('\n', ' ')
        if table_extracted in full_text:
            full_text = full_text.replace(table_extracted, tables_correct_text[index]).replace('\n', ' ')
        else:
            print("\nTable text error\n")
    
    #print(full_text)
    return full_text


def clean_text(text):
    text = text.replace(u"\uf0a8", "*")
    text = text.replace('  ', ' ')
    text = text.replace('`', '')
    text = text.replace('"', '')
    text = text.replace('“', '')
    return text


def treat_if_is_empty(value, default):
    if not value or value == '':
        return default
    return value
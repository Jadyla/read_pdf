#TODO: get the file name from the user (args or input). The structture is ready on main function
pdf_file_name = 'Plano Antigo Águas de Lindóia.pdf'
margin_bottom = 50
margin_top = 50

# Regex and string to remove from pdf text
sumario_id = '...'
summary_identifiers = ['....', '___']
figures_regex = r'Figura\s+\d+\.\d+\s-.*'
font_regex = r'Fonte:\s.*'
quadros_regex = r'QUADRO\s\d+\.\d+\s–.*'
tables_regex = r'Tabela\s+\d+\.\d+\s-.*'
# /Regex and string to remove from pdf text


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
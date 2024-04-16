import pdfplumber
from utils import *
import re
import os


class PDF:
    def __init__(self, pdf_file_name):
        self.pdf = pdfplumber.open(pdf_file_name)
        self.keywords_to_search_on_summary = ['objetivos', 'metas']
        self.summary_pages_ajustment = 0  # ajustment of real page number and page indicated on the summary
        self.last_page_to_look_for_summary = 25


    def search_for_summary(self):
        summary_page = 0
        for page in range(0, self.last_page_to_look_for_summary):
            text = self.pdf.pages[page].extract_text()
            if ('sumário' in text.lower()) and '.....' in text:
                summary_page = page
                break
        return summary_page


    def create_dict_from_summary(self):
        all_text = ''
        summary_page = self.search_for_summary()
        for num in range(summary_page, summary_page + 10):
            page = self.pdf.pages[num]
            width = page.width
            height = page.height
            reading_coordinate = (0, margin_top, width, height - margin_bottom)

            text = page.within_bbox(reading_coordinate).extract_text()

            for identifier in summary_identifiers:
                if identifier in text:
                    all_text += text
                    all_text += '\n'
        print(all_text)

        #summary_number_regex = r'\b\d+\.\d*\s'
        title_page_regex = r'(.+?)\s*\.{3,}\s*(\d+)'
        title_page_underline_regex = r'(.+?)\s*\_{3,}\s*(\d+)'

        #all_text = re.sub(summary_number_regex, '', all_text)

        title_page = re.findall(title_page_regex, all_text)
        if not title_page:
            title_page = re.findall(title_page_underline_regex, all_text)

        for title, page in title_page:
            print("Título:", title)
            print("Página:", page)
            print()

        return title_page


    def search_on_summary_titles(self, summary_titles):
        titles_dict = summary_titles
        pages_list = []
        for keyword in self.keywords_to_search_on_summary:
            for index, (title, page) in enumerate(titles_dict):
                if keyword in title.lower():
                    #print(f"A palavra-chave '{keyword}' foi encontrada no título '{title}' na página {page} na chave {index}\n\n")
                    pages_list.append(str(page) + '-' + str(list(titles_dict)[index + 2][1]))
                    del titles_dict[index]
        return pages_list


    def exctract_text_from_pdf(self, pages_to_extract_text):
        all_text = ''
        for pages_interval in pages_to_extract_text:
            first_page, last_page = pages_interval.split('-')
            first_page = int(first_page) - 1 + self.summary_pages_ajustment
            last_page = int(last_page) + self.summary_pages_ajustment
            for num in range(first_page, last_page):
                page = self.pdf.pages[num]
                width = page.width
                height = page.height
                reading_coordinate = (0, margin_top, width, height - margin_bottom)

                print(f"\n\n--------------------- PÁGINA {num + 1} ---------------------\n")
                if self.has_table(page):
                    print("****** POSSUI TABELA ******\n")
                    tables = page.extract_tables()
                    tables_correct_text = []
                    tables_extracted_text = []
                    all_text_with_tables = page.within_bbox(reading_coordinate).extract_text()

                    for table in tables:
                        tables_correct_text.append(self.extract_tables_text(table))

                    tables_box = page.find_tables()
                    
                    for table_box in tables_box:
                        box = table_box.bbox
                        tables_extracted_text.append(page.within_bbox(reading_coordinate).within_bbox(box).extract_text())
                        
                    text = replace_table_for_text(all_text_with_tables, tables_extracted_text, tables_correct_text)
                else:
                    text = page.within_bbox(reading_coordinate).extract_text().replace('\n', ' ')

                all_text += text
                print(text)

        all_text = clean_text(all_text)
        print('\n\n\n\n', '-------------------- TEXTO FINAL --------------------\n\n\n', all_text)


    def has_table(self, page):
        tables = page.extract_tables()
        if tables:
            return True
        return False


    def extract_tables_text(self, table):
        table_text = 'Tabela: '
        for row in table:
            row_reading = ['' if item is None else item for item in row]
            row_reading = [item.replace('\n', ' ') for item in row_reading]

            result = str(row_reading)
            table_text += result
            table_text += '\\n'

        return table_text



if __name__ == '__main__':
    pdf_file_name = select_pdf_file()
    if not os.path.exists(pdf_file_name):
        print('Arquivo não encontrado!')
        exit(1)

    pdf = PDF(pdf_file_name)
    summary_titles = pdf.create_dict_from_summary()
    pages_to_extract_text = pdf.search_on_summary_titles(summary_titles)
    pdf.exctract_text_from_pdf(pages_to_extract_text)

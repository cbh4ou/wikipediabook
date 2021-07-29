
import sys, requests, os, random, datetime
from pathlib import Path
from pikepdf import Pdf, Page, Rectangle, PdfImage
import img2pdf
from docx2pdf import convert
from glob import glob
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm, Inches, Mm, Emu
from urllib.parse import unquote



class Wiki:
    def __init__(self):
        super().__init__()
        self.wiki_urls = []
        self.cover = ""
        self.title = ""
    
    def split_string(self, string):
        # Split the string based on space delimiter
        list_string = ' '.join(string.split('_'))
        return list_string
    
    def build_book(self):
        # Split Urls into TOC Format
        chapters = [unquote(split_string(a)) for a in self.wiki_urls]
        imagepdf = Pdf.open('media/name.pdf')
        image1 = imagepdf.pages[0]
        thumbnail = Page(imagepdf.pages[0])

        directory =self.wiki_urls[0] +"/"
        request_url = 'https://en.wikipedia.org/api/rest_v1/page/pdf/'
        wiki_pdfs = []

        for step in range(0,len(wiki_urls)):
            uri =self.wiki_urls[step]
            response = requests.get(request_url + uri)
            filename = uri +'.pdf'
            wiki_pdfs.append(filename)
            
            Path(directory).mkdir(parents=True, exist_ok=True)
            with open(directory + filename, 'wb') as f:
                f.write(response.content)
                
        page_numbers=[3]  
            
        for pdf in wiki_pdfs:
            tmp_pdf = Pdf.open(directory +'/'+pdf)
            page_numbers.append((len(tmp_pdf.pages)  + page_numbers[len(page_numbers)-1]))
            version = tmp_pdf.pdf_version
            tmp_first_page = Page(tmp_pdf.pages[0])
            tmp_first_page.add_overlay(thumbnail, Rectangle(0,0, 1000,300))
            tmp_pdf.save(directory +'edited-' + pdf, min_version=version)
            


        del page_numbers[-1]    
        toc_data = list(zip(chapters,page_numbers))
        
        
        # Template for TOC
        template = DocxTemplate('doclayout.docx')

        #Generate List for TOC
        table_contents = []

        for i in range(0,len(toc_data)):
            table_contents.append({
                'Index': toc_data[i][0],
                'Value': toc_data[i][1]
                })


        context = {
            'title': self.title,
            'day': datetime.datetime.now().strftime('%d'),
            'month': datetime.datetime.now().strftime('%b'),
            'year': datetime.datetime.now().strftime('%Y'),
            'table_contents': table_contents,
            }

        #Render automated report
        template.render(context)
        template.save('poc.docx')

        convert("poc.docx")
        
       
        with open("cover.pdf","wb") as f:
            f.write(img2pdf.convert('foo.jpg'))
        cover_pdf = Pdf.open("cover.pdf")    
        toc_pdf = Pdf.open("poc.pdf")  
        
        del toc_pdf.pages[1:]
        
        cover_pdf.pages.extend(toc_pdf.pages)
        for pdf in wiki_pdfs:
            src = Pdf.open(directory+ "edited-"+pdf)
            cover_pdf.pages.extend(src.pages)
        cover_pdf.save(self.title + '.pdf')



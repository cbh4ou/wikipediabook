import sys, requests, os, random, datetime
from pathlib import Path
from pikepdf import Pdf, Page, Rectangle, PdfImage
import img2pdf
from docx2pdf import convert
from glob import glob
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm, Inches, Mm, Emu
from urllib.parse import unquote
import requests


class Wiki():
    def __init__(self, title):
        super().__init__()
        self.wiki_urls = 'wiki_urls.txt'
        self.cover = title + ".jpg"
        self.title = title

    
    def get_wiki_urls(self):
        with open("media/Docs/" + self.wiki_urls) as f:    content = [i.strip().rsplit('/', 1)[-1] for i in f.readlines()]
        return content
    
    def split_string(self, string):
        # Split the string based on space delimiter
        list_string = ' '.join(string.split('_'))
        return list_string
    
    def send_email_pdf_figs(self, path_to_pdf, title):
        from socket import gethostname
        #import email
        from email.mime.application import MIMEApplication
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib
        import json

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        config = json.load(f)
        server.login('connor@jkwenterprises.com', 'Primussucks72!')
        # Craft message (obj)
        msg = MIMEMultipart()
        message = f'{message}\nSend from Hostname: {gethostname()}'
        msg['Subject'] = "Ebook - " + self.title
        msg['From'] = 'connor@jkwenterprises.com'
        msg['To'] = ['832d9841.patriotpoweredpublishing.com@amer.teams.ms', 'cbh4ou@gmail.com']
        # Insert the text to the msg going by e-mail
        msg.attach(MIMEText(message, "plain"))
        # Attach the pdf to the msg going by e-mail
        with open(path_to_pdf, "rb") as f:
            #attach = email.mime.application.MIMEApplication(f.read(),_subtype="pdf")
            attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str(path_to_pdf))
        msg.attach(attach)
        # send msg
        server.send_message(msg)
        
        return "Email Sent"
    
    def build_book(self):
        # Split Urls into TOC Format
        chapters = [unquote(self.split_string(a)) for a in self.get_wiki_urls()]
        imagepdf = Pdf.open('media/Images/name.pdf')
        image1 = imagepdf.pages[0]
        thumbnail = Page(imagepdf.pages[0])

        directory = "media/chapter_covers/" 
        request_url = 'https://en.wikipedia.org/api/rest_v1/page/pdf/'
        wiki_pdfs = []

        for step in range(0,len(chapters)):
            
            uri = chapters[step]
            response = requests.get(request_url + uri)
            filename = uri +'.pdf'
            wiki_pdfs.append(filename)
            
            
            with open(directory + chapters[step] + ".pdf", 'wb') as f:
                f.write(response.content)
                
        page_numbers=[3]  
            
        for pdf in wiki_pdfs:
            tmp_pdf = Pdf.open('media/chapter_covers/'+pdf)
            page_numbers.append((len(tmp_pdf.pages)  + page_numbers[len(page_numbers)-1]))
            version = tmp_pdf.pdf_version
            tmp_first_page = Page(tmp_pdf.pages[0])
            tmp_first_page.add_overlay(thumbnail, Rectangle(0,0, 1000,300))
            tmp_pdf.save('media/Docs/'+'edited-' + pdf, min_version=version)
            


        del page_numbers[-1]    
        toc_data = list(zip(chapters,page_numbers))
        
        
        # Template for TOC
        template = DocxTemplate('media/Docs/doclayout.docx')

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
        template.save('media/Docs/poc.docx')
        import pythoncom
        import win32com.client as client

        pythoncom.CoInitialize()
        convert("media/Docs/poc.docx")
        
       
        with open("media/cover_images/" + self.title + ".pdf","wb") as f:
            f.write(img2pdf.convert('media/cover_images/' + self.cover))
        cover_pdf = Pdf.open('media/cover_images/' + self.title + ".pdf")    
        toc_pdf = Pdf.open("media/Docs/poc.pdf")  
        
        del toc_pdf.pages[1:]
        
        cover_pdf.pages.extend(toc_pdf.pages)
        for pdf in wiki_pdfs:
            src = Pdf.open("media/Docs/" + "edited-"+pdf)
            cover_pdf.pages.extend(src.pages)
        cover_pdf.save("media/final_book/" + self.title + '.pdf')
        
        self.send_email_pdf_figs("media/final_book/"+self.title+'.pdf' , self.title)
        
        return True


    
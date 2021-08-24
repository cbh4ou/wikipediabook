from .celery import app
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
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
import json
import urllib.request 
import time
from PIL import Image
import dropbox
import io

@app.task(typing=False)
def send_ebook(title):
    class Wiki():
        def __init__(self, title):
            super().__init__()
            self.wiki_urls = 'wiki_urls.txt'
            self.cover = title + ".jpg"
            self.title = title
            self.dbx = dropbox.Dropbox(settings.DROPBOX_TOKEN)
            self.textfile = title + ".txt"
        def get_wiki_urls(self):
            _, res = self.dbx.files_download("/Docs/" + self.textfile)

            res.raise_for_status()
            wiki_urls = []
            
            with io.BytesIO(res.content) as stream:
                # assume bytes_io is a `BytesIO` object
                byte_str = stream.read()

                # Convert to a "unicode" object
                text_obj = byte_str.decode('UTF-8')  # Or use the encoding you expect

                # Use text_obj how you see fit!
                lines = io.StringIO(text_obj) 
                for x in lines:
                    wiki_urls.append(x.rstrip())
            return wiki_urls
        def split_string(self, string):
            # Split the string based on space delimiter
            list_string = string.split('/')[-1]

            list_string = ' '.join(list_string.split('_'))
           
            return list_string
        
        def send_email_pdf_figs(self, ):
            from socket import gethostname
            #import email
            from email.mime.application import MIMEApplication
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            import smtplib, ssl
            import json

            subject = title + ' EBOOK HAS BEEN GENERATED'
            message = 'God Speed'
            recipient_list = ['bcce3c13.patriotpoweredpublishing.com@amer.teams.ms',]
            email_from = settings.EMAIL_HOST_USER
            email = EmailMessage(
            subject, message, email_from, recipient_list)
            metadata, edit = self.dbx.files_download(f"/final_pdfs/{self.title}.pdf")
            with io.BytesIO(edit.content) as final_pdf:
                email.attach( f"{self.title}.pdf", final_pdf.getvalue()  , mimetype="application/pdf")
            email.send()
            final_pdf.close()
            return "Email Sent"
        
        def build_book(self):
            
            # Split Urls into TOC Format
            chapters = [self.split_string(a) for a in self.get_wiki_urls()]
            
            
            metadata, f = self.dbx.files_download('/Images/image.pdf')
            with io.BytesIO(f.content) as img_file:
                imagepdf = Pdf.open(img_file)
                thumbnail = Page(imagepdf.pages[0])
                
            
                
            
            directory = "/chapter_covers/" 
            request_url = 'https://en.wikipedia.org/api/rest_v1/page/pdf/'
            wiki_pdfs = []
           
            for step in range(0,len(chapters)):    
                uri = chapters[step]
                response = requests.get(request_url + uri)
                filename = uri +'.pdf'
                wiki_pdfs.append(filename)
                with io.BytesIO(response.content) as open_pdf_file:
                    self.dbx.files_upload(open_pdf_file.read(), path=f"/chapter_covers/{filename}",mode=dropbox.files.WriteMode.overwrite)   
                    open_pdf_file.close()
                    
            
            for pdf in wiki_pdfs:
                
                metadata, edit = self.dbx.files_download(f"/chapter_covers/{pdf}")
                
                with io.BytesIO(edit.content) as edit_pdf:
                    
                    page_numbers=[3]  
                   
                    tmp_pdf = Pdf.open(edit_pdf)
                    
                    page_numbers.append((len(tmp_pdf.pages)  + page_numbers[len(page_numbers)-1]))
                    version = tmp_pdf.pdf_version
                    print(thumbnail)
                    tmp_first_page = Page(tmp_pdf.pages[0])
                    tmp_first_page.add_overlay(thumbnail, Rectangle(0,0, 1000,300))
                    in_mem = io.BytesIO()
                    tmp_pdf.save(in_mem, min_version=version)
                    
                    
                    print(in_mem)
                    something = self.dbx.files_upload(in_mem.getvalue(), path=f"/chapter_covers/edited-{pdf}",mode=dropbox.files.WriteMode.overwrite)
                    in_mem.close()
                    edit_pdf.close()
            img_file.close()

            #del page_numbers[-1]    
            toc_data = list(zip(chapters,page_numbers))
      
         
            #Generate List for TOC
            table_contents = []

            for i in range(0,len(toc_data)):
                table_contents.append({
                    'title': toc_data[i][0],
                    'page': toc_data[i][1]
                    })


            context = {
                'chapters': table_contents,
                }
            
            template_id = settings.TEMPLATE_ID
            toc_filename = ''
            
            
            dicti = {
                    "document": {
                    "document_template_id": template_id,
                    "payload": {},
                    "status": "pending"
                    }
                }
            dicti['document']['payload'].update(dict(context))
            



            url = "https://api.pdfmonkey.io/api/v1/documents"

            payload = json.dumps(dicti)
            headers = {
            'Content-Type': 'application/json',
            'Authorization': settings.PDFMONKEY_KEY
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            get_id = json.loads(response.text)

            doc_id = get_id['document']['id']
           
            while True:
                url = "https://api.pdfmonkey.io/api/v1/documents/" + doc_id
               

                headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer BWZigvUTWdJogQzqiAb-'
                }

                response = requests.request("GET", url, headers=headers)

                get_response = json.loads(response.text)
              
                if get_response['document']['status'] == 'success':
                    url = get_response['document']['download_url']
                    toc_filename = get_response['document']['filename']
                    response = urllib.request.urlopen(url)
                    self.dbx.files_upload(response.read(), path=f"/Docs/{toc_filename}",mode=dropbox.files.WriteMode.overwrite)
                    
                    break
                    
                    
                time.sleep(1)
            
            _, res = self.dbx.files_download("/Images/" + self.cover)
            
            path_pdf = '/chapter_covers/' + wiki_pdfs[0]
            
            metadata, f = self.dbx.files_download(path_pdf)
            
            
            image1 = Image.open(io.BytesIO(res.content))
            
            im1 = image1.convert('RGB')
            mem = io.BytesIO()
            im1.save(mem, format='PDF')
            
            #self.dbx.files_upload(mem.getvalue(), path=f"/Images/{self.title}.pdf",mode=dropbox.files.WriteMode.overwrite)   
                   
            cover_pdf = Pdf.open(mem)  
            
            _, res = self.dbx.files_download(f"/Docs/{toc_filename}")
            with io.BytesIO(res.content) as toc_file: 
                final_mem = io.BytesIO()
                toc_pdf = Pdf.open(toc_file)    
                
                del toc_pdf.pages[1:]
            
                cover_pdf.pages.extend(toc_pdf.pages)
                
                
                for pdf in wiki_pdfs:
                    
                    metadata, epdf = self.dbx.files_download("/chapter_covers/edited-" +pdf)
                    
                    with io.BytesIO(epdf.content) as edited_pdf:
                        
                        src = Pdf.open(edited_pdf)
                        
                        cover_pdf.pages.extend(src.pages)
                        
                        src.close()
                        edited_pdf.close()
                        
                cover_pdf.save(final_mem)
                cover_pdf.close()
                self.dbx.files_upload(final_mem.getvalue(), path=f"/final_pdfs/{self.title}.pdf",mode=dropbox.files.WriteMode.overwrite)  
                self.send_email_pdf_figs()
        
    book = Wiki(title)
    path = book.build_book()
    return path
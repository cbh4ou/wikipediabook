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
from django.conf import settings
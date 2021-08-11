from celery import app
from ebook.services import Wiki

@app.task
def send_ebook(title):
    book = Wiki(title)
    path = book.build_book
    return path
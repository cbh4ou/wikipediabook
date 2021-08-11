from .celery import app
from ebook.services import Wiki

@app.task(typing=False)
def send_ebook(title):
    book = Wiki(title)
    path = book.build_book()
    return path
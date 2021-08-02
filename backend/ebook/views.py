from django.shortcuts import render  # noqa
from rest_framework import viewsets
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.urls import reverse
from .forms import BookForm
from django.views import generic, View
from django.views.generic.edit import FormView
from django.conf import settings
from .services import Wiki
# Create your views here.

cover_folder = settings.MEDIA_URL + "cover_images/"
class BookView(View):
    template_name = 'common/index.html'

    def get(self, request, *args, **kwargs):
        submitted = False
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True

        return render(request,
            self.template_name,
            {'form': form, 'submitted': submitted}
            )

    
    def handle_file_upload(self, cover, title, urls ):
      with open('media/cover_images/' + title + '.jpg', 'wb+') as destination:
        for chunk in cover.chunks():
            destination.write(chunk)
      with open('media/Docs/wiki_urls.txt', 'wb+') as destination:
        for chunk in urls.chunks():
            destination.write(chunk)
    def post(self, request, *args, **kwargs):
       form = BookForm(request.POST)
       if form.clean():
          #cd = form.cleaned_data
          title = request.POST['Title']
          self.handle_file_upload(request.FILES['upload_cover'], title, request.FILES['upload_urls'] )
          book = Wiki(title)
          book_path = book.build_book()
          return FileResponse(open(book_path, 'rb'))
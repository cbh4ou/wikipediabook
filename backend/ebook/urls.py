from django.urls import include, path
from rest_framework import routers
from ebook.views import BookView

router = routers.DefaultRouter()
#router.register(r'create', BookView.as_view())



urlpatterns = [
   path('create', BookView.as_view(http_method_names=['get','post'])),
   
]


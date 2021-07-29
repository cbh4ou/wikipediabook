from django.urls import path, include

from . import views

app_name = 'common'
urlpatterns = [
    path('star-wars/', include('users.urls')),
    path('', views.IndexView.as_view(), name='index'),
]

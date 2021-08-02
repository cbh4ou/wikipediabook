from django.urls import include, path
from rest_framework import routers
from users.views import PersonViewSet, SpeciesViewSet, bookform

router = routers.DefaultRouter()

urlpatterns = [
   path('', include(router.urls)),
   
]

from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.conf import settings
import django_js_reverse.views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from common.routes import routes as common_routes

router = DefaultRouter()

routes = common_routes
for route in routes:
    router.register(route['regex'], route['viewset'], basename=route['basename'])

urlpatterns = [
    path("", include("common.urls"), name="common"),
    path("admin/", admin.site.urls, name="admin"),
    path("jsreverse/", django_js_reverse.views.urls_js, name="js_reverse"),
    path('ebook/', include('ebook.urls')),
    path("api/", include(router.urls), name="api"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
print(settings.MEDIA_URL, settings.MEDIA_ROOT)
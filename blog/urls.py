from django.contrib import admin
from django.urls import path,include
from posts.views import  IndexListView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexListView.as_view(), name='index'),
    path('posts/', include('posts.urls', namespace='posts')), #namespace is for templates: {% POSTS: index %}
    path('users/', include('users.urls', namespace='users')), #namespace is for templates: {% POSTS: index %}
    path('accounts/', include('allauth.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include   # 👈 include import zaroor karo
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # 👈 accounts app ke URLs include kar diye
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

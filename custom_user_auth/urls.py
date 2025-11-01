from django.contrib import admin
from django.urls import path, include   # 👈 include import zaroor karo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # 👈 accounts app ke URLs include kar diye
]

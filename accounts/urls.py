from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('home/', views.home, name='home'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),

    path('logout/', views.logout_user, name='logout'),
]

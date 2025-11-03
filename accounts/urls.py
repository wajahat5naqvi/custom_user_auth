from . import views
from django.urls import path


urlpatterns = [
    path('', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('users/', views.users, name='users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('logout/', views.logout_user, name='logout_user'),
]

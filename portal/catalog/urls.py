from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('check-username/', views.check_username, name='check_username'),
    path('register', views.Register.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('<int:pk>/profile/', views.Profile.as_view(), name='profile'),
]

urlpatterns += [
    path('new/', views.create_application, name='create_application'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
]
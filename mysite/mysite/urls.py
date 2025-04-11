"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # type: ignore
from django.urls import path  # type: ignore
from myapp import views
from django.contrib.auth import views as auth_views  # type: ignore
from myapp.views import generate_report_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('delete/<int:id>/', views.delete_consume, name='delete'),
    path('edit/<int:id>/', views.edit_consume, name='edit'), 
    path('summary/', views.daily_summary, name='summary'),    
    path('profile/', views.user_profile, name='profile'),
     path('download-report/', generate_report_pdf, name='download_report'),
    path('set-goal/', views.set_calorie_goal, name='set_goal'),

     
]

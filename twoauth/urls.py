"""twoauth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import home_view,auth_view,verify_view,register_view,logout_view,forget_view
from django.contrib.auth import views as auth_views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view,name='home-view'),
    path('login/',auth_view,name='login-view'),
    path('verify/',verify_view,name='verify-view'),
    path('register/', register_view, name="register-view"),
    path('logout/',logout_view,name="logout"),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="password_reset"),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name="password_reset_confirm"),
     path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete"),



]

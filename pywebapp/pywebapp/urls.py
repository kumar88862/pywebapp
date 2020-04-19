"""pywebapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from core import views
from reg import views as view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('signup',view.signup),
    path('mybooks',view.mybooks),
    path('logout',view.logout),
    path('login',view.login),
    path('change',view.change),
    path('upload',views.upload),
    path('delete',views.delete),
    path('share',views.share),
    path('sharefile',views.sharefile),
    path('sharedbooks',views.sharedbooks),
    path('home',views.home),
    path('receivedbooks',views.receivedbooks),
    path('mybookssearch',views.mybookssearch),
    path('sharedbookssearch',views.sharedbookssearch),
    path('receivedbookssearch',views.receivedbookssearch),
    path('stopsharing',views.stopsharing),
    path('removereceiving',views.removereceiving),
    path('sendemail',views.sendemail),
    path('reset',views.reset),
    path('check',views.check),
    path('changepassword',view.changepassword)


]

"""cookit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
import main.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', main.views.mainpage, name='mainpage'),
    url(r'^settings/$', main.views.settings, name='settings'),
    url(r'^feed/$', main.views.feed, name='feed'),
    url(r'^feed/add_my_ingredient/$', main.views.add_my_ingredient, name='add_my_ingredient'),
    url(r'^feed/(?P<feed_type>\w+)/$', main.views.feed, name='feed'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', main.views.register, name='register'),
    url(r'^user/(?P<user_id>\d+)/$', main.views.user, name='user'),
    url(r'^user/(?P<user_id>\d+)/favourite/$', main.views.add_favourite_user, name='add_favourite_user'),
    url(r'^recipes/(?P<recipe_id>\d+)/$', main.views.recipe, name='recipe'),
    url(r'^recipes/(?P<recipe_id>\d+)/cook/$', main.views.cook_recipe, name='cook_recipe'),
    url(r'^recipes/(?P<recipe_id>\d+)/favourite/$', main.views.add_favourite, name='add_favourite'),
    url(r'^recipes/(?P<recipe_id>\d+)/remove/$', main.views.remove_recipe, name='remove_recipe'),
    url(r'^recipes/new/$', main.views.new_recipe, name='new_recipe'),
]

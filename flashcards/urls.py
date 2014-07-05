from django.conf.urls import patterns, include, url
from flashcard_app import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flashcards.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^logout/$', views.user_logout, name = 'logout'),
    url(r'^register_redirect/$', views.register_redirect, name = 'register_redirect'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^delete_group/$', views.delete_flashcard_group, name = "delete_flashcard_group"),
    url(r'^delete_flashcard/$', views.delete_flashcard, name = "delete_flashcard"),
    url(r'^(?P<username>\w+)/home/$', views.home, name = 'home'),                   
    url(r'^(?P<username>\w+)/flashcards/', include('flashcard_app.urls')),
    url(r'^(?P<username>\w+)/create_flashcard_group/$', views.create_flashcard_group, name = 'create_flashcard_group'),
    
    url(r'^check_flashcard/$', views.check_flashcard, name = "check_flashcard"),
    url(r'^$', views.index, name='index'),
)
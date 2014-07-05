from django.conf.urls import patterns, url
from flashcard_app import views

urlpatterns = patterns('',
        url(r'^view_groups/$', views.view_flashcard_groups, name = 'view_flashcard_groups'),
        url(r'^create/(?P<groupname>\w+)/$', views.create_flashcard, name = 'create_flashcard'),
        url(r'^view/(?P<groupname>\w+)/$', views.view_flashcards, name = 'view_flashcards'),
        url(r'^practice/(?P<groupname>\w+)/(?P<side>\w+)/generate_flashcard/$', views.generate_flashcard, name = 'generate_flashcard'),         
        url(r'^practice/(?P<groupname>\w+)/(?P<side>\w+)/$', views.practice_flashcards, name = 'practice_flashcards'),
        url(r'^practice/(?P<groupname>\w+)/(?P<side>\w+)/results/$', views.results, name = 'results'),
        
)
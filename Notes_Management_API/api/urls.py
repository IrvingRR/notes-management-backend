from django.urls import path
from .views import NoteView

# These are the urls to do the http requests
urlpatterns = [
    path('notes', NoteView.as_view(), name='notes_list'),
    path('notes/<int:id>', NoteView.as_view(), name='notes_actions')
]
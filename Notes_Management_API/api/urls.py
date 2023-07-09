from django.urls import path
from .views import NoteView

urlpatterns = [
    path('notes', NoteView.as_view(), name='notes_list'),
    path('notes/<int:id>', NoteView.as_view(), name='notes_actions')
]
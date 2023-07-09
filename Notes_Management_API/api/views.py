from typing import Any
from django import http
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Note
import json


# Create your views here.

# This is the view which allows us to handle every endpoint to management the information
# We have fourth enpoints
# get: Allows us to get all notes from database or only one note by id depending of the id value
# post: Allows us to create a new note and save it into database if the title is not already exists
# put: Allows us to update by id the information of a specific note if it exists
# delete: Allows us to delete a note by id if it exists 

class NoteView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Endpoint to get all notes or only one by id
    def get(self, request, id = 0):
        # If id is grater than 0 we have to get only the note with that id
        if(id > 0):
            notes = list(Note.objects.filter(id = id).values())

            if len(notes) > 0:
                note = notes[0]
                response = {'ok': True, 'note': note}
            else:
                response = {'ok': False, 'note': {}, 'message': 'Note not found'}
            
            return JsonResponse(response)
        # If id is not exists or is less than 0 we have to get all notes from database
        else:
            notes = list(Note.objects.values())

            if len(notes) > 0:
                response = {'ok': True, 'notes': notes}
            else:
                response = {'ok': False, 'notes': [], 'message': 'Notes not found'}
            
            return JsonResponse(response)

    # Endpoint to create a new note if the title is already not exists in the database
    def post(self, request):

        try:
            data = json.loads(request.body)
            
            note = Note()
            note.title = data['title']
            note.description = data['description']

            note.full_clean()
            note.save()

            response = {'ok': True, 'note': data, 'message': 'Note created successfully'}
            return JsonResponse(response)
        
        except ValidationError as e:
            print(e)
            return JsonResponse({'ok': False, 'message': 'Oops!, the following errors occurred', 'errors': str(e)})
    
    # Endpoint to update a specific note by id if it exists
    def put(self, request, id):

        try:
            data = json.loads(request.body)
            notes = list(Note.objects.filter(id = id).values())

            if len(notes) > 0:

                noteDB = Note.objects.get(id = id)

                note = Note()
                note.title = data['title']
                note.description = data['description']
                note.full_clean()

                noteDB.title = data['title']
                noteDB.description = data['description']

                noteDB.save()

                response = {'ok': True, 'note': data, 'message': 'Note updated successfully'}
            else:
                response = {'ok': False, 'note': {}, 'message': 'Note not found'}

            return JsonResponse(response)

        except ValidationError as e:
            print(e)
            return JsonResponse({'ok': False, 'message': 'Oops!, the following errors occurred', 'errors': str(e)})
        
    # Endpoint to delete a specific note by id if it exists
    def delete(self, request, id):

        notes = list(Note.objects.filter(id = id).values())

        if len(notes) > 0:
            Note.objects.filter(id = id).delete()
            response = {'ok': True, 'note': {}, 'message': 'Note deleted successfully'} 
        else:
            response = {'ok': False, 'note': {}, 'message': 'Note not found'}

        return JsonResponse(response)
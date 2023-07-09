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

class NoteView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id = 0):

        if(id > 0):
            notes = list(Note.objects.filter(id = id).values())

            if len(notes) > 0:
                note = notes[0]
                response = {'ok': True, 'note': note}
            else:
                response = {'ok': False, 'note': {}, 'message': 'Note not found'}
            
            return JsonResponse(response)

        else:
            notes = list(Note.objects.values())

            if len(notes) > 0:
                response = {'ok': True, 'notes': notes}
            else:
                response = {'ok': False, 'notes': [], 'message': 'Notes not found'}
            
            return JsonResponse(response)

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
        
    def delete(self, request, id):

        notes = list(Note.objects.filter(id = id).values())

        if len(notes) > 0:
            Note.objects.filter(id = id).delete()
            response = {'ok': True, 'note': {}, 'message': 'Note deleted successfully'} 
        else:
            response = {'ok': False, 'note': {}, 'message': 'Note not found'}

        return JsonResponse(response)
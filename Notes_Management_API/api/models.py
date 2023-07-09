from django.db import models

# Create your models here.

# This is the model which goes handle the information about the notes
# @property {String} title: Is the title of the note
# @property {String} description: Is the description of the note

class Note(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000)
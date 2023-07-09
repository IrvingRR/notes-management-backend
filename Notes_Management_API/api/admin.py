from django.contrib import admin
from .models import Note

# Register your models here.
# We create an admin site to create data from the administrative plaform
admin.site.register(Note)
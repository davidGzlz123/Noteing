from django.contrib import admin
from .models import Note, CheckboxItem, NumberedItem

admin.site.register(Note)
admin.site.register(CheckboxItem)
admin.site.register(NumberedItem)

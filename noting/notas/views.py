from rest_framework import viewsets
from .models import Note, CheckboxItem, NumberedItem
from .serializers import NoteSerializer, CheckboxItemSerializer, NumberedItemSerializer

class NoteViewSet(viewsets.ModelViewSet):
  queryset = Note.objects.all()
  serializer_class = NoteSerializer

class CheckboxItemViewSet(viewsets.ModelViewSet):
  queryset = CheckboxItem.objects.all()
  serializer_class = CheckboxItemSerializer

class NumberedItemViewSet(viewsets.ModelViewSet):
  queryset = NumberedItem.objects.all()
  serializer_class = NumberedItemSerializer

from django.db import models


class Note(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField(blank=True)
  category = models.CharField(max_length=100, blank=True, null=True)
  image = models.ImageField(upload_to='note_images/', blank=True, null=True)


class CheckboxItem(models.Model):
  note = models.ForeignKey(Note, related_name='checkboxes', on_delete=models.CASCADE, null=True, blank=True)
  parent = models.ForeignKey('self', related_name='subcheckboxes', on_delete=models.CASCADE, null=True, blank=True)
  text = models.CharField(max_length=200)
  checked = models.BooleanField(default=False)
  image = models.ImageField(upload_to='checkbox_images/', blank=True, null=True)  # Imagen opcional por checkbox


class NumberedItem(models.Model):
  note = models.ForeignKey(Note, related_name='numbers', on_delete=models.CASCADE, null=True, blank=True)
  text = models.CharField(max_length=200)
  position = models.IntegerField()

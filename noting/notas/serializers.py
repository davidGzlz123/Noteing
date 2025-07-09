# serializers.py

from rest_framework import serializers
from .models import Note, CheckboxItem, NumberedItem
import json


class RecursiveField(serializers.Serializer):
  def to_representation(self, value):
    serializer = self.parent.parent.__class__(value, context=self.context)
    return serializer.data

  def to_internal_value(self, data):
    return data

class CheckboxItemSerializer(serializers.ModelSerializer):
  image = serializers.SerializerMethodField()
  parent = serializers.PrimaryKeyRelatedField(queryset=CheckboxItem.objects.all(), allow_null=True, required=False)
  subcheckboxes = RecursiveField(many=True, read_only=True)
  # Campo para indicar si la imagen debe ser eliminada
  delete_image = serializers.BooleanField(write_only=True, required=False)

  class Meta:
    model = CheckboxItem
    fields = ['id', 'text', 'checked', 'parent', 'note', 'image', 'subcheckboxes', 'delete_image']

  def get_image(self, obj):
    if obj.image:
      request = self.context.get('request')
      if request:
        return request.build_absolute_uri(obj.image.url)
      return obj.image.url
    return None


class NumberedItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = NumberedItem
    fields = ['id', 'text', 'position']


class NoteSerializer(serializers.ModelSerializer):
    checkboxes = serializers.SerializerMethodField()
    numbers = NumberedItemSerializer(many=True, required=False)
    # Campo para indicar si la imagen principal de la nota debe ser eliminada
    delete_main_image = serializers.BooleanField(write_only=True, required=False)


    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'category', 'image', 'checkboxes', 'numbers', 'delete_main_image']

    def get_checkboxes(self, instance):
        root_checkboxes = instance.checkboxes.filter(parent__isnull=True)
        return CheckboxItemSerializer(root_checkboxes, many=True, context=self.context).data

    def create(self, validated_data):
        request = self.context['request']
        checkboxes_data = request.data.get('checkboxes', '[]')
        checkboxes_data = json.loads(checkboxes_data)
        numbers_data = validated_data.pop('numbers', [])

        note = Note.objects.create(
          title=validated_data.get('title'),
          content=validated_data.get('content'),
          category=validated_data.get('category'),
          image=request.FILES.get('image')
        )
        self.create_checkboxes(note, checkboxes_data, request.FILES)
        for num_data in numbers_data:
          NumberedItem.objects.create(note=note, **num_data)
        return note

    def update(self, instance, validated_data):
        request = self.context['request']
        checkboxes_data = request.data.get('checkboxes', '[]')
        checkboxes_data = json.loads(checkboxes_data)
        numbers_data = validated_data.pop('numbers', [])

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.category = validated_data.get('category', instance.category)

        # Lógica de imagen de nota
        if 'image' in request.FILES:
            if instance.image:
                instance.image.delete(save=False)
            instance.image = request.FILES['image']
        elif validated_data.get('delete_main_image', False): # Usa la bandera del validated_data
            if instance.image:
                instance.image.delete(save=False)
                instance.image = None
        # Si no se envía imagen nueva y no se pide borrar, mantener la existente
        elif 'image' not in request.FILES and not validated_data.get('delete_main_image', False):
            pass # No hacer nada con la imagen, se mantiene la existente


        instance.save()

        self.update_checkboxes(instance, checkboxes_data, request.FILES)

        # Elimina los elementos numerados que ya no se envían
        current_numbers_ids = [num['id'] for num in numbers_data if 'id' in num]
        instance.numbers.exclude(id__in=current_numbers_ids).delete()

        # Actualiza o crea los elementos numerados
        for num_data in numbers_data:
            num_id = num_data.get('id', None)
            if num_id:
                numbered_item = NumberedItem.objects.get(id=num_id, note=instance)
                numbered_item.text = num_data.get('text', numbered_item.text)
                numbered_item.position = num_data.get('position', numbered_item.position)
                numbered_item.save()
            else:
                NumberedItem.objects.create(note=instance, **num_data)

        return instance

    def create_checkboxes(self, note, checkboxes_data, files, parent=None, prefix='checkbox'):
        for i, cb_data in enumerate(checkboxes_data):
          subcheckboxes_data = cb_data.pop('subcheckboxes', [])
          cb_data.pop('note', None)
          cb_data.pop('parent', None)
          cb_data.pop('delete_image', None) # Asegúrate de no pasar esta bandera al crear

          image_key = f'{prefix}_image_{i}'
          image_file = files.get(image_key, None)
          if image_file:
            cb_data['image'] = image_file

          cb_item = CheckboxItem.objects.create(note=note, parent=parent, **cb_data)

          # CORRECCIÓN: Construir el prefijo de forma recursiva para subcheckboxes
          self.create_checkboxes(note, subcheckboxes_data, files, parent=cb_item, prefix=f'{prefix}_{i}_subcheckbox')

    def update_checkboxes(self, note, checkboxes_data, files, parent=None, prefix='checkbox'):
        existing_items = CheckboxItem.objects.filter(note=note, parent=parent)
        existing_ids = set(item.id for item in existing_items)
        sent_ids = []

        for i, cb_data in enumerate(checkboxes_data):
            cb_id = cb_data.get('id', None)
            subcheckboxes_data = cb_data.pop('subcheckboxes', [])
            image_key = f'{prefix}_image_{i}'
            image_file = files.get(image_key, None)
            delete_image_flag = cb_data.get('delete_image', False) # Obtener la bandera delete_image

            # Busca el item existente
            if cb_id and cb_id in existing_ids:
                cb_item = existing_items.get(id=cb_id)
                cb_item.text = cb_data.get('text', cb_item.text)
                cb_item.checked = cb_data.get('checked', cb_item.checked)

                # Reemplaza la imagen si se envía una nueva
                if image_file:
                    if cb_item.image:
                        cb_item.image.delete(save=False)
                    cb_item.image = image_file
                # Elimina la imagen si se envía la bandera delete_image
                elif delete_image_flag:
                    if cb_item.image:
                        cb_item.image.delete(save=False)
                        cb_item.image = None
                # Si no se envía imagen nueva y no se pide borrar, mantener la existente
                elif not image_file and not delete_image_flag:
                    pass # No hacer nada con la imagen, se mantiene la existente


                cb_item.save()
            else: # Crea un nuevo item si no existe
                cb_data.pop('id', None)
                cb_data.pop('note', None)
                cb_data.pop('parent', None)
                cb_data.pop('delete_image', None) # Asegúrate de no pasar esta bandera al crear
                if image_file:
                    cb_data['image'] = image_file
                cb_item = CheckboxItem.objects.create(note=note, parent=parent, **cb_data)

            sent_ids.append(cb_item.id)
            # CORRECCIÓN: Construir el prefijo de forma recursiva para subcheckboxes
            self.update_checkboxes(note, subcheckboxes_data, files, parent=cb_item, prefix=f'{prefix}_{i}_subcheckbox')

        # Elimina los checkboxes que ya no se enviaron desde el frontend
        existing_items.exclude(id__in=sent_ids).delete()

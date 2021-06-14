import os

from django.conf import settings
from rest_framework import serializers

from files.models import File
from files.utils import generate_thumb_url


class ImageThumbSerializer(serializers.Serializer):
    size_100x100 = serializers.URLField()
    size_300x300 = serializers.URLField()

    def to_representation(self, obj: 'ImageThumbSerializer'):

        for size_field in self.get_fields():
            setattr(
                obj, size_field, generate_thumb_url(
                    content=obj.instance,
                    base_url=self.context.get('base_url') or settings.BASE_URL,
                    size=size_field.replace('size_', ''),
                )
            )

        return super().to_representation(obj)


class DefaultFileSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True)
    size = serializers.IntegerField(source='content.size', read_only=True)
    content = serializers.FileField(write_only=True)
    thumb = ImageThumbSerializer(read_only=True)

    class Meta:
        model = File
        exclude = ('user', )
        image_extensions = ('.jpg', '.jpeg', '.png',)

    def create(self, validated_data):
        content = validated_data['content']

        _, file_name = os.path.split(content.name)
        _, file_extension = os.path.splitext(file_name)

        if file_extension in self.Meta.image_extensions:
            type_ = File.TYPE_IMAGE
        else:
            type_ = File.TYPE_FILE

        validated_data.update({
            'user': self.context.get('user'),
            'file_name': file_name,
            'type': type_,
        })
        return super().create(validated_data)

    def to_representation(self, instance: File):
        instance.url = instance.generate_url(self.context.get('base_url') or settings.BASE_URL)

        if instance.type == File.TYPE_IMAGE:
            instance.thumb = ImageThumbSerializer(instance.content)

        return super().to_representation(instance)

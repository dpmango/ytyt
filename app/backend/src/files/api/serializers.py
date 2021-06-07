import os

from rest_framework import serializers
from files.models import File


class DefaultFileSerializer(serializers.ModelSerializer):
    url = serializers.URLField(read_only=True)

    class Meta:
        model = File
        exclude = ('user', )
        image_extensions = ('.jpg', '.jpeg', '.png', '.svg')
        file_extensions = ('.pdf', '.doc', 'docx', '.py')

    def create(self, validated_data):
        content = validated_data['content']

        _, file_name = os.path.split(content.name)
        _, file_extension = os.path.splitext(file_name)

        if file_extension in self.Meta.image_extensions:
            type_ = File.TYPE_IMAGE
        elif file_extension in self.Meta.file_extensions:
            type_ = File.TYPE_FILE
        else:
            type_ = File.TYPE_UNKNOWN

        validated_data.update({
            'user': self.context.get('user'),
            'file_name': file_name,
            'type': type_,
        })
        return super().create(validated_data)

    def to_representation(self, instance: File):
        instance.url = instance.generate_url(self.context.get('base_url'))

        return super().to_representation(instance)









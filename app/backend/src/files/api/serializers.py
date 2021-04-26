from rest_framework import serializers
from files.models import File


class DefaultFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        exclude = ('user', )

    def create(self, validated_data):
        validated_data.update({'user': self.context.get('user')})
        return super().create(validated_data)

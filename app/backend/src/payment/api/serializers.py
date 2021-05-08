from rest_framework import serializers, exceptions

from courses.models import Course
from payment.models import Payment


class InitCreationSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField()

    def validate(self, attrs: dict):

        course_id = attrs.pop('course_id', None)
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise exceptions.ValidationError('Курса `%s` не существует' % course_id)

        attrs['course'] = course
        return attrs

    def create(self, validated_data: dict):

        validated_data.update({
            'user': self.context.get('user'),
            'amount': validated_data['course'].cost_penny,
        })

        return self.Meta.model.objects.create(**validated_data)

    class Meta:
        model = Payment
        fields = ('course_id', )


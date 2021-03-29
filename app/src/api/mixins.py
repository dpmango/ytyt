class FlexibleSerializerModelViewSetMixin:
    def get_serializer_class(self):
        if hasattr(self, 'serializers'):
            try:
                return self.serializers[self.action]
            except (KeyError, AttributeError):
                return self.serializers['default']

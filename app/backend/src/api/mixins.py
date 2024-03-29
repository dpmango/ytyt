from django.db.models.query import QuerySet


class FlexibleSerializerModelViewSetMixin:
    def get_serializer_class(self):
        if hasattr(self, 'serializers'):
            try:
                return self.serializers[self.action]
            except (KeyError, AttributeError):
                return self.serializers['default']


class ParamsAutoFilterModelViewSetMixin:
    lookup_mapping = {}

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        kwargs = self.kwargs or {}

        # Делаем кастомную фильтрацию по разным полям из url
        query_filter = {
            lookup_param: kwargs.get(param) for param, lookup_param in self.lookup_mapping.items() if param in kwargs
        }

        return queryset.filter(**query_filter)


class PermissionsByActionModelViewSetMixin:
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

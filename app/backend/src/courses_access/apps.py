from django.apps import AppConfig


class CoursesAccessConfig(AppConfig):
    name = 'courses_access'

    def ready(self):
        import courses_access.signals  # noqa

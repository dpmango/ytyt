from django.utils import timezone


def upload_path(instance, filename):
    return '%s/%s/%s' % (timezone.now().strftime('%Y/%m'), instance.user.id, filename)

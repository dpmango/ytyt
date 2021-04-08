from rest_framework import viewsets
from rest_framework.response import Response

from courses_access.common.models import AccessBase


class ConstantsViewSet(viewsets.ViewSet):

    @staticmethod
    def export_constants(constants_list):
        result = {}
        for const_setting in constants_list:
            const_data = []
            const_titles = {}
            if len(const_setting) > 2:
                const_titles = dict(getattr(const_setting[0], const_setting[2]))

            for cls_prop in const_setting[0].__dict__.keys():

                if len(const_setting) > 4 and cls_prop == const_setting[4]:
                    continue

                if cls_prop.startswith(const_setting[1]):
                    if type(getattr(const_setting[0], cls_prop)) is str or type(getattr(const_setting[0], cls_prop)) is int:
                        val = {
                            'id': getattr(const_setting[0], cls_prop),
                            'code': cls_prop,
                            'title': const_titles.get(getattr(const_setting[0], cls_prop))
                        }

                        const_data.append(val)
            result['%s.%s' % (const_setting[0].__name__.lower().split('.')[-1], const_setting[2].lower())] = const_data
        return result

    def list(self, request):
        """
        Данный метод выводит списки всех доступных константных значений для всех моделей
        ```
        {
            "accessbase.courses_statuses": [
                {
                    "id": 1,
                    "code": "COURSES_STATUS_AVAILABLE",
                    "title": "Доступен"
                },
                {
                    "id": 2,
                    "code": "COURSES_STATUS_IN_PROGRESS",
                    "title": "В процессе"
                },
                {
                    "id": 3,
                    "code": "COURSES_STATUS_COMPLETED",
                    "title": "Завершен"
                },
                {
                    "id": 4,
                    "code": "COURSES_STATUS_BLOCK",
                    "title": "Заблокирован"
                }
            ]
        }
        ```
        """
        return Response(self.export_constants([
            [AccessBase, 'COURSES_STATUS_', 'COURSES_STATUSES'],
        ]))
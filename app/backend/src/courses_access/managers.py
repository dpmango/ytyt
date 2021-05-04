from django.db import connection
from django.db import models

from courses_access.utils import to_snake_case


class AccessManager(models.Manager):

    def count_by_status(self, to_struct: str, user_id: int, course_id, status: int = None) -> int:
        """
        Динамический метод, который по указанной структуре происзводит подсчет количества нужных статусов
        Возможные структуры:
            - Course
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Структура, в виде названия модели
        :param user_id: Уникальный id пользователя
        :param course_id: Уникальный id курса
        :param status: Статус, который необходимо учесть в подсчете. По умолчанию — только звершенные объекты
        """
        to_struct = to_snake_case(to_struct)
        status = status or self.model.STATUS_COMPLETED

        # Если запрос идет на количество законченных курсов, то сделаем запрос через django orm и вернем результат
        if to_struct == 'course':
            return self.filter(status=status, user_id=user_id).count()

        with connection.cursor() as cursor:
            sql = f"""
            SELECT count(*)
            FROM courses_access_access acc
            JOIN LATERAL jsonb_array_elements(acc.{to_struct}) obj(val) ON (obj.val ->> 'status')::INTEGER = {status}
            WHERE course_id = {course_id}
            """
            cursor.execute(sql)
            count = cursor.fetchone()

            return count[0] if count else 0

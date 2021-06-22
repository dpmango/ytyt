import typing as t
from datetime import timedelta

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models, transaction
from django.forms import model_to_dict
from django.utils import timezone

from courses.models import Course, CourseTheme, CourseLesson, LessonFragment
from courses_access.utils.any_ import force_int_pk, to_snake_case
from courses_access.utils import cache_access
from providers.mailgun.mixins import EmailNotification
from users.models import User


class Access(models.Model):
    STATUS_AVAILABLE = 1
    STATUS_IN_PROGRESS = 2
    STATUS_COMPLETED = 3
    STATUS_BLOCK = 4

    STATUSES = (
        (STATUS_AVAILABLE, 'Доступен'),
        (STATUS_IN_PROGRESS, 'В процессе'),
        (STATUS_COMPLETED, 'Завершен'),
        (STATUS_BLOCK, 'Заблокирован'),
    )

    WAITING_STATUS_COMPLETED_FRAGMENT = 5
    WAITING_STATUS_COMPLETED_LESSON = 6
    WAITING_STATUS_COMPLETED_THEME = 7
    WAITING_STATUS_PAID = 8
    WAITING_STATUSES = (
        (WAITING_STATUS_COMPLETED_FRAGMENT, 'Пройдите предыдущий фрагмент'),
        (WAITING_STATUS_COMPLETED_LESSON, 'Пройдите предыдущий урок'),
        (WAITING_STATUS_COMPLETED_THEME, 'Пройдите предыдущую тему'),
        (WAITING_STATUS_PAID, 'Не оплачено'),
    )

    AVAILABLE_STATUSES = (
        STATUS_AVAILABLE,
        STATUS_IN_PROGRESS,
        STATUS_COMPLETED
    )

    COURSE_ACCESS_TYPE_TRIAL = 1
    COURSE_ACCESS_TYPE_FULL_PAID = 2
    COURSE_ACCESS_TYPE_FULL_UNPAID = 3
    COURSE_ACCESS_TYPE_NONE = 4

    COURSE_ACCESS_TYPES = (
        (COURSE_ACCESS_TYPE_TRIAL, 'Пробный доступ'),
        (COURSE_ACCESS_TYPE_FULL_PAID, 'Оплаченный доступ'),
        (COURSE_ACCESS_TYPE_FULL_UNPAID, 'Полный неоплаченный доступ'),
        (COURSE_ACCESS_TYPE_NONE, 'Без доступа'),
    )

    AVAILABLE_ACCESS_TYPES_FULL = (
        COURSE_ACCESS_TYPE_FULL_PAID,
        COURSE_ACCESS_TYPE_FULL_UNPAID
    )

    AVAILABLE_ACCESS_TYPES = (
        *AVAILABLE_ACCESS_TYPES_FULL,
        COURSE_ACCESS_TYPE_TRIAL
    )

    BLOCK_REASON_FAST_PASSAGE = 1
    BLOCK_REASONS = (
        (BLOCK_REASON_FAST_PASSAGE, 'За сутки было пройдено две темы курса'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField('Дата обновления', auto_now=True)
    date_completed = models.DateTimeField('Дата завершения', null=True, blank=True)

    status = models.PositiveSmallIntegerField('Статус', choices=STATUSES, default=STATUS_BLOCK)

    access_type = models.PositiveSmallIntegerField('Тип доступа',
                                                   choices=COURSE_ACCESS_TYPES,
                                                   default=COURSE_ACCESS_TYPE_TRIAL)

    block_reason = models.PositiveIntegerField('Причина блокировки', choices=BLOCK_REASONS, null=True, blank=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    course_theme = models.JSONField('Доступы к темам',
                                    default=list, null=True, blank=True, encoder=DjangoJSONEncoder)

    course_lesson = models.JSONField('Доступы к урокам',
                                     default=list, null=True, blank=True, encoder=DjangoJSONEncoder)

    lesson_fragment = models.JSONField('Доступы к фрагментам',
                                       default=list, null=True, blank=True, encoder=DjangoJSONEncoder)

    manual_access = models.ManyToManyField(
        CourseLesson,
        verbose_name='Ручной доступ к уроку',
        blank=True,
        help_text='Укажите уроки, у которые будут доступны пользователю вместе с темой',
        related_name="manual_access_set",
    )

    class Meta:
        verbose_name = 'Доступ к учебным материалам'
        verbose_name_plural = 'Доступы к учебным материалам'

    def __str__(self):
        return '%s — %s' % (self.course_id, self.user.email)

    def set_empty_accesses(self) -> None:
        """
        Метод создает заблокированные доступы ко всем темам, урокам и фрагментам курса
        """
        course_themes = self.queryset_themes()
        status = self.STATUS_BLOCK

        access_themes = []
        access_course_lesson = []
        access_lesson_fragment = []

        for _theme in course_themes:
            access_themes.append(
                self._simple_struct(
                    _theme.pk, status, free_access=_theme.free_access,
                )
            )

            for _course_lesson in _theme.courselesson_set.all().order_by('order'):
                access_course_lesson.append(
                    self._simple_struct(
                        _course_lesson.pk, status, course_theme_id=_theme.pk
                    )
                )

                for _lesson_fragment in _course_lesson.lessonfragment_set.all().order_by('id'):
                    access_lesson_fragment.append(
                        self._simple_struct(
                            _lesson_fragment.pk, status, course_theme_id=_theme.pk, course_lesson_id=_course_lesson.pk,
                        )
                    )

        self.course_theme = access_themes
        self.course_lesson = access_course_lesson
        self.lesson_fragment = access_lesson_fragment

        self.save(update_fields=['course_theme', 'course_lesson', 'lesson_fragment', 'date_updated'])

    def set_trial(self) -> None:
        """
        Метод, который предоставляет доступ к бесплатной теме, которая обязательно является первой в курсе
        """
        self.set_empty_accesses()

        if len(self.course_theme) == 0:
            return None

        _theme = self.course_theme[0]
        _theme_id = _theme['pk']

        if not _theme['free_access']:
            return None

        self.course_theme[0]['status'] = self.STATUS_AVAILABLE

        for idx, _course_lesson in enumerate(self.course_lesson):
            if _course_lesson['course_theme_id'] == _theme_id:
                self.course_lesson[idx]['status'] = self.STATUS_AVAILABLE
                break

        for idx, _lesson_fragment in enumerate(self.lesson_fragment):
            if _lesson_fragment['course_theme_id'] == _theme_id:
                self.lesson_fragment[idx]['status'] = self.STATUS_AVAILABLE
                break

        self.save(update_fields=['course_theme', 'course_lesson', 'lesson_fragment', 'date_updated'])

    @transaction.atomic()
    def set_access_full_paid(self) -> None:
        """
        Метод предоставляет статус полного доступа и открывает доступ к первой платной теме, если это необходимо
        """
        self.set_access_first_theme_after_free()
        self.access_type = Access.COURSE_ACCESS_TYPE_FULL_PAID
        self.save()

    def queryset_themes(self, **_filter):
        themes = self.course.coursetheme_set.filter(**_filter)
        themes = themes.prefetch_related('courselesson_set', 'courselesson_set__lessonfragment_set')
        return themes.order_by('order')

    def set_completed_course(self) -> None:
        """
        Завершение курса пользователем
        """
        self.status = self.STATUS_COMPLETED
        self.date_completed = timezone.now()
        self.save()

    @force_int_pk
    def set_completed_course_theme(self, pk: int = None, **kwargs) -> None:
        """
        Метод закрывает выбранную тему
        :param pk: Уникальный id темы
        """
        self.set_status_course_theme(
            pk=pk, status=self.STATUS_COMPLETED, **{'date_completed': timezone.now(), **kwargs}
        )

    @force_int_pk
    def get_next_course_theme(self, pk: int = None) -> t.Optional[object]:
        """
        Метод получает следующую тему курса, если она существует
        :param pk: Уникальный id темы от которой идет отсчет
        """
        for idx, _course_theme in enumerate(self.course_theme):
            if _course_theme['pk'] == pk:
                try:
                    return self._struct_to_object(**self.course_theme[idx + 1])
                except IndexError:
                    return None
        return None

    @force_int_pk
    def set_completed_course_lesson(self, pk: int = None) -> None:
        """
        Метод закрывает выбранный урок
        :param pk: Уникальный ID урока
        """
        self.set_status_course_lesson(pk=pk, status=self.STATUS_COMPLETED, date_completed=timezone.now())

    @force_int_pk
    def get_next_course_lesson(self, pk: int = None) -> t.Optional[object]:
        """
        Метод возвращает информацию по доступу к следующему уроку, если он существует
        :param pk: Уникальный id урока
        """
        for idx, _course_lesson in enumerate(self.course_lesson):
            if _course_lesson['pk'] == pk:

                try:
                    _next_course_lesson = self.course_lesson[idx + 1]

                    if _course_lesson['course_theme_id'] == _next_course_lesson['course_theme_id']:
                        return self._struct_to_object(**_next_course_lesson)
                    return None

                except IndexError:
                    return None
        return None

    def get_direction_obj(self, to_struct: str, pk: int, direction) -> t.Optional[object]:
        """
        Метод вернет предыдущий/следующий объект для нужной структуры по ее id
        Доступыне стурктуры:
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Название структуры
        :param direction: Направление: next or prev
        :param pk: Уникальный id структуры
        """
        to_struct = to_snake_case(to_struct)

        if to_struct == 'course':
            return None

        to_struct = getattr(self, to_struct, [])

        for idx, _course_lesson in enumerate(to_struct):
            if _course_lesson['pk'] == pk:

                try:
                    if direction == 'prev':
                        need_idx = idx - 1

                        if need_idx < 0:
                            return None

                    elif direction == 'next':
                        need_idx = idx + 1

                    else:
                        return None

                    return self._struct_to_object(**to_struct[need_idx])
                except IndexError:
                    return None
        return None

    @force_int_pk
    def set_completed_lesson_fragment(self, pk: int = None) -> None:
        """
        Метод завершает фрагемент урока для пользователя
        :param pk: Уникальный id фрагмента урока
        """
        self.set_status_lesson_fragment(pk=pk, status=self.STATUS_COMPLETED, date_completed=timezone.now())

    @force_int_pk
    def get_next_lesson_fragment(self, pk: int = None) -> t.Optional[object]:
        """
        Метод получает следующий фрагмент урока
        - Если следующего фрагмента не существует — метод вернет None
        - Если у текущего и следующего фрагмента есть разница в `course_lesson_id` — метод вернет None
        :param pk: Уникальный id фрагмента урока
        """
        for idx, _lesson_fragment in enumerate(self.lesson_fragment):
            if _lesson_fragment['pk'] == pk:

                try:
                    _next_lesson_fragment = self.lesson_fragment[idx + 1]

                    if _lesson_fragment['course_lesson_id'] == _next_lesson_fragment['course_lesson_id']:
                        return self._struct_to_object(**_next_lesson_fragment)
                    return None

                except IndexError:
                    return None
        return None

    @force_int_pk
    def set_status_lesson_fragment(self, pk: int = None, status: int = None, **kwargs) -> None:
        """
        Метод устанавливает нужный стутус для фрагмента
        :param pk: Уникальный ID фрагмента
        :param status: Нужный статус для установки
        """
        for idx, _lesson_fragment in enumerate(self.lesson_fragment):
            if _lesson_fragment['pk'] == pk:
                self.lesson_fragment[idx].update({'status': status, 'date_updated': timezone.now(), **kwargs})

        self.save(update_fields=['lesson_fragment', 'date_updated'])

    @force_int_pk
    def set_status_course_lesson(self, pk: int = None, status: int = None, **kwargs) -> None:
        """
        Метод устанавливает нужный стутус для урока
        :param pk: Уникальный ID фрагмента
        :param status: Нужный статус для установки
        """
        for idx, _course_lesson in enumerate(self.course_lesson):
            if _course_lesson['pk'] == pk:
                self.course_lesson[idx].update({'status': status, 'date_updated': timezone.now(), **kwargs})

        self.save(update_fields=['course_lesson', 'date_updated'])

    @force_int_pk
    def set_status_course_theme(self, pk: int = None, status: int = None, **kwargs) -> None:
        """
        Метод устанавливает нужный статус у темы
        :param pk: Уникальный id темы
        :param status: Нужный статус для установки
        """
        for idx, _course_theme in enumerate(self.course_theme):
            if _course_theme['pk'] == pk:
                self.course_theme[idx].update({'status': status, 'date_updated': timezone.now(), **kwargs})

        self.save(update_fields=['course_theme', 'date_updated'])

    def set_access_first_theme_after_free(self) -> None:
        """
        Метод предоставляет доступ к первой теме, первому уроку, первому фрагменту после последней беспалтной темы
        Условие предоставление доступа:
            — У пользователя все бесплатные темы завершены. Иначе — оставляем все как было.
        """
        for theme in self.course_theme:
            if theme['free_access']:
                if theme['status'] != self.STATUS_COMPLETED:
                    return None
                else:
                    continue

            # Первая платная тема должна быть обработана один раз
            self.set__course_theme__course_lesson__lesson_fragment(pk=theme['pk'])
            return None

    @force_int_pk
    def set__course_lesson__lesson_fragment(self, pk: int = None) -> None:
        """
        Метод устаналивает доступ к уроку и первому фрагменту урока при наличии
        :param pk: Уникальный id урока
        """
        self.set_status_course_lesson(pk=pk, status=self.STATUS_AVAILABLE)

        for idx, _lesson_fragment in enumerate(self.lesson_fragment):
            if _lesson_fragment['course_lesson_id'] == pk:
                self.lesson_fragment[idx]['status'] = self.STATUS_AVAILABLE
                break

        self.save(update_fields=['lesson_fragment', 'date_updated'])

    @force_int_pk
    def set__course_theme__course_lesson__lesson_fragment(self, pk: int = None) -> None:
        """
        Метод устанавливает доступ к теме курса, к первому уроку и первому фрагменту урока
        :param pk: Уникальный id темы
        """
        self.set_status_course_theme(pk=pk, status=self.STATUS_AVAILABLE)

        for idx, _course_lesson in enumerate(self.course_lesson):
            if _course_lesson['course_theme_id'] == pk:
                self.set__course_lesson__lesson_fragment(pk=_course_lesson['pk'])
                break

    def update_access_structs(self, ) -> None:
        """
        Метод обновляет все структуры курса для пользователя
        """
        queryset_course_themes = self.queryset_themes()

        course_lessons = []
        lesson_fragments = []
        course_themes = self._extension_access_struct(
            to_struct='course_theme', data=queryset_course_themes
        )

        for _theme in queryset_course_themes.order_by('order'):
            _course_lessons = _theme.courselesson_set.all().order_by('order')
            course_lessons.extend(
                self._extension_access_struct(
                    to_struct='course_lesson',
                    data=_course_lessons,
                )
            )

            for _course_lesson in _course_lessons:
                _lesson_fragments = _course_lesson.lessonfragment_set.all().order_by('id')

                lesson_fragments.extend(
                    self._extension_access_struct(
                        to_struct='lesson_fragment',
                        data=_lesson_fragments,
                    )
                )

        self.course_theme = self._extension_access_status(course_themes, to_struct='course_theme')
        self.course_lesson = self._extension_access_status(course_lessons, to_struct='course_lesson')
        self.lesson_fragment = self._extension_access_status(lesson_fragments, to_struct='lesson_fragment')

        self.save(update_fields=['course_theme', 'course_lesson', 'lesson_fragment', 'date_updated'])

    def _extension_access_struct(
            self, to_struct: str, data: t.List[t.Union[CourseTheme, CourseLesson, LessonFragment]]) -> t.List[dict]:
        """
        Метод расширяет новые данные старыми статусами и дополнительными данными
        Если объект новый, то ему будет присвоен статус None для последующего определения на основе соседних объектов
        :param to_struct: Указание с какой структурой работать
        :param data: Новые для обновления
        """
        _extension_funcs_mapping = {
            'course_theme': lambda theme: dict(
                free_access=theme.free_access, pk=theme.pk
            ),
            'course_lesson': lambda course_lesson: dict(
                course_theme_id=course_lesson.course_theme.pk, pk=course_lesson.pk
            ),
            'lesson_fragment': lambda lesson_fragment: dict(
                course_theme_id=lesson_fragment.course_lesson.course_theme.pk,
                course_lesson_id=lesson_fragment.course_lesson.pk,
                pk=lesson_fragment.pk,
            ),
        }

        to_struct = to_snake_case(to_struct)
        extension_func = _extension_funcs_mapping.get(to_struct)
        extension_result = []

        for item_struct in data:
            object_old_struct = self.get_object(to_struct, pk=item_struct.pk)

            if object_old_struct:

                # Если структура ранее ожидалась на корректировку, то переводим ее немедленную корректировку, а
                # ожидание корректировки удаляем
                if cache_access.exists_pending_adjustment(to_struct, item_struct.pk):
                    cache_access.delete_pending_adjustment(to_struct, item_struct.pk)
                    kwargs_statuses = dict(status=None)

                else:
                    kwargs_statuses = dict(status=object_old_struct.status)
            else:
                kwargs_statuses = dict(status=None)

                # Если структура только добавлена, то ставим на ожидание корректировки
                cache_access.set_pending_adjustment(to_struct, item_struct.pk)

            extension_result.append(
                self._simple_struct(
                    **extension_func(item_struct), **kwargs_statuses,
                )
            )

        return extension_result

    def _extension_access_status(self, data: t.List[dict], to_struct: str) -> list:
        """
        Метод обновляет статусы для новых, ранее неизвестных, элементов структуры
        :param data: Данные для обновления статусов
        :param to_struct: Структура данных, с которой происходит работа
        """

        # Если курс завершен, то нет смысла что-то проверять, просто открываем доступ к новым/обновленным структурам
        if self.status == self.STATUS_COMPLETED:
            return [{**item, 'status': self.STATUS_AVAILABLE} for item in data]

        # Отдаем приоритет первому уроку в прогрессе
        control_index = None
        for idx, item in enumerate(data):
            if item['status'] == self.STATUS_IN_PROGRESS:
                control_index = idx

        # Если уроков в прогрессе нет, то ищем последний доступный
        if control_index is None:
            for idx, item in enumerate(data):
                if item['status'] == self.STATUS_AVAILABLE:
                    control_index = idx

        # Если последнего доступного нет, то ищем последний завершенный (Такого случить не должно, но все-таки)
        if control_index is None:
            for idx, item in enumerate(data):
                if item['status'] == self.STATUS_COMPLETED:
                    control_index = idx

        updated_struct = []
        nasty_status = self.STATUS_AVAILABLE

        # Если самый первый элемент структуры без статуса, то делаем его просто доступным
        if control_index == 0:
            status = data[control_index]['status']
            nasty_status = self.STATUS_AVAILABLE if status is None else status

        for idx, item in enumerate(data):

            if idx == control_index:
                status = data[control_index]['status']
            else:
                status = self.STATUS_BLOCK if idx > control_index else nasty_status

            updated_struct.append({**item, 'status': status, 'date_updated': timezone.now()})

        return updated_struct

    def check_manual_access(self, to_struct: str, pk: int) -> t.Optional[bool]:
        """
        Метод проверяет ручной доступ к темам/урокам/фрагментам
        Доступыне стурктуры:
            - Course
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Название структуры
        :param pk: ID элемента
        """
        to_struct = to_snake_case(to_struct)

        if to_struct == 'course':
            return self.status in self.AVAILABLE_STATUSES

        if to_struct == 'course_theme':
            # Если есть доступ к уроку, то к теме тоже должен быть
            return self.manual_access.all().filter(course_theme_id=pk).exists()

        if to_struct == 'course_lesson':
            # Если на вход получили структуру уроков, то напрямую проверяем ее
            return self.manual_access.all().filter(id=pk).exists()

        if to_struct == 'lesson_fragment':

            # Если получили фрагмент урока, то проверяем доступ к уроку через два вызова
            try:
                lesson_fragment = LessonFragment.objects.get(pk=pk)
            except LessonFragment.DoesNotExist:
                return None
            return self.manual_access.all().filter(id=lesson_fragment.course_lesson_id).exists()

    def count_by_status(self, to_struct: str, status: int = None, _where: t.Callable = None) -> int:
        """
        Метод возвращает количество элементов структуры, которые удовлетворяют статусу
        Доступыне стурктуры:
            - Course
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Название структуры
        :param status: Статус для поиска
        :param _where: дополнительное условие фильтрации
        """
        status = self.STATUS_COMPLETED if not status else status
        to_struct = to_snake_case(to_struct)

        if to_struct == 'course':
            return 1 if self.status == status else 0

        to_struct = [self._struct_to_object(**item) for item in getattr(self, to_struct, [])]

        items = [item for item in to_struct if item.status == status]
        items = list(filter(_where, items))

        return len(items)

    def get_accessible_objects(self, to_struct: str) -> list:
        """
        Метод вернет все доступыне по статусу объекты указанной структуры
        Доступыне стурктуры:
            - Course
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Название структуры
        """
        to_struct = to_snake_case(to_struct)

        if to_struct == 'course':
            return [self]

        to_struct = getattr(self, to_struct, [])
        return [
            self._struct_to_object(**item) for item in to_struct if item['status'] in self.AVAILABLE_STATUSES
        ]

    def get_objects(self, to_struct: str) -> list:
        """
        Метод вернет все объекты указанной структуры
        Доступыне стурктуры:
            - Course
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Название структуры
        """
        to_struct = to_snake_case(to_struct)

        if to_struct == 'course':
            return [self]
        return [self._struct_to_object(**item) for item in getattr(self, to_struct, [])]

    @force_int_pk
    def get_status(self, to_struct: str, pk: int) -> int:
        """
        Метод возвращает статус доступа для одной стуркутуры данных:
            - Course
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Название структуры
        :param pk: Уникальный id целевой структуры
        :return: Статус доступа
        """
        to_struct = to_snake_case(to_struct)

        if to_struct == 'course':
            return self.status

        for item in getattr(self, to_struct, []):
            if item['pk'] == pk:
                return item['status']

        return self.STATUS_BLOCK

    @force_int_pk
    def get_object(self, to_struct: str, pk: int):
        """
        Метод возвращает объект одной стуркутуры данных:
            - Course
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Название структуры
        :param pk: Уникальный id целевой структуры
        :return: Словарь, представленный объектом
        """
        to_struct = to_snake_case(to_struct)

        if to_struct == 'course':
            return self

        for item in getattr(self, to_struct, []):
            if item['pk'] == pk:
                return self._struct_to_object(**item)
        return None

    def get_learning_speed(self, to_struct: str) -> t.Optional[dict]:
        """
        Метод считает время прохождения каждого элмента для одной стуркутуры данных:
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Название структуры
        """
        to_struct = to_snake_case(to_struct)
        if to_struct == 'course':
            return None

        data = {}
        struct = getattr(self, to_struct, [])

        for item in struct:
            date_start = item.get('date_start')
            date_completed = item.get('date_completed')

            if not date_start or not date_completed:
                data[item.get('pk')] = None
            else:
                data[item.get('pk')] = (date_completed - date_start).seconds / 60

        return data

    @force_int_pk
    def change_status(self, to_struct: str, pk: int, from_status: int = None, to_status: int = None) -> None:
        """
        Метод меняет статус доступа для одной стуркутуры данных:
            - Course
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Название структуры
        :param pk: Уникальный id целевой структуры
        :param from_status: Статус, который должен иметь объяет для изменения статуса
        :param to_status: Статус, на который будет сменен статус `from_status`
        """
        to_struct = to_snake_case(to_struct)
        to_struct_method = getattr(self, f'set_status_{to_struct}')
        struct = getattr(self, to_struct, [])

        for idx, item in enumerate(struct):
            if item['pk'] != pk:
                continue

            if item['status'] != from_status:
                continue

            if from_status == self.STATUS_AVAILABLE and to_status == self.STATUS_IN_PROGRESS:
                to_struct_method(pk=pk, status=to_status, date_start=timezone.now())
            else:
                to_struct_method(pk=pk, status=to_status)

    @force_int_pk
    def check_course_permission(self) -> bool:
        """
        Метод проверяет наличие любого доступа к курсу
        """
        return bool(
            self.access_type in self.AVAILABLE_ACCESS_TYPES and
            self.status in self.AVAILABLE_STATUSES
        )

    @force_int_pk
    def check_course_theme_permission(self, pk: int = None) -> bool:
        """
        Проверка доступа к теме курса.
        Обязательные условия предоставления доступа:
            1. У юзера отсутствует блокировка к курсу
            2. У юзера нет явной блокировки к выбранной теме
        Общие условия предоставления курса:
            1. Пользователь имеет нужный доступ к теме в связи с прохождением предыдущей темы (status)
            2. Пользователь оплатил доступ к курсу
        Примечание:
            - Если выбранная тема бесплатная, то доступ предоставляется без проверки оплаты в общем порядке
        :param pk: ID темы курса
        """
        course_theme_access = self.get_object(to_struct='course_theme', pk=pk)

        if not course_theme_access:
            return False

        if course_theme_access.status == self.STATUS_BLOCK:
            return False

        if course_theme_access.free_access:
            return True

        return bool(
            course_theme_access.status in self.AVAILABLE_STATUSES and
            self.access_type in self.AVAILABLE_ACCESS_TYPES_FULL
        )

    @force_int_pk
    def check_course_lesson_permission(self, pk: int = None) -> bool:
        """
        Проверка доступа к уроку
        Обязательные условия предоставления доступа:
            1. У юзера отсутствует блокировка к курсу
            2. У юзера нет явной блокировки к выбранному уроку
        Общие условия предоставления курса:
            1. Пользователь имеет нужный доступ к уроку в связи с прохождением предыдущего урока (status)
            2. Пользователь оплатил доступ к курсу
        Примечание:
            - Если выбранная тема бесплатная, то доступ предоставляется без проверки оплаты в общем порядке
        :param pk: ID урока
        """
        course_lesson_access = self.get_object(to_struct='course_lesson', pk=pk)

        if not course_lesson_access:
            return False

        if course_lesson_access.status == self.STATUS_BLOCK:
            return False

        course_theme_access = self.get_object(to_struct='course_theme', pk=course_lesson_access.course_theme_id)
        if course_theme_access.free_access:
            return bool(course_lesson_access.status in self.AVAILABLE_STATUSES)

        return bool(
            course_lesson_access.status in self.AVAILABLE_STATUSES and
            self.access_type in self.AVAILABLE_ACCESS_TYPES_FULL
        )

    @force_int_pk
    def check_lesson_fragment_permission(self, pk: int = None) -> bool:
        """
        Проверка доступа к фрагменту урока.
        Метод отличается сигнатурой от базового метода и требует объекты курса и темы
        Обязательные условия предоставления доступа:
            1. У юзера отсутствует блокировка к курсу
            2. У юзера нет явной блокировки к выбранному фрагменту
        Общие условия предоставления курса:
            1. Пользователь имеет нужный доступ к фрагменту в связи с прохождением предыдущей темы (status)
            2. Пользователь оплатил доступ к курсу
        Примечание:
            - Если выбранная тема бесплатная, то доступ предоставляется без проверки оплаты в общем порядке
        :param pk: ID фрагмента урока
        """
        lesson_fragment_access = self.get_object(to_struct='lesson_fragment', pk=pk)

        if not lesson_fragment_access:
            return False

        if lesson_fragment_access.status == self.STATUS_BLOCK:
            return False

        course_theme_access = self.get_object(to_struct='course_theme', pk=lesson_fragment_access.course_theme_id)
        if course_theme_access and course_theme_access.free_access:
            return bool(lesson_fragment_access.status in self.AVAILABLE_STATUSES)

        return bool(
            lesson_fragment_access.status in self.AVAILABLE_STATUSES and
            self.access_type in self.AVAILABLE_ACCESS_TYPES_FULL
        )

    def check_learning_speed(self) -> t.Optional[dict]:
        """
        Проверка скорости прохождения тем курса:
        Условия пропуска проверки:
            - Пользователь является сотрудником сервиса
            - У пользователя пройдено 0 или 1 тема
        Условия блокирования доступа к курсу:
            - Разница между прохождением двух тем — менее одного дня

        :return: None or Raise
        """
        if 'coniaev2012' in self.user.email or self.user.in_stuff_groups:
            return None

        course_theme_completed = [
            self._struct_to_object(**item) for item in self.course_theme if item['status'] == self.STATUS_COMPLETED
        ]

        if len(course_theme_completed) in (0, 1):
            return None

        course_theme_access_last, course_theme_access_prev = course_theme_completed[-2:]

        now = timezone.now()
        date_completed_last = course_theme_access_last.date_completed
        date_completed_prev = course_theme_access_prev.date_completed

        if date_completed_last is None:
            date_completed_last = now
            self.set_completed_course_theme(pk=course_theme_access_last.pk, date_completed=date_completed_last)

        if date_completed_prev is None:
            date_completed_prev = now - timedelta(days=1, hours=1)
            self.set_completed_course_theme(pk=date_completed_prev.pk, date_completed=date_completed_prev)

        delta = date_completed_last - date_completed_prev
        if delta > timedelta(days=1):
            return None

        self.status = self.STATUS_BLOCK
        self.block_reason = self.BLOCK_REASON_FAST_PASSAGE
        self.save()

        mailgun = EmailNotification(
            subject_template_raw='У {email} был ограничен доступ к курсу',
            email_template_raw='Доступ к курсу ограничен по причине {block_reason}',
        )

        mailgun.send_mail({**model_to_dict(self), **model_to_dict(self.user)})
        return {
            'detail': 'Доступ к курсу временно ограничен. Пожалуйста, свяжитесь с администрацией',
            **self.get_block_reason(),
        }

    def get_block_reason(self) -> dict:
        return {'block_reason': dict(self.BLOCK_REASONS).get(self.block_reason, {})}

    @staticmethod
    def _struct_to_object(**kwargs) -> object:
        return type('AccessSimple', (), kwargs)

    @staticmethod
    def _simple_struct(pk: int, status: t.Optional[int], **kwargs) -> dict:
        """
        Метод возвращает пустую структкру для записи модели доступа
        :param pk: ID модели
        :param status: Статус доступа
        """
        return {
            'pk': pk,
            'status': status,
            'date_updated': timezone.now(),
            'date_completed': None,
            **kwargs,
        }

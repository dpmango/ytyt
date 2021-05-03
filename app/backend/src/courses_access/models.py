import typing
from datetime import timedelta

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.forms import model_to_dict
from django.utils import timezone

from courses.models import Course, CourseTheme, CourseLesson, LessonFragment
from courses_access.exceptions import AccessDenied
from courses_access.managers import AccessManager
from courses_access.utils import force_int_pk, to_snake_case
from providers.mailgun.mixins import EmailNotification
from users.models import User
from loguru import logger


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

    objects = AccessManager()

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

    def queryset_themes(self, **_filter):
        themes = self.course.coursetheme_set.filter(**_filter)
        themes = themes.prefetch_related('courselesson_set', 'courselesson_set__lessonfragment_set')
        return themes.order_by('order')

    def set_completed_course_theme(self, pk: int = None) -> None:
        """
        Метод закрывает выбранную тему
        :param pk: Уникальный id темы
        """
        for idx, _course_theme in enumerate(self.course_theme):
            if _course_theme['pk'] == pk:
                self.course_theme[idx].update({'status': self.STATUS_COMPLETED, 'date_completed': timezone.now()})

        self.save(update_fields=['course_theme', 'date_updated'])

    def get_next_course_theme(self, pk: int = None) -> typing.Optional[object]:
        """
        Метод получает следующую тему курса, если она существует
        :param pk: Уникальный id темы от которой идет отсчет
        """
        for idx, _course_theme in enumerate(self.course_theme):
            if _course_theme['pk'] == pk:
                try:
                    return self._struct_to_object(**self.course_theme[idx+1])
                except IndexError:
                    return None
        return None

    def set_completed_course_lesson(self, pk: int = None) -> None:
        """
        Метод закрывает выбранный урок
        :param pk: Уникальный ID урока
        """
        for idx, _course_lesson in enumerate(self.course_lesson):
            if _course_lesson['pk'] == pk:
                self.course_lesson[idx].update({'status': self.STATUS_COMPLETED, 'date_completed': timezone.now()})

        self.save(update_fields=['course_lesson', 'date_updated'])

    def get_next_course_lesson(self, pk: int = None) -> typing.Optional[object]:
        """
        Метод возвращает информацию по доступу к следующему уроку, если он существует
        :param pk: Уникальный id урока
        """
        for idx, _course_lesson in enumerate(self.course_lesson):
            if _course_lesson['pk'] == pk:

                try:
                    _next_course_lesson = self.lesson_fragment[idx+1]

                    if _course_lesson['course_theme_id'] == _next_course_lesson['course_theme_id']:
                        return self._struct_to_object(**_course_lesson)
                    return None

                except IndexError:
                    return None
        return None

    @force_int_pk
    def set_completed_lesson_fragment(self, pk: int = None) -> None:
        """
        Метод завершает фрагемент урока для пользователя
        :param pk: Уникальный id фрагмента урока
        """
        for idx, _lesson_fragment in enumerate(self.lesson_fragment):
            if _lesson_fragment['pk'] == pk:
                self.lesson_fragment[idx].update({'status': self.STATUS_COMPLETED, 'date_completed': timezone.now()})

        self.save(update_fields=['lesson_fragment', 'date_updated'])

    @force_int_pk
    def get_next_lesson_fragment(self, pk: int = None) -> typing.Optional[object]:
        """
        Метод получает следующий фрагмент урока
        - Если следующего фрагмента не существует — метод вернет None
        - Если у текущего и следующего фрагмента есть разница в `course_lesson_id` — метод вернет None
        :param pk: Уникальный id фрагмента урока
        """
        for idx, _lesson_fragment in enumerate(self.lesson_fragment):
            if _lesson_fragment['pk'] == pk:

                try:
                    _next_lesson_fragment = self.lesson_fragment[idx+1]

                    if _lesson_fragment['course_lesson_id'] == _next_lesson_fragment['course_lesson_id']:
                        return self._struct_to_object(**_next_lesson_fragment)
                    return None

                except IndexError:
                    return None
        return None

    def set_status_lesson_fragment(self, pk: int, status: int) -> None:
        """
        Метод устанавливает нужный стутус для фрагмента
        :param pk: Уникальный ID фрагмента
        :param status: Нужный статус для установки
        """
        for idx, _lesson_fragment in enumerate(self.lesson_fragment):
            if _lesson_fragment['pk'] == pk:
                self.lesson_fragment[idx].update({'status': status, 'date_updated': timezone.now()})

        self.save(update_fields=['lesson_fragment', 'date_updated'])

    def set_status_course_lesson(self, pk: int, status: int) -> None:
        """
        Метод устанавливает нужный стутус для урока
        :param pk: Уникальный ID фрагмента
        :param status: Нужный статус для установки
        """
        for idx, _course_lesson in enumerate(self.course_lesson):
            if _course_lesson['pk'] == pk:
                self.course_lesson[idx].update({'status': status, 'date_updated': timezone.now()})

        self.save(update_fields=['course_lesson', 'date_updated'])

    def set_status_course_theme(self, pk: int, status: int) -> None:
        """
        Метод устанавливает нужный статус у темы
        :param pk: Уникальный id темы
        :param status: Нужный статус для установки
        """
        for idx, _course_theme in enumerate(self.course_theme):
            if _course_theme['pk'] == pk:
                self.course_theme[idx].update({'status': status, 'date_updated': timezone.now()})

        self.save(update_fields=['course_theme', 'date_updated'])

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

    def update_structs(self) -> None:
        """
        Метод обновляет все структуры курса для пользователя
        """

        queryset_course_themes = self.queryset_themes()

        course_lessons = []
        lesson_fragments = []
        course_themes = self._merge(
            to_struct='course_theme',
            new_struct_data=queryset_course_themes,
        )

        for _theme in queryset_course_themes:
            _course_lessons = _theme.courselesson_set.all().order_by('order')
            course_lessons.extend(
                self._merge(
                    to_struct='course_lesson',
                    new_struct_data=_course_lessons,
                    old_struct_filter=lambda old_item: old_item.course_theme_id == _theme.pk,
                )
            )

            for _course_lesson in _course_lessons:
                _lesson_fragments = _course_lesson.lessonfragment_set.all().order_by('id')
                lesson_fragments.extend(
                    self._merge(
                        to_struct='lesson_fragment',
                        new_struct_data=_lesson_fragments,
                        old_struct_filter=lambda old_item: old_item.course_lesson_id == _course_lesson.pk,
                    )
                )

        self.course_theme = self._update_none_statuses(course_themes)
        self.course_lesson = self._update_none_statuses(course_lessons)
        self.lesson_fragment = self._update_none_statuses(lesson_fragments)

        self.save(update_fields=['course_theme', 'course_lesson', 'lesson_fragment', 'date_updated'])

    def _update_none_statuses(self, new_struct_data: typing.List[dict]) -> list:
        """
        Метод обновляет статусы для новых, ранее неизвестных, элементов структуры
        :param new_struct_data: Данные для обновления
        """

        try:
            item_in_progress_idx = [item['status'] for item in new_struct_data].index(self.STATUS_IN_PROGRESS)
        except (ValueError, IndexError):
            item_in_progress_idx = None

        if item_in_progress_idx is None:
            return [{**item, 'status': self.STATUS_BLOCK} for item in new_struct_data]

        for idx, item in enumerate(new_struct_data):
            if item.get('status') is None:
                status = self.STATUS_BLOCK if item_in_progress_idx > idx else self.STATUS_COMPLETED
                new_struct_data[idx].update({'status': status, 'date_updated': timezone.now()})

        return new_struct_data

    def _merge(self,
               to_struct: str, new_struct_data: typing.List[dict], old_struct_filter: typing.Callable = None) -> list:
        """
        Метод мерджит новые данные в старые данные структры, перенося новые данные на старые статусы
        Если структура новая, то ей проставляется статус None, который в дальнейшем доолжен быть доопределен
        Доступыне стурктуры:
            - CourseTheme
            - CourseLesson
            - LessonFragment
        :param to_struct: Название структуры
        :param new_struct_data: Новые данные для структуруы
        :param old_struct_filter: Фильтр для выборки старых данных
        """
        old_struct_data = [self._struct_to_object(**item) for item in getattr(self, to_struct, [])]
        old_struct_data = list(filter(old_struct_filter, old_struct_data))

        addition_kwargs_mapping = {
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

        get_addition_kwargs = addition_kwargs_mapping.get(to_struct)
        if len(old_struct_data) == 0:
            return [
                self._simple_struct(**get_addition_kwargs(item), status=None) for item in new_struct_data
            ]

        # Если старый объект структуры не равен объекту новой структуры и количество объектов не менялось,
        # то мы можем просто перезаписать новую структуру со старым статусом
        result = []
        for i in range(len(new_struct_data)):
            object_new_struct = new_struct_data[i]
            status = None

            try:
                status = old_struct_data[i].status
            except IndexError:
                pass

            result.append(self._simple_struct(**get_addition_kwargs(object_new_struct), status=status))

        return result

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
        struct = getattr(self, to_struct, [])

        for idx, item in enumerate(struct):
            if item['pk'] != pk:
                continue

            if item['status'] != from_status:
                continue

            getattr(self, f'set_status_{to_struct}', None)(
                pk=pk, status=to_status
            )

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

    def check_learning_speed(self):
        """
        Проверка скорости прохождения тем курса:
        Условия пропуска проверки:
            - Пользователь является сотрудником сервиса
            - У пользователя пройдено 0 или 1 тема
        Условия блокирования доступа к курсу:
            - Разница между прохождением двух тем — менее одного дня

        :return: None or Raise
        """
        if self.user.is_staff or self.user.is_superuser:
            return None

        course_theme_completed = [
            self._struct_to_object(**item) for item in self.course_theme if item['status'] == self.STATUS_COMPLETED
        ]

        if len(course_theme_completed) in (0, 1):
            return None

        course_theme_access_last, course_theme_access_prev = course_theme_completed[-2:]

        delta = course_theme_access_last.date_completed - course_theme_access_prev.date_completed
        if delta > timedelta(days=1):
            return None

        self.status = self.STATUS_BLOCK
        self.block_reason = self.BLOCK_REASON_FAST_PASSAGE
        self.save(update_fields=['status', 'block_reason', 'date_updated'])

        mailgun = EmailNotification(
            subject_template_raw='У {email} был ограничен доступ к курсу',
            email_template_raw='Доступ к курсу ограничен по причине {block_reason}',
        )

        mailgun.send_mail({**model_to_dict(self), **model_to_dict(self.user)})
        raise AccessDenied({
            'detail': 'Доступ к курсу временно ограничен. Пожалуйста, свяжитесь с администрацией',
            'block_reason': dict(self.BLOCK_REASONS).get(self.block_reason)
        })


    @staticmethod
    def _struct_to_object(**kwargs) -> object:
        return type('AccessSimple', (), kwargs)

    @staticmethod
    def _simple_struct(pk: int, status: typing.Optional[int], **kwargs) -> dict:
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

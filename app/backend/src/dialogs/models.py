import typing as t

from django import template
from django.db import models, connection
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from courses.models import CourseLesson
from courses.utils import html_to_text
from files.models import File
from users import permissions
from users.models import User


class DialogManager(models.Manager):

    def get_dialog_with_educator(self, user: User) -> t.Optional['Dialog']:
        """
        Метод вернет диалог с наставником
        :param user: Пользователь, для которого нужно найти диалог
        """
        return self.filter(
            users__in=[user, user.reviewer], with_role=permissions.GROUP_EDUCATOR
        ).distinct('id').first()

    def order_by_last_unread_message(self, **kwargs) -> t.List['Dialog']:
        """
        Метод выбирает и сортирует диалоги по последним сообщениям пользователя
        Дополнительно метод выполняет фильтрацию на две разновидности роли:
            - Суппорты
            - Все остальные
        :param kwargs: Переменные контекста sql запроса
            - with_role: Роль представителя платформы в диалоге (Указывается вместе с `is_support`)
            - is_support: Диалог происходит с супортом
            - user_id_: Пользователь, которому нужно выбрать диалоги
            - limit_: Количество запсией для выборки
            - offset_: Количество записей для пропуска
        :return: Набор диалогов в нужной сортировке
        """
        sql_template = """
            SELECT *
            FROM dialogs_dialog dd 
            INNER JOIN (
                SELECT 
                    dialog_id, 
                    max(id) AS last_message_id,
                    max(date_created) AS date_created
                FROM dialogs_dialogmessage
                GROUP BY dialog_id
            ) dm
            ON dm.dialog_id = dd.id
            INNER JOIN dialogs_dialog_users du ON dd.id = du.dialog_id
            {% if is_support %}
                WHERE 
                    dd.with_role = {{ with_role }} AND 
                    du.user_id IN (
                        SELECT U0.id
                        FROM users_user U0
                        INNER JOIN users_user_groups U1 ON U0.id = U1.user_id
                        WHERE U1.group_id = {{ with_role }}
                    )
            {% else %}
                WHERE du.user_id = {{ user_id_ }}
            {% endif %}
            ORDER BY dm.date_created DESC
            LIMIT {{ limit_ }}
            OFFSET {{ offset_ }}
        """
        sql = template.Template(sql_template).render(template.Context(kwargs))
        return self.raw(sql)

    @staticmethod
    def count_with_order_by(**kwargs) -> int:
        """
        Метод возвращает количетво записей с указанными фильтрами
        :param kwargs: Переменные контекста sql запроса
            - with_role: Роль представителя платформы в диалоге (Указывается вместе с `is_support`)
            - is_support: Диалог происходит с супортом
            - user_id_: Пользователь, которому нужно выбрать диалоги
        :return: Целочиесленное количество записей
        """
        with connection.cursor() as cursor:
            sql_template = """
                SELECT count(*)
                FROM dialogs_dialog dd 
                INNER JOIN (
                    SELECT 
                        dialog_id, 
                        max(id) AS last_message_id,
                        max(date_created) AS date_created
                    FROM dialogs_dialogmessage
                    GROUP BY dialog_id
                ) dm
                ON dm.dialog_id = dd.id
                INNER JOIN dialogs_dialog_users du ON dd.id = du.dialog_id
                {% if is_support %}
                    WHERE 
                        dd.with_role = {{ with_role }} AND 
                        du.user_id IN (
                            SELECT U0.id
                            FROM users_user U0
                            INNER JOIN users_user_groups U1 ON U0.id = U1.user_id
                            WHERE U1.group_id = {{ with_role }}
                        )
                {% else %}
                    WHERE du.user_id = {{ user_id_ }}
                {% endif %}
            """
            sql = template.Template(sql_template).render(template.Context(kwargs))

            cursor.execute(sql)
            count = cursor.fetchone()
            return count[0] if count is not None else 0


class Dialog(models.Model):

    date_created = models.DateTimeField('Дата создания', auto_now=True)
    users = models.ManyToManyField(
        User,
        verbose_name='Пользователи',
        blank=True,
        related_name="dialog_users_set",
        related_query_name="dialog_users",
    )

    with_role = models.PositiveIntegerField('Диалог с ролью', choices=permissions.GROUPS, null=True, blank=True)
    objects = DialogManager()

    def __str__(self) -> str:
        return '{%s}' % self.id + ' | '.join(map(lambda user: '(%s)%s' % (user.id, user.email), self.users.all()))

    def with_support(self) -> bool:
        return self.with_role == permissions.GROUP_SUPPORT

    def get_student(self) -> User:
        """
        Метод вернет пользователя из диалога, который является студентом
        """
        for user in self.users.all():
            if not user.in_stuff_groups and not user.is_staff:
                return user


class DialogMessageManager(models.Manager):

    _MENTOR_OR_EDUCATOR_HELLO = 'Приветствую, {student.first_name}! Меня зовут {educator.first_name}, я буду ' \
                                'сопровождать вас в ходе обучения. По любым вопросам, связанным непосредственно с ' \
                                'теорией или практикой, смело обращайтесь ко мне. А по вопросам, связанным с ' \
                                'документами, оплатой и т.д., вам с радостью помогут коллеги из соседнего чата ' \
                                '"Техническая поддержка". Желаю удачи в обучении!'

    _SUPPORT_HELLO = 'Добрый день, {student.first_name}! По любым организационным вопросам (работа с платформой, ' \
                     'оплата/документы, проблемы/претензии) без лишних раздумий пишите сюда, будем рады вам помочь. ' \
                     'Если у вас появятся предложения по улучшению платформы - вы также можете описать их прямо в ' \
                     'этом чате, и мы передадим их разработчикам.'

    def create_hello_educator(self, dialog: Dialog, from_user: User, student: User) -> None:
        """
        Метод создает приветственное сообщение для студента от препода
        :param dialog: Объект диалога
        :param from_user: Преподаватель
        :param student: Новый студент
        """
        self.create(
            dialog=dialog,
            user=from_user,
            body=self._MENTOR_OR_EDUCATOR_HELLO.format(
                educator=from_user, student=student
            )
        )

    def create_hello_support(self, dialog: Dialog, from_user: User, student: User) -> None:
        """
        Метод создает приветственное сообщение для студента от суппорта
        :param dialog: Объект диалога
        :param from_user: Суппорт
        :param student: Новый студент
        """
        self.create(
            dialog=dialog,
            user=from_user,
            body=self._SUPPORT_HELLO.format(
                student=student
            )
        )


class DialogMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(CourseLesson, on_delete=models.SET_NULL, null=True, blank=True)

    body = MarkdownxField('Сообщение', null=True, blank=True)
    reply = models.ForeignKey('DialogMessage', on_delete=models.SET_NULL, null=True, blank=True)
    file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True)

    date_created = models.DateTimeField('Дата отправления', auto_now_add=True)
    date_read = models.DateTimeField('Дата прочтения', null=True, blank=True)

    objects = DialogMessageManager()

    class Meta:
        ordering = ('date_created', )

    def get_body(self) -> str:
        return markdownify(self.body)

    def get_text_body(self) -> str:
        return html_to_text(self.get_body())

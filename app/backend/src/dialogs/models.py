from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from courses.models import CourseLesson
from courses.utils import html_to_text
from files.models import File
from users.models import User


class Dialog(models.Model):

    date_created = models.DateTimeField('Дата создания', auto_now=True)
    users = models.ManyToManyField(
        User,
        verbose_name='Пользователи',
        blank=True,
        related_name="dialog_users_set",
        related_query_name="dialog_users",
    )


class DialogMessageManager(models.Manager):

    _MENTOR_OR_EDUCATOR_HELLO = 'Приветствую, {student.first_name}! Меня зовут {mentor.first_name}, я буду ' \
                                'сопровождать вас в ходе обучения. По любым вопросам, связанным непосредственно с ' \
                                'теорией или практикой, смело обращайтесь ко мне. А по вопросам, связанным с ' \
                                'документами, оплатой и т.д., вам с радостью помогут коллеги из соседнего чата ' \
                                '"Техническая поддержка". Желаю удачи в обучении!'

    _SUPPORT_HELLO = 'Добрый день, {student.first_name}! По любым организационным вопросам (работа с платформой, ' \
                     'оплата/документы, проблемы/претензии) без лишних раздумий пишите сюда, будем рады вам помочь. ' \
                     'Если у вас появятся предложения по улучшению платформы - вы также можете описать их прямо в ' \
                     'этом чате, и мы передадим их разработчикам.'

    def create_hello(self, dialog: Dialog, from_user: User, student: User) -> None:
        """
        Метод создает приветственное сообщение для студента от необходимой роли
        :param dialog: Объект диалога
        :param from_user: Объект Пользователя, который может являться метором или суппортом
        :param student: Новый студент
        """
        if from_user.is_educator or from_user.is_mentor:
            body = self._MENTOR_OR_EDUCATOR_HELLO.format(mentor=from_user, student=student)
        else:
            body = self._SUPPORT_HELLO.format(student=student)

        self.create(dialog=dialog, user=from_user, body=body)


class DialogMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(CourseLesson, on_delete=models.SET_NULL, null=True, blank=True)

    body = MarkdownxField('Сообщение', null=True, blank=True)
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

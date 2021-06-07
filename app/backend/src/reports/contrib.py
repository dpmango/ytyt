import io
import typing

import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from courses.models import Course
from courses_access.models import Access
from dialogs.models import Dialog
from providers.mailgun.mixins import EmailNotification
from reports.configs import CONFIG
from users.models import User


class GenerateReport:
    HEADERS_HEIGHT = 30
    HEADERS_FORMAT = {
        'border': 4,
        'bold': False,
        'align': 'center',
        'valign': 'vcenter',
        'text_wrap': True
    }
    DATA_FORMAT = {
        'border': 4,
    }
    MIN_COLUMN_WIDTH = 5

    def __init__(self, report_name: str, **kwargs):
        self.workbook: typing.Optional[Workbook] = None
        self.worksheet: typing.Optional[Worksheet] = None
        self.column_auto_width = {}
        self.row_count = 0
        self.col_count = 0
        self.config = CONFIG[report_name]
        self.meta = self.config['meta']
        self.mapping = self.config['mapping']

        if kwargs.get('update_mapping', False):
            self.update_mapping()

    def update_mapping(self) -> None:
        """
        Расширяем стандартный мэппинг данными по темам и урокам курса
        """
        course = Course.objects.first()
        course_themes = course.coursetheme_set.all()

        self.mapping.extend([
            dict(
                value='learning_speed',
                set_column_auto_width=True,
                struct='course_theme',
                pk=theme.pk,
                title=theme.title,
            ) for theme in course_themes
        ])

        for course_theme in course.coursetheme_set.all():
            self.mapping.extend([
                dict(
                    value='learning_speed',
                    pk=lesson.pk,
                    set_column_auto_width=True,
                    struct='course_lesson',
                    title=lesson.title,
                ) for lesson in course_theme.courselesson_set.all()
            ])

    def process(self):
        output = io.BytesIO()
        title = self.meta['ru']

        self.workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        self.worksheet = self.workbook.add_worksheet()

        self.write_headers()
        self.write_data()
        self.write_settings()

        self.workbook.close()
        output.seek(0)

        mailgun = EmailNotification(
            subject_template_raw=title,
            email_template_raw='Сгенерирован %s. Файл во вложении' % title,
        )
        mailgun.send_mail(
            without_thread=True,
            files=[
                ('attachment', ('%s.xlsx' % title, output.read())),
            ]
        )

        return True

    def set_column_auto_width(self, column_index, value) -> None:
        """
        Устанавливает ширину колонки

        Определяем ширину колонки, для числовых типов у которых применяется формат разделителем тысяч нужно
        добавлять в ширину пробелы. Также если формат содержит % или дробную часть, то это также добавляется
        к ширине
        """
        column_width = len(str(value)) + 2
        self.column_auto_width.setdefault(column_index, self.MIN_COLUMN_WIDTH)

        if column_width > self.column_auto_width[column_index]:
            self.column_auto_width[column_index] = column_width

    def get_queryset(self) -> typing.List[User]:
        """
        Получение пользователей, которые не являются ревьюерами, а так же связанные с ними данными
        """
        query = self.meta['query']
        related_args = ('access_set', 'payment_set', 'dialogmessage_set')

        return User.objects.get_queryset().filter(query).prefetch_related(*related_args)

    def write_headers(self):
        """
        Записывает заголовок таблицы отчета.
        """
        row_index = 0
        column_index = 0
        for field in self.mapping:
            self.worksheet.write(row_index, column_index, field['title'])
            self.set_column_auto_width(column_index, field['title'])
            column_index += 1

        self.col_count = column_index
        self.worksheet.set_row(0, self.HEADERS_HEIGHT, self.workbook.add_format(self.HEADERS_FORMAT))

    def write_data(self) -> None:
        """
        Запись данных с поддержкой пагинации
        """
        queryset = self.get_queryset()
        offset = 0
        limit = 10000

        row_index = 1
        while True:
            rows = queryset[offset:limit]
            if len(rows) == 0:
                break

            for row in rows:
                self.write_data_row(row, row_index)
                row_index += 1

            offset += limit
        self.row_count = row_index

    def write_data_row(self, row, row_index):
        """
        Запись отдельного значения строки
        :param row: Одна строка для записи
        :param row_index: Индекс строки для записи
        :return:
        """
        col_index = 0
        for column in self.mapping:

            value_func = column.get('value')
            value = self.get_value(value_func, row, **column)

            self.worksheet.write(row_index, col_index, value)

            if column.get('set_column_auto_width', False) is True:
                self.set_column_auto_width(col_index, value)
            col_index += 1

    def write_settings(self) -> None:
        """
        Производим autofit и autofilter, т.е. окончательную настройку колонок
        """
        for column_index, width in self.column_auto_width.items():
            self.worksheet.set_column(column_index, column_index, width)

        self.worksheet.autofilter(0, 0, self.row_count - 1, self.col_count - 1)

    def get_value(self, value_func: typing.Union[str, typing.Callable], user: User, **kwargs):
        """
        Извлекает значение из объекта пользователя
        """
        if callable(value_func):
            return value_func(user)

        if isinstance(value_func, str):
            value_func = getattr(self, f'get_value__{value_func}', None)

            if callable(value_func):
                return value_func(user,  **kwargs)

        return None

    @staticmethod
    def get_value__learning_speed(user: User, **kwargs):
        if struct := kwargs.get('struct'):
            access: Access = user.access_set.first()
            return access.get_learning_speed(struct).get(kwargs.get('pk'))

        return None

    @staticmethod
    def get_value__last_lesson_completed(user: User, **kwargs) -> typing.Optional[int]:
        access = user.access_set.first()
        if not access:
            return None

        course_lessons = [item for item in access.course_lesson]
        last_course_lesson = None

        for course_lesson in course_lessons:
            if course_lesson['status'] == Access.STATUS_COMPLETED:
                last_course_lesson = course_lesson['pk']
        return last_course_lesson

    @staticmethod
    def get_value__average_time_answer(reviewer: User, **kwargs):
        """
        Среднее время ответа на вопрос считается как среднее время ответа на сообщение студента
        :param reviewer: Объект ревьюера
        """
        dialogs = Dialog.objects.filter(users__in=[reviewer])

        dialogs_time_answers = []
        for dialog in dialogs:
            prev_user = prev_answer_date = None
            time_answers = []

            for message in dialog.dialogmessage_set.all():
                if prev_user is None and (message.user.is_mentor or message.user.is_educator):
                    continue

                if message.user == prev_user:
                    continue

                prev_user = message.user

                if prev_answer_date is None:
                    prev_answer_date = message.date_created
                else:
                    time_answers.append((message.date_created - prev_answer_date).seconds)
                    prev_answer_date = None

            try:
                dialogs_time_answers.append(sum(time_answers) / len(time_answers))
            except ZeroDivisionError:
                pass

        try:
            mean_time_answer = sum(dialogs_time_answers) / len(dialogs_time_answers)
            mean_time_answer /= 60
        except ZeroDivisionError:
            mean_time_answer = 0

        return mean_time_answer

    @staticmethod
    def get_value__fact_of_payment(user: User, **kwargs) -> str:
        """
        Метод проверяет факт оплаты доступа к курсу
        :param user: Пользователь
        """
        fact = user.access_set.filter(access_type=Access.COURSE_ACCESS_TYPE_FULL_PAID).exists()
        if fact:
            return 'Да'
        return 'Нет'

    @staticmethod
    def get_value__date_payment(user: User, **kwargs) -> typing.Optional[str]:
        """
        Метод возвращает дату оплаты курса
        :param user: Пользователь
        """
        payment = user.payment_set.first()
        if payment and payment.date_payment:
            return payment.date_payment.strftime('%d-%m-%Y')

        payment_credit = user.paymentcredit_set.first()
        if payment_credit and payment_credit.date_approval:
            return payment.date_approval.strftime('%d-%m-%Y')

        return None

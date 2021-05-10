import io
import typing

import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from courses_access.models import Access
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

    def process(self):
        output = io.BytesIO()

        self.workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        self.worksheet = self.workbook.add_worksheet()

        self.write_headers()
        self.write_data()
        self.write_settings()

        self.workbook.close()
        output.seek(0)

        mailgun = EmailNotification(
            subject_template_raw='Отчет о пользователях',
            email_template_raw='Сгеенирован отчет о пользователях. Файл во вложении',
        )
        mailgun.send_mail(
            files=[
                ('attachment', ('%s.xlsx' % self.meta['ru'], output.read())),
            ]
        )

        return True

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
            value = self.get_value(value_func, row)

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

    def get_value(self, value_func: typing.Union[str, typing.Callable], user: User):
        """
        Извлекает значение из объекта пользователя
        """
        if callable(value_func):
            return value_func(user)

        if isinstance(value_func, str):
            value_func = getattr(self, f'get_value__{value_func}', None)

            if callable(value_func):
                return value_func(user)

        return None

    @staticmethod
    def get_value__fact_of_payment(user: User) -> str:
        """
        Метод проверяет факт оплаты доступа к курсу
        :param user: Пользователь
        """
        fact = user.access_set.filter(access_type=Access.COURSE_ACCESS_TYPE_FULL_PAID).exists()
        if fact:
            return 'Да'
        return 'Нет'

    @staticmethod
    def get_value__date_payment(user: User) -> typing.Optional[str]:
        """
        Метод возвращает дату оплаты курса
        :param user: Пользователь
        """
        payment = user.payment_set.first()
        if not payment or not payment.date_payment:
            return None
        return payment.date_payment.strftime('%d-%m-%Y')

    @staticmethod
    def get_value__last_lesson_completed(user: User) -> typing.Optional[int]:
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
    def get_value__average_time_answer(reviewer: User) -> int:
        return 10

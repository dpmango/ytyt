import typing

from django.db.models import Q
from xlsxwriter import Workbook
import io

from xlsxwriter.worksheet import Worksheet

from users.models import User
from courses_access.models import Access
import xlsxwriter


class GenerateUsersReport:

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
    MAPPING = [
        {
            'title': 'ФИО',
            'value': lambda user: user.fio,
            'set_column_auto_width': True,
        },
        {
            'title': 'Email',
            'value': lambda user: user.email,
            'set_column_auto_width': True,
        },
        {
            'title': 'Оплатил/не оплатил',
            'value': 'fact_of_payment',
            'set_column_auto_width': True,
        },
        {
            'title': 'Дата регистрации',
            'value': lambda user: user.date_joined.strftime('%d-%m-%Y'),
            'set_column_auto_width': True,
        },
        {
            'title': 'Дата оплаты',
            'value': lambda user: user,
            'set_column_auto_width': True,
        },
        {
            'title': 'Последний пройденный урок',
            'value': lambda user: user,
            'set_column_auto_width': True,
        },
        {
            'title': 'Назначенный ментор',
            'value': lambda user: user.reviewer.email,
            'set_column_auto_width': True,
        },
        {
            'title': 'Количество сообщений ревьюеру',
            'value': lambda user: user.dialogmessage_set.count(),
            'set_column_auto_width': True,
        },
    ]

    def __init__(self, users: typing.Optional[typing.List[int]] = None):
        self.workbook: typing.Optional[Workbook] = None
        self.worksheet: typing.Optional[Worksheet] = None
        self.column_auto_width = {}
        self.row_count = 0
        self.col_count = 0
        self.users = users

    def process(self):

        output = io.BytesIO()
        # https://stackoverflow.com/questions/16393242/xlsxwriter-object-save-as-http-response-to-create-download-in-django
        self.workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        self.worksheet = self.workbook.add_worksheet()

        self.write_headers()
        self.write_data()
        self.write_settings()

        self.workbook.close()
        output.seek(0)

        return True

    def write_headers(self):
        """
        Записывает заголовок таблицы отчета.
        """
        row_index = 0
        column_index = 0
        for field in self.MAPPING:
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

            users = queryset[offset:limit]
            if len(users) == 0:
                break

            for user in users:
                self.write_data_row(user, row_index)
                row_index += 1

            offset += limit
        self.row_count = row_index

    def write_data_row(self, user: User, row_index):
        """
        Запись отдельного значения строки
        :param user: Пользователь для записи
        :param row_index: Индекс строки для записи
        :return:
        """
        col_index = 0
        for column in self.MAPPING:

            value_func = column.get('value')
            value = self.get_value(value_func, user)

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
        query = Q(is_staff=False)
        related_args = ('courselessonaccess_set', 'courseaccess_set', 'dialogmessage_set')

        if isinstance(self.users, list) and len(self.users) > 0:
            query &= Q(id__in=self.users)

        return User.objects.get_queryset().filter(query).select_related(*related_args)

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
        fact = user.courseaccess_set.filter(access_type=AccessStatuses.COURSE_ACCESS_TYPE_FULL_PAID).exists()
        if fact:
            return 'Да'
        return 'Нет'


from bs4 import BeautifulSoup


def html_to_text(content: str) -> str:
    """
    Функция конвертирует html в текст без тегов
    :param content: HTML для конвертации
    :return: Очищенный текст
    """
    return ''.join(BeautifulSoup(content, features='html.parser').findAll(text=True))


def upload_path(instance, filename):
    return 'ipynb/course_%s/course_theme_%s/course_lesson_%s/%s' % (
        instance.course_theme.course_id, instance.course_theme_id, instance.pk, filename
    )

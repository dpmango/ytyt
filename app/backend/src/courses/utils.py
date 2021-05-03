from bs4 import BeautifulSoup


def html_to_text(content: str) -> str:
    """
    Функция конвертирует html в текст без тегов
    :param content: HTML для конвертации
    :return: Очищенный текст
    """
    return ''.join(BeautifulSoup(content, features='html.parser').findAll(text=True))

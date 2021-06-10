import re
import typing as t

from bs4 import BeautifulSoup as Bs
from bs4.element import ResultSet
from loguru import logger


class InlineCommandExtend:

    def __init__(self, content: str, tag_magic_command: str = None, sep_magic_command: str = None):
        self.content = Bs(content, features='html.parser')
        self.tag_magic_command = tag_magic_command or '%'
        self.sep_magic_command = sep_magic_command or '='

    def render(self) -> str:
        """
        Метод извлекает и испольняет все указанные функции из файла, а после удаляет теги
        """
        commands = self.search_commands()

        for command_tag in commands:
            command = command_tag.text.lower().replace(self.tag_magic_command, '')
            command, arg = command.split(self.sep_magic_command)

            try:
                getattr(self, '_command_%s' % command)(arg)
            except AttributeError as e:
                logger.exception('Указанной команды `%s` не существует' % (command, ), e)
            else:
                command_tag.extract()

        return self.content.decode().strip()

    def search_commands(self, return_str: bool = None) -> t.Union[str, ResultSet]:
        """
        Метод возвращает список всех инлайн-команд
        :param return_str: Сообщает в каком формате вернуть результат поиска: в текстовом или массиве
        """
        tags = self.content.find_all('p', string=re.compile(self.tag_magic_command))

        if return_str:
            return '\n\n'.join(tag.text for tag in tags) + '\n'
        return tags

    def _command_default_language(self, arg: str) -> None:
        """
        Метод устанавливает дефолтное значение языка для блока кода
        :param arg: Дефолтное значение языка
        """
        code_blocks = self.content.find_all('code', attrs={'class': None})

        for code_block in code_blocks:
            code_block.attrs = {
                **code_block.attrs, 'class': 'language-%s' % arg
            }

    def _command_brython_snippets(self, arg) -> None:
        """
        Метод устанавливает все куски кода со сниппетами без классов для инициализации в брайтон на фронте
        """
        code_blocks = self.content.find_all('code', attrs={'class': 'language-brython-snippet'})
        for code_block in code_blocks:
            code_block.attrs = {}

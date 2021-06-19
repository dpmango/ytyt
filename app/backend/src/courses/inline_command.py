import re
import typing as t
from urllib.parse import urljoin

from bs4 import BeautifulSoup as Bs
from bs4.element import ResultSet
from django.conf import settings
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
        commands = self.get_commands()
        self.call_default_commands(commands)

        for command_item in commands:
            command_tag = command_item['command_tag']
            command = command_item['command']
            arg = command_item['arg']

            try:
                getattr(self, '_command_%s' % command)(arg)
            except AttributeError as e:
                logger.exception('Указанной команды `%s` не существует' % (command, ), e)
            else:
                command_tag.extract()

        return self.content.decode().strip()

    def get_commands(self) -> t.List[dict]:
        """
        Метод вернет набор всех команд и аргументов
        :return:
        """
        commands = []
        for command_tag in self.search_commands():
            command = command_tag.text.lower().replace(self.tag_magic_command, '')
            command, arg = command.split(self.sep_magic_command)

            commands.append({
                'command_tag': command_tag, 'command': command, 'arg': arg
            })

        return commands

    def call_default_commands(self, commands: t.List[dict]) -> None:
        """
        Метод инициализирует дефолтные команды, если они не были указаны
        :param commands: Набор входящих команд
        """
        input_commands = [command_item['command'] for command_item in commands]
        for atr in self.__dir__():

            func = getattr(self, atr, None)
            if not callable(func):
                continue

            default_call = getattr(func, 'default_call', None)
            if not default_call:
                continue

            func_name = atr.replace('_command_', '')
            default_arg = getattr(func, 'default_arg', None)

            if func_name in input_commands:
                continue
            func(default_arg)

    def search_commands(self, return_str: bool = None) -> t.Union[str, ResultSet]:
        """
        Метод возвращает список всех инлайн-команд
        :param return_str: Сообщает в каком формате вернуть результат поиска: в текстовом или массиве
        """
        regex = r'%s[a-zA-Z]+=[a-zA-Z0-9]+' % self.tag_magic_command
        tags = self.content.find_all('p', string=re.compile(regex))

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

            brython_snippet = self.content.new_tag('p')
            brython_snippet.string = '[brython-snippet]%s[/brython-snippet]' % code_block.text

            code_block.parent.replace_with(brython_snippet)
            code_block.parent.extract()

    def _command_add_host_to_media(self, arg: str = None) -> None:
        """
        Дефолтная команда, которая подставляет базовый хост ко всем медиа-файлам
        :param arg: Возможный хост
        """
        base_url = arg or settings.BASE_URL
        code_blocks = self.content.find_all('img', attrs={'src': re.compile('/media/')})

        for code_block in code_blocks:
            src = code_block.attrs.get('src')
            if not src:
                continue

            code_block.attrs = {
                **code_block.attrs, 'src': urljoin(base_url, src)
            }

    _command_default_language.default_call = True
    _command_default_language.default_arg = 'python'

    _command_brython_snippets.default_call = True
    _command_brython_snippets.default_arg = 'true'

    _command_add_host_to_media.default_call = True

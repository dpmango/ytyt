import json
import typing

from loguru import logger
from payment.layout.exception import PaymentException
from abc import ABC, abstractmethod


class Layout(ABC):

    def __init__(self, cli):
        self.cli = cli
        self.errors: typing.Optional[dict] = None

    def is_valid(self, raise_exception: bool = None):
        if not self.errors or len(self.errors) == 0:
            return True

        if raise_exception:
            raise PaymentException(self.errors)
        return False

    @abstractmethod
    def receive(self, raw: dict):
        logger.info(
            '[%s][receive-raw] raw:\n%s' % (
                self._class, json.dumps(raw, indent=4, ensure_ascii=False)
            )
        )

    @property
    def _class(self) -> str:
        return self.__class__.__name__

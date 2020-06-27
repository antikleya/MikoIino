# -*- coding: utf-8 -*-
from utils import class_construct


class Context(object):
    _contextName = None
    _error = None

    @class_construct
    def __init__(self, contextName="None", error="None"):
        self._contextName = contextName
        self._error = error

    @property
    def name(self) -> str:
        return self._contextName

    @property
    def error(self) -> str:
        return self._error

    def is_parameter_passed(self, name: str) -> bool:
        return name in self.__dict__

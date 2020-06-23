# -*- coding: utf-8 -*-

import json
import pkg_resources

from core.logger import debug


class JsonHandler(object):
    """
    Handler for simple get stuff like a LoL servers and LoL roles
    """

    _servers = None
    _roles = None
    _messages = None
    _TAG = "JsonHandler"

    def __init__(self):
        self._resource_package = __name__

        self._resource_path = '/'.join(('../static', 'data.json'))
        template = pkg_resources.resource_stream(self._resource_package, self._resource_path)
        line = template.read().decode('utf-8')
        self._servers = json.loads(line)['servers']
        self._roles = json.loads(line)['roles']
        debug(self._TAG, "Get servers and roles")
        template.close()

        self._resource_path = '/'.join(('../static', 'messages.json'))
        template = pkg_resources.resource_stream(self._resource_package, self._resource_path)
        line = template.read().decode('utf-8')
        self._messages = json.loads(line)
        debug(self._TAG, "Get servers and roles")
        template.close()

    @property
    def servers(self):
        """
        Get all LoL servers
        :return: all LoL servers
        :rtype: list
        """

        return self._servers

    @property
    def roles(self):
        """
        Get all LoL roles
        :return: all LoL roles
        :rtype: list
        """

        return self._roles

    @property
    def messages(self):
        """
        Get all messages what bot can send
        :return: all messages what bot can send
        :rtype: dict
        """

        return self._messages


json_handler = JsonHandler()

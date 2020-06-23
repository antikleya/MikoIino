# -*- coding: utf-8 -*-
import json
import pkg_resources

from utils.logger import debug


class JsonHandler(object):
    """
    Handler for simple get stuff like a LoL servers and LoL lanes
    """

    _servers = None
    _lanes = None
    _messages = None
    _channels = None
    _commands = None
    _token = None

    _TAG = "JsonHandler"

    def __init__(self):
        self._resource_package = __name__

        self._resource_path = '/'.join(('../static', 'lol_data.json'))
        template = pkg_resources.resource_stream(self._resource_package, self._resource_path)
        line = template.read().decode('utf-8')
        self._servers = json.loads(line)['servers']
        self._lanes = json.loads(line)['lanes']
        debug(self._TAG, "Get servers and lanes")
        template.close()

        self._resource_path = '/'.join(('../static', 'messages.json'))
        template = pkg_resources.resource_stream(self._resource_package, self._resource_path)
        line = template.read().decode('utf-8')
        self._messages = json.loads(line)
        debug(self._TAG, "Get messages")
        template.close()

        self._resource_path = '/'.join(('../static', 'auth_consts.json'))
        template = pkg_resources.resource_stream(self._resource_package, self._resource_path)
        line = template.read().decode('utf-8')
        self._token = json.loads(line)['token']
        debug(self._TAG, "Get auth token")
        template.close()

        self._resource_path = '/'.join(('../static', 'channels.json'))
        template = pkg_resources.resource_stream(self._resource_package, self._resource_path)
        line = template.read().decode('utf-8')
        self._channels = json.loads(line)
        debug(self._TAG, "Get list of channels")
        template.close()

        self._resource_path = '/'.join(('../static', 'commands.json'))
        template = pkg_resources.resource_stream(self._resource_package, self._resource_path)
        line = template.read().decode('utf-8')
        self._commands = json.loads(line)
        debug(self._TAG, "Get list of commands")
        template.close()

    @property
    def servers(self) -> list:
        """
        Get all LoL servers
        """

        return self._servers

    @property
    def lanes(self) -> list:
        """
        Get all LoL lanes
        """

        return self._lanes

    @property
    def messages(self) -> dict:
        """
        Get all messages what bot can send
        """

        return self._messages

    @property
    def token(self) -> str:
        """
        Get auth token
        """

        return self._token

    @property
    def channels(self) -> int:
        """
        Get list of channels for bot
        """

        return self._channels

    @property
    def commands(self) -> list:
        """
        Get list of commands for bot
        """

        return self._commands['commands']


json_handler = JsonHandler()

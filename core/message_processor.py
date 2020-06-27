# -*- coding: utf-8 -*-
import re

import discord

from core import Context
from utils import class_construct, debug, error, warning
from utils import json_handler, is_word_in_list


class MessageProcessor(object):
    _TAG = None

    @class_construct
    def __init__(self):
        self._TAG = "MessageProcessor"

    def preprocess(self, message: 'discord.Message') -> Context:
        """
        Preprocess user's message for CommandProcessor

        :param message: user's message

        :return: Context object for command execute
        """
        message_for_send = re.search(r'\"(.*)\"', message.content)
        message_for_process = " ".join(re.split(r' \".*\"', message.content))

        split_msg = message_for_process.lower().split()
        context = Context(split_msg[0])

        context.lanes = []
        context.lanes_name = []
        context.servers = []
        context.servers_name = []
        context.message = message_for_send.group(1) if message_for_send else ""

        for word in split_msg[1:]:
            lane = is_word_in_list(word, json_handler.lanes.keys())
            server = is_word_in_list(word, json_handler.servers.keys())

            if lane:
                debug(self._TAG, "Find lane " + lane)
                context.lanes.append(json_handler.lanes[lane])
                context.lanes_name.append(lane)
            elif server:
                debug(self._TAG, "Find server " + server)
                context.servers.append(json_handler.servers[server])
                context.servers_name.append(server)
            else:
                debug(self._TAG, "Find useless part of message " + word)

        return context

    def postprocess(self, msg_context: Context) -> tuple:
        """
        Postprocess data from command, create message from it and prepare it for send

        :param msg_context: context for postprocessing.
        Context must provide list of users, message of type "str" and channel of type "discord.Channel" for send it.
        If message not present Context must provide names of lanes and servers.

        :return: channel and message for send

        :rtype: tuple
        """

        if msg_context.name == "UserError":
            error(self._TAG, "Get user error Context")
            return None, msg_context.error

        if msg_context.name == "Error":
            error(self._TAG, "Get error Context")
            return None, None

        if not msg_context.is_parameter_passed("users"):
            error(self._TAG, "No users has been passed")
            return None, None

        if not msg_context.is_parameter_passed("message"):
            warning(self._TAG, "No message has been passed")

            if not msg_context.is_parameter_passed("lanes_name"):
                error(self._TAG, "No lanes names have been passed")
                return None, None

            if not msg_context.is_parameter_passed("servers_name"):
                error(self._TAG, "No servers names have been passed")
                return None, None

        if not msg_context.is_parameter_passed("channel"):
            error(self._TAG, "No channel has been passed")
            return None, None

        if msg_context.users:
            if msg_context.message:
                debug(self._TAG, "Find message " + msg_context.message)
                msg = msg_context.message
            else:
                debug(self._TAG, "No message has been found")
                msg = "List of " + ", ".join(msg_context.lanes_name) + " on " + \
                      ", ".join(msg_context.servers_name) + " server:\n"

            for user in msg_context.users:
                debug(self._TAG, "Find user " + user.name)
                msg += " <@{.id}> ".format(user)
        else:
            debug(self._TAG, "Nothing has been founded")
            msg = 'There is no one you are looking for'

        return msg_context.channel, msg

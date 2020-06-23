# -*- coding: utf-8 -*-
import discord

from core import Context
from utils import json_handler, debug, error, is_word_in_list


class MessageProcessor(object):
    _TAG = None

    def __init__(self):
        self._TAG = "MessageProcessor"

    def preprocess(self, message: 'discord.Message') -> Context:
        """
        Preprocess user's message for command processor
        :param message: user's message
        :return: context for command
        """
        split_msg = message.content.lower().split()
        context = Context()

        context.command = split_msg[0]
        context.lanes = []
        context.lanes_name = ""
        context.servers = []
        context.servers_name = ""
        context.message = ""

        for word in split_msg[1:]:
            if is_word_in_list(word, json_handler.lanes.keys()):
                debug(self._TAG, "Find lane " + word)
                context.lanes.append(json_handler.lanes[word])
                if context.lanes_name != "":
                    context.lanes_name += ", "
                context.lanes_name += word
            elif is_word_in_list(word, json_handler.servers.keys()):
                debug(self._TAG, "Find server " + word)
                context.servers.append(json_handler.servers[word])
                if context.servers_name != "":
                    context.servers_name += ", "
                context.servers_name += word
            else:
                debug(self._TAG, "Find part of message " + word)
                context.message += word
                context.message += " "

        return context

    def postprocess(self, msg_context: Context) -> tuple:
        """
        Postprocess data from command, create message from it and prepare it for send
        :param msg_context: context for postprocessing
        :return: channel and message for send
        :rtype: tuple
        """

        try:
            if msg_context.users:
                if msg_context.message:
                    debug(self._TAG, "Find message " + msg_context.message)
                    msg = msg_context.message
                else:
                    debug(self._TAG, "No message has been founded")
                    msg = "List of " + msg_context.lanes_name + " on " + msg_context.servers_name + " server:\n"

                for user in msg_context.users:
                    debug(self._TAG, "Find user " + user.name)
                    msg += " <@{.id}> ".format(user)
            else:
                debug(self._TAG, "Nothing has been founded")
                msg = 'There is no one you are looking for'

            return msg_context.channel, msg
        except AttributeError:
            error(self._TAG, "One of parameters haven't been founded!")
            return msg_context.channel, None

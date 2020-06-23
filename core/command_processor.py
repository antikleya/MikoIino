# -*- coding: utf-8 -*-
import discord
import os

from core import Context
from utils import json_handler, intersection, error, debug


class CommandProcessor(object):
    _guild = None
    _TAG = None
    _context = None
    _server_roles = {}
    _commands = {}

    def __init__(self, guild: "discord.Guild"):
        self._guild = guild
        self._TAG = "CommandProcessor"

        self._commands = {
            "/find": self._find_lane
        }

        for role in guild.roles:
            self._server_roles[role.id] = role

    def execute_command(self, context: Context) -> Context:
        """
        Call function for command
        """

        self._context = context

        try:
            return self._commands[self._context.command]()
        except AttributeError:
            error(self._TAG, "No commands were passed")
            return Context()

    def _find_lane(self) -> Context:
        """
        Function for find user on given LoL servers for given lanes
        """

        self._context.users = []

        try:
            for member in self._guild.members:
                if not member.bot and member.status != discord.Status.offline \
                        and (intersection([role.id for role in member.roles], self._context.servers)) \
                        and (intersection([role.id for role in member.roles], self._context.lanes)):
                    self._context.users.append(member)
        except AttributeError:
            error(self._TAG, "No servers or lanes were passed")
            self._context.users = []

        debug(self._TAG, os.environ['MIKO_TEST'])

        if os.environ['MIKO_TEST'] == "1":
            self._context.channel = self._guild.get_channel(json_handler.channels['test_channel'])
        else:
            self._context.channel = self._guild.get_channel(json_handler.channels['miko_channel'])

        return self._context

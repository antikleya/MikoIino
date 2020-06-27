# -*- coding: utf-8 -*-
import discord

from core import Context
from utils import error, class_construct
from utils import json_handler, intersection


class CommandProcessor(object):
    _guild = None
    _TAG = None
    _context = None
    _server_roles = {}
    _commands = {}

    @class_construct
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

        :param context: Context must provide command name as his name and it's parameters for execute
        """

        self._context = context

        if self._context.name not in self._commands:
            error(self._TAG, "No commands has been passed")
            return Context("Error", "No commands has been passed")

        return self._commands[self._context.name]()

    def _find_lane(self) -> Context:
        """
        Function for find user on given LoL servers for given lanes.
        Context must provide fields "lanes" and "servers" of "list" type for find users

        :return: list of selected users as Context field "users"
        :rtype: Context
        """

        if not self._context.is_parameter_passed("servers") or not self._context.servers:
            error(self._TAG, "No servers has been passed")
            return Context("UserError", "No servers has been passed")

        if not self._context.is_parameter_passed("lanes") or not self._context.lanes:
            error(self._TAG, "No lanes has been passed")
            return Context("UserError", "No lanes has been passed")

        self._context.users = []

        for member in self._guild.members:
            if not member.bot and member.status != discord.Status.offline \
                    and (intersection([role.id for role in member.roles], self._context.servers)) \
                    and (intersection([role.id for role in member.roles], self._context.lanes)):
                self._context.users.append(member)

        self._context.channel = self._guild.get_channel(json_handler.bot_channel)

        return self._context

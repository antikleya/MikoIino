# -*- coding: utf-8 -*-
import discord

from core import CommandProcessor, MessageProcessor
from utils import debug, info
from utils import json_handler
from . import client

global cp
global mp
TAG = "EventHandler"


@client.event
async def on_ready() -> None:
    global cp
    global mp
    cp = CommandProcessor(client.guilds[0])
    mp = MessageProcessor()
    print('Ready!')


@client.event
async def on_message(message: 'discord.Message') -> None:
    for command in json_handler.commands:
        if message.content.startswith(command):
            info(TAG, "Receive command " + command)
            debug(TAG, "Received message: " + message.content)

            context = mp.preprocess(message)
            msg_context = cp.execute_command(context)
            channel, msg = mp.postprocess(msg_context)

            if channel:
                debug(TAG, "Send message \"" + msg + "\" to \"" + channel.name + "\"")
                await channel.send(msg)
            elif msg:
                debug(TAG, "Send message \"" + msg + "\" to \"" + message.channel.name + "\"")
                await message.channel.send(msg)
            else:
                debug(TAG, "Send error message to \"" + message.channel.name + "\"")
                await message.channel.send(json_handler.messages['internal_error'])

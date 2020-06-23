# -*- coding: utf-8 -*-
from utils import debug, info, json_handler
from core import CommandProcessor, MessageProcessor
from . import client

import discord

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
            info(TAG, "Receive command")
            debug(TAG, "Received message: " + message.content)

            context = mp.preprocess(message)
            msg_context = cp.execute_command(context)
            channel, msg = mp.postprocess(msg_context)

            debug(TAG, channel.name + " " + msg)

            if msg:
                await channel.send(msg)
            else:
                await channel.send(json_handler.messages['internal_error'])

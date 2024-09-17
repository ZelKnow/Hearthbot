#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : auto_reply.py
@Description   : Auto reply.
@Date          : 2024/09/17 20:23:46
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.rule import to_me
from nonebot.typing import T_State

at_message = on_message(rule=to_me(), priority=10, block=True)


@at_message.handle()
async def auto_reply(bot: Bot, event: Event, state: T_State):
    if bot.config.auto_reply:
        await at_message.finish(bot.config.auto_reply)

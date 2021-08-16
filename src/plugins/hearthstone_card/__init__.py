#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : __init__.py
@Description   : Main plugin for Hearthstone card, including card pic, card tags and so on.
@Date          : 2021/08/06 16:25:36
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

from nonebot import get_driver
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
from .card_handler import CardHandler
from nonebot.adapters.cqhttp.message import MessageSegment
from .utils import supported_langs
from nonebot.message import handle_event
cardhandler = CardHandler()
global_config = get_driver().config

hearthstone_card = on_command("card", aliases={"c", "C", "CARD", "Card"},
                              state={"type": "card"}, priority=0)
hearthstone_tags = on_command("tags", aliases={"t", "T", "TAGS", "Tags", "tag"},
                              state={"type": "tags"}, priority=1)
max_response = global_config.max_response


@hearthstone_tags.handle()
@hearthstone_card.handle()
async def handle_frist_receive(bot: Bot, event: Event, state: T_State):
    parts = str(event.get_message()).strip().lower().split()
    state['terms'] = []
    state['args'] = {'lang': 'zhCN'}
    for part in parts:
        if not handle_args(part, state["args"]):
            state['terms'].append(part)
    state['cards'], state['hint'] = cardhandler.first_handle(
        state['terms'], max_response)
    if len(state['cards']) == 1:
        msg = hscard_msg(state['cards'][0], state['args'], state["type"])
        await bot.send(event, msg)
    elif len(state['cards']) == 0:
        await hearthstone_card.finish(state['hint'])
    else:
        await hearthstone_card.pause(state['hint'])


@hearthstone_tags.handle()
@hearthstone_card.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    raw = str(event.get_message()).strip()
    if raw.startswith('\\') or raw.startswith('/'):
        try:
            card = state['cards'][int(raw[1:])-1]
        except Exception as e:
            await hearthstone_card.reject("卡牌编号输入有误，请重新输入")
        msg = hscard_msg(card, state['args'], state["type"])
        await hearthstone_card.reject(msg)
    elif raw.isdigit():
        page = int(raw)
        state['hint'] = cardhandler.second_handle(
            state['cards'], page, max_response)
        await hearthstone_card.reject(state['hint'])
    else:
        await handle_event(bot, event)
        await hearthstone_card.finish()


def handle_args(part, args):
    if len(part) == 4:
        lang = part[0:2].lower()+part[2:4].upper()
        if lang in supported_langs:
            args['lang'] = lang
            return True
    return False


def hscard_msg(card, args, type):
    print(args)
    if type == "card":
        url = cardhandler.get_pic(card, args)
        return MessageSegment.image(url)
    elif type == "tags":
        tags = cardhandler.get_tags(card, args)
        return tags

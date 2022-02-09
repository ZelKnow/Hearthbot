#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : __init__.py
@Description   : Main plugin for Hearthstone card, including card pic, card tags.
@Date          : 2021/08/06 16:25:36
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

import re
from nonebot import get_driver
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .card_handler import CardHandler, supported_langs
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.message import handle_event

global_config = get_driver().config
max_response = global_config.max_response
Blizz_ID = global_config.blizz_id
Blizz_Sec = global_config.blizz_sec

cardhandler = CardHandler(Blizz_ID, Blizz_Sec)

hearthstone_card = on_command("card",
                              aliases={"c", "C", "CARD", "Card"},
                              state={"type": "card"},
                              priority=0)
hearthstone_tags = on_command("tags",
                              aliases={"t", "T", "TAGS", "Tags", "tag"},
                              state={"type": "tags"},
                              priority=1)
hearthstone_ori = on_command("ori",
                             aliases={"o", "O", "ORI", "Ori", "art"},
                             state={"type": "ori"},
                             priority=2)


@hearthstone_ori.handle()
@hearthstone_tags.handle()
@hearthstone_card.handle()
async def handle_frist_receive(bot: Bot, event: Event, state: T_State):
    parts = str(event.get_message()).strip().lower().split()
    state["terms"] = []
    state["args"] = {"lang": "zhCN", "is_bgs": False}
    for part in parts:
        if not handle_args(part, state["args"]):
            state["terms"].append(part)
    state["cards"], state["hint"] = cardhandler.first_handle(
        state["terms"], state["args"]["is_bgs"], max_response)
    if len(state["cards"]) == 1:
        msg = await hscard_msg(state["cards"][0], state["args"], state["type"])
        await bot.send(event, msg)
    elif len(state["cards"]) == 0:
        await hearthstone_card.finish(state["hint"])
    else:
        await hearthstone_card.pause(state["hint"])


@hearthstone_ori.handle()
@hearthstone_tags.handle()
@hearthstone_card.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    raw = str(event.get_message()).strip()
    if re.match(r"[\\/]\s*[1-9]\d*$", raw):
        num = int(raw[1:]) - 1
        if num > len(state["cards"]):
            await hearthstone_card.reject("输入的编号超过结果总数量，请重新输入。")
        card = state["cards"][num]
        msg = await hscard_msg(card, state["args"], state["type"])
        await hearthstone_card.reject(msg)
    elif raw.isdigit():
        page = int(raw)
        state["hint"] = cardhandler.second_handle(state["cards"], page,
                                                  state["args"]["is_bgs"],
                                                  max_response)
        await hearthstone_card.reject(state["hint"])
    else:
        await handle_event(bot, event)
        await hearthstone_card.finish()


def handle_args(part, args):
    if len(part) == 4:
        lang = part[0:2].lower() + part[2:4].upper()
        if lang in supported_langs:
            args["lang"] = lang
            return True
    elif part.lower() in ["bg", "bgs"]:
        args["is_bgs"] = True
        return True
    return False


async def hscard_msg(card, args, type):
    if type == "card":
        url = await cardhandler.get_pic(card, args)
        return MessageSegment.image(url, timeout=10)
    elif type == "tags":
        tags = cardhandler.get_tags(card, args)
        return tags
    elif type == "ori":
        url = cardhandler.get_ori(card)
        return MessageSegment.image(url, timeout=10)

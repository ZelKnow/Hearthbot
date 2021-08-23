#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : __init__.py
@Description   : Main plugin for Hearthstone deck.
@Date          : 2021/08/18 09:59:52
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

from nonebot import on_command
from nonebot.plugin import on_keyword
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.adapters import Bot, Event
from nonebot.log import logger
from .deck_handler import DeckHandler, supported_locale
import re
import base64
from io import BytesIO
import traceback

deck_handler = DeckHandler()

hearthstone_deck = on_command("deck",
                              aliases={"d", "D", "DECK", "Deck"},
                              priority=0)
deck_keyword = on_keyword("AAE", priority=3)


@hearthstone_deck.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    parts = str(event.get_message()).split()
    locale = "zhCN"
    if len(parts[0][1:]) == 4:
        lang = parts[0][1:]
        if lang[0:2].lower() + lang[2:4].upper() in supported_locale:
            locale = lang
            parts = parts[1:]
        else:
            await hearthstone_deck.finish("不支持该语言")
    decks, names = handle_args(parts)
    deck_imgs = []
    for i in range(len(decks)):
        try:
            img = deck_handler.deck_to_image(decks[i], names[i], locale)
        except Exception as e:
            logger.error(traceback.format_exc())
            await hearthstone_deck.finish("卡组生成失败，请检查代码及命令格式！")
        deck_imgs.append(img)
    img = deck_handler.merge(deck_imgs)
    img = img.convert('RGB')
    msg = get_img_msg(img)
    await bot.send(event, msg)


@deck_keyword.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    m = re.search(r"AAE[+-0123456789=A-Z/a-z ]{50,140}",
                  str(event.get_message()))
    if m:
        deck = m.group(0)
        try:
            img = deck_handler.deck_to_image(deck, "")
        except Exception as e:
            logger.error(traceback.format_exc())
            await deck_keyword.finish()
        img = img.convert('RGB')
        msg = get_img_msg(img)
        await deck_keyword.finish(msg)


def handle_args(parts):
    if parts[-1].startswith("AAE"):
        decks = parts
        names = [""] * (len(parts))
    elif parts[1].startswith("AAE"):
        decks = parts[:-1]
        names = [parts[-1]] * (len(parts) - 1)
    else:
        decks = parts[::2]
        names = parts[1::2]
    return decks, names


def get_img_msg(img):
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return MessageSegment.image("base64://" + str(base64_str)[2:-1])

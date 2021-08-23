#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : help.py
@Description   : Send help message.
@Date          : 2021/08/19 15:51:12
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

from nonebot import get_driver
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.rule import to_me
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.message import handle_event

help = on_command("help", aliases={"帮助", "h", "HELP", "Help"}, priority=3)


@help.handle()
async def send_help_msg(bot: Bot, event: Event, state: T_State):
    msg = """使用帮助：
    本机器人可查询炉石卡牌、生成卡组图片。
    1）使用命令 “!card 卡牌名称” 即可查询卡牌图片。使用命令 “!tags 卡牌名称” 即可查询卡牌文字信息。使用命令 “!ori 卡牌名称” 查询卡牌原画。
    1.1)可进行多关键字查询，如“!card 雷诺 神奇”
    1.2)如要查找战棋随从，请在关键字中添加一个bgs，如“!card 鱼人 bgs”
    1.3)如要查找其他语言版本，请在关键字中添加语言代码，如“!card 鱼人 enUS”
    2) 使用命令 “!deck 卡组代码 卡组名称（可选）” 即可生成卡组图片。
    2.1) deck命令也可以实现多卡组拼成一张图，“!deck 卡组1代码 卡组1名称 卡组2代码 卡组2名称 ......”
    2.2) 上述卡组名称可以省略，或在最后带上卡组名称，这样每个卡组都会命成同一个名称
    2.3) 上述卡组名称可以省略，或在最后带上卡组名称，这样每个卡组都会命成同一个名称
    2.4）如要输出英文卡图，请使用命令“!deck.enUS 代码”
    3)可以只输入命令的首字母，如“!c 银背组长”"""
    await help.finish(msg)

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : auto_agree.py
@Description   : Auto agree requests.
@Date          : 2021/08/19 15:44:46
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"


from nonebot import on_request
from nonebot.adapters.cqhttp import Bot, FriendRequestEvent, GroupRequestEvent
from nonebot.typing import T_State


friend_req = on_request(priority=5)


@friend_req.handle()
async def friend_agree(bot: Bot, event: FriendRequestEvent, state: T_State):
    if bot.config.auto_agree or str(event.user_id) in bot.config.superusers:
        await bot.set_friend_add_request(flag=event.flag, approve=True)


group_invite = on_request(priority=5)


@group_invite.handle()
async def group_agree(bot: Bot, event: GroupRequestEvent, state: T_State):
    if bot.config.auto_agree or (event.sub_type == "invite" and
                                 str(event.user_id) in bot.config.superusers):
        await bot.set_group_add_request(flag=event.flag, sub_type="invite",
                                        approve=True)

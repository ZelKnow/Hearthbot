#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : bot.py
@Description   : Entry File of the Bot
@Date          : 2021/08/06 15:45:54
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

config = driver.config
nonebot.load_all_plugins(set(config.plugins), set(config.plugin_dirs))

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
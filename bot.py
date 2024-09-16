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
from nonebot.adapters.qq import Adapter as QQAdapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(QQAdapter)

config = driver.config
nonebot.load_all_plugins(set(config.plugins), set(config.plugin_dirs))

if __name__ == "__main__":
    nonebot.run()
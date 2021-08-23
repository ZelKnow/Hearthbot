#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : utils.py
@Description   : 
@Date          : 2021/08/20 08:49:05
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

from hearthstone.cardxml import load_dbf

_CARD_DATA_CACHE = {}


def card_db():
    if "db" not in _CARD_DATA_CACHE:
        db, _ = load_dbf()
        _CARD_DATA_CACHE["db"] = db
    return _CARD_DATA_CACHE["db"]

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : rules.py
@Description   :
@Date          : 2021/08/19 22:09:16
@Author        : HearthSim
@Github        : https://github.com/HearthSim
"""
__author__ = "HearthSim"

from hearthstone.enums import CardType, GameTag

from .utils import card_db

db = card_db()


def is_highlander_deck(data_point):
    return len(data_point["cards"]) == 30


def is_quest_deck(data_point):
    for dbf_id in data_point["cards"]:
        card = db[int(dbf_id)]
        if GameTag.QUEST in card.tags:
            return True
    return False


def is_quest_line_deck(data_point):
    for dbf_id in data_point["cards"]:
        card = db[int(dbf_id)]
        if GameTag.QUESTLINE in card.tags:
            return True
    return False


def is_even_only_deck(data_point):
    for dbf_id in data_point["cards"]:
        card = db[int(dbf_id)]
        if card.cost % 2 != 0:
            return False
    return True


def is_odd_only_deck(data_point):
    for dbf_id in data_point["cards"]:
        card = db[int(dbf_id)]
        if card.cost % 2 != 1:
            return False
    return True


def is_no_minion_deck(data_point):
    for dbf_id in data_point["cards"]:
        card = db[int(dbf_id)]
        if (card.type != CardType.SPELL and dbf_id != 61503):
            return False
    return True


FALSE_POSITIVE_RULES = {
    "is_highlander_deck": is_highlander_deck,
    "is_quest_deck": is_quest_deck,
    "is_even_only_deck": is_even_only_deck,
    "is_odd_only_deck": is_odd_only_deck,
    "is_quest_line_deck": is_quest_line_deck
}

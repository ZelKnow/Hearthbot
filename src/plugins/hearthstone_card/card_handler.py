#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : card_handler.py
@Description   : Handle Hearthstone card.
@Date          : 2021/08/12 22:40:39
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

from hearthstone import cardxml
from hearthstone.cardxml import CardXML
from hearthstone.enums import CardType, GameTag, Race, Rarity, MultiClassGroup, CardSet
from .utils import set_map, class_map, multiclass_map, type_map, rarity_map, race_map
import operator
import math


def card_compare(a, b):
    if a.collectible == b.collectible:
        if a.card_set.is_standard == b.card_set.is_standard:
            return a.card_set.numerator > b.card_set.numerator
        else:
            return a.card_set.is_standard
    else:
        return a.collectible


def loc_name(self, locale):
    return self.strings[GameTag.CARDNAME][locale]


def set_name(self, locale):
    return self.strings[GameTag.CARD_SET][locale]


def loc_text(self, locale):
    return self.strings[GameTag.CARDTEXT_INHAND][locale]


def loc_flavor(self, locale):
    return self.strings[GameTag.FLAVORTEXT][locale]


CardXML.loc_name = loc_name
CardXML.loc_text = loc_text
CardXML.loc_flavor = loc_flavor


class CardHandler():
    def __init__(self):
        db, _ = cardxml.load()
        self.cards_list = self._init_cards(db)
        self.bgs_list = self._init_bgs(db)

    def _init_cards(self, db):
        cards_list = []
        for card in db:
            if db[card].type != CardType.ENCHANTMENT:
                cards_list.append(db[card])
        cards_list.sort(key=operator.attrgetter("collectible",
                        "card_set.is_standard", "card_set.numerator", "cost"), reverse=True)
        return cards_list

    def _init_bgs(self, db):
        temp = {}
        bgs = {}
        for card in db:
            if (GameTag.TECH_LEVEL in db[card].tags 
               and db[card].card_set not in [CardSet.VANILLA, CardSet.CORE]):
                temp[db[card].dbf_id] = db[card]
        for card in temp:
            if 1429 in temp[card].tags:
                bgs[card] = temp[card]
                bgs[temp[card].tags[1429]] = temp[temp[card].tags[1429]]
        return bgs.values()

    def first_handle(self, terms, is_bgs, max_response):
        cards = []
        search_list = self.bgs_list if is_bgs else self.cards_list
        for card in search_list:
            card_name = card.loc_name("zhCN").lower()
            if all([term in card_name for term in terms]):
                cards.append(card)
        num_cards = len(cards)
        if num_cards == 0:
            hint = "找不到相应的卡牌"
        elif num_cards == 1:
            hint = ""
        else:
            hint = self.second_handle(cards, 1, is_bgs, max_response)
        return cards, hint

    def second_handle(self, cards, page, is_bgs, max_response):
        num_cards = len(cards)
        page_size = min(max_response, num_cards)
        page_count = math.ceil(num_cards / page_size)
        page = min(page_count, max(1, page))
        offset = (page-1) * page_size
        page_hint = (
            "查询到%d个卡牌，当前页数[%d/%d]，直接输入数字进行翻页\n"
            % (num_cards, page, page_count)
        )
        hint = page_hint + "\n".join(
            self.stringify_card(cards[i], i + 1, is_bgs)
            for i in range(offset, min(offset + page_size, num_cards))
        )
        return hint

    def stringify_card(self, card, index, is_bgs):
        collectible = "可收藏" if card.collectible else "不可收藏"
        card_class = (multiclass_map[card.multi_class_group.name] 
                     if card.multi_class_group != MultiClassGroup.INVALID 
                     else class_map[card.card_class.name])
        cost = "%d星" % card.tags[GameTag.TECH_LEVEL] if is_bgs else "%d费" % card.cost
        card_type = type_map[card.type.name]
        name = card.loc_name("zhCN")
        gold = "（金）" if is_bgs and 1429 not in card.tags else ""
        card_set = set_map[card.card_set.name]
        return (
            "\\%d：%s%s，%s%s%s，%s，%s"
            % (index, name, gold, cost, card_class, card_type, 
              collectible, card_set)
        )

    def get_pic(self, card, args):
        if args["is_bgs"]:
            if 1429 not in card.tags:
                return ("https://art.hearthstonejson.com/v1/bgs/latest/%s/512x/%s_triple.png" 
                       % (args["lang"], card.id))
            else:
                return ("https://art.hearthstonejson.com/v1/bgs/latest/%s/512x/%s.png" 
                       % (args["lang"], card.id))
        else:
            return ("http://art.hearthstonejson.com/v1/render/latest/%s/512x/%s.png" 
                    % (args["lang"], card.id))

    def get_ori(self, card):
        return "https://art.hearthstonejson.com/v1/orig/%s.png" % card.id

    def get_tags(self, card, args):
        lang = args["lang"]
        name = "名称：%s" % card.loc_name(lang)
        card_id = "\nid：%s" % card.id
        health = (card.durability if card.type == CardType.WEAPON 
                 else card.health)
        cost = ("\n酒馆等级：%d星" % card.tags[GameTag.TECH_LEVEL] 
               if args["is_bgs"] else "\n费用：%d费" % card.cost)
        stats = ("\n身材：%s/%s" % (card.atk,
                health) if card.atk + health > 0 else "")
        race = ("\n种族：%s" % race_map[card.race.name] 
               if card.race != Race.INVALID else "")
        rarity = ("\n稀有度：%s" % rarity_map[card.rarity.name] 
                 if card.rarity != Rarity.INVALID else "")
        text = "\n" + card.loc_text(lang) if len(card.description) else ""
        flavor = ("\n卡牌趣文：" + 
                 card.loc_flavor(lang) if len(card.flavortext) else "")
        card_class = ("\n职业：%s" % (multiclass_map[card.multi_class_group.name]
                     if card.multi_class_group != MultiClassGroup.INVALID 
                     else class_map[card.card_class.name]))
        card_set = "\n扩展包：%s" % set_map[card.card_set.name]
        collectible = "\n可否收藏：%s" % ("是" if card.collectible else "否")
        tags = (name + card_id + text + flavor + card_class +
               race + card_set + cost + stats + rarity + collectible)
        return tags

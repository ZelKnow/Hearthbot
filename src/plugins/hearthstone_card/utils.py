#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : utils.py
@Description   : None
@Date          : 2021/08/13 11:11:26
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

set_map = {'STORMWIND': '暴风城', 'THE_BARRENS': '贫瘠之地', 'DARKMOON_FAIRE': '暗月马戏团', 'SCH': '通灵学园', 'SCHOLOMANCE': '通灵学园', 'DEMON_HUNTER_INITIATE': '恶魔猎手新兵', 'BLACK_TEMPLE': '外域', 'TB': '乱斗模式', 'TGT': '冠军的试炼', 'HERO_SKINS': '皮肤', 'LEGACY': '基本', 'CORE': '核心', 'BATTLEGROUNDS': '战棋', 'BOOMSDAY': '砰砰计划', 'BRM': '黑石山', 'GANGS': '加基森', 'CREDITS': '开发者', 'EXPERT1': '经典',
           'HOF': '荣誉室', 'DALARAN': '暗影崛起', 'DRAGONS': '巨龙降临', 'YEAR_OF_THE_DRAGON': '迦拉克隆的觉醒', 'NAXX': '纳克萨玛斯', 'GILNEAS': '女巫森林', 'GVG': '地精大战侏儒', 'ICECROWN': '冰封王座', 'UNGORO': '安格洛', 'LOOTAPALOOZA': '狗头人', 'KARA': '卡拉赞', 'LOE': '探险者协会', 'OG': '古神', 'TAVERNS_OF_TIME': '时光乱斗', 'TROLL': '大乱斗', 'MISSIONS': '新手引导', 'ULDUM': '奥丹姆', 'WILD_EVENT': '狂野回归', 'VANILLA': '经典模式专用'}

multiclass_map = {'GRIMY_GOONS': '污手党', 'KABAL': '暗金教', 'JADE_LOTUS': '玉莲帮', 'PRIEST_WARLOCK': '牧术', 'PALADIN_PRIEST': '骑牧', 'DRUID_SHAMAN': '德萨', 'MAGE_SHAMAN': '法萨',
                  'DRUID_HUNTER': '德猎', 'HUNTER_DEMONHUNTER': '猎瞎', 'WARLOCK_DEMONHUNTER': '术瞎', 'MAGE_ROGUE': '法贼', 'ROGUE_WARRIOR': '贼战', 'PALADIN_WARRIOR': '骑战'}

spellschool_map = {'FIRE': '火焰', 'ARCANE': '奥术', 'HOLY': '神圣',
                   'SHADOW': '暗影', 'FEL': '邪能', 'NATURE': '自然', 'FROST': '冰霜'}

race_map = {'NIGHTELF': '暗夜精灵', 'BEAST': '野兽', 'DRAGON': '龙', 'DEMON': '恶魔', 'PIRATE': '海盗', 'TOTEM': '图腾',
            'MURLOC': '鱼人', 'ELEMENTAL': '元素', 'MECHANICAL': '机械', 'MECH': '机械', 'ALL': '全部', 'ORC': '兽人', 'QUILBOAR': '野猪人'}

rarity_map = {'LEGENDARY': '传说', 'COMMON': '普通',
              'RARE': '稀有', 'EPIC': '史诗', 'FREE': '免费'}

type_map = {'MINION': '随从牌', 'SPELL': '法术牌', 'WEAPON': '武器牌',
            'HERO_POWER': '技能', 'HERO': '英雄牌', 'ENCHANTMENT': '强化'}

class_map = {'DEMONHUNTER': '恶魔猎手', 'NEUTRAL': '中立', 'MAGE': '法师', 'HUNTER': '猎人', 'PRIEST': '牧师', 'WARLOCK': '术士', 'ROGUE': '盗贼',
             'DRUID': '德鲁伊', 'SHAMAN': '萨满', 'WARRIOR': '战士', 'PALADIN': '骑士', 'WHIZBANG': '威兹班', 'DREAM': '梦境', 'DEATHKNIGHT': '死亡骑士'}

supported_langs = ['deDE', 'enUS', 'esES', 'esMX', 'frFR', 'itIT',
                   'jaJP', 'koKR', 'plPL', 'ptBR', 'ruRU', 'thTH', 'zhCN', 'zhTW']
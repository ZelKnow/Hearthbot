#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : deck_handler.py
@Description   : Generate deck image. Inspired by
                 https://github.com/rikumiyao/HS-Deck-to-Image
@Date          : 2021/08/18 11:54:41
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

from hearthstone.deckstrings import Deck
from .utils import card_db
from hearthstone.cardxml import CardXML
from hearthstone.enums import GameTag
import json
from PIL import Image, ImageDraw, ImageFont
import os
from .archetype import deckname

path = os.path.dirname(__file__)
tile_loc = os.path.join(path, "hs-card-tiles", "Tiles")
tile_container_number = os.path.join(path, "resources",
                                     "tile_container_number.png")
tile_container_open = os.path.join(path, "resources",
                                   "tile_container_open.png")
star = os.path.join(path, "resources", "star.png")
number_font = os.path.join(path, "resources", "Belwe-Bold.ttf")
heroes = [
    x for x in os.listdir(os.path.join(path, "resources"))
    if x.endswith(".jpg")
]

with open(os.path.join(path, "config.json"), encoding="utf-8") as json_file:
    cfg = json.load(json_file)
supported_locale = cfg.keys()


def loc_name(self, locale):
    return self.strings[GameTag.CARDNAME][locale]


CardXML.loc_name = loc_name


def parse_deck(text):
    for i in range(3):
        try:
            deck = Deck.from_deckstring(text + "=" * i)
            return deck
        except:
            continue
    return None


class DeckHandler():
    def __init__(self):
        self.card_dict = card_db()

    def deck_to_image(self, deckstr, name, locale="zhCN"):
        deck = parse_deck(deckstr)
        hero = self.card_dict[deck.heroes[0]].card_class.name
        if hero not in heroes:
            for x, _ in deck.cards:
                if self.card_dict[x].card_class.name in heroes:
                    hero = self.card_dict[x].card_class.name
                    break
        imclass = Image.open(os.path.join(path, "resources", hero + ".jpg"))
        cards = [(self.card_dict[x[0]], x[1]) for x in deck.cards]
        cards.sort(key=lambda x: (x[0].cost, x[0].loc_name(locale)))
        if name == "":
            name = deckname(deck, hero, deck.format)
        width = 243
        height = 39 * len(cards) + imclass.size[1]

        master = Image.new("RGBA", (width, height))
        for index, (card, count) in enumerate(cards):
            image = os.path.join(tile_loc, card.id + ".png")
            im = Image.open(image)
            color_palette = [(41, 48, 58, 255), (93, 68, 68, 0)]
            if count == 2 or card.rarity.name == "LEGENDARY":
                xoff = 81
                minx = 105
                maxx = 221
            else:
                xoff = 105
                minx = 129
                maxx = 245
            master.paste(im, (xoff, 3 + 39 * index, xoff + 130, 39 *
                              (index + 1) - 2))

            gradient = Image.new("RGBA", (width, height))
            draw = ImageDraw.Draw(gradient)
            for x in range(20, minx):
                draw.line([(x, 39 * index), (x, 39 * (index + 1))],
                          fill=color_palette[0])
            for x in range(minx, maxx):
                color = self._interpolate_color(minx, maxx, x, color_palette)
                draw.line([(x, 39 * index), (x, 39 * (index + 1))], fill=color)

            master = Image.alpha_composite(master, gradient)
            draw = ImageDraw.Draw(master)

            font_sizes = cfg[locale]["font_sizes"]
            bounds = cfg[locale]["bounds"]
            for i in range(len(font_sizes)):
                if len(card.loc_name(locale)) > bounds[i]:
                    deck_font_size = font_sizes[i]
                    break

            deck_font = os.path.join(path, "resources",
                                     cfg[locale]["deck_font"])
            name_font = os.path.join(path, "resources",
                                     cfg[locale]["name_font"])
            base = cfg[locale]["base"]
            font = ImageFont.truetype(deck_font, deck_font_size)
            self._draw_shadow(draw, 45, base - deck_font_size / 2 + 39 * index,
                              card.loc_name(locale), font)
            draw.text((45, base - deck_font_size / 2 + 39 * index),
                      card.loc_name(locale),
                      font=font)

            if count == 2:
                bg = Image.open(tile_container_number)
                master.paste(bg, (0, 39 * index, 239, 39 * (index + 1)), bg)
                font = ImageFont.truetype(number_font, 16)
                w, h = draw.textsize("2", font=font)
                draw.text(((30 - w) / 2 + 209, (39 - h) / 2 + 39 * index),
                          "2",
                          font=font,
                          fill=(229, 181, 68))
            elif card.rarity.name == "LEGENDARY":
                bg = Image.open(tile_container_number)
                master.paste(bg, (0, 39 * index, 239, 39 * (index + 1)), bg)
                imstar = Image.open(star)
                master.paste(imstar,
                             (214, 39 * index + 10, 233, 39 * index + 29),
                             imstar)
            else:
                bg = Image.open(tile_container_open)
                master.paste(bg, (0, 39 * index, 239, 39 * (index + 1)), bg)
            msg = str(card.cost)
            font = ImageFont.truetype(number_font, 25)
            w, h = draw.textsize(msg, font=font)
            self._draw_shadow(draw, (44 - w) / 2, (39 - h) / 2 + 39 * index,
                              str(card.cost), font)
            draw.text(((44 - w) / 2, (39 - h) / 2 + 39 * index),
                      str(card.cost),
                      font=font)
        draw = ImageDraw.Draw(master)
        decklist = master.crop((0, 0, 243, 39 * len(cards)))
        master.paste(decklist, (0, 97, 243, 39 * len(cards) + 97))
        master.paste(imclass, (0, 0, 243, 97))
        title = name
        font_locale = ImageFont.truetype(name_font, 24)
        font_en = ImageFont.truetype(number_font, 24)
        _, h_locale = draw.textsize(title, font=font_locale)
        _, h_en = draw.textsize(title, font=font_en)
        w = 0
        for i in range(len(title)):
            if title[i].isdigit() or title[i].islower() or title[i].isupper():
                font = font_en
                aw, _ = draw.textsize(title[i], font=font)
                self._draw_shadow(draw, 22 + w, 72 - h_en, title[i], font)
                draw.text((22 + w, 72 - h_en), title[i], font=font)
            else:
                font = font_locale
                aw, _ = draw.textsize(title[i], font=font)
                self._draw_shadow(draw, 22 + w, 72 - h_locale, title[i], font)
                draw.text((22 + w, 72 - h_locale), title[i], font=font)
            w += aw
        return master

    def merge(self, imgs):
        width = sum(x.size[0] for x in imgs)
        height = max(x.size[1] for x in imgs)
        master = Image.new("RGBA", (width, height))
        x = 0
        for img in imgs:
            w, h = img.size
            master.paste(img, (x, 0, x + w, h), img)
            x += w
        return master

    def _interpolate_color(self, minval, maxval, val, color_palette):
        max_index = len(color_palette) - 1
        v = float(val - minval) / float(maxval - minval) * max_index
        i1, i2 = int(v), min(int(v) + 1, max_index)
        (r1, g1, b1, a1), (r2, g2, b2,
                           a2) = color_palette[i1], color_palette[i2]
        f = v - i1
        return int(r1 + f *
                   (r2 - r1)), int(g1 + f *
                                   (g2 - g1)), int(b1 + f *
                                                   (b2 - b1)), int(a1 + f *
                                                                   (a2 - a1))

    def _draw_shadow(self, draw, x, y, text, font, shadowcolor="black"):
        draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)
        draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
        draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)

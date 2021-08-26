#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File          : archetype.py
@Description   : Classify decks. Code from 
                 https://github.com/HearthSim/hsarchetypes 
@Date          : 2021/08/20 08:46:31
@Author        : ZelKnow
@Github        : https://github.com/ZelKnow
"""
__author__ = "ZelKnow"

from hearthstone.deckstrings import FormatType
import httpx
from .rules import FALSE_POSITIVE_RULES
from nonebot import require
from nonebot.log import logger
import traceback


scheduler = require("nonebot_plugin_apscheduler").scheduler

class_name = {
    "DEMONHUNTER": "恶魔猎手",
    "MAGE": "法师",
    "DRUID": "德鲁伊",
    "HUNTER": "猎人",
    "PALADIN": "圣骑士",
    "ROGUE": "潜行者",
    "WARLOCK": "术士",
    "SHAMAN": "萨满",
    "WARRIOR": "战士",
    "PRIEST": "牧师",
}


def init_clusters(cluster_data):
    clusters = {}
    cluster_map = {}
    for raw_cluster in cluster_data:
        hero = raw_cluster["player_class"].upper()
        cluster = {}
        for deck_id in raw_cluster["signatures"]:
            if (raw_cluster["cluster_map"][deck_id] == None):
                continue
            temp = {}
            temp["signature_weights"] = dict(
                raw_cluster["signatures"][deck_id])
            temp["required_cards"] = raw_cluster["cluster_required_cards"][
                deck_id]
            cluster[deck_id] = temp
        cluster_map[hero] = raw_cluster["cluster_map"]
        clusters[hero] = cluster
    clusters["as_of"] = cluster_data[0]["as_of"]
    return clusters, cluster_map


cluster_url = "https://hsreplay.net/analytics/clustering/data/live/FT_STANDARD/"
deck_url = "https://hsreplay.net/api/v1/archetypes/"
headers = {"accept-language": "zh-CN,zh"}
try:
    cluster_data = httpx.get(cluster_url).json()
    clusters, cluster_map = init_clusters(cluster_data)
    deck_data = httpx.get(deck_url, headers=headers).json()
    not_classify = False
except:
    logger.error(traceback.format_exc())
    not_classify = True

def deckname(cardlist, hero, format):
    if format != FormatType.FT_STANDARD or not_classify:
        return class_name[hero]
    cluster = clusters[hero]
    deck = {dbf_id: count for (dbf_id, count) in cardlist.cards}
    classify_id = classify_deck(deck, cluster)
    if classify_id:
        deck_id = cluster_map[hero][classify_id]
        deckname = [x["name"] for x in deck_data if x["id"] == deck_id][0]
    else:
        deckname = class_name[hero]
    return deckname


def classify_deck(deck, clusters, failure_callback=None):
    """Attempt to classify the specified deck to one of the target archetype clusters.
    Each cluster in the array of cluster data should be a dict with the following keys:
    - signature_weights - a map of dbf_id (int) to prevalence (float)
    - required_cards (optional) - an array of dbf_ids that must appear in the deck
    - rules (optional) - an array of names of false positive rules to apply to the deck
    The (optional) failure callback is invoked when a deck was blocked from a possible
    classification by the application of a required card check or false positive rule.
    :param deck: the deck, as a map of dbf_id (int) to included count
    :param clusters: an array of cluster objects as above
    :param failure_callback: the failure callback, or None
    :return: the nearest above-threshold classification for the deck, or None
    """
    distances = []
    archetype_normalizers, cutoff_threshold = calculate_archetype_normalizers(
        clusters)
    for cluster_id, cluster in clusters.items():
        distance = 0

        weights = cluster["signature_weights"]
        for dbf_id, weight in weights.items():
            if dbf_id in deck:
                distance += weight * float(deck[dbf_id])
        distance *= archetype_normalizers[cluster_id]
        # If this cluster has a required card list and any required cards aren't in the
        # deck, nuke this deck's distance score down to zero.

        required_cards = cluster.get("required_cards", [])
        for required_card in required_cards:
            if required_card not in deck:

                # If this could have been a successful classification if the required card
                # had been present, invoke the failure callback to notify the caller.

                if failure_callback and distance >= cutoff_threshold:
                    failure_callback({
                        "archetype_id": cluster_id,
                        "reason": "missing_required_card",
                        "dbf_id": required_card
                    })

                distance *= 0
                break
        rules = cluster.get("rules", [])
        for rule in rules:
            if rule in FALSE_POSITIVE_RULES:
                if not FALSE_POSITIVE_RULES[rule]({"cards": deck}):

                    # If this could have been a successful classification without the false
                    # positive rule failure, invoke the failure callback to notify the
                    # caller.

                    if failure_callback and distance >= cutoff_threshold:
                        failure_callback({
                            "archetype_id": cluster_id,
                            "reason": "false_positive",
                            "rule": rule
                        })

                    distance *= 0
                    break
        if distance and distance >= cutoff_threshold:
            distances.append((cluster_id, distance))
    if distances:
        distances = sorted(distances, key=lambda t: t[1], reverse=True)
        return distances[0][0]


def calculate_archetype_normalizers(clusters):
    largest_signature_id = None
    largest_signature_max_score = 0.0
    for archetype_id, cluster in clusters.items():
        signature = cluster["signature_weights"]
        max_score = float(sum(signature.values()))
        if max_score > largest_signature_max_score:
            largest_signature_max_score = max_score
            largest_signature_id = archetype_id

    cutoff_threshold = largest_signature_max_score * .25
    result = {largest_signature_id: 1.0}
    for archetype_id, cluster in clusters.items():
        signature = cluster["signature_weights"]
        if archetype_id != largest_signature_id:
            result[archetype_id] = largest_signature_max_score / \
                float(sum(signature.values()))
    return result, cutoff_threshold


@scheduler.scheduled_job("cron", hour="6")
async def update():
    if not_classify:
        return
    global clusters, cluster_map, deck_data
    async with httpx.AsyncClient() as client:
        cluster_data = await client.get(cluster_url)
        cluster_data = cluster_data.json()
        header = {"accept-language": "zh-CN,zh"}
        deck_data = await client.get(deck_url, headers=header)
        deck_data = deck_data.json()
    clusters, cluster_map = init_clusters(cluster_data)

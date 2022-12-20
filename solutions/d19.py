from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque
import re
from functools import lru_cache
from multiprocessing import Pool


@dataclass(kw_only=True, frozen=True, eq=True)
class Robot:
    ore_cost: int = 0
    clay_cost: int = 0
    obsidian_cost: int = 0


@dataclass(frozen=True, eq=True)
class Blueprint:
    ore: Robot
    clay: Robot
    obsidian: Robot
    geode: Robot


@dataclass(frozen=True, eq=True)
class Node:
    time: int = 0
    ore_bots: int = 1
    clay_bots: int = 0
    obsidian_bots: int = 0
    geode_bots: int = 0

    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

@lru_cache(maxsize=None)
def quality(blueprint: Blueprint, max_ore: int, max_time: int, geode: int, curr: Node):
    if curr.time == max_time:
        return max(curr.geode, geode)

    # t = curr.time
    # g = curr.geode
    # i = 0
    # while t < max_time:
    #     t += 1
    #     g += curr.geode_bots + i
    #     i += 1
    dt = max_time - curr.time
    if curr.geode + curr.geode_bots * dt + (dt - 1) * dt // 2 < geode:
        return geode

    if curr.ore >= blueprint.geode.ore_cost and curr.obsidian >= blueprint.geode.obsidian_cost:
        geode = max(geode, quality(blueprint, max_ore, max_time, geode,
                               Node(
                                   curr.time + 1,
                                   curr.ore_bots,
                                   curr.clay_bots,
                                   curr.obsidian_bots,
                                   curr.geode_bots + 1,
                                   curr.ore + curr.ore_bots - blueprint.geode.ore_cost,
                                   curr.clay + curr.clay_bots,
                                   curr.obsidian + curr.obsidian_bots - blueprint.geode.obsidian_cost,
                                   curr.geode + curr.geode_bots
                               )))
    else:
        build_count = 0
        if curr.obsidian_bots < blueprint.geode.obsidian_cost and curr.ore >= blueprint.obsidian.ore_cost and curr.clay >= blueprint.obsidian.clay_cost:
            build_count += 1
            # build 1 obsidian bot
            geode = max(geode, quality(blueprint, max_ore, max_time, geode,
                                Node(
                                    curr.time + 1,
                                    curr.ore_bots,
                                    curr.clay_bots,
                                    curr.obsidian_bots + 1,
                                    curr.geode_bots,
                                    curr.ore + curr.ore_bots - blueprint.obsidian.ore_cost,
                                    curr.clay + curr.clay_bots - blueprint.obsidian.clay_cost,
                                    curr.obsidian + curr.obsidian_bots,
                                    curr.geode + curr.geode_bots
                                )))
        if curr.clay_bots < blueprint.obsidian.clay_cost and curr.ore >= blueprint.clay.ore_cost:
            build_count += 1
            # build 1 clay bot
            geode = max(geode, quality(blueprint, max_ore, max_time, geode,
                                Node(
                                    curr.time + 1,
                                    curr.ore_bots,
                                    curr.clay_bots + 1,
                                    curr.obsidian_bots,
                                    curr.geode_bots,
                                    curr.ore + curr.ore_bots - blueprint.clay.ore_cost,
                                    curr.clay + curr.clay_bots,
                                    curr.obsidian + curr.obsidian_bots,
                                    curr.geode + curr.geode_bots
                                )))
        if curr.ore_bots < max_ore and curr.ore >= blueprint.ore.ore_cost:
            build_count += 1
            # build 1 ore bot
            geode = max(geode, quality(blueprint, max_ore, max_time, geode,
                                Node(
                                    curr.time + 1,
                                    curr.ore_bots + 1,
                                    curr.clay_bots,
                                    curr.obsidian_bots,
                                    curr.geode_bots,
                                    curr.ore + curr.ore_bots - blueprint.ore.ore_cost,
                                    curr.clay + curr.clay_bots,
                                    curr.obsidian + curr.obsidian_bots,
                                    curr.geode + curr.geode_bots
                                )))
        if build_count < 3:
            geode = max(geode, quality(blueprint, max_ore, max_time,  geode, Node(
                curr.time + 1,
                curr.ore_bots,
                curr.clay_bots,
                curr.obsidian_bots,
                curr.geode_bots,
                curr.ore + curr.ore_bots,
                curr.clay + curr.clay_bots,
                curr.obsidian + curr.obsidian_bots,
                curr.geode + curr.geode_bots
            )))

    return geode


def main(file: TextIOWrapper):
    blueprints1: list[Blueprint] = []
    blueprints2: list[Blueprint] = []
    for line in file.readlines():
        _, ore_bot, clay_bot, obsidian_bot_ore, obsidian_bot_clay, geode_bot_ore, geode_bot_obsidian = map(
            int, (re.findall('\d+', line.strip())))
        max_ore = max(ore_bot, clay_bot, obsidian_bot_ore, geode_bot_ore)
        blueprints1.append((Blueprint(
            Robot(ore_cost=ore_bot),
            Robot(ore_cost=clay_bot),
            Robot(ore_cost=obsidian_bot_ore, clay_cost=obsidian_bot_clay),
            Robot(ore_cost=geode_bot_ore, obsidian_cost=geode_bot_obsidian)
        ), max_ore, 24, 0, Node()))
        if len(blueprints2) < 3:
            blueprints2.append((Blueprint(
                Robot(ore_cost=ore_bot),
                Robot(ore_cost=clay_bot),
                Robot(ore_cost=obsidian_bot_ore, clay_cost=obsidian_bot_clay),
                Robot(ore_cost=geode_bot_ore, obsidian_cost=geode_bot_obsidian)
            ), max_ore, 32, 0, Node()))

    total1 = 0
    for bid, blueprint in enumerate(blueprints1, start=1):
        q = quality(*blueprint)
        total1 += bid * q

    total2 = 1
    for bid, blueprint in enumerate(blueprints2[:3], start=1):
        q = quality(*blueprint)
        total2 *= q

    """
    parallel version
    total1 = 0
    pool = Pool()
    l = pool.starmap(quality, blueprints1)
    for i, ans in enumerate(l, start=1):
        total1 += ans * i
    quality.cache_clear()

    total2 = 1
    l = pool.starmap(quality, blueprints2)
    for i, ans in enumerate(l):
        total2 *= ans
    
    """

    return total1, total2

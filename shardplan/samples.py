"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _place(shards, node):
    return {s: node for s in shards}


def run(name):
    if name == "duplicate":
        placements = _place(["s1", "s2", "s3", "s4"], "A")
        caps = {"A": 2, "B": 2}
        moves = core.plan(placements, caps, 10, core.Counter())
        print(core.render(moves, placements, caps))
        return 0
    if name == "budget":
        placements = _place(["s1", "s2", "s3", "s4"], "A")
        caps = {"A": 1, "B": 5}
        moves = core.plan(placements, caps, 1, core.Counter())
        print(core.render(moves, placements, caps))
        return 0
    if name == "capacity":
        placements = _place(["s1", "s2", "s3", "s4"], "A")
        caps = {"A": 2, "B": 1, "C": 1}
        moves = core.plan(placements, caps, 10, core.Counter())
        print(core.render(moves, placements, caps))
        return 0
    if name == "work":
        placements = _place(["s%04d" % i for i in range(2000)], "A")
        caps = {"A": 1000, "B": 1000, "C": 1000}
        counter = core.Counter()
        moves = core.plan(placements, caps, 2000, counter)
        print(json.dumps({"shards": 2000, "moves": len(moves), "scanned": counter.scanned}))
        return 0
    raise SystemExit("未知场景：" + name)

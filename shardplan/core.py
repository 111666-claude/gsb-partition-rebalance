"""算搬迁计划并渲染。"""


class Counter:
    """记录算计划时做过的比较次数。"""

    def __init__(self):
        self.scanned = 0


def node_load(placements, counter=None):
    load = {}
    for node in placements.values():
        if counter is not None:
            counter.scanned += 1
        load[node] = load.get(node, 0) + 1
    return load


def plan(placements, caps, budget, counter):
    """从超容量节点往外搬分片，返回搬迁列表。"""
    load = node_load(placements, counter)
    moves = []
    while True:
        src = None
        for node in caps:
            counter.scanned += 1
            if load.get(node, 0) > caps[node]:
                src = node
                break
        if src is None:
            break
        shard = None
        for name, node in placements.items():
            counter.scanned += 1
            if node == src and (shard is None or name < shard):
                shard = name
        dst = None
        for node in caps:
            counter.scanned += 1
            if node != src:
                dst = node
                break
        if shard is None or dst is None:
            break
        moves.append({"shard": shard, "src": src, "dst": dst})
        load[src] = load.get(src, 0) - 1
    return moves


def render(moves, placements, caps):
    """把计划渲染成文本，并给出执行后的容量结论。"""
    load = node_load(placements)
    for m in moves:
        load[m["src"]] = load.get(m["src"], 0) - 1
        load[m["dst"]] = load.get(m["dst"], 0) + 1
    ok = all(load.get(node, 0) <= caps[node] for node in caps)
    distinct = len({m["shard"] for m in moves})
    lines = ["%s %s -> %s" % (m["shard"], m["src"], m["dst"]) for m in moves]
    lines.append("moves=%d moved=%d capacity-ok=%s" % (len(moves), distinct, "true" if ok else "false"))
    return "\n".join(lines)

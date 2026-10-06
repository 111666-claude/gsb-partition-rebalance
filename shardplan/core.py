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
    by_node = {}
    for name, node in placements.items():
        by_node.setdefault(node, []).append(name)
    for shards in by_node.values():
        shards.sort(reverse=True)
    nodes = list(caps)
    src_i = 0
    dst_i = 0
    moves = []
    while len(moves) < budget:
        while src_i < len(nodes):
            counter.scanned += 1
            if load.get(nodes[src_i], 0) > caps[nodes[src_i]]:
                break
            src_i += 1
        if src_i >= len(nodes):
            break
        src = nodes[src_i]
        stack = by_node.get(src)
        if not stack:
            src_i += 1
            continue
        while dst_i < len(nodes):
            counter.scanned += 1
            dst = nodes[dst_i]
            if dst != src and load.get(dst, 0) < caps[dst]:
                break
            dst_i += 1
        if dst_i >= len(nodes):
            break
        dst = nodes[dst_i]
        shard = stack.pop()
        counter.scanned += 1
        moves.append({"shard": shard, "src": src, "dst": dst})
        load[src] = load.get(src, 0) - 1
        load[dst] = load.get(dst, 0) + 1
        by_node.setdefault(dst, []).append(shard)
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

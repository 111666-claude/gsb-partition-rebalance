# partition-rebalance

给一份分片摆放（分片 → 节点）和每个节点的容量，算一个搬迁计划再渲染成可读文本。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m shardplan --sample=duplicate
python3 -m shardplan --sample=budget
python3 -m shardplan --sample=capacity
python3 -m shardplan --sample=work
```

## 口径

- **容量**：计划执行后，每个节点持有的分片数不超过它的容量。
- **不重复**：一个分片在一次计划里最多搬一次。
- **预算**：计划里的搬迁条数不超过给定的搬迁预算；预算不够时给出部分计划。
- **只搬超载节点**：只从超容量的节点往外搬，不搬已经在容量内的节点。

## 不变量

- 每条搬迁都有 `shard` / `src` / `dst`，且 `src` 是分片当前所在节点。
- 计划里的分片互不重复，条数不超过预算。
- `scanned` 不随分片数平方级放大：两千个分片的 `scanned` 不超过 6000。

## 输出契约

渲染成文本：每条搬迁一行 `<shard> <src> -> <dst>`，末行 `moves=<条数> moved=<去重后分片数> capacity-ok=<true|false>`，
`capacity-ok` 表示按该计划执行后每个节点都不超容量。
`--sample=work` 只打印 `{"shards": N, "moves": N, "scanned": N}`。

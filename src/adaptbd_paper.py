# src/adaptbd_paper.py
from typing import Dict, List, Tuple, Set
from functools import lru_cache
from .scc import tarjan_scc

def _subgraph(vertices: List[str], edges: List[Tuple[str, str]], subset: Set[str]):
    V = [v for v in vertices if v in subset]
    E = [(u, v) for (u, v) in edges if u in subset and v in subset]
    return V, E

def _adjacency(vertices: List[str], edges: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    adj = {v: [] for v in vertices}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
    return adj

def _bound_inside_scc(
    V: List[str],
    E: List[Tuple[str, str]],
    W: Dict[str, int],
    Qset: Set[str],
) -> int:
    """
    Exact, small-graph enumerator:
    - Counts max number of query nodes visited along any walk that respects per-node visit caps W.
    - Works inside one SCC (but also fine for general subgraphs).
    - Sound and exact for demo sizes; exponential in worst case, so keep SCCs small (which they are in our demo).
    """
    if not V:
        return 0
    order = list(V)
    idx = {v: i for i, v in enumerate(order)}
    adj = _adjacency(V, E)

    @lru_cache(maxsize=None)
    def dfs(state: Tuple[str, ...]) -> int:
        """
        state = (current_or_NONE, remaining_w[v0], remaining_w[v1], ...)
        """
        cur = state[0]  # may be "NONE"
        rem = {order[i]: state[i + 1] for i in range(len(order))}

        gain = 0
        if cur != "NONE":
            if rem[cur] <= 0:
                return 0
            rem[cur] -= 1
            if cur in Qset:
                gain += 1

        best = gain

        # Choose next step (stay, stop, or move along edges)
        if cur == "NONE":
            # Start at any vertex with remaining budget
            for v in order:
                if rem[v] > 0:
                    nxt = (v, *[rem[u] for u in order])
                    best = max(best, dfs(nxt))
            return best

        moved = False
        for w in adj.get(cur, []):
            if rem[w] > 0:
                moved = True
                nxt = (w, *[rem[u] for u in order])
                best = max(best, gain + dfs(nxt))
        # Option to stop here
        if not moved:
            best = max(best, gain)
        return best

    start = ("NONE", *[W[v] for v in order])
    return dfs(start)

def adaptivity_bound_paper(
    vertices: List[str],
    edges: List[Tuple[str, str]],
    weights: Dict[str, int],
    query_vertices: List[str],
) -> int:
    """
    AdaptFun-like pipeline:
      1) Decompose into SCCs (Tarjan).
      2) For each SCC, compute an internal bound (enumerator above).
      3) Build SCC-DAG and do DP to propagate best totals across components.
         For demo we combine as: inbound_best + scc_internal_bound along DAG.
    """
    Qset = set(query_vertices)
    V = list(vertices)
    E = list(edges)

    # 1) SCCs
    comps = tarjan_scc(V, E)  # list of lists, each a component
    comp_id: Dict[str, int] = {}
    for i, comp in enumerate(comps):
        for v in comp:
            comp_id[v] = i

    # 2) Bound inside each SCC
    scc_bound: Dict[int, int] = {}
    for i, comp in enumerate(comps):
        subV, subE = _subgraph(V, E, set(comp))
        scc_bound[i] = _bound_inside_scc(subV, subE, weights, Qset)

    # 3) Build SCC-DAG
    dag_edges: Dict[int, List[int]] = {i: [] for i in range(len(comps))}
    indeg: Dict[int, int] = {i: 0 for i in range(len(comps))}
    for (u, v) in E:
        cu, cv = comp_id[u], comp_id[v]
        if cu != cv:
            dag_edges[cu].append(cv)
            indeg[cv] += 1

    # Topological order over SCC-DAG
    queue = [i for i in range(len(comps)) if indeg[i] == 0]
    topo: List[int] = []
    while queue:
        x = queue.pop()
        topo.append(x)
        for y in dag_edges[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                queue.append(y)

    # DP: best total reaching each SCC = max over preds (best[pred]) + scc_bound[this]
    best: Dict[int, int] = {i: float("-inf") for i in range(len(comps))}
    for i in topo:
        incoming_best = 0  # if no predecessors
        # find predecessors
        preds = [p for p in range(len(comps)) if i in dag_edges.get(p, [])]
        if preds:
            incoming_best = max(best[p] for p in preds)
        best[i] = incoming_best + scc_bound[i]

    # Global bound is max over SCCs
    return max(best.values()) if best else 0

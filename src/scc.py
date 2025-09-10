# src/scc.py
from typing import Dict, List, Tuple

def tarjan_scc(vertices: List[str], edges: List[Tuple[str, str]]) -> List[List[str]]:
    adj: Dict[str, List[str]] = {v: [] for v in vertices}
    for u, v in edges:
        adj.setdefault(u, []).append(v)

    index = 0
    stack: List[str] = []
    onstack: Dict[str, bool] = {v: False for v in vertices}
    indices: Dict[str, int] = {}
    lowlink: Dict[str, int] = {}
    comps: List[List[str]] = []

    def strongconnect(v: str):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v); onstack[v] = True

        for w in adj.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif onstack[w]:
                lowlink[v] = min(lowlink[v], indices[w])

        # Root of an SCC
        if lowlink[v] == indices[v]:
            comp: List[str] = []
            while True:
                w = stack.pop()
                onstack[w] = False
                comp.append(w)
                if w == v:
                    break
            comps.append(comp)

    for v in vertices:
        if v not in indices:
            strongconnect(v)

    return comps

# src/adaptbd.py

def adaptivity_bound(V, E, W, Q):
    """
    Naive upper bound: count max query nodes along any path
    using DFS and respecting weights.
    """
    from collections import defaultdict

    graph = defaultdict(list)
    for u, v in E:
        graph[u].append(v)

    best_score = 0

    def dfs(node, score, visits):
        nonlocal best_score

        best_score = max(best_score, score)

        for nxt in graph[node]:
            if visits[nxt] < W.get(nxt, 1):
                visits[nxt] += 1
                dfs(nxt, score + (1 if nxt in Q else 0), visits)
                visits[nxt] -= 1

    for v in V:
        dfs(v, (1 if v in Q else 0), {u: 0 for u in V})

    return best_score


def critical_path(V, E, W, Q):
    """
    Return one critical path (walk with max queries).
    """
    from collections import defaultdict

    graph = defaultdict(list)
    for u, v in E:
        graph[u].append(v)

    best_path = []
    best_score = -1

    def dfs(node, path, score, visits):
        nonlocal best_path, best_score

        if score > best_score:
            best_score = score
            best_path = path[:]

        for nxt in graph[node]:
            if visits[nxt] < W.get(nxt, 1):
                visits[nxt] += 1
                dfs(nxt, path + [nxt], score + (1 if nxt in Q else 0), visits)
                visits[nxt] -= 1

    for v in V:
        dfs(v, [v], (1 if v in Q else 0), {u: 0 for u in V})

    return best_path

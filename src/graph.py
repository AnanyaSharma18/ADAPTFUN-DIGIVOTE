from types import FunctionType
from typing import Dict, List, Tuple

def build_graph(module) -> Tuple[List[str], List[Tuple[str, str]], Dict[str, int], List[str]]:
    vertices, edges, weights, query_vertices = [], [], {}, []

    for name, obj in module.__dict__.items():
        # include only functions defined in this module
        if isinstance(obj, FunctionType) and obj.__module__ == module.__name__:
            v = getattr(obj, "__query_name__", name)
            vertices.append(v)
            weights[v] = getattr(obj, "__weight__", 1)
            for d in getattr(obj, "__deps__", []):
                edges.append((d, v))
            if getattr(obj, "__is_query__", False):
                query_vertices.append(v)

    # deduplicate while preserving order
    def dedup(xs):
        seen, out = set(), []
        for x in xs:
            if x not in seen:
                seen.add(x); out.append(x)
        return out

    return dedup(vertices), dedup(edges), weights, dedup(query_vertices)

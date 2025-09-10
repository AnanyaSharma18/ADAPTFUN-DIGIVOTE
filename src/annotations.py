# src/annotations.py

_vertices = set()
_edges = []
_weights = {}
_queries = set()

def query(name):
    def decorator(func):
        _vertices.add(name)
        _queries.add(name)
        # attach metadata
        setattr(func, "_vertex", name)
        return func
    return decorator

def depends_on(dep):
    def decorator(func):
        this = getattr(func, "_vertex", func.__name__)
        _edges.append((dep, this))
        _vertices.add(this)
        _vertices.add(dep)
        return func
    return decorator

def weight(val):
    def decorator(func):
        this = getattr(func, "_vertex", func.__name__)
        _weights[this] = val
        _vertices.add(this)
        return func
    return decorator

def build_graph():
    """Return vertices, edges, weights, query nodes"""
    return list(_vertices), list(_edges), dict(_weights), list(_queries)

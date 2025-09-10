# src/run_demo.py

try:
    # Force load flow so decorators execute
    from . import flow
    from .annotations import build_graph
    from .adaptbd import adaptivity_bound
except ImportError:
    import flow
    from annotations import build_graph
    from adaptbd import adaptivity_bound


def main():
    # Build graph from annotations
    V, E, W, Q = build_graph()

    print("Vertices:", V)
    print("Edges:", E)
    print("Weights:", W)
    print("Query vertices:", Q)

    # Compute adaptivity bound
    bound = adaptivity_bound(V, E, W, Q)

    print("\n=== Bounds ===")
    print("Simple enumerator bound: ", bound)
    print("Interpretation: Max # of query steps along a weight-respecting walk.")


if __name__ == "__main__":
    main()

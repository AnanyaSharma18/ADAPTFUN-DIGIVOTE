# src/simulate_errors.py
"""
Generates Fig-2-style plots:
- RMSE (generalization error) vs query index
for None, DataSplitting, GaussianNoise, Thresholdout.

Run:
    python -m src.simulate_errors
"""

import os
import numpy as np
import matplotlib.pyplot as plt

try:
    from .mechanisms import NoMechanism, DataSplitting, GaussianNoise, Thresholdout
except ImportError:
    from mechanisms import NoMechanism, DataSplitting, GaussianNoise, Thresholdout


# ---------- Synthetic data + analyst ----------

def make_dataset(rng, n=500, d=50):
    """
    Population ~ N(0, I_d). Draw 'S' (train) and 'H' (holdout).
    Ground-truth expectation of v·X is 0 for any unit v.
    """
    S = rng.normal(size=(n, d))
    H = rng.normal(size=(n, d))
    return S, H


def random_unit_vectors(rng, k, d):
    V = rng.normal(size=(k, d))
    V /= np.maximum(np.linalg.norm(V, axis=1, keepdims=True), 1e-12)
    return V


def adaptive_analyst(rng, mech, S, H, Q=400, k_pool=200, d=50):
    """
    Simple adaptive strategy:
    - At each round, sample a small pool of candidate queries (unit vectors).
    - Score them using the *released answers so far* to induce adaptivity:
      pick the candidate that maximizes correlation with signed residuals.
    - Ask the mechanism for the answer to that query.
    Returns:
        errors: per-round generalization error |released - true|
    """
    errors = []
    # running "residual" target to overfit towards (toy but induces adaptivity)
    # start with random direction
    residual = rng.normal(size=d)
    residual /= np.linalg.norm(residual) + 1e-12

    for t in range(Q):
        pool = random_unit_vectors(rng, k_pool, d)
        scores = pool @ residual   # choose direction aligned with residual
        v = pool[np.argmax(scores)]

        # mechanism gives answer (using S, maybe H)
        released = mech.answer(v, S, H)

        # true population expectation is 0 for zero-mean Gaussian (unit v)
        truth = 0.0
        err = abs(released - truth)
        errors.append(err)

        # update residual using released value to create adaptivity
        residual = 0.5 * residual + released * v
        nrm = np.linalg.norm(residual)
        if nrm > 0:
            residual /= nrm

    return np.array(errors)


# ---------- Plotting helpers ----------

def run_single_curve(rng, mech, label, color=None, Q=400, d=50):
    S, H = make_dataset(rng, n=500, d=d)
    errs = adaptive_analyst(rng, mech, S, H, Q=Q, d=d)
    xs = np.arange(1, Q + 1)
    if color is None:
        plt.plot(xs, errs, label=label)
    else:
        plt.plot(xs, errs, label=label, color=color)
    return errs


def panel_rmse_vs_queries(seed=7, Q=400, savepath="outputs/generalization_errors.png"):
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    rng = np.random.default_rng(seed)

    plt.figure(figsize=(13, 4))

    # ------ Panel (a): small adaptivity (Q=50) ------
    plt.subplot(1, 3, 1)
    rng1 = np.random.default_rng(seed)
    e_none = run_single_curve(rng1, NoMechanism(rng1), "overfitting")
    rng1 = np.random.default_rng(seed)
    e_ds   = run_single_curve(rng1, DataSplitting(rng1, M=25), "data splitting")
    rng1 = np.random.default_rng(seed)
    e_gs   = run_single_curve(rng1, GaussianNoise(rng1, sigma=0.05), "gaussian noise")
    rng1 = np.random.default_rng(seed)
    e_ts   = run_single_curve(rng1, Thresholdout(rng1, tau=0.05, B=20), "thresholdout")

    plt.title("(a) ~50 queries")
    plt.xlabel("Queries")
    plt.ylabel("Generalization Error (|released - truth|)")
    plt.ylim(0, max(0.4, np.max([e_none, e_ds, e_gs, e_ts])))
    plt.legend(loc="upper left", fontsize=8)

    # ------ Panel (b): high adaptivity (Q=400) ------
    plt.subplot(1, 3, 2)
    rng2 = np.random.default_rng(seed + 1)
    e_none2 = run_single_curve(rng2, NoMechanism(rng2), "overfitting")
    rng2 = np.random.default_rng(seed + 1)
    e_ds2   = run_single_curve(rng2, DataSplitting(rng2, M=25), "data splitting")
    rng2 = np.random.default_rng(seed + 1)
    e_gs2   = run_single_curve(rng2, GaussianNoise(rng2, sigma=0.05), "gaussian noise")
    rng2 = np.random.default_rng(seed + 1)
    e_ts2   = run_single_curve(rng2, Thresholdout(rng2, tau=0.05, B=50), "thresholdout")

    plt.title("(b) ~400 queries")
    plt.xlabel("Queries")
    plt.ylim(0, max(0.4, np.max([e_none2, e_ds2, e_gs2, e_ts2])))
    plt.legend(loc="upper left", fontsize=8)

    # ------ Panel (c): RMSE growth w.r.t. #queries ------
    plt.subplot(1, 3, 3)
    rng3 = np.random.default_rng(seed + 2)
    Qs = [50, 200, 400, 800, 1200]
    rmses_none, rmses_ds, rmses_gs, rmses_ts = [], [], [], []
    for Qcur in Qs:
        S, H = make_dataset(rng3, n=500, d=50)
        # to keep comparisons fair, new RNG per mechanism per Q
        r = np.random.default_rng(seed + 100 + Qcur)
        rmses_none.append(np.sqrt(np.mean(adaptive_analyst(r, NoMechanism(r), S, H, Q=Qcur) ** 2)))
        r = np.random.default_rng(seed + 200 + Qcur)
        rmses_ds.append(np.sqrt(np.mean(adaptive_analyst(r, DataSplitting(r, M=25), S, H, Q=Qcur) ** 2)))
        r = np.random.default_rng(seed + 300 + Qcur)
        rmses_gs.append(np.sqrt(np.mean(adaptive_analyst(r, GaussianNoise(r, sigma=0.05), S, H, Q=Qcur) ** 2)))
        r = np.random.default_rng(seed + 400 + Qcur)
        rmses_ts.append(np.sqrt(np.mean(adaptive_analyst(r, Thresholdout(r, tau=0.05, B=50), S, H, Q=Qcur) ** 2)))

    xs = np.array(Qs)
    plt.plot(xs, rmses_ds, label="data splitting")
    plt.plot(xs, rmses_gs, label="gaussian noise")
    plt.plot(xs, rmses_ts, label="thresholdout")
    plt.plot(xs, rmses_none, label="overfitting")
    plt.title("(c) RMSE vs #queries")
    plt.xlabel("#Queries")
    plt.ylabel("RMSE")
    plt.legend(loc="upper left", fontsize=8)

    plt.tight_layout()
    plt.savefig(savepath, dpi=180)
    print(f"Saved: {savepath}")
    plt.show()


if __name__ == "__main__":
    panel_rmse_vs_queries()

# src/mechanisms.py
import numpy as np

class MechanismBase:
    def __init__(self, rng):
        self.rng = rng

    def answer(self, query_vec, S, H):
        """
        query_vec : (d,) vector defining linear query q(x) = v·x
        S         : training sample array, shape (n, d)
        H         : holdout sample array, shape (n_holdout, d) or None
        Returns: released answer (float)
        """
        raise NotImplementedError


class NoMechanism(MechanismBase):
    """Overfitting baseline: release empirical mean on S with no noise/safeguard."""
    def answer(self, v, S, H):
        return float(np.mean(S @ v))


class DataSplitting(MechanismBase):
    """
    Pre-split S into M disjoint chunks; each query uses next chunk only.
    Keeps generalization low but adds variance. Classic tradeoff.
    """
    def __init__(self, rng, M=20):
        super().__init__(rng)
        self.M = M
        self.counter = 0
        self.chunks = None

    def _ensure_chunks(self, S):
        if self.chunks is None:
            n = len(S)
            idx = np.arange(n)
            self.rng.shuffle(idx)
            self.chunks = np.array_split(S[idx], self.M)

    def answer(self, v, S, H):
        self._ensure_chunks(S)
        chunk = self.chunks[self.counter % len(self.chunks)]
        self.counter += 1
        return float(np.mean(chunk @ v))


class GaussianNoise(MechanismBase):
    """
    Release empirical mean on S plus Gaussian noise.
    sigma is a demo parameter (not DP-tight here).
    """
    def __init__(self, rng, sigma=0.05):
        super().__init__(rng)
        self.sigma = sigma

    def answer(self, v, S, H):
        mu = float(np.mean(S @ v))
        return mu + self.rng.normal(0.0, self.sigma)


class Thresholdout(MechanismBase):
    """
    Very light-weight 'thresholdout'-style monitor:
    - Compare train and holdout means.
    - If gap <= tau: release train + small noise.
    - Else: release holdout + larger noise; decrement budget B.
    """
    def __init__(self, rng, tau=0.05, B=50, sigma_small=0.01, sigma_big=0.05):
        super().__init__(rng)
        self.tau = tau
        self.B = B
        self.sigma_small = sigma_small
        self.sigma_big = sigma_big

    def answer(self, v, S, H):
        if H is None:
            # fallback to train if no holdout provided
            return float(np.mean(S @ v))

        train = float(np.mean(S @ v))
        hold  = float(np.mean(H @ v))
        gap = abs(train - hold)

        if gap <= self.tau:
            return train + self.rng.normal(0.0, self.sigma_small)
        else:
            if self.B > 0:
                self.B -= 1
            # release holdout (less overfit) with a bit more noise
            return hold + self.rng.normal(0.0, self.sigma_big)

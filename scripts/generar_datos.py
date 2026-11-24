import numpy as np, pandas as pd

rng = np.random.default_rng(42)
n = 5000
df = pd.DataFrame({
    "edad": rng.integers(15, 80, n),
    "forma_fisica": rng.integers(1, 11, n),
    "sabe_conducir": rng.integers(0, 2, n),
    "mascota": rng.integers(0, 2, n),
    "vive_en_campo": rng.integers(0, 2, n),
    "pelis_zombis": rng.integers(0, 60, n),
    "primeros_auxilios": rng.integers(0, 2, n),
    "horas_sueno": rng.normal(7, 1.5, n).clip(3, 10),
})


score = (
    df.forma_fisica * 6
    - (df.edad - 30).abs() * 0.4
    + df.sabe_conducir * 12
    + df.vive_en_campo * 10
    + df.pelis_zombis * 0.5
    + df.primeros_auxilios * 8
    - df.mascota * 5            
    - (df.horas_sueno - 7).abs() * 2
    + rng.normal(0, 8, n)       # ruido
)
df["prob_supervivencia"] = ((score - score.min()) / (score.max() - score.min()) * 100).round(1)
df.to_csv("data/zombies.csv", index=False)
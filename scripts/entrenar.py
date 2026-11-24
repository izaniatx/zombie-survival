import pandas as pd, joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

df = pd.read_csv("data/zombies.csv")
X, y = df.drop(columns="prob_supervivencia"), df["prob_supervivencia"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)

modelo = RandomForestRegressor(n_estimators=200, random_state=0).fit(X_tr, y_tr)
print("R2:", r2_score(y_te, modelo.predict(X_te)))
joblib.dump((modelo, list(X.columns)), "model/zombies.joblib")
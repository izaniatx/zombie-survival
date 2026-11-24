import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

modelo, columnas = joblib.load("model/zombies.joblib")
dataset = pd.read_csv("data/zombies.csv")

app = FastAPI(title="Zombie Survival")


class Persona(BaseModel):
    edad: int = Field(ge=15, le=80)
    forma_fisica: int = Field(ge=1, le=10)
    sabe_conducir: int = Field(ge=0, le=1)
    mascota: int = Field(ge=0, le=1)
    vive_en_campo: int = Field(ge=0, le=1)
    pelis_zombis: int = Field(ge=0, le=60)
    primeros_auxilios: int = Field(ge=0, le=1)
    horas_sueno: float = Field(ge=3, le=10)

RANGOS = {
    "edad": range(15, 81),
    "forma_fisica": range(1, 11),
    "pelis_zombis": range(0, 60),
    "horas_sueno": [h / 2 for h in range(6, 21)],  # 3.0, 3.5 ... 10.0
    "sabe_conducir": [0, 1],
    "mascota": [0, 1],
    "vive_en_campo": [0, 1],
    "primeros_auxilios": [0, 1],
}


def calcular_lastres(base: dict, prob: float):
    lastres = []
    for variable, valores in RANGOS.items():
        candidatas = pd.DataFrame([{**base, variable: v} for v in valores])[columnas]
        mejor = float(modelo.predict(candidatas).max())
        lastres.append({
            "variable": variable,
            "perdida": round(max(0.0, mejor - prob), 1),
        })
    return sorted(lastres, key=lambda x: x["perdida"], reverse=True)


@app.post("/predecir")
def predecir(p: Persona):
    base = p.model_dump()
    fila = pd.DataFrame([base])[columnas]
    prob = float(modelo.predict(fila)[0])
    percentil = float((dataset["prob_supervivencia"] < prob).mean() * 100)
    return {
        "probabilidad": round(prob, 1),
        "percentil": round(percentil, 1),
        "lastres": calcular_lastres(base, prob),
    }


@app.get("/importancias")
def importancias():
    pares = zip(columnas, modelo.feature_importances_)
    return sorted(
        [{"variable": c, "peso": round(float(i), 3)} for c, i in pares],
        key=lambda x: x["peso"],
        reverse=True,
    )

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.svg", media_type="image/svg+xml")

@app.get("/")
def inicio():
    return FileResponse("static/index.html")
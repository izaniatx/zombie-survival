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


@app.post("/predecir")
def predecir(p: Persona):
    fila = pd.DataFrame([p.model_dump()])[columnas]
    prob = float(modelo.predict(fila)[0])
    percentil = float((dataset["prob_supervivencia"] < prob).mean() * 100)
    return {
        "probabilidad": round(prob, 1),
        "percentil": round(percentil, 1),
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


@app.get("/")
def inicio():
    return FileResponse("static/index.html")
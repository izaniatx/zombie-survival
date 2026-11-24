
<div align="center">
# ZOMBIE SURVIVAL

Metes tu perfil: edad, forma física, si sabes conducir, si tienes mascota (el perro ladra y os delata)... y el modelo te da tu **probabilidad de supervivencia**, tu **percentil** frente al resto y un gráfico con **lo que más te está hundiendo**.

Todo corre en local. Sin APIs externas, sin claves, sin cuentas.

## Lo que lleva dentro

|                                |                                                                                      |
| ------------------------------ | ------------------------------------------------------------------------------------ |
| **Dataset propio**       | 5.000 supervivientes simulados con reglas inventadas, relaciones no lineales y ruido |
| **Modelo propio**        | Random Forest entrenado desde cero, R² de 0,85                                      |
| **Análisis individual** | Cuántos puntos ganarías arreglando cada variable por separado                      |
| **API**                  | FastAPI con validación de datos y documentación automática                        |
| **Frontend**             | JavaScript vanilla, Chart.js y estética de informe de campo                         |

## Pruébalo

```bash
git clone https://github.com/TU_USUARIO/zombie-survival.git
cd zombie-survival
 
python3 -m venv .venv
source .venv/bin/activate        # fish: .venv/bin/activate.fish | Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdir -p data model
 
python generar_datos.py && python entrenar.py
uvicorn app:app --reload
```

Abre **http://127.0.0.1:8000** y a sobrevivir.

<details>
<summary><b>Detalles técnicos</b></summary>
<br>
**Cómo se generan los datos.** No existen datos reales de supervivencia zombi, así que `generar_datos.py` simula las variables con distribuciones uniformes y normales, calcula una puntuación con reglas inventadas (por ejemplo `abs(edad - 30)` para que lo ideal esté en el centro), le suma ruido gaussiano y la normaliza a 0-100. La semilla es fija, así que todo el mundo obtiene los mismos datos.

**Validación.** Las importancias del modelo coinciden con la contribución teórica de cada variable (coeficiente² × varianza): forma física 53 %, pelis de zombis 18 %, edad 10 %. El R² de 0,85 está limitado por el ruido que se añadió a propósito.

**Qué te está matando.** Para cada variable se prueban todos sus valores con el resto del perfil fijo y se mide cuánto sube la predicción. Es un análisis contrafactual sencillo; la versión rigurosa serían los valores SHAP.

**Endpoints**

| Método  | Ruta              | Descripción                        |
| -------- | ----------------- | ----------------------------------- |
| `POST` | `/predecir`     | Probabilidad, percentil y lastres   |
| `GET`  | `/importancias` | Importancia global de cada variable |
| `GET`  | `/docs`         | Documentación interactiva          |

**Limitaciones.** El modelo no aprende la realidad, aprende mis reglas. Es divertido, no científico. Chart.js y las fuentes se cargan desde un CDN, así que hace falta internet.

</details>
## Próximos pasos

- [ ] Valores SHAP en lugar del análisis contrafactual
- [ ] Comparar dos perfiles lado a lado
- [ ] Desplegarlo online

<div align="center">
Proyecto de portfolio · Desarrollo web + Especialidad en IA

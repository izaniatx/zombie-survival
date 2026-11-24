const numericos = ["edad", "forma_fisica", "pelis_zombis", "horas_sueno"];
const binarios = ["sabe_conducir", "mascota", "vive_en_campo", "primeros_auxilios"];
const $ = (id) => document.getElementById(id);

Chart.defaults.font.family = "'IBM Plex Mono', monospace";
Chart.defaults.color = "#8a8672";

// --- Leer el formulario y convertirlo al JSON que espera la API ---
function leerPersona() {
  const persona = {};
  numericos.forEach((k) => (persona[k] = Number($(k).value)));
  binarios.forEach((k) => (persona[k] = $(k).checked ? 1 : 0));
  return persona;
}

// --- Título según el resultado ---
function titulo(prob) {
  if (prob < 20) return "Carne de cañón";
  if (prob < 40) return "El primero en caer";
  if (prob < 60) return "Superviviente de relleno";
  if (prob < 80) return "Veterano del apocalipsis";
  return "Líder de la resistencia";
}

function colorProb(prob) {
  if (prob < 30) return "#b3261e";
  if (prob < 60) return "#d9a21b";
  return "#7a9a3a";
}

// --- Stats del radar, todas en escala 0-100 ---
function statsRadar(p) {
  const limitar = (x) => Math.max(0, Math.min(100, x));
  return [
    p.forma_fisica * 10,
    limitar(100 - Math.abs(p.edad - 30) * 2),
    limitar(100 - Math.abs(p.horas_sueno - 7) * 25),
    (p.pelis_zombis / 59) * 100,
    p.sabe_conducir * 100,
    p.vive_en_campo * 100,
    p.primeros_auxilios * 100,
    p.mascota ? 0 : 100, // sin mascota = más sigiloso
  ];
}

// --- Gráfico de radar ---
const radar = new Chart($("radar"), {
  type: "radar",
  data: {
    labels: ["Forma física", "Edad ideal", "Sueño", "Cultura zombi",
             "Conducción", "Campo", "Primeros auxilios", "Sigilo"],
    datasets: [{
      data: [],
      backgroundColor: "rgba(194, 80, 26, 0.25)",
      borderColor: "#c2501a",
      pointBackgroundColor: "#d9a21b",
    }],
  },
  options: {
    maintainAspectRatio: false,
    scales: {
      r: {
        min: 0,
        max: 100,
        ticks: { display: false },
        grid: { color: "#2a2d22" },
        angleLines: { color: "#2a2d22" },
        pointLabels: { color: "#d8d2c0" },
      },
    },
    plugins: { legend: { display: false } },
  },
});

// --- Predecir: llama a la API y actualiza la pantalla ---
async function actualizar() {
  const persona = leerPersona();
  const r = await fetch("/predecir", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(persona),
  });
  if (!r.ok) return;
  const { probabilidad, percentil } = await r.json();

  $("probabilidad").parentElement.style.color = colorProb(probabilidad);
  $("probabilidad").textContent = probabilidad;
  $("percentil").textContent = `Sobrevives más que el ${percentil}% de la gente`;
  $("titulo").textContent = titulo(probabilidad);

  radar.data.datasets[0].data = statsRadar(persona);
  radar.update();
}

// --- Mostrar el valor de cada slider junto a su etiqueta ---
numericos.forEach((k) => {
  const mostrar = () => ($(`${k}-valor`).textContent = $(k).value);
  $(k).addEventListener("input", mostrar);
  mostrar();
});

// --- Recalcular al cambiar cualquier cosa (con un pequeño retardo) ---
let temporizador;
$("formulario").addEventListener("input", () => {
  clearTimeout(temporizador);
  temporizador = setTimeout(actualizar, 150);
});

// --- Gráfico de importancias (se carga una sola vez) ---
async function cargarImportancias() {
  const datos = await (await fetch("/importancias")).json();
  new Chart($("barras"), {
    type: "bar",
    data: {
      labels: datos.map((d) => d.variable),
      datasets: [{
        data: datos.map((d) => d.peso * 100),
        backgroundColor: "#8f3a17",
      }],
    },
    options: {
      indexAxis: "y",
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: {
          title: { display: true, text: "Importancia (%)" },
          grid: { color: "#2a2d22" },
        },
        y: {
          ticks: { color: "#d8d2c0" },
          grid: { display: false },
        },
      },
    },
  });
}

actualizar();
cargarImportancias();
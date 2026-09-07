document.addEventListener("DOMContentLoaded", function () {
  // =========================================================
  // OCULTAR / MOSTRAR VALORES DOS CARDS
  // =========================================================

  const botoes = document.querySelectorAll(".toggle-valores");

  botoes.forEach(function (botao) {
    botao.addEventListener("click", function () {
      const card = botao.closest(".card");

      if (!card) return;

      const valor = card.querySelector(".valor-dashboard");

      if (!valor) return;

      const estaOculto = valor.dataset.oculto === "true";

      if (estaOculto) {
        // MOSTRAR
        valor.textContent = valor.dataset.valor;
        valor.dataset.oculto = "false";

        botao.textContent = "👁️";
        botao.setAttribute("aria-label", "Ocultar valor");
        botao.setAttribute("title", "Ocultar valor");
      } else {
        // ESCONDER
        valor.textContent = "R$ ••••••";
        valor.dataset.oculto = "true";

        botao.textContent = "🙈";
        botao.setAttribute("aria-label", "Mostrar valor");
        botao.setAttribute("title", "Mostrar valor");
      }
    });
  });

  // =========================================================
  // GRÁFICO DE FATURAMENTO
  // =========================================================

  const canvas = document.getElementById("graficoFaturamento");

  if (!canvas || typeof Chart === "undefined") {
    return;
  }

  const elementoDados = document.getElementById("dados-faturamento");

  if (!elementoDados) {
    console.warn("Dados do faturamento não encontrados.");
    return;
  }

  let dados = [];

  try {
    dados = JSON.parse(elementoDados.textContent);
  } catch (erro) {
    console.error("Erro ao carregar dados do gráfico:", erro);
    return;
  }

  // =========================================================
  // TRANSFORMAR OS DADOS
  // =========================================================

  const labels = dados.map(function (item) {
    return item.dia;
  });

  const valores = dados.map(function (item) {
    return Number(item.total);
  });

  // =========================================================
  // CORES DAS BARRAS
  // MAIOR = VERDE
  // MENOR = VERMELHO
  // =========================================================

  const maiorValor = Math.max(...valores);

  const menorValor = Math.min(...valores);

  const cores = valores.map(function (valor) {
    if (valor === maiorValor) {
      return "#22c55e";
    }

    if (valor === menorValor) {
      return "#ef4444";
    }

    return "#3b82f6";
  });

  // =========================================================
  // CRIAR GRÁFICO
  // =========================================================

  new Chart(canvas, {
    type: "bar",

    data: {
      labels: labels,

      datasets: [
        {
          label: "Faturamento",

          data: valores,

          backgroundColor: cores,

          borderWidth: 0,

          borderRadius: 6,

          barPercentage: 0.55,

          categoryPercentage: 0.65,
        },
      ],
    },

    options: {
      responsive: true,

      maintainAspectRatio: false,

      plugins: {
        legend: {
          display: false,
        },

        tooltip: {
          callbacks: {
            label: function (context) {
              return (
                " R$ " +
                context.raw.toLocaleString("pt-BR", {
                  minimumFractionDigits: 2,

                  maximumFractionDigits: 2,
                })
              );
            },
          },
        },
      },

      scales: {
        y: {
          beginAtZero: true,

          ticks: {
            callback: function (value) {
              return "R$ " + Number(value).toLocaleString("pt-BR");
            },
          },
        },

        x: {
          grid: {
            display: false,
          },

          ticks: {
            maxRotation: 0,

            minRotation: 0,
          },
        },
      },
    },
  });
});

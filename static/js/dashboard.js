document.addEventListener("DOMContentLoaded", function () {
  const botoes = document.querySelectorAll(".toggle-valores");

  botoes.forEach(function (botao) {
    botao.addEventListener("click", function () {
      const card = botao.closest(".card");
      const valor = card.querySelector(".valor-dashboard");

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
});

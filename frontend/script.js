/* ==========================================================
   GREEN — Etapa 1
   - Animação por quadros (sprites em assets/sprites)
   - Menu que aparece ao clicar no personagem
   - Interações iniciais: conversar, brincar, alimentar, dormir
   Ainda NÃO há: necessidades, IA, voz, memória (etapas 3 a 5).
   ========================================================== */

(() => {
  "use strict";

  /* ---------- 1. Animações (quadros e velocidade) ---------- */
  const PASTA_SPRITES = "assets/sprites/";

  const ANIMACOES = {
    idle:      { quadros: ["idle_1", "idle_2"],         intervalo: 900 },
    happy:     { quadros: ["happy_1", "happy_2"],       intervalo: 260 },
    surprised: { quadros: ["surprised"],                intervalo: 1000 },
    sleeping:  { quadros: ["sleeping_1", "sleeping_2"], intervalo: 1500 },
    sad:       { quadros: ["sad"],                      intervalo: 1000 },
    curious:   { quadros: ["curious"],                  intervalo: 1000 },
    talking:   { quadros: ["talking_1", "talking_2"],   intervalo: 170 },
    listening: { quadros: ["listening"],                intervalo: 1000 },
  };

  // Pré-carrega todas as imagens para evitar "piscadas" ao trocar de quadro
  const nomesDeQuadros = new Set(["idle_blink"]);
  Object.values(ANIMACOES).forEach(a => a.quadros.forEach(q => nomesDeQuadros.add(q)));
  nomesDeQuadros.forEach(nome => { new Image().src = `${PASTA_SPRITES}${nome}.png`; });

  /* ---------- 2. Elementos da página ---------- */
  const cartao = document.getElementById("cartao");
  const personagem = document.getElementById("personagem");
  const sprite = document.getElementById("sprite");
  const balao = document.getElementById("balao");
  const menu = document.getElementById("menu");
  const painelConversa = document.getElementById("painel-conversa");
  const painelConfig = document.getElementById("painel-configuracoes");
  const formConversa = document.getElementById("form-conversa");
  const entradaMensagem = document.getElementById("entrada-mensagem");
  const listaMensagens = document.getElementById("mensagens");

  /* ---------- 3. Motor de animação ---------- */
  let estadoBase = "idle";      // estado de fundo: "idle" ou "sleeping"
  let animacaoAtual = null;     // animação que está sendo exibida
  let temporizadorQuadro = null;
  let temporizadorTemporario = null;
  let temporizadorPiscar = null;
  let indiceQuadro = 0;

  function mostrarQuadro(nome) {
    sprite.src = `${PASTA_SPRITES}${nome}.png`;
  }

  /** Toca uma animação em loop até ser trocada. */
  function tocar(nome) {
    const anim = ANIMACOES[nome];
    if (!anim) return;
    clearInterval(temporizadorQuadro);
    clearTimeout(temporizadorTemporario);   // uma nova animação cancela a temporária anterior
    animacaoAtual = nome;
    indiceQuadro = 0;
    mostrarQuadro(anim.quadros[0]);
    if (anim.quadros.length > 1) {
      temporizadorQuadro = setInterval(() => {
        indiceQuadro = (indiceQuadro + 1) % anim.quadros.length;
        mostrarQuadro(anim.quadros[indiceQuadro]);
      }, anim.intervalo);
    }
    agendarPiscada();
  }

  /** Toca uma expressão por um tempo e depois volta ao estado base. */
  function expressaoTemporaria(nome, duracaoMs, aoTerminar) {
    clearTimeout(temporizadorTemporario);
    tocar(nome);
    temporizadorTemporario = setTimeout(() => {
      voltarAoEstadoBase();
      if (aoTerminar) aoTerminar();
    }, duracaoMs);
  }

  function voltarAoEstadoBase() {
    clearTimeout(temporizadorTemporario);
    tocar(estadoBase);
  }

  /** Piscar de olhos ocasional, apenas quando está em idle. */
  function agendarPiscada() {
    clearTimeout(temporizadorPiscar);
    if (animacaoAtual !== "idle") return;
    temporizadorPiscar = setTimeout(() => {
      if (animacaoAtual !== "idle") return;
      mostrarQuadro("idle_blink");
      setTimeout(() => {
        if (animacaoAtual === "idle") {
          mostrarQuadro(ANIMACOES.idle.quadros[indiceQuadro]);
        }
        agendarPiscada();
      }, 160);
    }, 2500 + Math.random() * 3500);
  }

  /* ---------- 4. Balão de fala ---------- */
  let temporizadorBalao = null;

  function falar(texto, duracaoMs = 2600) {
    balao.textContent = texto;
    balao.hidden = false;
    clearTimeout(temporizadorBalao);
    if (duracaoMs > 0) {
      temporizadorBalao = setTimeout(() => { balao.hidden = true; }, duracaoMs);
    }
  }

  function esconderBalao() {
    clearTimeout(temporizadorBalao);
    balao.hidden = true;
  }

  /* ---------- 5. Menu e painéis ---------- */
  function menuAberto() { return !menu.hidden; }

  function abrirMenu() {
    fecharPaineis();
    menu.hidden = false;
    personagem.setAttribute("aria-expanded", "true");
    expressaoTemporaria("surprised", 450, () => {
      if (menuAberto()) tocar("curious");
    });
  }

  function fecharMenu() {
    if (!menuAberto()) return;
    menu.hidden = true;
    personagem.setAttribute("aria-expanded", "false");
    if (animacaoAtual === "curious") voltarAoEstadoBase();
  }

  function fecharPaineis() {
    painelConversa.hidden = true;
    painelConfig.hidden = true;
  }

  /* ---------- 6. Reação ao clique no Green ---------- */
  function aoClicarNoPersonagem(evento) {
    evento.stopPropagation();

    if (estadoBase === "sleeping") {
      acordar();
      return;
    }
    if (menuAberto()) {
      fecharMenu();
    } else {
      esconderBalao();
      abrirMenu();
    }
  }

  function acordar() {
    estadoBase = "idle";
    expressaoTemporaria("surprised", 900, () => falar("Bom dia! Já estou acordado."));
  }

  /* ---------- 7. Ações do menu ---------- */
  const ACOES = {
    conversar() {
      fecharMenu();
      painelConversa.hidden = false;
      esconderBalao();
      tocar("listening");
      entradaMensagem.focus();
    },

    brincar() {
      fecharMenu();
      falar("Eba! Vamos brincar!");
      expressaoTemporaria("happy", 3200);
    },

    alimentar() {
      fecharMenu();
      falar("Nham nham! Obrigado!");
      expressaoTemporaria("happy", 2400);
    },

    dormir() {
      fecharMenu();
      estadoBase = "sleeping";
      falar("Zzz... boa noite.", 2200);
      tocar("sleeping");
    },

    configuracoes() {
      fecharMenu();
      esconderBalao();
      painelConfig.hidden = false;
      tocar(estadoBase);
    },
  };

  menu.addEventListener("click", (evento) => {
    const botao = evento.target.closest("button[data-acao]");
    if (!botao) return;
    const acao = ACOES[botao.dataset.acao];
    if (acao) acao();
  });

  /* ---------- 8. Conversa (provisória, sem IA) ---------- */
  function adicionarMensagem(texto, autor) {
    const item = document.createElement("li");
    item.textContent = texto;
    if (autor === "usuario") item.classList.add("usuario");
    listaMensagens.appendChild(item);
    listaMensagens.scrollTop = listaMensagens.scrollHeight;
  }

  formConversa.addEventListener("submit", (evento) => {
    evento.preventDefault();
    const texto = entradaMensagem.value.trim();
    if (!texto) return;

    adicionarMensagem(texto, "usuario");
    entradaMensagem.value = "";

    // Resposta provisória: a IA real será conectada na Etapa 4.
    const resposta = "Ainda não consigo conversar de verdade. Minha inteligência chega na Etapa 4!";
    adicionarMensagem(resposta, "green");
    expressaoTemporaria("talking", 1800, () => {
      if (!painelConversa.hidden) tocar("listening");
    });
  });

  /* ---------- 9. Fechar painéis e menu ---------- */
  document.querySelectorAll("[data-fechar]").forEach((botao) => {
    botao.addEventListener("click", () => {
      document.getElementById(botao.dataset.fechar).hidden = true;
      voltarAoEstadoBase();
    });
  });

  // Clique fora do menu fecha o menu
  document.addEventListener("click", (evento) => {
    if (menuAberto() && !menu.contains(evento.target)) fecharMenu();
  });

  document.addEventListener("keydown", (evento) => {
    if (evento.key !== "Escape") return;
    fecharMenu();
    if (!painelConversa.hidden || !painelConfig.hidden) {
      fecharPaineis();
      voltarAoEstadoBase();
    }
  });

  personagem.addEventListener("click", aoClicarNoPersonagem);

  /* ---------- 10. Início ---------- */
  tocar("idle");
})();

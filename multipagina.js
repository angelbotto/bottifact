/* NOTA TIKIN · multipágina · septiembre 2026
   Pegar DESPUÉS de interacciones.js, dentro de su propio <script>.

   Reparte una nota larga en páginas con su propio temario, sin cargar nada remoto y sin
   romper el enlace directo: cada página tiene su id y queda en el hash.

   Espera este esqueleto —ver componentes.md, «Multipágina»—:
     .barra con un <button data-ir="id"> por página
     main.hoja.multipagina  >  article.pagina[id]  (la primera con class="viva")
     .paginacion con [data-nav="prev"] y [data-nav="next"]

   Dos cosas que resuelve y que no son evidentes:

   1. El índice de interacciones.js recorre TODOS los enlaces del documento. Las secciones
      de las páginas ocultas miden cero, así que las da por pasadas y tacha el temario
      entero. Aquí se recalcula mirando sólo la página viva, con clases propias
      (`aqui-visto`, `aqui-actual`) que en la hoja pintan por encima de las suyas.
   2. Al cambiar de página cambia la altura del documento; se avisa para que la regla de
      lectura y el índice se recalculen. */
(function () {
  "use strict";
  var hoja = document.querySelector(".hoja.multipagina");
  if (!hoja) return;
  var botones = Array.prototype.slice.call(document.querySelectorAll(".barra [data-ir]"));
  var pags = botones.map(function (b) { return document.getElementById(b.dataset.ir); });
  if (!pags.length || pags.some(function (p) { return !p; })) return;
  var titulos = botones.map(function (b) {
    var n = b.querySelector(".n");
    return (n ? b.textContent.replace(n.textContent, "") : b.textContent).trim();
  });
  var nav = document.querySelector("[data-paginacion]");
  var prev = nav && nav.querySelector('[data-nav="prev"]');
  var next = nav && nav.querySelector('[data-nav="next"]');
  var actual = 0;

  function pintarNav() {
    if (!nav) return;
    prev.disabled = actual === 0;
    next.disabled = actual === pags.length - 1;
    var a = prev.querySelector(".tit"), b = next.querySelector(".tit");
    if (a) a.textContent = actual > 0 ? titulos[actual - 1] : "—";
    if (b) b.textContent = actual < pags.length - 1 ? titulos[actual + 1] : "—";
  }

  function ir(i, conFoco) {
    if (i < 0 || i >= pags.length) return;
    actual = i;
    pags.forEach(function (p, k) { p.hidden = k !== i; p.classList.toggle("viva", k === i); });
    botones.forEach(function (b, k) {
      if (k === i) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current");
    });
    pintarNav();
    if (location.hash.slice(1) !== pags[i].id) history.replaceState(null, "", "#" + pags[i].id);
    var suave = conFoco && !matchMedia("(prefers-reduced-motion: reduce)").matches;
    scrollTo({ top: 0, behavior: suave ? "smooth" : "auto" });
    if (conFoco) {
      var h = pags[i].querySelector("h1");
      if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
    }
    document.dispatchEvent(new CustomEvent("nota:pagina", { detail: { indice: i, id: pags[i].id } }));
  }

  botones.forEach(function (b, k) { b.addEventListener("click", function () { ir(k, true); }); });
  if (prev) prev.addEventListener("click", function () { ir(actual - 1, true); });
  if (next) next.addEventListener("click", function () { ir(actual + 1, true); });
  addEventListener("hashchange", function () {
    var i = pags.findIndex(function (p) { return p.id === location.hash.slice(1); });
    if (i >= 0 && i !== actual) ir(i, true);
  });

  /* El temario, mirando sólo la página viva. */
  function indiceVivo() {
    var pg = pags[actual];
    if (!pg) return;
    Array.prototype.forEach.call(document.querySelectorAll(".indice li"), function (li) {
      if (!pg.contains(li)) li.classList.remove("aqui-visto", "aqui-actual");
    });
    var links = Array.prototype.slice.call(pg.querySelectorAll('.indice a[href^="#"]'));
    var act = -1;
    links.forEach(function (a, i) {
      var s = document.getElementById(a.hash.slice(1));
      if (s && s.getBoundingClientRect().top <= 120) act = i;
    });
    links.forEach(function (a, i) {
      var li = a.closest("li");
      if (!li) return;
      li.classList.toggle("aqui-visto", i < act);
      li.classList.toggle("aqui-actual", i === act);
    });
  }
  var pend = 0;
  function programar() {
    if (!pend) pend = requestAnimationFrame(function () { pend = 0; indiceVivo(); });
  }
  addEventListener("scroll", programar, { passive: true });
  addEventListener("resize", programar);
  document.addEventListener("nota:pagina", programar);

  var inicial = pags.findIndex(function (p) { return p.id === location.hash.slice(1); });
  if (inicial > 0) ir(inicial, false); else { pintarNav(); programar(); }
})();

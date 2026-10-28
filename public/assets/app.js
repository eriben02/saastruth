(function () {
  window.chargeflowNetFromGmv = function (gmvMo) {
    var disputed = gmvMo * 12 * 0.0065;
    return Math.round(disputed * 0.65 * 0.75);
  };

  function normalizeResultLayout() {
    document.querySelectorAll(".wb-result-col").forEach(function (col) {
      var total = col.querySelector(".wb-big-total");
      var drawer = col.querySelector(":scope > .math-drawer, .math-drawer");
      if (total && drawer && total.nextElementSibling !== drawer) {
        total.insertAdjacentElement("afterend", drawer);
      }
    });
    var order = [
      ".summary-label",
      ".summary-metric",
      ".math-drawer",
      ".summary-scenario",
      ".summary-breakdown",
      ".summary-caveat",
      ".summary-actions"
    ];
    document.querySelectorAll(".summary-card").forEach(function (card) {
      var desired = [];
      order.forEach(function (sel) {
        var el = card.querySelector(":scope > " + sel);
        if (el) desired.push(el);
      });
      var current = Array.prototype.filter.call(card.children, function (el) {
        return desired.indexOf(el) !== -1;
      });
      var same = current.length === desired.length && current.every(function (el, i) {
        return el === desired[i];
      });
      if (!same) desired.forEach(function (el) { card.appendChild(el); });
    });
  }

  var layingOut = false;
  function scheduleLayout() {
    if (layingOut) return;
    layingOut = true;
    normalizeResultLayout();
    layingOut = false;
  }

  document.addEventListener("toggle", function (event) {
    var drawer = event.target;
    if (!drawer || !drawer.classList || !drawer.classList.contains("math-drawer")) return;
    if (!drawer.open) return;
    document.querySelectorAll("details.math-drawer[open]").forEach(function (other) {
      if (other !== drawer) other.open = false;
    });
  }, true);

  document.addEventListener("click", function (event) {
    document.querySelectorAll("details.math-drawer[open]").forEach(function (drawer) {
      if (!drawer.contains(event.target)) drawer.open = false;
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    document.querySelectorAll("details.math-drawer[open]").forEach(function (drawer) {
      drawer.open = false;
    });
  });

  document.addEventListener("DOMContentLoaded", function () {
    scheduleLayout();
    if (typeof window.renderDirectory === "function") window.renderDirectory();
    var root = document.body;
    if (!root || typeof MutationObserver === "undefined") return;
    var observer = new MutationObserver(function () { scheduleLayout(); });
    observer.observe(root, { childList: true, subtree: true });
  });
})();

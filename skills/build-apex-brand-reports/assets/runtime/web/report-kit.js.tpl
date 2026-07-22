/* Optional static copy. The essential idempotent runtime is also returned inline by {{ENGINE_PACKAGE}}. */
(function (window, document) {
  "use strict";
  function init(context) {
    (context || document).querySelectorAll("[data-abrk-root]").forEach(function (root) {
      if (root.dataset.abrkStaticBound === "true") return;
      root.dataset.abrkStaticBound = "true";
    });
  }
  window.ApexBrandReportKitStatic = { init: init };
  init(document);
  document.addEventListener("apexafterrefresh", function (event) { init(event.target); });
})(window, document);

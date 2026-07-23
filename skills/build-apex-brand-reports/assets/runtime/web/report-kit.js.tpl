/* Optional static copy. The essential idempotent runtime is also returned inline by {{ENGINE_PACKAGE}}. */
(function (window, document) {
  "use strict";
  function roots(context) {
    var scope = context || document;
    var found = [];
    if (scope.matches && scope.matches("[data-abrk-root]")) found.push(scope);
    return found.concat(Array.prototype.slice.call(scope.querySelectorAll("[data-abrk-root]")));
  }
  function init(context) {
    roots(context).forEach(function (root) {
      if (root.dataset.abrkStaticBound === "true") return;
      root.dataset.abrkStaticBound = "true";
    });
  }
  window.ApexBrandReportKitStatic = { init: init };
  init(document);
  if (window.apex && window.apex.jQuery) {
    window.apex.jQuery(document)
      .off("apexafterrefresh.abrkStatic")
      .on("apexafterrefresh.abrkStatic", function (event) { init(event.target); });
  } else {
    document.addEventListener("apexafterrefresh", function (event) { init(event.target); });
  }
})(window, document);

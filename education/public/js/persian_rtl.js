// Persian-first RTL setup for Frappe Desk and website pages.
(function () {
  function applyPersianDirection() {
    document.documentElement.setAttribute("lang", "fa");
    document.documentElement.setAttribute("dir", "rtl");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyPersianDirection, { once: true });
  } else {
    applyPersianDirection();
  }
})();

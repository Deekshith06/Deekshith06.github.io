(() => {
  "use strict";

  const tabs = [...document.querySelectorAll("[data-tab]")];
  const panels = [...document.querySelectorAll("[data-panel]")];
  const openers = [...document.querySelectorAll("[data-open-panel]")];

  const activate = (name, { focus = false } = {}) => {
    const targetTab = tabs.find((tab) => tab.dataset.tab === name);
    const targetPanel = panels.find((panel) => panel.dataset.panel === name);
    if (!targetTab || !targetPanel) return;

    tabs.forEach((tab) => {
      const active = tab === targetTab;
      tab.classList.toggle("is-active", active);
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
    });

    panels.forEach((panel) => {
      const active = panel === targetPanel;
      panel.hidden = !active;
      panel.classList.toggle("is-active", active);
    });

    if (focus) targetTab.focus();
    history.replaceState(null, "", `#${name}`);
  };

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activate(tab.dataset.tab));
    tab.addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      let nextIndex = index;
      if (event.key === "ArrowRight") nextIndex = (index + 1) % tabs.length;
      if (event.key === "ArrowLeft") nextIndex = (index - 1 + tabs.length) % tabs.length;
      if (event.key === "Home") nextIndex = 0;
      if (event.key === "End") nextIndex = tabs.length - 1;
      activate(tabs[nextIndex].dataset.tab, { focus: true });
    });
  });

  openers.forEach((button) => {
    button.addEventListener("click", () => activate(button.dataset.openPanel));
  });

  const hashPanel = window.location.hash.slice(1);
  if (tabs.some((tab) => tab.dataset.tab === hashPanel)) activate(hashPanel);
})();

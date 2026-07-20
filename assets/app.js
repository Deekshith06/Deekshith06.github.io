(() => {
  "use strict";

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const portraitResult = document.querySelector("#portrait-result");
  const typedNodes = [...document.querySelectorAll("[data-type]")];

  const sleep = (ms) => new Promise((resolve) => window.setTimeout(resolve, ms));

  // Reveal complete words from left to right, then continue on the next terminal line.
  const typeText = async (node, text, speed = 22) => {
    const tokens = text.match(/\S+\s*/g) || [text];
    node.textContent = "";
    for (const token of tokens) {
      node.textContent += token;
      await sleep(speed);
    }
  };

  const runTerminalSequence = async () => {
    if (reducedMotion) {
      portraitResult?.classList.add("is-visible");
      return;
    }

    const entries = typedNodes.map((node) => ({ node, text: node.dataset.type || node.textContent || "" }));
    entries.forEach(({ node }) => { node.textContent = ""; });

    await sleep(160);
    for (const [index, entry] of entries.entries()) {
      const speed = index === 0 ? 42 : index >= entries.length - 2 ? 28 : 20;
      await typeText(entry.node, entry.text, speed);
      await sleep(index === 0 ? 55 : 18);
    }
  };

  window.addEventListener("load", () => {
    runTerminalSequence().catch(() => {
      typedNodes.forEach((node) => { node.textContent = node.dataset.type || ""; });
    });

    if (reducedMotion) {
      portraitResult?.classList.add("is-visible");
    } else {
      window.setTimeout(() => portraitResult?.classList.add("is-visible"), 4800);
    }
  }, { once: true });

  const mobileTabs = [...document.querySelectorAll("[data-mobile-target]")];
  const mobilePanels = [...document.querySelectorAll("[data-mobile-panel]")];

  const activateMobilePanel = (name) => {
    mobileTabs.forEach((tab) => tab.classList.toggle("is-active", tab.dataset.mobileTarget === name));
    mobilePanels.forEach((panel) => panel.classList.toggle("is-mobile-active", panel.dataset.mobilePanel === name));
  };

  mobileTabs.forEach((tab) => {
    tab.addEventListener("click", () => activateMobilePanel(tab.dataset.mobileTarget));
  });
})();

/**
 * Script de exploración profunda de Shadow DOM.
 * Desciende recursivamente a través de el.shadowRoot hasta N niveles de profundidad
 * para extraer texto, botones e inputs inaccesibles en el árbol de DOM estándar.
 */

async function walkShadowDOM(page, maxDepth = 16) {
  return await page.evaluate(({ maxDepth }) => {
    const results = [];

    function traverse(node, depth = 0) {
      if (!node || depth > maxDepth) return;

      // Extraer información del nodo actual si es interactivo o contiene texto
      if (node.nodeType === Node.ELEMENT_NODE) {
        const tagName = node.tagName.toLowerCase();
        const isInteractive = ['button', 'a', 'input', 'select', 'textarea'].includes(tagName);
        const textContent = node.innerText ? node.innerText.trim() : '';

        if (isInteractive || textContent.length > 0) {
          results.push({
            tagName,
            id: node.id || null,
            className: node.className || null,
            text: textContent.substring(0, 150),
            attributes: Array.from(node.attributes || []).reduce((acc, attr) => {
              acc[attr.name] = attr.value;
              return acc;
            }, {}),
            depth
          });
        }
      }

      // Si el elemento tiene Shadow Root, descender recursivamente
      if (node.shadowRoot) {
        Array.from(node.shadowRoot.children).forEach(child => traverse(child, depth + 1));
      }

      // Descender por hijos estándar
      if (node.children) {
        Array.from(node.children).forEach(child => traverse(child, depth + 1));
      }
    }

    traverse(document.body, 0);
    return results;
  }, { maxDepth });
}

module.exports = { walkShadowDOM };
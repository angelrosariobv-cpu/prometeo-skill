const { chromium } = require('playwright');

/**
 * Inicializa una instancia de navegador emulada con flags de evasión de automatización.
 */
async function launchStealthBrowser(options = {}) {
  const browser = await chromium.launch({
    headless: options.headless !== undefined ? options.headless : true,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-web-security',
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  });

  const context = await browser.newContext({
    userAgent: options.userAgent || 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    viewport: { width: 1920, height: 1080 },
    locale: 'es-ES',
    timezoneId: 'America/Panama'
  });

  // Ocultar la propiedad navigator.webdriver
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined,
    });
  });

  return { browser, context };
}

module.exports = { launchStealthBrowser };
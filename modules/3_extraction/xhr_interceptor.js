/**
 * Intercepta pasivamente las llamadas Fetch/XHR de red para capturar
 * los payloads JSON/datos en segundo plano antes del renderizado de la UI.
 */
async function attachXHRInterceptor(page, targetUrlPatterns = ['/api/', '/query', '/v1/']) {
  const capturedResponses = [];

  page.on('response', async (response) => {
    const url = response.url();
    const isTarget = targetUrlPatterns.some(pattern => url.includes(pattern));

    if (isTarget && response.status() === 200) {
      try {
        const contentType = response.headers()['content-type'] || '';
        if (contentType.includes('application/json')) {
          const jsonBody = await response.json();
          capturedResponses.push({
            url,
            status: response.status(),
            contentType,
            payload: jsonBody,
            timestamp: new Date().toISOString()
          });
        }
      } catch (err) {
        // Ignorar fallos de lectura en streams binarios
      }
    }
  });

  return capturedResponses;
}

module.exports = { attachXHRInterceptor };
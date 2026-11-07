import json
import re
from typing import Dict, List, Optional
import requests

class ContextDiscovery:
    """
    Rastrea y analiza páginas de ayuda, documentación (/help, /docs)
    o APIs de documentos compartidos para construir un diccionario de términos,
    nombres de tablas y esquemas válidos del sitio.
    """

    DEFAULT_DOC_PATHS = [
        "/help",
        "/docs",
        "/api-docs",
        "/swagger",
        "/platform/document/v1/documents",  # API de cuadernos/documentos compartidos
    ]

    def __init__(self, base_url: str, session: Optional[requests.Session] = None):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.vocabulary: Dict[str, List[str]] = {
            "tables": [],
            "fields": [],
            "keywords": [],
            "endpoints": []
        }

    def scan_documentation_endpoints(self) -> Dict[str, List[str]]:
        """Intenta ubicar y extraer texto de las rutas de ayuda conocidas."""
        discovered_text = []

        for path in self.DEFAULT_DOC_PATHS:
            target_url = f"{self.base_url}{path}"
            try:
                response = self.session.get(target_url, timeout=5)
                if response.status_code == 200:
                    self.vocabulary["endpoints"].append(path)
                    discovered_text.append(response.text)
            except requests.RequestException:
                continue

        full_doc_content = "\n".join(discovered_text)
        self._extract_vocabulary_from_text(full_doc_content)
        return self.vocabulary

    def _extract_vocabulary_from_text(self, text: str) -> None:
        """Aísla nombres de tablas, campos y palabras clave usando regex semántico."""
        if not text:
            return

        table_matches = re.findall(r'\b(?:table|bucket|dataset|from)\s+([a-zA-Z0-9_\.\-]+)', text, re.IGNORECASE)
        field_matches = re.findall(r'\b([a-zA-Z0-9_\.]+\.[a-zA-Z0-9_]+)\b', text)

        self.vocabulary["tables"] = sorted(list(set(table_matches)))
        self.vocabulary["fields"] = sorted(list(set(field_matches)))

    def save_vocabulary_cache(self, output_filepath: str) -> None:
        """Guarda el diccionario extraído en la memoria persistente del agente."""
        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(self.vocabulary, f, indent=2, ensure_ascii=False)
        print(f"[ContextDiscovery] Diccionario guardado en {output_filepath}")
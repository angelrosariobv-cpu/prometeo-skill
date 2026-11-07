import json
import re
from typing import Any, Dict, List, Union
from bs4 import BeautifulSoup

class MultiformatParser:
    """Parsea y normaliza datos en crudo provenientes de JSON, XML, HTML o registros de texto plano."""

    @staticmethod
    def parse_payload(raw_data: str, content_type_hint: str = "auto") -> Union[Dict[str, Any], List[Any], str]:
        """Detecta automáticamente el formato y entrega una estructura limpia."""
        if not raw_data:
            return ""

        data_str = raw_data.strip()

        # 1. Intento de Parseo JSON
        if content_type_hint == "json" or data_str.startswith(("{", "[")):
            try:
                return json.loads(data_str)
            except json.JSONDecodeError:
                pass

        # 2. Intento de Parseo XML/HTML
        if content_type_hint in ("xml", "html") or data_str.startswith("<"):
            try:
                soup = BeautifulSoup(data_str, "xml" if content_type_hint == "xml" else "html.parser")
                return soup.get_text(separator="\n", strip=True)
            except Exception:
                pass

        # 3. Fallback a texto plano / Log regex extractor
        return data_str

    @staticmethod
    def extract_log_entries(log_text: str) -> List[Dict[str, str]]:
        """Extrae entradas estructuradas de archivos de log de texto plano."""
        entries = []
        pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?)\s+\[(?P<level>[A-Z]+)\]\s+(?P<message>.*)'
        
        for line in log_text.splitlines():
            match = re.match(pattern, line)
            if match:
                entries.append(match.groupdict())
            else:
                entries.append({"raw": line})
        return entries
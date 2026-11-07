import re
from typing import Any, Dict, List, Optional

class PatternExtractor:
    """Aísla métricas, flags o datos específicos filtrando el ruido irrelevante del corpus."""

    @staticmethod
    def filter_noise(records: List[Dict[str, Any]], exclude_levels: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Descarta registros de prueba o sin valor (ej. loglevel NONE o mensajes vacíos)."""
        if exclude_levels is None:
            exclude_levels = ["NONE", "TRACE", "DEBUG"]

        clean_records = []
        for r in records:
            # Filtrar por loglevel si existe
            level = str(r.get("loglevel", r.get("level", ""))).upper()
            if level in exclude_levels:
                continue

            # Filtrar registros totalmente vacíos
            if not any(r.values()):
                continue

            clean_records.append(r)

        return clean_records

    @staticmethod
    def extract_by_regex(text: str, pattern: str) -> List[str]:
        """Busca coincidencias exactas con patrones regex (útil para banderas CTF, UUIDs o tokens)."""
        try:
            return re.findall(pattern, text)
        except re.error as e:
            print(f"[PatternExtractor] Error en el patrón regex '{pattern}': {e}")
            return []

    @staticmethod
    def calculate_numeric_metric(records: List[Dict[str, Any]], target_key: str, aggregation: str = "sum") -> float:
        """Calcula agregaciones numéricas sobre una clave específica de los registros filtrados."""
        values = []
        for r in records:
            val = r.get(target_key)
            if val is not None:
                try:
                    values.append(float(val))
                except (ValueError, TypeError):
                    continue

        if not values:
            return 0.0

        if aggregation == "sum":
            return round(sum(values), 2)
        elif aggregation == "avg":
            return round(sum(values) / len(values), 2)
        elif aggregation == "count":
            return float(len(values))

        return 0.0
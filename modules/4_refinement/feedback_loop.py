import re
from typing import Dict, Optional, Tuple

class FeedbackLoop:
    """Analiza respuestas de error de consulta/API y genera ajustes automáticos de sintaxis."""

    COMMON_SYNTAX_RULES = [
        # Detección de comillas simples prohibidas (DQL / DPL)
        (r"single quotes are not supported", "replace_single_quotes"),
        # Campo inexistente
        (r"FIELD_DOES_NOT_EXIST", "fix_field_name"),
        # Error de comillas de escape
        (r"invalid escape sequence", "fix_escapes"),
    ]

    @classmethod
    def analyze_error_body(cls, error_body: str, original_query: str) -> Tuple[bool, str, str]:
        """
        Inspecciona el cuerpo de error HTTP 400 y devuelve (solucionado, query_corregida, diagnóstico).
        """
        if not error_body:
            return False, original_query, "Error sin cuerpo de respuesta."

        # Rule 1: Reemplazar comillas simples por dobles
        if "single quotes" in error_body.lower():
            fixed_query = cls._replace_single_quotes_in_literals(original_query)
            return True, fixed_query, "Se reemplazaron comillas simples por comillas dobles en la query."

        # Rule 2: Error de operador 'contains' o 'like'
        if "contains" in error_body.lower() or "like" in error_body.lower():
            fixed_query = re.sub(r'\bcontains\b', 'matchesPhrase', original_query, flags=re.IGNORECASE)
            return True, fixed_query, "Se reemplazó operador prohibido por 'matchesPhrase'."

        # Rule 3: Error de nombre de entidad id vs entity.name
        if "entity.id" in error_body:
            fixed_query = original_query.replace("entity.id", "id")
            return True, fixed_query, "Se corrigió 'entity.id' a 'id'."

        return False, original_query, f"Error no catalogado: {error_body[:150]}"

    @staticmethod
    def _replace_single_quotes_in_literals(query: str) -> str:
        """Reemplaza comillas simples externas por dobles en cadenas de consulta."""
        # Cambia 'cadena' por "cadena"
        return re.sub(r"'([^'\\]*(?:\\.[^'\\]*)*)'", r'"\1"', query)
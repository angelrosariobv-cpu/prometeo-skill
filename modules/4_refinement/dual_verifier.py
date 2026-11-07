import time
from typing import Any, Callable, Dict, Tuple

class DualVerifier:
    """Verifica resultados por dos vías independientes antes de darlos por válidos."""

    @staticmethod
    def verify_results(result_method_a: Any, result_method_b: Any, tolerance: float = 0.001) -> Tuple[bool, str]:
        """Compara las respuestas de dos métodos de cálculo distintos."""
        if type(result_method_a) != type(result_method_b):
            # Convertir a flotantes si ambos son numéricos
            try:
                val_a = float(result_method_a)
                val_b = float(result_method_b)
                diff = abs(val_a - val_b)
                if diff <= tolerance:
                    return True, f"Coincidencia exacta por conversión (Val: {val_a})"
                return False, f"Discrepancia numérica: Método A = {val_a}, Método B = {val_b}"
            except (ValueError, TypeError):
                return False, f"Discrepancia de tipos: Método A ({type(result_method_a)}) vs Método B ({type(result_method_b)})"

        if result_method_a == result_method_b:
            return True, f"Coincidencia exacta de 100%: {result_method_a}"

        return False, f"Discrepancia de valores: A='{result_method_a}' vs B='{result_method_b}'"

    @staticmethod
    def check_stream_stability(fetch_fn: Callable[[], Any], gap_seconds: int = 5) -> Tuple[bool, Any, Any]:
        """
        Realiza dos lecturas espaciadas en el tiempo para confirmar si un conjunto
        de datos es estático o si está cambiando activamente en vivo.
        """
        first_run = fetch_fn()
        time.sleep(gap_seconds)
        second_run = fetch_fn()

        is_stable = (first_run == second_run)
        return is_stable, first_run, second_run
import time
import requests

class ChallengeHandler:
    """Maneja respuestas de límite de tasa (HTTP 429) y denegación de acceso (401/403)."""

    def __init__(self, max_retries: int = 3, base_backoff_sec: float = 2.0):
        self.max_retries = max_retries
        self.base_backoff_sec = base_backoff_sec

    def execute_with_backoff(self, request_func, *args, **kwargs):
        """Ejecuta una función de petición con reintentos y backoff exponencial."""
        for attempt in range(1, self.max_retries + 1):
            response = request_func(*args, **kwargs)
            status_code = getattr(response, "status_code", 200)

            if status_code == 200:
                return response

            if status_code == 429:
                wait_time = self.base_backoff_sec * (2 ** (attempt - 1))
                print(f"[Warning] HTTP 429: Límite de peticiones alcanzado. Esperando {wait_time}s...")
                time.sleep(wait_time)
                continue

            if status_code in (401, 403):
                print(f"[Error] HTTP {status_code}: Acceso denegado o sesión expirada.")
                return response

            print(f"[Warning] HTTP {status_code} en intento {attempt}/{self.max_retries}.")

        return response
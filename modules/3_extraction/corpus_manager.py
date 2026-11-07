import json
import os
from typing import Any, List

class CorpusManager:
    """Maneja el almacenamiento en disco y paginación de grandes volúmenes de datos scrapeados."""

    def __init__(self, storage_dir: str = ".agents/skills/prometeo/storage"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_chunk(self, chunk_id: str, data: Any) -> str:
        """Guarda un bloque de datos en un archivo JSON temporal para no saturar memoria RAM."""
        filepath = os.path.join(self.storage_dir, f"chunk_{chunk_id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filepath

    def read_chunk(self, chunk_id: str) -> Any:
        """Lee un bloque específico de datos desde disco."""
        filepath = os.path.join(self.storage_dir, f"chunk_{chunk_id}.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def merge_chunks(self, chunk_ids: List[str]) -> List[Any]:
        """Combina múltiples bloques descargados en una sola lista."""
        merged = []
        for cid in chunk_ids:
            chunk_data = self.read_chunk(cid)
            if isinstance(chunk_data, list):
                merged.extend(chunk_data)
            elif chunk_data:
                merged.append(chunk_data)
        return merged
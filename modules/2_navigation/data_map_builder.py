from datetime import datetime
from typing import Any, Dict, List

class DataMapBuilder:
    """
    Construye un inventario de fuentes de datos. Clasifica datasets entre
    'Estáticos' (congelados) y 'Streams Vivos' midiendo la evolución del timestamp.
    """

    def __init__(self):
        self.inventory: Dict[str, Dict[str, Any]] = {}

    def profile_dataset(
        self,
        dataset_id: str,
        records: List[Dict[str, Any]],
        timestamp_key: str = "timestamp"
    ) -> Dict[str, Any]:
        """
        Analiza un conjunto de registros de muestra para determinar si es un stream
        activo o un conjunto de datos estático (vital para evitar sumas acumulativas erróneas).
        """
        if not records:
            return {"status": "empty", "type": "unknown"}

        timestamps = []
        for r in records:
            val = r.get(timestamp_key)
            if val:
                try:
                    # Soporta ISO strings o timestamps numéricos
                    if isinstance(val, (int, float)):
                        ts = datetime.fromtimestamp(val / 1000.0 if val > 1e11 else val)
                    else:
                        ts = datetime.fromisoformat(str(val).replace("Z", "+00:00"))
                    timestamps.append(ts)
                except ValueError:
                    continue

        if not timestamps:
            is_stream = False
            min_ts, max_ts = None, None
        else:
            min_ts = min(timestamps)
            max_ts = max(timestamps)
            # Si el registro más reciente dista menos de 2 minutos del tiempo actual, es un Stream Vivo
            now = datetime.now(max_ts.tzinfo) if max_ts.tzinfo else datetime.now()
            time_diff_seconds = (now - max_ts).total_seconds()
            is_stream = time_diff_seconds < 120

        profile = {
            "total_sample_count": len(records),
            "min_timestamp": min_ts.isoformat() if min_ts else None,
            "max_timestamp": max_ts.isoformat() if max_ts else None,
            "is_live_stream": is_stream,
            "category": "DYNAMIC_STREAM" if is_stream else "STATIC_DATASET",
            "sample_keys": list(records[0].keys()) if records else []
        }

        self.inventory[dataset_id] = profile
        return profile
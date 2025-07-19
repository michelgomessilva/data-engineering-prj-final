"""
VehiclesNormalizer

Classe responsável por transformar os dados brutos retornados pela API da Carris
em uma estrutura tabular compatível com o schema do domínio (vehicle_schema).

Responsabilidades:
- Validar e converter os campos de entrada (normalização).
- Garantir tipos consistentes mesmo com dados ausentes ou malformados.

Método:
- normalize(data: list) -> list[dict]
"""

from infrastructure.logging.logger import logger


class VehiclesNormalizer:
    @staticmethod
    def normalize(data: list) -> list[dict]:
        normalized = []
        for item in data:
            try:
                normalized.append(
                    {
                        "vehicle_id": str(item.get("id", "")),
                        "line_id": str(item.get("line_id", "")),
                        "latitude": float(item.get("lat", 0.0) or 0.0),
                        "longitude": float(item.get("lon", 0.0) or 0.0),
                        "timestamp": int(item.get("timestamp", 0) or 0),
                        "current_status": str(item.get("current_status", "")),
                        "speed": float(item.get("speed", 0.0) or 0.0),
                        "trip_id": str(item.get("trip_id", "")),
                        "stop_id": str(item.get("stop_id", "")),
                        "bearing": int(item.get("bearing", "")),
                        "block_id": str(item.get("block_id", "")),
                        "pattern_id": str(item.get("pattern_id", "")),
                        "route_id": str(item.get("route_id", "")),
                        "schedule_relationship": str(
                            item.get("schedule_relationship", "")
                        ),
                        "shift_id": str(item.get("shift_id", "")),
                    }
                )
            except Exception as e:
                logger.warning(f"Erro ao normalizar item: {item}\n{e}")
        return normalized

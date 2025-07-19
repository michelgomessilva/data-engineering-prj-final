"""
StopsNormalizer

Classe responsável por transformar os dados brutos retornados pela API da Carris
em uma estrutura tabular compatível com o schema do domínio (stops_schema).

Responsabilidades:
- Validar e converter os campos de entrada (normalização).
- Garantir tipos consistentes mesmo com dados ausentes ou malformados.

Método:
- normalize(data: list) -> list[dict]
"""

from infrastructure.logging.logger import logger


class StopsNormalizer:
    @staticmethod
    def normalize(data: list) -> list[dict]:
        normalized = []
        for item in data:
            try:
                normalized.append(
                    {
                        "district_id": str(item.get("district_id", "")),
                        "district_name": str(item.get("district_name", "")),
                        "facilities": item.get("facilities", []),
                        "id": str(item.get("id", "")),
                        "lat": str(item.get("lat", "")),
                        "lines": item.get("lines", []),
                        "locality": str(item.get("locality", "")),
                        "lon": str(item.get("lon", "")),
                        "municipality_id": str(item.get("municipality_id", "")),
                        "municipality_name": str(item.get("municipality_name", "")),
                        "stop_name": str(item.get("name", "")),
                        "operational_status": str(item.get("operational_status", "")),
                        "parish_id": str(item.get("parish_id", "")),
                        "parish_name": str(item.get("parish_name", "")),
                        "patterns": item.get("patterns", []),
                        "region_id": str(item.get("region_id", "")),
                        "region_name": str(item.get("region_name", "")),
                        "routes": item.get("routes", []),
                        "short_name": str(item.get("short_name", "")),
                        "stop_id": str(item.get("stop_id", "")),
                        "tts_name": str(item.get("tts_name", "")),
                        "wheelchair_boarding": str(item.get("wheelchair_boarding", "")),
                    }
                )
            except Exception as e:
                logger.warning(f"Erro ao normalizar item: {item}\n{e}")
        return normalized

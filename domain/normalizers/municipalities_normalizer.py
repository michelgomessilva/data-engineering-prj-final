"""
MunicipalitiesNormalizer

Classe responsável por transformar os dados brutos retornados pela API da Carris
em uma estrutura tabular compatível com o schema do domínio (municipalities_schema).

Responsabilidades:
- Validar e converter os campos de entrada (normalização).
- Garantir tipos consistentes mesmo com dados ausentes ou malformados.

Método:
- normalize(data: list) -> list[dict]
"""

from infrastructure.logging.logger import logger


class MunicipalitiesNormalizer:
    @staticmethod
    def normalize(data: list) -> list[dict]:
        normalized = []
        for item in data:
            try:
                normalized.append(
                    {
                        "municipality_id": str(item.get("municipality_id", "")),
                        "municipality_name": str(item.get("municipality_name", "")),
                        "prefix": str(item.get("prefix", "")),
                        "district_id": str(item.get("district_id", "")),
                        "district_name": str(item.get("district_name", "")),
                        "region_id": str(item.get("region_id", "")),
                        "region_name": str(item.get("region_name", "")),
                    }
                )
            except Exception as e:
                logger.warning(f"Erro ao normalizar item: {item}\n{e}")
        return normalized

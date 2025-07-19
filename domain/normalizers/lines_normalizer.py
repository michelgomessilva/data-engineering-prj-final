"""
LinesNormalizer

Classe responsável por transformar os dados brutos retornados pela API da Carris
em uma estrutura tabular compatível com o schema do domínio (lines_schema).

Responsabilidades:
- Validar e converter os campos de entrada (normalização).
- Garantir tipos consistentes mesmo com dados ausentes ou malformados.

Método:
- normalize(data: list) -> list[dict]
"""

from infrastructure.logging.logger import logger


class LinesNormalizer:
    @staticmethod
    def normalize(data: list) -> list[dict]:
        normalized = []
        for item in data:
            try:
                normalized.append(
                    {
                        "line_id": str(item.get("id", "")),
                        "localities": item.get("localities", []),
                        "long_name": str(item.get("long_name", "")),
                        "municipalities": item.get("municipalities", []),
                        "short_name": str(item.get("short_name", "")),
                        "routes": item.get("routes", []),
                        "facilities": item.get("facilities", []),
                        "patterns": item.get("patterns", []),
                        "color": str(item.get("color", "")),
                        "text_color": str(item.get("text_color", "")),
                        "_corrupt_record": str(item.get("_corrupt_record", "")),
                    }
                )
            except Exception as e:
                logger.warning(f"Erro ao normalizar item: {item}\n{e}")
        return normalized

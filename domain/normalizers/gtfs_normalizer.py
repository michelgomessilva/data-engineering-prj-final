import csv
from typing import Dict, List


class GTFSNormalizer:
    """
    Normaliza arquivos GTFS (.txt extraídos do ZIP) em listas de dicionários
    para ingestão com Spark.

    Exemplo de arquivos comuns: stops.txt, routes.txt, trips.txt etc.
    """

    @staticmethod
    def normalize(file_path: str) -> List[Dict[str, str]]:
        """
        Lê um arquivo GTFS delimitado por tabulação ou vírgula e retorna os registros normalizados.

        Args:
            file_path (str): Caminho completo para o arquivo GTFS (como stops.txt).

        Returns:
            List[Dict[str, str]]: Lista de registros normalizados (dicionários).
        """
        records: List[Dict[str, str]] = []

        with open(file_path, mode="r", encoding="utf-8") as file:
            # Detecta delimitador automaticamente
            sample = file.read(1024)
            file.seek(0)

            delimiter = "\t" if "\t" in sample else ","
            reader = csv.DictReader(file, delimiter=delimiter)

            for row in reader:
                # Remove espaços extras e ignora linhas vazias
                if any(row.values()):
                    cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
                    records.append(cleaned_row)

        return records

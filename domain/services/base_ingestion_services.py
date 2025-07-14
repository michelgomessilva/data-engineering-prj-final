from abc import ABC, abstractmethod


class IBaseIngestService(ABC):
    """
    Interface para serviços de ingestão de dados.

    Responsável por definir o contrato base que qualquer classe de serviço de ingestão
    deve seguir, garantindo consistência e permitindo fácil substituição ou mock para testes.

    Métodos:
        ingest(): Executa o pipeline completo de ingestão de dados.
    """

    @abstractmethod
    def ingest(self):
        """
        Executa o processo completo de ingestão de dados brutos:
        - Busca na API externa
        - Normalização dos dados
        - Conversão para DataFrame Spark
        - Escrita no storage em formato particionado

        Raises:
            NotImplementedError: se a subclasse não implementar este método.
        """
        pass

"""
Domain Ports — Interfaces abstractas (contratos)
En arquitectura hexagonal, los puertos definen QUÉ se necesita,
sin importar CÓMO se implementa. La infraestructura implementa estos contratos.
"""
from abc import ABC, abstractmethod
from src.domain.entities.database_schema import DatabaseSchema


class SQLGeneratorPort(ABC):
    """Puerto para generar SQL a partir de lenguaje natural."""

    @abstractmethod
    def generate_sql(self, question: str, schema: DatabaseSchema) -> str:
        """Genera una query SQL dado una pregunta y el esquema de la BD."""
        raise NotImplementedError

    @abstractmethod
    def interpret_results(
        self,
        question: str,
        sql: str,
        columns: list[str],
        rows: list[list],
    ) -> str:
        """Interpreta los resultados de la query en lenguaje natural."""
        raise NotImplementedError

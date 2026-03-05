"""
Domain Port: DatabaseRepositoryPort
Contrato abstracto para interacción con la base de datos.
"""
from abc import ABC, abstractmethod
from src.domain.entities.database_schema import DatabaseSchema


class DatabaseRepositoryPort(ABC):
    """Puerto para operaciones con la base de datos."""

    @abstractmethod
    def get_schema(self) -> DatabaseSchema:
        """Extrae y retorna el esquema completo de la base de datos."""
        raise NotImplementedError

    @abstractmethod
    def execute_query(self, sql: str) -> dict:
        """
        Ejecuta una query SQL de solo lectura.
        Retorna: {"columns": [...], "rows": [[...], ...]}
        """
        raise NotImplementedError
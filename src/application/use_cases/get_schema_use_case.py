"""
Application Use Case: GetDatabaseSchema
Retorna el esquema formateado de la base de datos.
"""
import logging
from src.domain.ports.database_repository_port import DatabaseRepositoryPort

logger = logging.getLogger(__name__)


class GetDatabaseSchemaUseCase:
    """Caso de uso: Obtener el esquema de la base de datos."""

    def __init__(self, db_repository: DatabaseRepositoryPort):
        self._db_repository = db_repository

    def execute(self) -> dict:
        try:
            schema = self._db_repository.get_schema()
            return {
                "success": True,
                "schema": schema.to_prompt_text(),
                "tables": schema.table_names,
            }
        except Exception as e:
            logger.exception(f"Error obteniendo esquema: {e}")
            return {"success": False, "error": str(e)}
"""
Application Use Case: ProcessNaturalLanguageQuery
Orquesta el flujo completo de una consulta en lenguaje natural.

Este use case es el corazón de la aplicación — coordina los puertos
del dominio sin conocer los detalles de infraestructura.
"""
import time
import logging
from src.domain.ports.sql_generator_port import SQLGeneratorPort
from src.domain.ports.database_repository_port import DatabaseRepositoryPort
from src.domain.entities.query_result import QueryResult
from src.domain.exceptions.domain_exceptions import (
    DangerousQueryException,
    EmptyQuestionException,
    SQLGenerationException,
    DatabaseQueryException,
)
from src.application.dtos.query_dtos import QueryRequestDTO, QueryResponseDTO

logger = logging.getLogger(__name__)

# Palabras clave que indican queries destructivas
DANGEROUS_KEYWORDS = frozenset([
    "DROP", "TRUNCATE", "DELETE", "UPDATE",
    "INSERT", "ALTER", "CREATE", "GRANT", "REVOKE",
])


class ProcessNaturalLanguageQueryUseCase:
    """
    Caso de uso: Procesar una consulta en lenguaje natural.

    Flujo:
      1. Validar la pregunta
      2. Obtener el esquema de la BD
      3. Generar SQL con el LLM
      4. Validar que el SQL sea seguro
      5. Ejecutar la query
      6. Interpretar los resultados
      7. Retornar el DTO de respuesta
    """

    def __init__(
        self,
        sql_generator: SQLGeneratorPort,
        db_repository: DatabaseRepositoryPort,
    ):
        self._sql_generator = sql_generator
        self._db_repository = db_repository

    def execute(self, request: QueryRequestDTO) -> QueryResponseDTO:
        start_time = time.time()

        try:
            # 1. Validar pregunta
            self._validate_question(request.question)
            logger.info(f"Procesando consulta: '{request.question}'")

            # 2. Obtener esquema de la BD
            schema = self._db_repository.get_schema()
            logger.debug(f"Esquema obtenido: {schema.table_names}")

            # 3. Generar SQL con el LLM
            sql = self._sql_generator.generate_sql(request.question, schema)
            logger.info(f"SQL generado: {sql[:100]}...")

            # 4. Validar seguridad del SQL
            self._validate_sql_safety(sql)

            # 5. Ejecutar query
            db_result = self._db_repository.execute_query(sql)

            # 6. Interpretar resultados
            interpretation = self._sql_generator.interpret_results(
                question=request.question,
                sql=sql,
                columns=db_result["columns"],
                rows=db_result["rows"][:20],
            )

            # 7. Construir entidad del dominio
            execution_time = (time.time() - start_time) * 1000
            result = QueryResult(
                question=request.question,
                sql=sql,
                columns=db_result["columns"],
                rows=db_result["rows"],
                interpretation=interpretation,
                total_rows=len(db_result["rows"]),
                execution_time_ms=round(execution_time, 2),
            )

            logger.info(f"Consulta completada en {result.execution_time_ms}ms — {result.total_rows} filas")

            return QueryResponseDTO(
                success=True,
                question=result.question,
                sql=result.sql,
                columns=result.columns,
                rows=result.rows,
                total_rows=result.total_rows,
                interpretation=result.interpretation,
                execution_time_ms=result.execution_time_ms,
            )

        except (EmptyQuestionException, DangerousQueryException,
                SQLGenerationException, DatabaseQueryException) as e:
            logger.warning(f"Error de dominio: {e}")
            return QueryResponseDTO(
                success=False,
                question=request.question,
                error=str(e),
            )

        except Exception as e:
            logger.exception(f"Error inesperado procesando consulta: {e}")
            return QueryResponseDTO(
                success=False,
                question=request.question,
                error="Error interno del servidor. Por favor intenta de nuevo.",
            )

    def _validate_question(self, question: str) -> None:
        if not question or not question.strip():
            raise EmptyQuestionException()

    def _validate_sql_safety(self, sql: str) -> None:
        sql_upper = sql.upper()
        for keyword in DANGEROUS_KEYWORDS:
            if keyword in sql_upper:
                raise DangerousQueryException(sql)
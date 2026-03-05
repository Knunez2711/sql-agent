"""
Unit Tests: ProcessNaturalLanguageQueryUseCase
Prueba el caso de uso de forma aislada usando mocks.
"""
import pytest
from unittest.mock import MagicMock
from src.application.use_cases.process_query_use_case import ProcessNaturalLanguageQueryUseCase
from src.application.dtos.query_dtos import QueryRequestDTO
from src.domain.entities.database_schema import DatabaseSchema, Table, TableColumn
from src.domain.exceptions.domain_exceptions import DangerousQueryException


def make_mock_schema() -> DatabaseSchema:
    return DatabaseSchema(tables=[
        Table(name="empleados", columns=[
            TableColumn(name="id", data_type="integer"),
            TableColumn(name="nombre", data_type="varchar"),
            TableColumn(name="salario", data_type="numeric"),
        ])
    ])


def make_use_case(sql="SELECT * FROM empleados;", interpretation="Hay 10 empleados."):
    """Crea el caso de uso con mocks configurados."""
    mock_generator = MagicMock()
    mock_generator.generate_sql.return_value = sql
    mock_generator.interpret_results.return_value = interpretation

    mock_repo = MagicMock()
    mock_repo.get_schema.return_value = make_mock_schema()
    mock_repo.execute_query.return_value = {
        "columns": ["id", "nombre", "salario"],
        "rows": [[1, "Ana García", 8500000], [2, "Carlos López", 9000000]],
    }

    use_case = ProcessNaturalLanguageQueryUseCase(
        sql_generator=mock_generator,
        db_repository=mock_repo,
    )
    return use_case, mock_generator, mock_repo


class TestProcessQueryUseCase:

    def test_successful_query_returns_results(self):
        use_case, _, _ = make_use_case()
        result = use_case.execute(QueryRequestDTO(question="¿Cuántos empleados hay?"))

        assert result.success is True
        assert result.total_rows == 2
        assert result.sql == "SELECT * FROM empleados;"
        assert result.interpretation == "Hay 10 empleados."

    def test_empty_question_returns_error(self):
        use_case, _, _ = make_use_case()
        result = use_case.execute(QueryRequestDTO(question=""))

        assert result.success is False
        assert result.error is not None

    def test_dangerous_sql_is_blocked(self):
        use_case, _, _ = make_use_case(sql="DROP TABLE empleados;")
        result = use_case.execute(QueryRequestDTO(question="Elimina todos los empleados"))

        assert result.success is False
        assert "lectura" in result.error.lower() or "SELECT" in result.error

    def test_delete_sql_is_blocked(self):
        use_case, _, _ = make_use_case(sql="DELETE FROM empleados WHERE id = 1;")
        result = use_case.execute(QueryRequestDTO(question="Borra al empleado 1"))

        assert result.success is False

    def test_execution_time_is_recorded(self):
        use_case, _, _ = make_use_case()
        result = use_case.execute(QueryRequestDTO(question="¿Cuántos empleados hay?"))

        assert result.execution_time_ms is not None
        assert result.execution_time_ms > 0

    def test_whitespace_only_question_returns_error(self):
        use_case, _, _ = make_use_case()
        result = use_case.execute(QueryRequestDTO(question="   "))

        assert result.success is False
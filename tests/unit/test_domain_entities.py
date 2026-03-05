"""
Unit Tests: Domain Entities
"""
import pytest
from src.domain.entities.query_result import QueryResult
from src.domain.entities.database_schema import DatabaseSchema, Table, TableColumn


class TestQueryResult:

    def test_has_results_when_rows_exist(self):
        result = QueryResult(
            question="test",
            sql="SELECT 1",
            columns=["id"],
            rows=[[1], [2]],
            interpretation="Hay 2 resultados.",
            total_rows=2,
        )
        assert result.has_results is True
        assert result.is_empty is False

    def test_is_empty_when_no_rows(self):
        result = QueryResult(
            question="test",
            sql="SELECT 1",
            columns=["id"],
            rows=[],
            interpretation="No hay resultados.",
            total_rows=0,
        )
        assert result.is_empty is True
        assert result.has_results is False

    def test_to_dict_contains_all_fields(self):
        result = QueryResult(
            question="pregunta",
            sql="SELECT * FROM empleados",
            columns=["nombre"],
            rows=[["Ana"]],
            interpretation="Ana es la única empleada.",
            total_rows=1,
        )
        d = result.to_dict()
        assert "question" in d
        assert "sql" in d
        assert "columns" in d
        assert "rows" in d
        assert "interpretation" in d


class TestDatabaseSchema:

    def test_to_prompt_text_formats_correctly(self):
        schema = DatabaseSchema(tables=[
            Table(name="empleados", columns=[
                TableColumn(name="id", data_type="integer"),
                TableColumn(name="nombre", data_type="varchar"),
            ])
        ])
        text = schema.to_prompt_text()
        assert "empleados" in text
        assert "id" in text
        assert "nombre" in text

    def test_table_names_returns_list(self):
        schema = DatabaseSchema(tables=[
            Table(name="empleados", columns=[]),
            Table(name="ventas", columns=[]),
        ])
        assert schema.table_names == ["empleados", "ventas"]
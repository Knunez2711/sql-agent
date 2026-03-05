"""
Domain Entity: QueryResult
Representa el resultado completo de una consulta procesada por el agente.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class QueryResult:
    """Entidad central del dominio — resultado de una consulta en lenguaje natural."""

    question: str
    sql: str
    columns: list[str]
    rows: list[list]
    interpretation: str
    total_rows: int
    executed_at: datetime = field(default_factory=datetime.utcnow)
    execution_time_ms: Optional[float] = None

    @property
    def has_results(self) -> bool:
        return self.total_rows > 0

    @property
    def is_empty(self) -> bool:
        return self.total_rows == 0

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "sql": self.sql,
            "columns": self.columns,
            "rows": self.rows,
            "interpretation": self.interpretation,
            "total_rows": self.total_rows,
            "executed_at": self.executed_at.isoformat(),
            "execution_time_ms": self.execution_time_ms,
        }
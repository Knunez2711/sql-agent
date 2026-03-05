"""
Application DTOs (Data Transfer Objects)
Objetos que viajan entre la capa de aplicación y las interfaces.
No contienen lógica de negocio.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class QueryRequestDTO:
    """DTO de entrada: pregunta del usuario."""
    question: str


@dataclass
class QueryResponseDTO:
    """DTO de salida: respuesta completa del agente."""
    success: bool
    question: str
    sql: Optional[str] = None
    columns: Optional[list] = None
    rows: Optional[list] = None
    total_rows: Optional[int] = None
    interpretation: Optional[str] = None
    execution_time_ms: Optional[float] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}

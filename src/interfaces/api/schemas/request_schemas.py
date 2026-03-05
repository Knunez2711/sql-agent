"""
Interface: API Schemas
Validación de entrada/salida de la API con Pydantic.
"""
from pydantic import BaseModel, field_validator


class QueryRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("La pregunta no puede estar vacía.")
        if len(v) > 500:
            raise ValueError("La pregunta no puede superar los 500 caracteres.")
        return v.strip()


class ExecuteSQLRequest(BaseModel):
    sql: str

    @field_validator("sql")
    @classmethod
    def sql_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El SQL no puede estar vacío.")
        return v.strip()
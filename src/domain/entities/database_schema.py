"""
Domain Entity: DatabaseSchema
Representa el esquema de la base de datos que el agente usa como contexto.
"""
from dataclasses import dataclass


@dataclass
class TableColumn:
    name: str
    data_type: str
    is_nullable: bool = True
    constraint: str = ""

    def __str__(self) -> str:
        constraint_str = f" [{self.constraint}]" if self.constraint else ""
        return f"  - {self.name} ({self.data_type}){constraint_str}"


@dataclass
class Table:
    name: str
    columns: list[TableColumn]

    def __str__(self) -> str:
        cols = "\n".join(str(col) for col in self.columns)
        return f"Tabla: {self.name}\nColumnas:\n{cols}"


@dataclass
class DatabaseSchema:
    tables: list[Table]

    def to_prompt_text(self) -> str:
        """Formatea el esquema para incluirlo en el prompt del LLM."""
        return "\n\n".join(str(table) for table in self.tables)

    @property
    def table_names(self) -> list[str]:
        return [t.name for t in self.tables]
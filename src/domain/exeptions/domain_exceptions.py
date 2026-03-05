"""
Domain Exceptions — Errores propios del negocio.
Separar las excepciones del dominio permite manejarlas
de forma limpia en cada capa sin acoplar la infraestructura al dominio.
"""


class DomainException(Exception):
    """Excepción base del dominio."""
    pass


class DangerousQueryException(DomainException):
    """Se lanza cuando el SQL generado intenta modificar datos."""

    def __init__(self, sql: str):
        self.sql = sql
        super().__init__(
            f"Consulta peligrosa detectada. Solo se permiten operaciones de lectura (SELECT)."
        )


class EmptyQuestionException(DomainException):
    """Se lanza cuando la pregunta del usuario está vacía."""

    def __init__(self):
        super().__init__("La pregunta no puede estar vacía.")


class SQLGenerationException(DomainException):
    """Se lanza cuando el LLM no puede generar un SQL válido."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"No se pudo generar el SQL: {reason}")


class DatabaseQueryException(DomainException):
    """Se lanza cuando la ejecución de la query falla."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"Error ejecutando la consulta en la base de datos: {reason}")

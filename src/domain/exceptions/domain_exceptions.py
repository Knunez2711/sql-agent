class DomainException(Exception):
    pass

class DangerousQueryException(DomainException):
    def __init__(self, sql: str):
        self.sql = sql
        super().__init__("Consulta peligrosa detectada. Solo se permiten operaciones de lectura (SELECT).")

class EmptyQuestionException(DomainException):
    def __init__(self):
        super().__init__("La pregunta no puede estar vacía.")

class SQLGenerationException(DomainException):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"No se pudo generar el SQL: {reason}")

class DatabaseQueryException(DomainException):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"Error ejecutando la consulta en la base de datos: {reason}")

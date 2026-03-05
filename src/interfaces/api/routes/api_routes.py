"""
Interface: API Routes
Blueprint de Flask con todos los endpoints de la API REST.
"""
import logging
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from src.interfaces.api.schemas.request_schemas import QueryRequest
from src.infrastructure.db.dependency_container import container
from src.application.dtos.query_dtos import QueryRequestDTO

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__, url_prefix="/api")

EXAMPLE_QUESTIONS = [
    "¿Cuántas ventas hubo en total en el año 2024?",
    "¿Cuál es el empleado con más ventas?",
    "¿Cuánto es el total de ventas por mes en 2024?",
    "¿Cuáles son los 5 productos más vendidos?",
    "¿Cuál es el salario promedio por departamento?",
    "¿Cuántos empleados hay en cada departamento?",
    "¿Cuál fue el mes con mayor facturación?",
    "¿Qué productos tienen stock menor a 20 unidades?",
    "¿Cuál es el total de ventas de Ana García?",
    "¿Cuáles son los empleados activos ordenados por salario?",
]


@api_bp.route("/query", methods=["POST"])
def query():
    """
    POST /api/query
    Procesa una pregunta en lenguaje natural y retorna SQL + resultados + interpretación.
    """
    try:
        body = QueryRequest(**request.get_json(force=True))
    except (ValidationError, TypeError) as e:
        return jsonify({"success": False, "error": str(e)}), 400

    dto = QueryRequestDTO(question=body.question)
    result = container.process_query_use_case.execute(dto)

    status_code = 200 if result.success else 500
    return jsonify(result.to_dict()), status_code


@api_bp.route("/schema", methods=["GET"])
def schema():
    """GET /api/schema — Retorna el esquema de la base de datos."""
    result = container.get_schema_use_case.execute()
    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code


@api_bp.route("/suggestions", methods=["GET"])
def suggestions():
    """GET /api/suggestions — Retorna preguntas de ejemplo."""
    return jsonify({"suggestions": EXAMPLE_QUESTIONS})


@api_bp.route("/health", methods=["GET"])
def health():
    """GET /api/health — Health check del servicio."""
    return jsonify({
        "status": "ok",
        "service": "SQL Agent IA",
        "version": "2.0.0",
    })
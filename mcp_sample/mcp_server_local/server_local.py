"""Servidor MCP simple que expone herramientas aritméticas y un saludo."""
from __future__ import annotations
import logging
from typing import Annotated
from mcp.server.fastmcp import FastMCP

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

server = FastMCP(
    "stdio-calculator",
    instructions=(
        "Resuelve operaciones básicas de calculadora (suma, resta, "
        "multiplicación y división) y puede saludar a las personas."
    ),
)

Number = Annotated[float, "Valor numérico aceptado por la calculadora"]

@server.tool()
async def add(a: Number, b: Number) -> str:
    """Suma dos números y regresa el resultado."""
    logger.info(f"ADD: {a} + {b}")
    return str(a + b)

@server.tool()
async def subtract(a: Number, b: Number) -> str:
    """Resta b de a."""
    logger.info(f"SUBTRACT: {a} - {b}")
    return str(a - b)

@server.tool()
async def multiply(a: Number, b: Number) -> str:
    """Multiplica dos valores."""
    logger.info(f"MULTIPLY: {a} * {b}")
    return str(a * b)

@server.tool()
async def divide(a: Number, b: Number) -> str:
    """Divide a entre b controlando divisiones entre cero."""
    logger.info(f"DIVIDE: {a} / {b}")
    if b == 0:
        logger.warning(f"División entre cero: {a} / {b}")
        raise ValueError("La división entre cero no está permitida.")
    return str(a / b)

@server.tool(name="hello-mcp")
async def greet(name: Annotated[str, "Nombre de la persona a saludar"] = "Amigo usuario") -> str:
    """Emite un saludo en español."""
    logger.info(f"GREET: nombre={name}")
    return f"Hola {name}! ¿Cómo puedo ayudarte hoy?"

if __name__ == "__main__":
    logger.info("🚀 Servidor MCP iniciado y corriendo...")
    server.run()
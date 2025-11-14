import asyncio
import logging

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

server_params = StdioServerParameters(
    command="python3",
    args=["server_local.py"],
)


async def get_tool_result(session, tool_name, arguments):
    """Ejecuta una tool y retorna el resultado como texto."""
    result = await session.call_tool(tool_name, arguments=arguments)
    if isinstance(result.content[0], types.TextContent):
        return result.content[0].text
    return None


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            logger.info("Conexión inicializada")

            tools = await session.list_tools()
            tool_names = [t.name for t in tools.tools]
            logger.info(f"Herramientas disponibles: {tool_names}")

            tests = [
                ("add", {"a": 5, "b": 3}, "Suma: 5 + 3"),
                ("subtract", {"a": 10, "b": 4}, "Resta: 10 - 4"),
                ("multiply", {"a": 7, "b": 6}, "Multiplicación: 7 × 6"),
                ("divide", {"a": 20, "b": 4}, "División: 20 ÷ 4"),
                ("hello-mcp", {"name": "Juan"}, "Saludo: hello-mcp"),
                ("hello-mcp", {}, "Saludo sin parámetro"),
            ]

            for tool_name, args, description in tests:
                try:
                    result = await get_tool_result(session, tool_name, args)
                    print(f"{description} -> {result}")
                except Exception as e:
                    logger.error(f"{description} -> Error: {e}")

            logger.info("Ejemplos completados")


if __name__ == "__main__":
    asyncio.run(run())

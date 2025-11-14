# 🧩 Agent Basics: LangChain + MCP

Este repo reúne ejemplos mínimos para comprender cómo LangChain orquesta agentes y cómo el protocolo MCP (Model Context Protocol) expone herramientas externas que los LLM pueden invocar de forma segura.

---

## 🧠 Conceptos express

- **LangChain** ([docs](https://python.langchain.com)): framework para encadenar LLMs con memoria, prompts y herramientas. Sus agentes deciden cuándo llamar funciones externas y cómo razonar paso a paso.
- **MCP (Model Context Protocol)** ([spec](https://modelcontextprotocol.io/)): estándar abierto para anunciar herramientas (APIs, scripts, DBs) a los modelos. Define cómo descubrir, describir y ejecutar capacidades vía transporte `stdio`, WebSockets, etc.
- **Adapters LangChain–MCP**: permiten que un agente de LangChain trate a un servidor MCP como un paquete de `tools`, de modo que pueda ejecutarlos igual que cualquier otra función instrumentada.

---

## 📂 Qué hay en este repo

- `mcp_sample/mcp_server_local/server_local.py`: servidor MCP local (FastMCP) con cinco herramientas 👉 suma, resta, multiplicación, división con validación y un saludo (`hello-mcp`). Ideal para ver cómo se tipan parámetros con `typing.Annotated`.
- `mcp_sample/mcp_client/client_async_simple.py`: cliente LangChain asíncrono que instancia `MultiServerMCPClient`, descubre herramientas `stdio` y crea un agente `ChatOpenAI` con prompt en español.
- `mcp_sample/mcp_client/client_stdio_simple.py`: variante síncrona via `stdio` puro, útil para depurar.
- `notebooks/`: espacio para experimentos o tutoriales prácticos (no incluido en este README, pero recomendado para pruebas).
- `a2a/`: carpeta reservada para exploraciones adicionales (agents-to-agents, integraciones, etc.).

---

## 📋 Contenido

- `server_local.py` - Servidor MCP con herramientas matemáticas y de saludo
- `client_async_simple.py` - **⭐ Cliente Asincrónico (RECOMENDADO)**
- `client_stdio_simple.py` - Cliente Sincrónico (con conversión)

---

## 🚀 Inicio Rápido

### Cliente Asincrónico (Recomendado)

```bash
# Ejecutar el cliente asincrónico
cd mcp_sample/mcp_client
conda run -n llm-agent python client_async_simple.py
```

**Salida esperada:**
```
2025-11-14 00:12:10,376 - __main__ - INFO - 🚀 Servidor MCP iniciado y corriendo...
2025-11-14 00:12:10,382 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-11-14 00:12:24,763 - __main__ - INFO - 🚀 Servidor MCP iniciado y corriendo...
2025-11-14 00:12:24,769 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2025-11-14 00:12:24,769 - __main__ - INFO - GREET: nombre=Alexander

{
    "messages": [
        "content="" ...
    ]
}
```

## 🔧 Herramientas Disponibles

El servidor MCP expone las siguientes herramientas:

| Herramienta | Descripción | Parámetros |
|-------------|-------------|-----------|
| `add` | Suma dos números | `a: float, b: float` |
| `subtract` | Resta b de a | `a: float, b: float` |
| `multiply` | Multiplica dos valores | `a: float, b: float` |
| `divide` | Divide a entre b | `a: float, b: float` |
| `hello-mcp` | Emite un saludo | `name: str = "amigo"` |

---

## ⚙️ Cómo probar

1. **Instala dependencias mínimas**
   ```bash
   pip install langchain langchain-openai langchain-mcp-adapters fastmcp
   ```
2. **Lanza el servidor MCP local**
   ```bash
   python mcp_sample/mcp_server_local/server_local.py
   ```
3. **Ejecuta el cliente**
   ```bash
   python mcp_sample/mcp_client/client_async_simple.py
   ```
   Verás cómo el agente:
   - Detecta las herramientas publicadas vía MCP.
   - Saluda al usuario.
   - Llama al sumador remoto para resolver `15 + 27`.

> 💡 Usa cualquier endpoint compatible con la API de OpenAI (ej. [`lmstudio.ai`](https://lmstudio.ai), [`docker model runner (DMR)`](https://docs.docker.com/ai/model-runner/api-reference/)) u otros ajustando `base_url`, `model` y `api_key` en el cliente.

---

## 📚 Recursos útiles

- LangChain Agent Toolkit: https://python.langchain.com/docs/modules/agents/
- MCP reference impl (FastMCP): https://github.com/modelcontextprotocol/fastmcp
- Tutoriales oficiales MCP: https://modelcontextprotocol.io/tutorials
- Ejemplo multi-servidor LangChain + MCP: https://github.com/langchain-ai/langchain-mcp

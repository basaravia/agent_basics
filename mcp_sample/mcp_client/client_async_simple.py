# from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import asyncio
import json

async def main():
    client = MultiServerMCPClient(
        {
            "stdio_server": {
                "transport": "stdio",
                "command": "python",
                "args": ["../mcp_server_local/server_local.py"] #[str(Path(__file__).with_name("server_local.py"))],
            }
        }
    )
    
    tools = await client.get_tools()
    
    llm = ChatOpenAI(
        model="ai/gemma3n:latest",
        temperature=0.2,
        max_tokens=256,
        api_key="dummy",
        base_url="http://localhost:12434/engines/llama.cpp/v1",
    )
    
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="Eres un asistente muy útil que habla en español de Ecuador.",
    )
    
    user_input = "Hola, soy Alexander. Por favor salúdame y luego suma 15 y 27."
    
    response = await agent.ainvoke(
        {"messages": [HumanMessage(content=user_input)]}
    )
    
    # Pretty print the response
    print(json.dumps(response, indent=4, default=str))

if __name__ == "__main__":
    asyncio.run(main())

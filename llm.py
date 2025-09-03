import os
from dotenv import load_dotenv
from tools import get_all_tools, download_repo_tool, scan_envs_tool
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# load .env
load_dotenv(dotenv_path="./.env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def llm_node(user_prompt: str):
    api_key = GROQ_API_KEY
    if not api_key:
        raise RuntimeError("Error: GROQ_API_KEY not found")

    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=api_key, temperature=0)
    llm = llm.bind_tools(get_all_tools())

    # start convo
    messages = [HumanMessage(content=user_prompt)]
    response = llm.invoke(messages)

    # keep running until no more tool calls
    while response.tool_calls:
        for tc in response.tool_calls:
            if tc["name"] == "download_repo":
                result = download_repo_tool.func(**tc["args"])
            elif tc["name"] == "scan_envs":
                result = scan_envs_tool.func(**tc["args"])
            else:
                result = {"error": f"Unknown tool {tc['name']}"}

            print(f"🔧 ran {tc['name']} → {result}")

            # feed result back in
            followup = ToolMessage(content=str(result), tool_call_id=tc["id"])
            messages.extend([response, followup])
            response = llm.invoke(messages)

    print("🤖 AI says:", response.content)
    return response

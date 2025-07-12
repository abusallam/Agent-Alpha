from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import asyncio
from typing import Optional, List, Dict, Any, Union
import os # For environment variables
import importlib

# Attempt to import necessary components from the WebDancer demo structure
try:
    # Dynamically determine the base path for demos to make imports more robust
    # Assuming api_wrapper.py is in research_agent/WebDancer/demos/
    # Adjust if the file location is different.
    # For example, if api_wrapper.py is in src/, then imports might be from ..demos

    # This relative import style is standard if api_wrapper.py is part of the 'demos' package
    SearchAgent = importlib.import_module(".agents.search_agent", package="...demos").SearchAgent
    QwenMessage = importlib.import_module("qwen_agent.llm.schema", package="...demos").Message
    USER = importlib.import_module("qwen_agent.llm.schema", package="...demos").USER
    SYSTEM = importlib.import_module("qwen_agent.llm.schema", package="...demos").SYSTEM
    TextChatAtOAI = importlib.import_module(".llm.oai", package="...demos").TextChatAtOAI
    QwenChatAtDS = importlib.import_module(".llm.qwen_dashscope", package="...demos").QwenChatAtDS

except ImportError as e:
    # Fallback for environments where relative imports might be tricky (e.g. direct script run)
    # or if the structure is slightly different. This assumes a certain project layout.
    print(f"Warning: Could not import WebDancer components using relative paths due to: {e}. Trying alternative import for dev.")
    try:
        from research_agent.WebDancer.demos.agents.search_agent import SearchAgent
        from qwen_agent.llm.schema import Message as QwenMessage
        from qwen_agent.llm.schema import USER, SYSTEM
        from research_agent.WebDancer.demos.llm.oai import TextChatAtOAI
        from research_agent.WebDancer.demos.llm.qwen_dashscope import QwenChatAtDS
    except ImportError as e2:
        print(f"CRITICAL: Failed to import WebDancer components with alternative path: {e2}. Using dummy fallbacks.")
        class SearchAgent: pass
        class QwenMessage:
            def __init__(self, role: str, content: str): self.role = role; self.content = content
        USER, SYSTEM = "user", "system"
        class TextChatAtOAI: pass
        class QwenChatAtDS: pass


# --- Pydantic Models ---
class ResearchRequest(BaseModel):
    query: str = Field(..., description="The research query or question.")
    max_llm_calls: Optional[int] = Field(10, description="Maximum number of LLM calls the agent should make.")
    reasoning_enabled: Optional[bool] = Field(True, description="Enable reasoning steps for the agent.")

class ResearchResponse(BaseModel):
    query: str
    result: Optional[str] = Field(None, description="The final answer or primary result.")
    full_interaction_log: Optional[List[str]] = Field(None, description="Log of all messages from the agent's run.")
    error: Optional[str] = Field(None, description="Error message if the task failed.")

# --- FastAPI App ---
app = FastAPI(
    title="WebDancer Research API",
    description="API wrapper for the WebDancer agent.",
    version="0.1.0"
)

webdancer_agent_instance: Optional[SearchAgent] = None

@app.on_event("startup")
async def startup_event():
    global webdancer_agent_instance

    llm_backend_type = os.getenv("WEBDANCER_LLM_BACKEND_TYPE", "DASHSCOPE_QWEN")
    llm_config_for_webdancer = None

    print(f"WebDancer API: Attempting to initialize LLM backend: {llm_backend_type}")

    if llm_backend_type == "DASHSCOPE_QWEN":
        dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
        qwen_model = os.getenv("WEBDANCER_QWEN_MODEL", "qwen-max")
        if not dashscope_api_key:
            print("CRITICAL: DASHSCOPE_API_KEY environment variable not set for WebDancer API.")
            return
        try:
            if QwenChatAtDS.__name__ == "QwenChatAtDS" and hasattr(QwenChatAtDS, '__init__'):
                llm_config_for_webdancer = QwenChatAtDS({
                    'model': qwen_model, 'model_type': 'qwen_dashscope',
                    'model_server': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
                    'api_key': dashscope_api_key, 'generate_cfg': {'fncall_prompt_type': 'nous'},
                })
                print(f"WebDancer API: Initialized QwenChatAtDS with model {qwen_model}")
            else:
                print("CRITICAL: QwenChatAtDS dummy class is being used. Cannot initialize.")
                return
        except Exception as e:
            print(f"CRITICAL: Failed to initialize QwenChatAtDS for WebDancer API: {e}")
            return
    elif llm_backend_type == "OAI_CUSTOM":
        oai_api_key = os.getenv("WEBDANCER_OAI_API_KEY", "EMPTY")
        oai_model_server = os.getenv("WEBDANCER_OAI_MODEL_SERVER")
        oai_model_name = os.getenv("WEBDANCER_OAI_MODEL_NAME", "")
        if not oai_model_server:
            print("CRITICAL: WEBDANCER_OAI_MODEL_SERVER environment variable not set for WebDancer API.")
            return
        try:
            if TextChatAtOAI.__name__ == "TextChatAtOAI" and hasattr(TextChatAtOAI, '__init__'):
                llm_config_for_webdancer = TextChatAtOAI({
                    'model': oai_model_name, 'model_type': 'oai', 'model_server': oai_model_server,
                    'api_key': oai_api_key,
                    'generate_cfg': {
                        'fncall_prompt_type': 'nous', 'temperature': 0.6, 'top_p': 0.95,
                        'max_tokens': 32768, 'stream_options': {'include_usage': True}, 'timeout': 3000
                    },
                })
                print(f"WebDancer API: Initialized TextChatAtOAI with model server {oai_model_server}")
            else:
                print("CRITICAL: TextChatAtOAI dummy class is being used. Cannot initialize.")
                return
        except Exception as e:
            print(f"CRITICAL: Failed to initialize TextChatAtOAI for WebDancer API: {e}")
            return
    else:
        print(f"CRITICAL: Invalid WEBDANCER_LLM_BACKEND_TYPE: {llm_backend_type}. Agent will not be initialized.")
        return

    if not llm_config_for_webdancer:
        print("CRITICAL: LLM configuration for WebDancer could not be established. Agent not initialized.")
        return

    tools_for_webdancer = ['search', 'visit']

    try:
        if SearchAgent.__name__ == "SearchAgent" and hasattr(SearchAgent, '__init__'): # Check if not dummy
            webdancer_agent_instance = SearchAgent(
                llm=llm_config_for_webdancer,
                function_list=tools_for_webdancer,
                name="WebDancerAPIInstance",
                description="WebDancer instance for API calls",
                extra={'reasoning': True, 'max_llm_calls': 10}
            )
            print("WebDancer agent fully initialized for API.")
        else:
            print("CRITICAL: SearchAgent is a dummy class. Cannot initialize WebDancer agent.")
    except Exception as e:
        print(f"CRITICAL: Failed to initialize SearchAgent for WebDancer API: {e}")
        import traceback
        traceback.print_exc()
        webdancer_agent_instance = None


@app.post("/research", response_model=ResearchResponse)
async def perform_webdancer_research(request: ResearchRequest):
    global webdancer_agent_instance
    if not webdancer_agent_instance:
        print("Error: WebDancer agent not initialized. Check server startup logs.")
        raise HTTPException(status_code=503, detail="WebDancer agent is not initialized. Please check server logs for errors during startup.")

    print(f"API - WebDancer: Query: '{request.query}', Max LLM Calls: {request.max_llm_calls}, Reasoning: {request.reasoning_enabled}")

    current_extra_config = webdancer_agent_instance.extra.copy() if webdancer_agent_instance.extra else {}
    current_extra_config['max_llm_calls'] = request.max_llm_calls
    current_extra_config['reasoning'] = request.reasoning_enabled

    # Temporarily update the agent instance's extra config for this call.
    # This is a bit of a hack; ideally SearchAgent's _run would take these as params.
    original_extra = webdancer_agent_instance.extra
    webdancer_agent_instance.extra = current_extra_config

    system_prompt_content = ""
    if hasattr(webdancer_agent_instance, 'make_system_prompt') and callable(webdancer_agent_instance.make_system_prompt):
        system_prompt_content = webdancer_agent_instance.make_system_prompt()

    initial_messages_for_agent = []
    if system_prompt_content:
        initial_messages_for_agent.append(QwenMessage(role=SYSTEM, content=system_prompt_content))
    initial_messages_for_agent.append(QwenMessage(role=USER, content=request.query))

    interaction_log = []
    final_answer = None

    try:
        async for response_message_list in webdancer_agent_instance._run(messages=initial_messages_for_agent, lang='zh'):
            if response_message_list:
                for msg in response_message_list:
                    content_str = str(msg.content)
                    interaction_log.append(f"Role: {msg.role}, Content: {content_str}")
                    if isinstance(content_str, str) and "<answer>" in content_str and "</answer>" in content_str:
                        answer_match = content_str.split("<answer>", 1)
                        if len(answer_match) > 1:
                            final_answer = answer_match[1].split("</answer>", 1)[0].strip()

    except Exception as e:
        print(f"API - WebDancer: Error during agent execution: {e}")
        import traceback
        traceback.print_exc()
        webdancer_agent_instance.extra = original_extra # Restore original extra config
        return ResearchResponse(query=request.query, error=f"An error occurred: {str(e)}", full_interaction_log=interaction_log)
    finally:
        # Restore original extra config
        webdancer_agent_instance.extra = original_extra

    if final_answer:
        return ResearchResponse(query=request.query, result=final_answer, full_interaction_log=interaction_log)
    elif interaction_log:
        return ResearchResponse(query=request.query, result="Processing complete. Review log.", full_interaction_log=interaction_log)
    else:
        return ResearchResponse(query=request.query, error="WebDancer produced no output.", full_interaction_log=interaction_log)

# For local testing:
# Ensure PYTHONPATH includes the project root e.g., export PYTHONPATH=$PYTHONPATH:$(pwd)
# Then run: uvicorn research_agent.WebDancer.demos.api_wrapper:app --host 0.0.0.0 --port 8001 --reload
# (Assuming this file is at research_agent/WebDancer/demos/api_wrapper.py)
# Required ENV VARS: WEBDANCER_LLM_BACKEND_TYPE, DASHSCOPE_API_KEY (if using Qwen), etc.

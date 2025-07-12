from python.helpers.tool import Tool, ToolResponse

# URLs for the UIs based on docker-compose.yml host ports
RESEARCHER_UI_URLS = {
    "WebWalker": "http://localhost:7860",
import requests
import json

# Internal API URLs for the researcher agent APIs
RESEARCHER_API_URLS = {
    "WebWalker": "http://research_agent_webwalker_api:8000/research", # Internal port 8000
    "WebDancer": "http://research_agent_webdancer_api:8001/research", # Internal port 8001
    "WebSailor": "http://research_agent_websailor_api:8002/research", # Internal port 8002
}

DEFAULT_MAX_STEPS = 7
DEFAULT_REASONING_ENABLED_WEBDANCER = True
# For WebSailor, sglang_model_identifier can be passed, or its API uses ENV default
DEFAULT_SGLANG_MODEL_ID_WEBSAILOR = None # Let API wrapper use ENV default unless specified

class PerformWebResearch(Tool):
    def __init__(self, agent, **kwargs):
        super().__init__(agent, **kwargs)
        self.name = "perform_web_research"
        self.description = (
            "Delegates complex web research or question-answering tasks to a specialized researcher agent. "
            "Requires 'query'. Optional: 'research_agent_type' (e.g., 'WebDancer', 'WebWalker', 'WebSailor'), "
            "'max_steps' (integer), 'reasoning_enabled' (boolean, for WebDancer), "
            "'sglang_model_identifier' (string, for WebSailor)."
        )

    async def execute(self, query: str, research_agent_type: str = "WebDancer",
                      max_steps: int = DEFAULT_MAX_STEPS,
                      reasoning_enabled: bool = DEFAULT_REASONING_ENABLED_WEBDANCER,
                      sglang_model_identifier: str = None, # New parameter for WebSailor
                      **kwargs) -> ToolResponse:
        if not query:
            return ToolResponse(success=False, message="Error: 'query' is a required parameter.", break_loop=False)

        chosen_agent_type = research_agent_type
        if chosen_agent_type not in RESEARCHER_API_URLS:
            self.agent.context.log.log("warning", f"Unknown research_agent_type: '{chosen_agent_type}'. Defaulting to WebDancer.")
            chosen_agent_type = "WebDancer"
            if chosen_agent_type not in RESEARCHER_API_URLS:
                 return ToolResponse(success=False, message=f"Error: Default researcher agent '{chosen_agent_type}' API URL not configured.", break_loop=False)

        endpoint = RESEARCHER_API_URLS.get(chosen_agent_type)
        payload = {"query": query}

        if chosen_agent_type == "WebWalker":
            payload["max_steps"] = max_steps
        elif chosen_agent_type == "WebDancer":
            payload["max_llm_calls"] = max_steps
            payload["reasoning_enabled"] = reasoning_enabled
        elif chosen_agent_type == "WebSailor":
            payload["max_llm_calls"] = max_steps # WebSailor API's ResearchRequest takes max_llm_calls
            if sglang_model_identifier: # Only add if provided, otherwise API uses ENV default
                payload["sglang_model_identifier"] = sglang_model_identifier
            # `reasoning_enabled` is not directly in WebSailor's ResearchRequest, it's part of agent's general config

        self.agent.context.log.log(
            type="info",
            content=f"Delegating research query to '{chosen_agent_type}' API: Endpoint: {endpoint}",
            kvps={"payload": payload}
        )

        try:
            response = requests.post(endpoint, json=payload, timeout=120) # Increased timeout for potentially long research tasks
            response.raise_for_status()

            response_data = response.json()

            result_message = f"Research by {chosen_agent_type} completed.\n"
            if response_data.get("result"):
                result_message += f"Result: {response_data.get('result')}\n"
            if response_data.get("error"):
                 result_message += f"Error from agent: {response_data.get('error')}\n"
            # Consider including a snippet of full_interaction_log if it's very useful and not too long
            # For now, primarily focus on 'result' or 'error'

            self.agent.context.log.log("success", f"Response from {chosen_agent_type} API: {response_data}")
            return ToolResponse(success=True, message=result_message, data=response_data, break_loop=False)

        except requests.exceptions.ConnectionError as e:
            error_message = f"Error connecting to {chosen_agent_type} API at {endpoint}. Is it running? Detail: {e}"
            self.agent.context.log.log("error", error_message)
            return ToolResponse(success=False, message=error_message, break_loop=False)
        except requests.exceptions.HTTPError as e:
            error_message = f"{chosen_agent_type} API request failed with status {e.response.status_code}. Response: {e.response.text}. Endpoint: {endpoint}"
            self.agent.context.log.log("error", error_message)
            return ToolResponse(success=False, message=error_message, break_loop=False)
        except requests.exceptions.Timeout:
            error_message = f"Request to {chosen_agent_type} API at {endpoint} timed out."
            self.agent.context.log.log("error", error_message)
            return ToolResponse(success=False, message=error_message, break_loop=False)
        except Exception as e:
            error_message = f"An unexpected error occurred while calling {chosen_agent_type} API at {endpoint}: {e}"
            self.agent.context.log.log("error", error_message)
            return ToolResponse(success=False, message=error_message, break_loop=False)

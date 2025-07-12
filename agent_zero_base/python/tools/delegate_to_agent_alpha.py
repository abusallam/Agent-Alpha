import json
import requests
from python.helpers.tool import Tool, ToolResponse

AGENT_ALPHA_API_URL = "http://agent_alpha:8000"  # Internal Docker network URL

class DelegateToAgentAlpha(Tool):
    def __init__(self, agent, **kwargs):
        super().__init__(agent, **kwargs)
        self.name = "delegate_to_agent_alpha"
        self.description = (
            "Delegates tasks to Agent Alpha. "
            "For 'create_agent' action: requires 'agent_definition' (JSON string with role, initial_prompt, etc.). 'task_description' can be a high-level goal. "
            "For 'run_task' action: requires 'task_description'. Optional: 'agent_id', 'agent_name', 'task_parameters' (JSON string)."
        )

    async def execute(self, action: str, task_description: str,
                      agent_name: str = None, agent_id: str = None,
                      agent_definition: str = None, task_parameters: str = None,
                      **kwargs) -> ToolResponse:

        if not action:
            return ToolResponse(success=False, message="Error: 'action' is a required parameter.", break_loop=False)

        payload = {}
        endpoint = ""

        if action == "create_agent":
            if not agent_definition:
                return ToolResponse(success=False, message="Error: 'agent_definition' (JSON string) is required for 'create_agent' action.", break_loop=False)
            try:
                definition_data = json.loads(agent_definition)
                # Expected fields for AgentCreateRequest schema
                payload["role"] = definition_data.get("role")
                payload["initial_prompt"] = definition_data.get("initial_prompt")
                if not payload["role"] or not payload["initial_prompt"]:
                    return ToolResponse(success=False, message="Error: 'agent_definition' JSON must contain 'role' and 'initial_prompt'.", break_loop=False)

                payload["name"] = definition_data.get("name", agent_name) # Use name from definition, fallback to agent_name param
                payload["capabilities"] = definition_data.get("capabilities")
                payload["config"] = definition_data.get("config")
                # Clean None values from payload to match Pydantic Optional behavior
                payload = {k: v for k, v in payload.items() if v is not None}

            except json.JSONDecodeError:
                return ToolResponse(success=False, message="Error: 'agent_definition' is not a valid JSON string.", break_loop=False)
            except TypeError: # Handles if definition_data is not a dict (e.g. json.loads returns a list)
                 return ToolResponse(success=False, message="Error: 'agent_definition' JSON must be a valid JSON object.", break_loop=False)

            endpoint = f"{AGENT_ALPHA_API_URL}/agents/"
            # task_description for create_agent is more of a high-level goal, not directly part of AgentCreateRequest payload
            # but useful for logging and for the LLM to frame the request. We'll log it.
            log_task_desc = task_description

        elif action == "run_task":
            if not task_description:
                 return ToolResponse(success=False, message="Error: 'task_description' is required for 'run_task' action.", break_loop=False)
            payload["task_description"] = task_description
            if agent_id:
                payload["agent_id"] = agent_id
            if agent_name: # agent_name can supplement agent_id or be an alternative
                payload["agent_name"] = agent_name
            if task_parameters:
                try:
                    payload["parameters"] = json.loads(task_parameters)
                except json.JSONDecodeError:
                    return ToolResponse(success=False, message="Error: 'task_parameters' is not a valid JSON string.", break_loop=False)

            # Clean None values
            payload = {k: v for k, v in payload.items() if v is not None}
            endpoint = f"{AGENT_ALPHA_API_URL}/tasks/"
            log_task_desc = task_description

        else:
            return ToolResponse(success=False, message=f"Error: Unknown action '{action}'. Supported actions are 'create_agent', 'run_task'.", break_loop=False)

        log_message_content = f"Attempting to delegate to Agent Alpha: Action: {action}, Endpoint: {endpoint}"
        if action == "create_agent" and task_description:
             log_message_content += f", Goal: {task_description}"

        self.agent.context.log.log(
            type="info",
            content=log_message_content,
            kvps={"payload": payload}
        )

        try:
            response = requests.post(endpoint, json=payload, timeout=30)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

            response_data = response.json()
            success_message = f"Successfully delegated '{action}' to Agent Alpha. Response: {json.dumps(response_data)}"
            self.agent.context.log.log("success", success_message)
            return ToolResponse(success=True, message=success_message, data=response_data, break_loop=False)

        except requests.exceptions.ConnectionError as e:
            error_message = f"Error connecting to Agent Alpha at {endpoint}. Is Agent Alpha running and accessible? Detail: {e}"
            self.agent.context.log.log("error", error_message)
            return ToolResponse(success=False, message=error_message, break_loop=False)
        except requests.exceptions.HTTPError as e:
            error_message = f"Agent Alpha API request failed with status {e.response.status_code}. Response: {e.response.text}. Endpoint: {endpoint}"
            # Check for 501 Not Implemented or similar, as endpoints might not be ready
            if e.response.status_code == 501 or e.response.status_code == 404:
                error_message += " (This might indicate the Agent Alpha API endpoint is not yet implemented)."
            self.agent.context.log.log("error", error_message)
            return ToolResponse(success=False, message=error_message, break_loop=False)
        except requests.exceptions.Timeout:
            error_message = f"Request to Agent Alpha at {endpoint} timed out."
            self.agent.context.log.log("error", error_message)
            return ToolResponse(success=False, message=error_message, break_loop=False)
        except Exception as e:
            error_message = f"An unexpected error occurred while calling Agent Alpha API at {endpoint}: {e}"
            self.agent.context.log.log("error", error_message)
            return ToolResponse(success=False, message=error_message, break_loop=False)

# Example usage (for testing within Agent Zero's tool loading mechanism):
# def get_tools(agent) -> list[Tool]:
#     return [DelegateToAgentAlpha(agent=agent)]

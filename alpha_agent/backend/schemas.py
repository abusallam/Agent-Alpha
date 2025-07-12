from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid

class AgentCreateRequest(BaseModel):
    name: Optional[str] = Field(None, description="Optional name for the new agent.")
    role: str = Field(..., description="The primary role or persona of the agent.")
    initial_prompt: str = Field(..., description="The initial system prompt or instruction set for the agent.")
    capabilities: Optional[List[str]] = Field(None, description="A list of capabilities or tools the agent should possess.")
    config: Optional[Dict[str, Any]] = Field(None, description="Additional configuration parameters for the agent.")

class AgentResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique ID of the agent.")
    name: Optional[str] = Field(None, description="Name of the agent.")
    status: str = Field(default="Agent definition received", description="Current status of the agent.")
    message: Optional[str] = Field(None, description="Additional message regarding the agent status.")

class TaskSubmitRequest(BaseModel):
    agent_id: Optional[str] = Field(None, description="ID of an existing agent to run the task. If None, Agent Alpha might use a default agent or create one based on task_description.")
    agent_name: Optional[str] = Field(None, description="Name of an existing agent (alternative to agent_id).")
    task_description: str = Field(..., description="Detailed description of the task to be performed.")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Additional parameters or inputs for the task.")
    # Could also include a field for an agent definition if an agent needs to be created on-the-fly for this task
    # agent_definition_for_task: Optional[AgentCreateRequest] = None

class TaskStatusResponse(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique ID of the submitted task.")
    status: str = Field(default="Task received, pending execution", description="Current status of the task.")
    result_summary: Optional[str] = Field(None, description="A brief summary of the task result, if completed.")
    result_detail: Optional[Any] = Field(None, description="Detailed result of the task, if completed (can be any structure).")
    error_message: Optional[str] = Field(None, description="Error message if the task failed.")
    agent_id: Optional[str] = Field(None, description="ID of the agent that executed or is executing the task.")

class HealthCheckResponse(BaseModel):
    status: str = Field(default="OK", description="API health status.")

# Example of a more detailed Agent Definition that could be part of AgentCreateRequest or TaskSubmitRequest
# class AgentDefinition(BaseModel):
#     role: str
#     goals: List[str]
#     tools: List[str]
#     constraints: List[str]
#     initial_prompt_override: Optional[str] = None
#     personality: Optional[str] = None
#
# if we use this, AgentCreateRequest.initial_prompt might become part of this definition.
# For now, keeping AgentCreateRequest simpler.

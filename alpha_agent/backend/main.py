from fastapi import FastAPI

app = FastAPI(
    title="AgentAlpha API",
    description="The main API for the AgentAlpha framework.",
    version="0.1.0",
)

# Import schemas and other necessary modules
from .schemas import AgentCreateRequest, AgentResponse, HealthCheckResponse # Assuming schemas.py is in the same directory
import logging
import uuid

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory store for created agents (placeholder for now)
# In a real application, this would be a database.
# Key: agent_id (str), Value: AgentCreateRequest model or similar dict
created_agents_db: dict[str, AgentCreateRequest] = {}


@app.get("/", response_model=HealthCheckResponse)
def read_root():
    """
    The root endpoint of the API, also serves as a basic health check.
    """
    logger.info("Root endpoint '/' accessed (health check).")
    return HealthCheckResponse(status="OK, Agent Alpha API is running!")

@app.post("/agents/", response_model=AgentResponse, status_code=201)
async def create_agent(agent_create_request: AgentCreateRequest):
    """
    Create a new Agent Alpha agent.

    This endpoint receives an agent definition and is intended to initialize
    a new agent within the Agent Alpha system.

    (Placeholder implementation: Logs request and stores definition in-memory.)
    """
    logger.info(f"Received request to create agent: Name='{agent_create_request.name}', Role='{agent_create_request.role}'")

    agent_id = str(uuid.uuid4())
    agent_name = agent_create_request.name if agent_create_request.name else f"Agent_{agent_id[:8]}"

    # Store the agent definition in our placeholder DB
    created_agents_db[agent_id] = agent_create_request

    logger.info(f"Agent definition for '{agent_name}' (ID: {agent_id}) stored (in-memory).")

    return AgentResponse(
        id=agent_id,
        name=agent_name,
        status="Agent definition received and registered.",
        message=f"Agent '{agent_name}' with ID '{agent_id}' has been registered."
    )

# In-memory store for submitted tasks (placeholder)
# Key: task_id (str), Value: TaskSubmitRequest model or similar dict
submitted_tasks_db: dict[str, TaskSubmitRequest] = {}

@app.post("/tasks/", response_model=TaskStatusResponse, status_code=202) # 202 Accepted
async def submit_task(task_submit_request: TaskSubmitRequest):
    """
    Submit a new task to an Agent Alpha agent.

    This endpoint receives a task description and is intended to queue it
    for execution by a specified (or default) agent.

    (Placeholder implementation: Logs request and stores task in-memory.)
    """
    logger.info(f"Received request to submit task: Description='{task_submit_request.task_description}', AgentID='{task_submit_request.agent_id}', AgentName='{task_submit_request.agent_name}'")

    task_id = str(uuid.uuid4())

    # Validate agent_id if provided (simple check against our in-memory agent DB)
    if task_submit_request.agent_id and task_submit_request.agent_id not in created_agents_db:
        logger.warning(f"Task submission for unknown agent_id: {task_submit_request.agent_id}")
        # In a real app, you might return a 404 or 400 here.
        # For placeholder, we'll still accept the task but log a warning.
        # Or, return an error:
        # raise HTTPException(status_code=404, detail=f"Agent with ID '{task_submit_request.agent_id}' not found.")

    # Store the task definition in our placeholder DB
    submitted_tasks_db[task_id] = task_submit_request

    logger.info(f"Task '{task_submit_request.task_description[:50]}...' (ID: {task_id}) stored (in-memory) for agent '{task_submit_request.agent_id or task_submit_request.agent_name or 'default'}'.")

    return TaskStatusResponse(
        task_id=task_id,
        status="Task received and accepted for processing.", # Changed from default "pending execution" to "accepted"
        agent_id=task_submit_request.agent_id
    )

@app.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Retrieve the status and details of a specific task.

    (Placeholder implementation: Retrieves task from in-memory store.)
    """
    logger.info(f"Received request to get status for task_id: {task_id}")

    task_info = submitted_tasks_db.get(task_id)

    if not task_info:
        logger.warning(f"Task with ID '{task_id}' not found.")
        # In a real application, you would import HTTPException from fastapi
        # and raise HTTPException(status_code=404, detail=f"Task with ID '{task_id}' not found.")
        # For this placeholder, returning a specific error status in the response.
        return TaskStatusResponse(
            task_id=task_id,
            status="Error: Task not found",
            error_message=f"Task with ID '{task_id}' not found."
        )

    logger.info(f"Returning status for task_id: {task_id}. Current status: 'Task received and accepted for processing.' (placeholder).")

    # For this placeholder, we always return the initial status.
    # A real implementation would update status as the task progresses
    # and potentially include results or errors.
    return TaskStatusResponse(
        task_id=task_id,
        status="Task received and accepted for processing.", # Or a more dynamic status if implemented
        agent_id=task_info.agent_id,
        # result_summary="Still pending or mock result.", # Example for future
        # result_detail={"data": "some mock data"},       # Example for future
    )

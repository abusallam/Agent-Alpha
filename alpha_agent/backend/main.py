from fastapi import FastAPI

app = FastAPI(
    title="AgentAlpha API",
    description="The main API for the AgentAlpha framework.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """
    The root endpoint of the API.
    """
    return {"message": "Welcome to the AgentAlpha API"}

# In the next steps, we will add more endpoints for managing agents, tasks, etc.

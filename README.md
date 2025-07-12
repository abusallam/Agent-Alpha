# Multi-Agent AI Platform

This project is a multi-agent AI platform consisting of three main agents: Agent Zero, Agent Alpha, and a Researcher Agent. The entire platform is orchestrated using Docker Compose, providing a scalable and production-ready environment.

## Architecture

The platform is designed around a central UI provided by **Agent Zero**. Agent Zero acts as the primary interface and orchestrator, capable of delegating tasks to specialized backend agents like Agent Alpha and various Researcher Agents.

-   **Agent Zero (`agent_zero`)**: The main user-facing application (UI on port `8081`), providing tools to manage tasks, and an underlying agent capable of orchestrating with other backend services.
-   **Agent Alpha Frontend (`agent_alpha_frontend`)**: A UI for the Agent Alpha system (UI on port `8082`).
-   **Agent Alpha (`agent_alpha`)**: A backend agent system responsible for creating and running intelligent agents for various tasks.
-   **Researcher Agent - WebWalker (`research_agent_webwalker_ui`)**: A backend agent specialized in web traversal research tasks, with a Streamlit UI (UI on port `7860`). An internal API service (`research_agent_webwalker_api`) is also available for Agent Zero.
-   **Researcher Agent - WebDancer (`research_agent_webdancer_ui`)**: A backend agent specialized in autonomous information seeking, with a Gradio UI (UI on port `7861`). An internal API service (`research_agent_webdancer_api`) is also available for Agent Zero.
-   **Researcher Agent - WebSailor (abusallam/Websailor) (`research_agent_websailor_api`)**: An advanced research agent for complex reasoning and information seeking. Interacted with via an internal API by Agent Zero. This service also depends on an SGLang model server (`sglang_server_websailor`). This version of WebSailor does not have a separate UI.
-   **LiveKit (`livekit`)**: A real-time communication service.
-   **Redis (`redis`)**: An in-memory data store.

All services are connected via an internal Docker network (`agents-net`), ensuring secure and efficient communication.

## Getting Started

### Prerequisites

-   Docker and Docker Compose installed on your system.
-   Git for cloning the repository.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create an environment file:**
    Create a `.env` file in the root of the project by copying the `.env.example` file:
    ```bash
    cp .env.example .env
    ```
    Update the `.env` file with your API keys and other configuration values. Ensure you have copied `agent_zero_base/.env.example` to `agent_zero_base/.env` if applicable for Agent Zero specific settings, and the root `.env.example` to `.env` for platform-wide keys.
    The root `.env` file should include:
    ```
    OPENAI_API_KEY=your_openai_api_key
    GOOGLE_API_KEY=your_google_api_key      # General Google API Key
    LIVEKIT_API_KEY=your_livekit_api_key
    LIVEKIT_API_SECRET=your_livekit_api_secret

    # Required for Researcher Agents (WebWalker, WebDancer)
    DASHSCOPE_API_KEY=your_dashscope_api_key
    OPENAI_MODEL_SERVER=your_openai_compatible_model_server_url # e.g., for local models or specific OpenAI deployments
    GOOGLE_SEARCH_KEY=your_google_custom_search_api_key # Specific for Google Search (Serper, etc.)
    JINA_API_KEY=your_jina_api_key

    # Required for WebSailor (abusallam/Websailor)
    WEBSAILOR_SGLANG_MODEL_IDENTIFIER="Qwen/Qwen1.5-7B-Chat" # Example, use desired model
    WEBSAILOR_LLM_LOCAL_PATH_FOR_TOKENIZER="Qwen/Qwen1.5-7B-Chat" # Or path to local model for tokenizer
    # WEBSAILOR_SGLANG_TP_SIZE=1 # Optional
    # WEBSAILOR_MAX_LLM_CALLS=15 # Optional
    # WEBSAILOR_TEMPERATURE=0.6 # Optional
    # WEBSAILOR_TOP_P=0.95 # Optional
    ```
    *(Note: Refer to `.env.example` for the full list, defaults, and detailed comments for all variables, including those for WebDancer's specific LLM backend configuration.)*

### Running the Platform

To run the entire platform, use the following Docker Compose command:

```bash
docker-compose up --build
```

This will build the Docker images for all agents and start all the services defined in `docker-compose.yml`.

### Accessing the UIs

Once all the services are running, you can access the UIs in your browser at:

-   **Agent Zero UI**: [http://localhost:8081](http://localhost:8081)
    -   *From Agent Zero's settings, you can also find links to the other agent UIs.*
-   **Agent Alpha Frontend UI**: [http://localhost:8082](http://localhost:8082)
-   **WebWalker UI (Researcher Agent)**: [http://localhost:7860](http://localhost:7860)
-   **WebDancer UI (Researcher Agent)**: [http://localhost:7861](http://localhost:7861)

## Services

The `docker-compose.yml` file defines the following key services:

-   `agent_zero`: The main UI application and orchestration agent.
-   `agent_alpha_frontend`: Frontend UI for Agent Alpha.
-   `agent_alpha`: Backend system for Agent Alpha.
-   `research_agent_webwalker_ui`: WebWalker research agent UI.
-   `research_agent_webwalker_api`: WebWalker research agent internal API.
-   `research_agent_webdancer_ui`: WebDancer research agent UI.
-   `research_agent_webdancer_api`: WebDancer research agent internal API.
-   `sglang_server_websailor`: SGLang model server for WebSailor.
-   `research_agent_websailor_api`: WebSailor (abusallam/Websailor) research agent internal API.
-   `livekit`: The real-time communication server.
-   `redis`: The Redis data store.

All services are configured to restart automatically (`restart: unless-stopped`), ensuring resilience in a production environment.

## Contributing

Please refer to the documentation within each agent's directory for more details on their specific implementation and how to contribute.

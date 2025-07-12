# Multi-Agent AI Platform

This project is a multi-agent AI platform consisting of three main agents: Agent Zero, Agent Alpha, and a Researcher Agent. The entire platform is orchestrated using Docker Compose, providing a scalable and production-ready environment.

## Architecture

The platform is designed around a central UI provided by **Agent Zero**, which communicates with the other agents via internal APIs.

-   **Agent Zero (`agent_zero`)**: The main user-facing application, providing a UI to create, manage, and interact with other agents.
-   **Agent Alpha (`agent_alpha`)**: A backend agent responsible for creating and running intelligent agents for various tasks.
-   **Researcher Agent (`research_agent`)**: A backend agent specialized in research tasks, implemented as the `WebWalker` application.
-   **LiveKit (`livekit`)**: A real-time communication service, likely for features like live collaboration or streaming.
-   **Redis (`redis`)**: An in-memory data store, used for caching and other real-time data needs.

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
    Update the `.env` file with your API keys and other configuration values:
    ```
    OPENAI_API_KEY=your_openai_api_key
    GOOGLE_API_KEY=your_google_api_key
    LIVEKIT_API_KEY=your_livekit_api_key
    LIVEKIT_API_SECRET=your_livekit_api_secret
    ```

### Running the Platform

To run the entire platform, use the following Docker Compose command:

```bash
docker-compose up --build
```

This will build the Docker images for all agents and start all the services defined in `docker-compose.yml`.

### Accessing the UI

Once all the services are running, you can access the Agent Zero UI in your browser at:

[http://localhost:8081](http://localhost:8081)

## Services

The `docker-compose.yml` file defines the following services:

-   `agent_zero`: The main UI application.
-   `agent_alpha`: The backend agent for task execution.
-   `research_agent`: The backend agent for research tasks.
-   `livekit`: The real-time communication server.
-   `redis`: The Redis data store.

All services are configured to restart automatically (`restart: unless-stopped`), ensuring resilience in a production environment.

## Contributing

Please refer to the documentation within each agent's directory for more details on their specific implementation and how to contribute.

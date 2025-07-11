# Gemini Project Overview: Agent Alpha Framework

This document provides a comprehensive overview of the Agent Alpha Framework for the Gemini assistant.

## 1. Project Summary

Agent Alpha is a modular, production-ready multi-agent system designed for artificial general intelligence orchestration. It enables intelligent agents to self-modify, spawn child agents, manage prompt context dynamically, and collaborate via secure protocols (A2A, MCP) in real-time. The project includes a FastAPI backend, a React frontend, and is containerized with Docker.

## 2. Tech Stack

- **Backend**: FastAPI, Redis, Python
- **Frontend**: React, TailwindCSS, WebSockets
- **Deployment**: Docker Compose, Nginx
- **Security**: JWT, OAuth2, Bandit, pip-audit, Snyk, npm audit

## 3. Project Structure

```
/home/asim/Documents/AgentAlpha/
├── backend/
│   ├── cli/                  # CLI tools
│   ├── agent/                # ADK-based agents
│   ├── auth/                 # JWT, OAuth
│   ├── memory/               # Redis wrapper
│   ├── a2a/                  # A2A client
│   ├── mcp/                  # MCP tool client
│   ├── prompts/              # Prompt templates
│   └── main.py               # FastAPI entrypoint
├── frontend/
│   ├── scripts/              # Env setup scripts
│   ├── src/components/       # UI widgets
│   ├── src/pages/            # Main views
│   └── main.jsx              # React entrypoint
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── nginx/
│   └── nginx.conf
├── scripts/
│   └── audit-security.sh
├── docs/
│   ├── architecture.md
│   ├── dev-guide.md
│   ├── security.md
│   ├── agent.md
│   └── api-reference.md
├── .env.example
├── AgentAlphaFramework-FullDocs.md
└── README.md
```

## 4. Key Components & Logic

- **Agent Lifecycle**: Agents are governed by an `AgentManager` and can be executed via different runners (`SequentialRunner`, `LoopRunner`, `SelfModifyingRunner`). They can also spawn child agents.
- **Tool Integration (MCP)**: Agents can dynamically load external tools defined in `prompts/popular_mcp_tools.json`.
- **Agent-to-Agent (A2A) Communication**: A secure `A2AClient` facilitates communication between agents using token-scoped calls and asynchronous messaging.
- **Context Management**: A `ContextPromptAgent` uses a Redis-backed store to manage and build adaptive prompts for other agents.
- **Authentication**: The system uses JWT tokens with role scopes and supports OAuth2 providers. An Nginx reverse proxy adds a layer of security.
- **Frontend UI**: A comprehensive UI provides an agent tree view, prompt editor, task dashboard, and live logs via WebSockets.

## 5. How to Run the Project

1.  **Clone the repository** (if not already done).
2.  **Set up environment variables**: `cp .env.example .env`
3.  **Run the setup script**: `./frontend/scripts/setup-env.sh`
4.  **Build and start the services**: `docker-compose up --build -d`

The primary services are `backend`, `frontend`, `redis`, and `nginx`.

## 6. How to Run Tests & Audits

The project includes a script for running a suite of security and dependency audits.

- **Run security audit**: `./scripts/audit-security.sh`
This command executes Bandit, pip-audit, Snyk, and npm audit.

## 7. CLI Usage

The framework includes a command-line interface for managing the project:

- `agentalpha setup`: Bootstraps the project.
- `agentalpha validate`: Runs security and dependency audits.
- `agentalpha build`: Builds the Docker containers.
- `agentalpha deploy`: Deploys the application.

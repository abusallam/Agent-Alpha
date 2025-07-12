
# Agent Alpha Framework — Full Developer Manual

## Table of Contents
- [Vision & Scope](#vision--scope)
- [System Architecture](#system-architecture)
- [Directory Structure](#directory-structure)
- [Quick Start Guide](#quick-start-guide)
- [CLI Usage](#cli-usage)
- [Authentication & Security](#authentication--security)
- [Agent Lifecycle](#agent-lifecycle)
- [Tool Integration (MCP)](#tool-integration-mcp)
- [Agent-to-Agent Communication (A2A)](#agent-to-agent-communication-a2a)
- [Memory & Context Management](#memory--context-management)
- [Frontend UI](#frontend-ui)
- [Deployment (Docker + Coolify)](#deployment-docker--coolify)
- [DevOps and Scripts](#devops-and-scripts)
- [API Reference](#api-reference)
- [Contributing Guide](#contributing-guide)

---

## Vision & Scope

Agent Alpha is a modular, production-ready multi-agent system designed for artificial general intelligence orchestration. It enables intelligent agents to self-modify, spawn child agents, manage prompt context dynamically, and collaborate via secure protocols (A2A, MCP) in real-time.

---

## System Architecture

- **Backend**: FastAPI + Redis + ADK runners + JWT + OAuth2
- **Frontend**: React + TailwindCSS with live WebSocket logs
- **Deployment**: Docker Compose with Kali Linux base image
- **Agent Control**: ContextPromptAgent governs dynamic prompt/context delivery to agents
- **Security**: OAuth2 login, JWT tokens, secure Nginx config, audit tools

---

## Directory Structure

```
backend/
├── cli/                  # CLI tools
├── agent/                # ADK-based agents
├── auth/                 # JWT, OAuth
├── memory/               # Redis wrapper
├── a2a/                  # A2A client
├── mcp/                  # MCP tool client
├── prompts/              # Prompt templates
├── main.py               # FastAPI entrypoint

frontend/
├── scripts/              # Env setup scripts
├── src/components/       # UI widgets
├── src/pages/            # Main views
├── public/               # index.html
├── tailwind.config.js

docker/
├── Dockerfile
├── docker-compose.yml

nginx/
├── nginx.conf

scripts/
├── audit-security.sh

docs/
├── architecture.md
├── dev-guide.md
├── security.md
├── agent.md
├── api-reference.md
```

---

## Quick Start Guide

```bash
git clone https://repo.url/AgentAlphaFramework.git
cd AgentAlphaFramework
cp .env.example .env
./frontend/scripts/setup-env.sh
docker-compose up --build -d
```

---

## CLI Usage

```bash
agentalpha setup       # Bootstrap the project
agentalpha validate    # Run Bandit, pip-audit, etc.
agentalpha build       # Build Docker containers
agentalpha deploy      # Deploy to Docker or Coolify
```

---

## Authentication & Security

- JWT tokens issued with role scopes
- OAuth2 provider support (Google, GitHub)
- Hardened Nginx reverse proxy
- Scripts for Bandit, npm audit, pip-audit, Snyk

---

## Agent Lifecycle

Each agent:
- Receives a prompt and context
- Executes via `SequentialRunner`, `LoopRunner`, or `SelfModifyingRunner`
- Can spawn a child agent with scoped tools
- Is supervised by the AgentManager

---

## Tool Integration (MCP)

Agents can load external tools dynamically via:
```json
{
  "tool": "WebScraper",
  "config": { "base_url": "https://example.com" }
}
```

Stored in `prompts/popular_mcp_tools.json`

---

## Agent-to-Agent Communication (A2A)

Agents communicate with each other securely using `A2AClient`:
- Token-scoped calls
- Asynchronous message routing
- Compatible with memory injection

---

## Memory & Context Management

- Redis-backed key-value store
- Supports append, slice, retrieve context
- Validated via JSON Schema
- Used by ContextPromptAgent to build adaptive prompts

---

## Frontend UI

- Agent Tree View
- Prompt Editor
- Task Dashboard
- Live WebSocket Logs
- JWT-secured login system
- Built with React, Tailwind, and modular components

---

## Deployment (Docker + Coolify)

```bash
docker-compose up --build -d
```

Coolify-compatible, no Kubernetes required. Default services:
- backend
- frontend
- redis
- nginx

---

## DevOps and Scripts

```bash
./scripts/audit-security.sh
```

Runs Bandit, pip-audit, Snyk, and npm audit.

---

## API Reference

- `/agents/` POST to create an agent
- `/tasks/` GET/POST for task queue
- `/prompt/` PUT to update dynamic prompt
- `/logs/ws` for WebSocket streaming

*(Note: The Agent Zero system is being enhanced to interact with the `/agents/` and `/tasks/` endpoints. Full functionality of these interactions is contingent on the implementation of these API endpoints in the Agent Alpha backend.)*

Full OpenAPI spec in `docs/api-reference.md`

---

## Contributing Guide

1. Fork repo
2. Create a feature branch
3. Test & lint
4. Submit PR with description

---

© 2025 Agent Alpha Framework Contributors

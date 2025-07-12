## Tools available:

{{ include './agent.system.tool.response.md' }}

{{ include './agent.system.tool.call_sub.md' }}

{{ include './agent.system.tool.behaviour.md' }}

{{ include './agent.system.tool.search_engine.md' }}

{{ include './agent.system.tool.memory.md' }}

{{ include './agent.system.tool.code_exe.md' }}

{{ include './agent.system.tool.input.md' }}

{{ include './agent.system.tool.browser.md' }}

{{ include './agent.system.tool.scheduler.md' }}

{{ include './agent.system.tool.document_query.md' }}

---
### Tool: delegate_to_agent_alpha
**Description:** Use this tool to delegate tasks to Agent Alpha, such as creating new specialized agents or running tasks with existing ones.
**Parameters:**
- `action` (string, required): The action for Agent Alpha. Must be 'create_agent' or 'run_task'.
- `task_description` (string, required):
    - For 'create_agent': A high-level description of the goal or purpose for creating the new agent. The detailed definition of the agent itself goes into `agent_definition`.
    - For 'run_task': The detailed description of the task to be performed by Agent Alpha.
- `agent_definition` (string, optional): Required if `action` is 'create_agent'. A JSON string defining the new agent. Must include 'role' (string) and 'initial_prompt' (string). Can also include 'name' (string), 'capabilities' (list of strings), and 'config' (JSON object). Example: `"{\"role\": \"Data Analyst\", \"initial_prompt\": \"Analyze the provided dataset for trends.\", \"name\": \"DataAnalysisBot\", \"capabilities\": [\"python\", \"data_visualization\"]}"`
- `agent_id` (string, optional): For 'run_task', the ID of an existing Agent Alpha agent to perform the task.
- `agent_name` (string, optional): For 'run_task', the name of an existing Agent Alpha agent. Can also be used to suggest a name if `action` is 'create_agent' and 'name' is not in `agent_definition`.
- `task_parameters` (string, optional): For 'run_task', a JSON string representing additional parameters or inputs for the task. Example: `"{\"dataset_url\": \"http://example.com/data.csv\", \"target_column\": \"sales\"}"`

**JSON Examples:**

*Creating an agent:*
```json
{
  "tool_name": "delegate_to_agent_alpha",
  "tool_args": {
    "action": "create_agent",
    "task_description": "Need an agent to help with financial analysis.",
    "agent_definition": "{\"role\": \"Financial Analyst Agent\", \"initial_prompt\": \"Analyze financial data and generate reports.\", \"name\": \"FinanceBot1\", \"capabilities\": [\"data_analysis\", \"report_generation\"]}"
  }
}
```

*Running a task with an existing agent (by name):*
```json
{
  "tool_name": "delegate_to_agent_alpha",
  "tool_args": {
    "action": "run_task",
    "agent_name": "FinanceBot1",
    "task_description": "Generate a quarterly sales report for Q3.",
    "task_parameters": "{\"report_period\": \"Q3\", \"year\": 2024}"
  }
}
```

---
### Tool: perform_web_research
**Description:** Use this tool to conduct in-depth web research or answer complex questions requiring information seeking from the internet, by delegating to specialized researcher agents like WebDancer, WebWalker, or WebSailor.
**Parameters:**
- `query` (string, required): The detailed research question or topic.
- `research_agent_type` (string, optional): Specify 'WebDancer' (deep research), 'WebWalker' (web traversal), or 'WebSailor' (complex reasoning & information seeking). Defaults to 'WebDancer'.
- `max_steps` (integer, optional): The maximum number of steps or LLM calls the researcher agent should take. Defaults to 7.
- `reasoning_enabled` (boolean, optional): For WebDancer, specifies if it should perform explicit reasoning steps. Defaults to true. (This parameter may not apply to all agent types).
- `sglang_model_identifier` (string, optional): For WebSailor, you can optionally specify the SGLang model identifier (e.g., 'Qwen/Qwen2-7B-Instruct') if you want to override the API's default.

**JSON Example (using WebDancer):**
```json
{
  "tool_name": "perform_web_research",
  "tool_args": {
    "query": "What are the latest advancements in fusion energy and their projected timelines?",
    "research_agent_type": "WebDancer",
    "max_steps": 10,
    "reasoning_enabled": true
  }
}
```

**JSON Example (using WebSailor):**
```json
{
  "tool_name": "perform_web_research",
  "tool_args": {
    "query": "Investigate the impact of quantum computing on current encryption standards.",
    "research_agent_type": "WebSailor",
    "max_steps": 15,
    "sglang_model_identifier": "Qwen/Qwen2-7B-Instruct"
  }
}
```

from .base import AgentBase

class ContextPromptAgent(AgentBase):
    """
    An agent that manages memory, dynamic prompting, and A2A messaging.
    """
    def __init__(self, name, role, memory, llm):
        """
        Initializes a new ContextPromptAgent.

        Args:
            name (str): The name of the agent.
            role (str): The role of the agent.
            memory (object): The memory system for the agent.
            llm (object): The language model for the agent.
        """
        super().__init__(name, role, memory, llm)

    def update_context(self, key, value):
        """
        Updates the agent's memory with a new key-value pair.

        Args:
            key (str): The key to store in memory.
            value (any): The value to store.
        """
        print(f"Updating context for agent {self.name} ({self.id}): {key} = {value}")
        self.memory.set(f"{self.id}:{key}", value)

    def get_context(self, key):
        """
        Retrieves a value from the agent's memory.

        Args:
            key (str): The key to retrieve from memory.

        Returns:
            any: The value associated with the key, or None if not found.
        """
        return self.memory.get(f"{self.id}:{key}")

    def dispatch_prompt(self, task_type, context_keys=None):
        """
        Generates a prompt based on the task type and context, and sends it to the LLM.

        Args:
            task_type (str): The type of task to generate a prompt for.
            context_keys (list, optional): A list of keys to retrieve from memory to build the prompt context. Defaults to None.

        Returns:
            str: The response from the language model.
        """
        prompt = f"Task: {task_type}\n\n"
        if context_keys:
            prompt += "Context:\n"
            for key in context_keys:
                value = self.get_context(key)
                if value:
                    prompt += f"- {key}: {value}\n"
        
        print(f"Dispatching prompt for agent {self.name} ({self.id}):\n{prompt}")
        
        # In a real implementation, this would call the LLM
        # response = self.llm.generate(prompt)
        # For now, we'll return a placeholder
        response = f"LLM response for task '{task_type}'"
        
        return response

    def execute_task(self, task):
        """
        Executes a task by dispatching a prompt to the LLM.

        Args:
            task (dict): The task to execute. Expected to have 'type' and 'context_keys' keys.
        """
        if not isinstance(task, dict) or 'type' not in task:
            raise ValueError("Task must be a dictionary with a 'type' key.")

        task_type = task['type']
        context_keys = task.get('context_keys')

        return self.dispatch_prompt(task_type, context_keys)

from .base import AgentBase

class SequentialAgent(AgentBase):
    """
    An agent that executes a fixed series of tasks in order.
    """
    def __init__(self, name, role, tasks, memory=None, llm=None):
        """
        Initializes a new SequentialAgent.

        Args:
            name (str): The name of the agent.
            role (str): The role of the agent.
            tasks (list): A list of tasks to execute in sequence.
            memory (object, optional): The memory system for the agent. Defaults to None.
            llm (object, optional): The language model for the agent. Defaults to None.
        """
        super().__init__(name, role, memory, llm)
        self.tasks = tasks

    def execute_task(self, task=None):
        """
        Executes the predefined sequence of tasks.

        Args:
            task (any, optional): This argument is ignored, as the agent uses its predefined task list.
        
        Returns:
            list: A list of results from each executed task.
        """
        print(f"Agent {self.name} ({self.id}) starting sequential task execution.")
        results = []
        for i, task_item in enumerate(self.tasks):
            print(f"Executing task {i+1}/{len(self.tasks)}: {task_item}")
            # In a real implementation, this would be more sophisticated
            # For now, we'll just append the task description as the result
            result = f"Result of task: {task_item}"
            results.append(result)
        
        print(f"Agent {self.name} ({self.id}) finished sequential task execution.")
        return results

    def add_task(self, task):
        """
        Adds a task to the end of the sequence.

        Args:
            task (any): The task to add.
        """
        self.tasks.append(task)

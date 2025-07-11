from .base import AgentBase
import time

class LoopAgent(AgentBase):
    """
    An agent that repeats a task based on a trigger or memory state.
    """
    def __init__(self, name, role, task, loop_condition, memory=None, llm=None):
        """
        Initializes a new LoopAgent.

        Args:
            name (str): The name of the agent.
            role (str): The role of the agent.
            task (any): The task to repeat.
            loop_condition (function): A function that returns True to continue the loop, False to stop.
            memory (object, optional): The memory system for the agent. Defaults to None.
            llm (object, optional): The language model for the agent. Defaults to None.
        """
        super().__init__(name, role, memory, llm)
        self.task = task
        self.loop_condition = loop_condition

    def execute_task(self, task=None):
        """
        Executes the task in a loop until the loop_condition returns False.

        Args:
            task (any, optional): This argument is ignored, as the agent uses its predefined task.
        """
        print(f"Agent {self.name} ({self.id}) starting loop.")
        
        while self.loop_condition():
            print(f"Executing task in loop: {self.task}")
            # In a real implementation, this would be more sophisticated
            # For now, we'll just print a message
            print(f"Result of task: {self.task}")
            time.sleep(1)  # To prevent a tight loop in this example

        print(f"Agent {self.name} ({self.id}) finished loop.")

    def update_loop_condition(self, new_condition):
        """
        Updates the loop condition function.

        Args:
            new_condition (function): The new loop condition function.
        """
        self.loop_condition = new_condition

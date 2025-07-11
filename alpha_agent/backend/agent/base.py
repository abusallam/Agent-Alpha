import uuid

class AgentBase:
    """
    The base class for all agents in the AgentAlpha framework.
    """
    def __init__(self, name, role, memory=None, llm=None):
        """
        Initializes a new agent.

        Args:
            name (str): The name of the agent.
            role (str): The role of the agent.
            memory (object, optional): The memory system for the agent. Defaults to None.
            llm (object, optional): The language model for the agent. Defaults to None.
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.memory = memory
        self.llm = llm
        self.is_running = False

    def start(self):
        """
        Starts the agent's main loop.
        """
        self.is_running = True
        print(f"Agent {self.name} ({self.id}) started.")

    def stop(self):
        """
        Stops the agent's main loop.
        """
        self.is_running = False
        print(f"Agent {self.name} ({self.id}) stopped.")

    def execute_task(self, task):
        """
        Executes a given task. This method should be overridden by subclasses.

        Args:
            task (object): The task to execute.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def __repr__(self):
        return f"AgentBase(id={self.id}, name='{self.name}', role='{self.role}')"

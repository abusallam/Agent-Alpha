import secrets
from .base import AgentBase

class ReinforcementLearningAgent(AgentBase):
    """
    An agent that uses reinforcement learning to improve its performance.
    """
    def __init__(self, name, role, actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1, memory=None, llm=None):
        """
        Initializes a new ReinforcementLearningAgent.

        Args:
            name (str): The name of the agent.
            role (str): The role of the agent.
            actions (list): A list of possible actions the agent can take.
            learning_rate (float, optional): The learning rate. Defaults to 0.1.
            discount_factor (float, optional): The discount factor for future rewards. Defaults to 0.9.
            exploration_rate (float, optional): The exploration rate for choosing random actions. Defaults to 0.1.
            memory (object, optional): The memory system for the agent. Defaults to None.
            llm (object, optional): The language model for the agent. Defaults to None.
        """
        super().__init__(name, role, memory, llm)
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}

    def get_q_value(self, state, action):
        """
        Gets the Q-value for a given state-action pair.
        """
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        """
        Chooses an action based on the current state using an epsilon-greedy strategy.
        """
        if secrets.SystemRandom().random() < self.exploration_rate:
            return secrets.choice(self.actions)  # Explore
        else:
            q_values = [self.get_q_value(state, a) for a in self.actions]
            max_q = max(q_values)
            if q_values.count(max_q) > 1:
                # If there are multiple actions with the same max Q-value, choose one randomly
                best_actions = [i for i, x in enumerate(q_values) if x == max_q]
                i = secrets.choice(best_actions)
            else:
                i = q_values.index(max_q)
            return self.actions[i]  # Exploit

    def update_policy(self, state, action, reward, next_state):
        """
        Updates the Q-table based on the reward received.
        """
        old_q = self.get_q_value(state, action)
        future_q = max([self.get_q_value(next_state, a) for a in self.actions])
        new_q = old_q + self.learning_rate * (reward + self.discount_factor * future_q - old_q)
        self.q_table[(state, action)] = new_q

    def execute_task(self, task):
        """
        Executes a task by choosing an action, receiving a reward, and updating the policy.
        """
        if not isinstance(task, dict) or 'state' not in task:
            raise ValueError("Task must be a dictionary with a 'state' key.")

        state = task['state']
        action = self.choose_action(state)
        
        # In a real implementation, the reward and next_state would come from the environment
        reward = task.get('reward', 0)
        next_state = task.get('next_state', state)
        
        self.update_policy(state, action, reward, next_state)
        
        return {"action": action, "reward": reward}

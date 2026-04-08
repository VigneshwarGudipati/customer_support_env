import random
from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import CustomerSupportAction, CustomerSupportObservation
except ImportError:
    from models import CustomerSupportAction, CustomerSupportObservation


class CustomerSupportEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.task_type = "easy"

    def reset(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.task_type = random.choice(["easy", "medium", "hard"])

        if self.task_type == "easy":
            message = "My order is delayed."
        elif self.task_type == "medium":
            message = "I received a damaged product."
        else:
            message = "I ordered 2 weeks ago, still not delivered and I am very frustrated!"

        return CustomerSupportObservation(
            echoed_message=message,
            message_length=len(message),
            done=False,
            reward=0.0,
            metadata={"task_type": self.task_type}
        )

    def step(self, action):
        self._state.step_count += 1

        response = action.message.lower()
        reward = 0.0

        # Empathy
        if "sorry" in response or "apologize" in response:
            reward += 0.3

        # Understanding
        if "understand" in response or "frustrated" in response:
            reward += 0.2

        # Solution
        if any(word in response for word in ["refund", "replace", "resolve", "track"]):
            reward += 0.4

        # Politeness
        if "thank" in response:
            reward += 0.1

        # Penalty
        if len(response.split()) < 5:
            reward -= 0.2

        done = self._state.step_count >= 3

        return CustomerSupportObservation(
            echoed_message="Customer is waiting for resolution...",
            message_length=len(response),
            done=done,
            reward=round(reward, 2),
            metadata={
                "task_type": self.task_type,
                "step": self._state.step_count,
                "response": response
            },
        )

    @property
    def state(self):
        return self._state
    
    # updated version
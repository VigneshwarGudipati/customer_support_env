import random
from env.grader import evaluate_response
from env.reward import compute_reward

TASKS = [
    {"level": "easy", "query": "Where is my order?", "expected": ["check", "status"]},
    {"level": "medium", "query": "I received a damaged product", "expected": ["sorry", "replace"]},
    {"level": "hard", "query": "Your service is terrible!", "expected": ["sorry", "understand"]},
]


class Env:
    def __init__(self):
        self.task = None
        self.done = False
        self.current_state = ""

    def reset(self):
        self.task = random.choice(TASKS)
        self.done = False
        self.current_state = self.task["query"]
        return {"state": self.current_state}

    def step(self, action: str):
        score, breakdown = evaluate_response(action, self.task)
        reward = compute_reward(score, self.task["level"])

        self.done = True
        self.current_state = "Conversation ended"

        return {
            "observation": {"state": self.current_state},
            "reward": reward,
            "done": self.done,
            "info": breakdown,
        }

    def state(self):
        return {"state": self.current_state}
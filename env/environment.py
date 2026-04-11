def reset(self):
    self.task = random.choice(TASKS)
    self.done = False
    self.current_state = self.task["query"]
    return {"state": self.current_state}
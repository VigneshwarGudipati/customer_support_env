from pydantic import BaseModel
from typing import Dict, Any


class Action(BaseModel):
    action: str


class Observation(BaseModel):
    state: str


class Reward(BaseModel):
    reward: float


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]
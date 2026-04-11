from fastapi import FastAPI
from env.environment import Env
from env.models import Action

app = FastAPI()
env = Env()


@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": state["state"] if isinstance(state, dict) else state}


@app.post("/step")
def step(action: Action):
    return env.step(action.action)


@app.get("/state")
def state():
    return env.state()
from fastapi import FastAPI
from env.environment import Env
from env.models import Action

app = FastAPI()
env = Env()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    return env.reset()


@app.post("/step")
def step(action: Action):
    return env.step(action.action)


@app.get("/state")
def state():
    return env.state()
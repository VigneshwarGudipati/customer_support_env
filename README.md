---

title: CustomerSupportEnv
emoji: 🎧
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: apache-2.0
tags:

* openenv
* reinforcement-learning
* customer-support

---

# 🎧 CustomerSupportEnv — Reinforcement Learning Environment for Customer Support

## 🧠 Overview

CustomerSupportEnv is a reinforcement learning (RL) environment designed to simulate realistic customer support interactions.

The system enables an AI agent to learn how to generate responses that are:

* Empathetic
* Contextually appropriate
* Solution-oriented

The environment provides structured evaluation and reward signals, allowing agents to improve through iterative interaction.

---

## 🎯 Motivation

Customer support systems are increasingly automated using AI. However, generating responses alone is insufficient — the **quality of interaction** determines user satisfaction.

In real-world settings, support agents must:

* Interpret user intent under ambiguity
* Respond with empathy and professionalism
* Provide actionable solutions
* Handle emotionally charged interactions

This environment models these requirements in a controlled RL framework, enabling systematic improvement of agent behavior.

---

## 🔁 Reinforcement Learning Framework

```text
State → Action → Evaluation → Reward → Next State
```

* **State** → Customer query
* **Action** → Agent-generated response
* **Evaluation** → Response assessment
* **Reward** → Score in range [0.0, 1.0]
* **Next State** → Updated interaction context

---

## 🏗️ System Architecture

```text
LLM Agent
   ↓
Inference Layer (inference.py)
   ↓
Environment API (/reset, /step)
   ↓
Environment Core (environment.py)
   ↓
Evaluation Layer (grader.py)
   ↓
Reward Function (reward.py)
   ↓
Feedback Loop
```

### Description

* **Inference Layer** handles agent interaction and logging
* **API Layer** exposes environment endpoints via FastAPI
* **Environment Core** manages state transitions and task selection
* **Evaluation Layer** scores agent responses
* **Reward Function** converts scores into learning signals

---

## 🧩 Task Design

### Easy — Informational Queries

* Example: "Where is my order?"
* Focus: basic assistance

### Medium — Problem Resolution

* Example: "I received a damaged product"
* Focus: corrective action

### Hard — Emotional Interactions

* Example: "Your service is terrible!"
* Focus: empathy and de-escalation

---

## ⚙️ Evaluation System

Responses are evaluated using rule-based heuristics.

### Evaluation Criteria

* **Empathy** → presence of apology or understanding
* **Correctness** → alignment with expected response intent
* **Actionability** → whether a solution is provided
* **Clarity** → completeness and readability

---

## 🏆 Reward Function

Rewards are normalized to the range **[0.0, 1.0]**.

### Reward Factors

* Response quality
* Behavioral signals
* Completeness of solution

### Difficulty Scaling

* Easy → baseline
* Medium → moderate
* Hard → higher weighting

---

## 🧾 Code Structure and Responsibilities

* `env/environment.py` → core environment logic
* `env/grader.py` → response evaluation
* `env/reward.py` → reward computation
* `env/models.py` → API schemas
* `server/app.py` → FastAPI endpoints
* `inference.py` → agent interaction loop

---

# 🔍 Detailed Code Walkthrough

## Environment Core (`env/environment.py`)

```python
def reset(self):
    self.task = random.choice(TASKS)
    self.done = False
    self.current_state = self.task["query"]
    return {"state": self.current_state}
```

**Explanation:**
Initializes a new episode by selecting a task and returning the customer query.

---

```python
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
```

**Explanation:**
Evaluates the agent response, computes reward, and returns structured output.

---

## Evaluation Logic (`env/grader.py`)

```python
def evaluate_response(response, task):
    response = response.lower()
    score = 0

    if any(word in response for word in ["sorry", "understand"]):
        score += 3

    if any(word in response for word in task["expected"]):
        score += 3

    if len(response) > 20:
        score += 2

    return score, {}
```

**Explanation:**
Scores responses based on empathy, correctness, and length.

---

## Reward Function (`env/reward.py`)

```python
def compute_reward(score, level):
    base = score / 10.0

    if level == "easy":
        multiplier = 1.0
    elif level == "medium":
        multiplier = 1.2
    else:
        multiplier = 1.5

    reward = base * multiplier
    return max(0.0, min(reward, 1.0))
```

**Explanation:**
Normalizes score and applies difficulty scaling.

---

## API Layer (`server/app.py`)

```python
@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    return env.step(action.action)

@app.get("/state")
def state():
    return env.state()
```

**Explanation:**
Exposes environment functionality via REST API.

---

## Inference Loop (`inference.py`)

```python
completion = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "system", "content": "..."},
        {"role": "user", "content": state},
    ],
)
```

**Explanation:**
Generates agent response using LLM.

---

```python
response = requests.post(
    f"{ENV_URL}/step",
    json={"action": action},
)
```

**Explanation:**
Sends action to environment and retrieves reward.

---

```python
state = data.get("observation", {}).get("state", state)
```

**Explanation:**
Updates state for next iteration.

---

## 🤖 Inference System

* Uses `API_BASE_URL` and `API_KEY`
* Ensures proxy-based API calls
* Logs execution in structured format:

```
[START]
[STEP]
[END]
```

---

## 🌐 API Endpoints

| Method | Endpoint |
| ------ | -------- |
| POST   | `/reset` |
| POST   | `/step`  |
| GET    | `/state` |

---

## 📦 Project Structure

```
customer_support_env/
├── env/
├── server/
├── inference.py
├── openenv.yaml
├── requirements.txt
```

---

## 🧠 Design Decisions

* Rule-based evaluation for deterministic scoring
* Normalized rewards for RL compatibility
* Single-turn design for simplicity
* Modular architecture for extensibility

---

## ⚠️ Limitations

* Single-turn interaction
* Heuristic evaluation
* Limited scenarios

---

## 🚀 Future Work

* Multi-turn conversations
* LLM-based evaluation
* Expanded task diversity

---

## 🏁 Conclusion

CustomerSupportEnv provides a structured RL environment that:

* Simulates customer support scenarios
* Evaluates responses systematically
* Enables iterative improvement

It serves as a foundation for building intelligent support agents.

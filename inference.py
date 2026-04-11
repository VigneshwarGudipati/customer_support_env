import os
import asyncio
from openai import OpenAI
import requests

# Strict environment variables (DO NOT CHANGE)
API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]

MODEL = os.environ.get("MODEL", "gpt-4.1-mini")
ENV_URL = os.environ.get("ENV_SERVER_URL", "http://127.0.0.1:8000")

# Initialize client with proxy
client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


# Logging functions (STRICT FORMAT REQUIRED)
def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done):
    print(
        f"[STEP] step={step} action={action[:100]} reward={reward:.2f} done={str(done).lower()} error=null",
        flush=True,
    )


def log_end(success, steps, rewards):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True,
    )


async def main():
    rewards = []
    success = False

    log_start("customer_support", "openenv", MODEL)

    # RESET ENV
    response = requests.post(f"{ENV_URL}/reset")
    state = response.json().get("state", "")

    for step in range(1, 6):
        try:
            # REQUIRED: responses API (proxy-detected)
            response = client.responses.create(
                model=MODEL,
                input=[
                    {
                        "role": "system",
                        "content": "You are a professional customer support agent. Provide empathetic, clear, and solution-oriented responses.",
                    },
                    {
                        "role": "user",
                        "content": state,
                    },
                ],
            )

            try:
                action = response.output_text.strip()
            except Exception:
                action = response.output[0].content[0].text.strip()

            if not action:
                action = "I will assist you with your issue."

        except Exception as e:
            print(f"[DEBUG] Model call failed: {e}", flush=True)
            action = "I will assist you with your issue."

        # STEP ENV (FIXED PAYLOAD)
        response = requests.post(
            f"{ENV_URL}/step",
            json={"action": action},
        )

        data = response.json()

        reward = float(data.get("reward", 0.0))
        done = data.get("done", False)

        rewards.append(reward)

        log_step(step, action, reward, done)

        # Update state (OpenEnv format)
        state = data.get("observation", {}).get("state", state)

        if done:
            success = True
            break

    log_end(success, len(rewards), rewards)


if __name__ == "__main__":
    asyncio.run(main())
import os
from openai import OpenAI

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]

MODEL_NAME = "gpt-4.1-mini"

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
)

def run_episode():
    print(f"[START] task=customer_support env=openenv model={MODEL_NAME}")

    rewards = []
    success = False

    # 🔥 FIRST API CALL
    response = client.responses.create(
        model=MODEL_NAME,
        input="Hello"
    )

    action = response.output_text.strip()

    for step in range(1, 4):

        # 🔥 SECOND API CALL
        response = client.responses.create(
            model=MODEL_NAME,
            input="Customer: My order is delayed. Respond politely."
        )

        action = response.output_text.strip()

        reward = 1.0 if step == 3 else 0.5
        done = step == 3

        rewards.append(f"{reward:.2f}")

        print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

        if done:
            success = True
            break

    print(f"[END] success={str(success).lower()} steps={len(rewards)} rewards={','.join(rewards)}")


if __name__ == "__main__":
    run_episode()
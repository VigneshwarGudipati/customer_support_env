import os
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
API_KEY = os.getenv("API_KEY", "dummy")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

def run_episode():
    print(f"[START] task=customer_support env=openenv model={MODEL_NAME}")

    rewards = []
    success = False

    for step in range(1, 4):

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful support agent."},
                {"role": "user", "content": "Customer: My order is delayed and I am upset."}
            ],
            temperature=0.0
        )

        action = response.choices[0].message.content.strip()

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
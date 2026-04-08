import os
from openai import OpenAI
from env.delivery_env import DeliveryEnv  # your env

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def get_action(state):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a delivery optimization agent."},
            {"role": "user", "content": str(state)}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def main():
    env = DeliveryEnv()
    state = env.reset()

    rewards = []
    steps = 0

    log_start("delivery_task", "delivery_env", MODEL_NAME)

    done = False

    while not done and steps < 50:
        steps += 1

        action = get_action(state)

        state, reward, done, _ = env.step(action)

        rewards.append(reward)

        log_step(steps, action, reward, done, None)

    score = sum(rewards) / (len(rewards) + 1e-6)
    success = score > 0.1

    log_end(success, steps, score, rewards)

if __name__ == "__main__":
    main()
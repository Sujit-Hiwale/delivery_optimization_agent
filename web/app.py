import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, jsonify, request
from env.environment import DeliveryEnv
from env.models import Action, Order
from env.grader import grade
from agents.baseline import baseline_agent

app = Flask(__name__)

env = DeliveryEnv(num_vehicles=3)
obs = env.reset()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/step")
def step():
    global obs

    action = baseline_agent(obs)
    obs, reward, done, _ = env.step(action)

    return jsonify({
        "orders": [
            {
                "id": o.id,
                "lat": o.location[0],
                "lon": o.location[1],
                "delivered": o.delivered,
                "picked": getattr(o, "picked", False)
            }
            for o in obs.orders
        ],
        "vehicles": [
            {"id": v.id, "lat": v.location[0], "lon": v.location[1]}
            for v in obs.vehicles
        ],
        "warehouses": [
            {"lat": w[0], "lon": w[1]}
            for w in env.warehouses
        ],
        "metrics": {
            "reward": reward,
            "score": grade(env),
            "time": obs.time,
            "delivery_rate": env.completed / (env.completed + len(env.orders) + 1),
            "vehicle_stats": env.vehicle_stats
        },
        "done": done
    })


@app.route("/reset", methods=["POST"])
def reset():
    global env, obs

    data = request.json
    vehicles = data.get("vehicles", 3)

    env = DeliveryEnv(num_vehicles=vehicles)
    obs = env.reset()

    return {"status": "ok"}


@app.route("/add_order", methods=["POST"])
def add_order():
    data = request.get_json()

    order = Order(
        id=len(env.orders),
        location=(data["lat"], data["lon"]),
        deadline=env.time + 20,
        pickup=random.choice(env.warehouses),
        picked=False
    )

    env.orders.append(order)

    return jsonify({"status": "added"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
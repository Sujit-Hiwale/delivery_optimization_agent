# AI Delivery Optimization Agent

## Overview

This project is an AI-driven logistics simulation system that models multi-vehicle delivery operations in an urban environment. It integrates real-time visualization with intelligent routing strategies to simulate warehouse-based pickup and delivery workflows.

The system supports dynamic order creation, multi-vehicle coordination, and route optimization with the goal of minimizing total travel distance while maximizing delivery efficiency.

---

## Features

- Multi-vehicle delivery simulation
- Warehouse-based pickup and delivery flow
- Real-time map visualization using Leaflet
- Intelligent routing via heuristic baseline agent
- Distance-based reward optimization
- Vehicle-level performance metrics
- Interactive order placement via map clicks
- Live performance tracking using Chart.js

---

## System Architecture

```

Frontend (HTML + JS + Leaflet)
↓
Flask Backend API
↓
Delivery Environment (Simulation Engine)
↓
Agent (Routing Logic)

```

---

## Project Structure

```

Meta/
│
├── web/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── script.js
│
├── env/
│   ├── environment.py
│   ├── models.py
│   └── grader.py
│
├── agents/
│   └── baseline.py
│
├── tasks/
│   └── hard.py
│
├── scripts/
│   └── run_baseline.py
│
├── requirements.txt
├── Dockerfile
└── README.md

````

---

## Installation

### Clone the repository

```bash
git clone [<your-repo-url>](https://github.com/Sujit-Hiwale/delivery_optimization_agent)
````

---

### Create virtual environment

```
python -m venv venv
source venv/bin/activate
```

For Windows:

```
venv\Scripts\activate
```

---

### Install dependencies

```
pip install -r requirements.txt
```

---

## Running the Application

### Start the Flask server

```
python web/app.py
```

---

### Access the application

Open your browser and go to:

```
http://127.0.0.1:7860
```

---

## 🐳 Docker Support

You can run the application using Docker for a consistent environment across systems.

### Build the Docker image

```
docker build -t ai-delivery-system .
```

### Run the container

```
docker run -p 7860:7860 ai-delivery-system
```

### Access the application

Open your browser and go to:

```
http://127.0.0.1:7860
```

---

## Usage

### Add Orders

Click anywhere on the map to create a delivery order

### Reset Simulation

Set number of vehicles in the sidebar

Click "Reset Simulation"

---

## Visualization

| Element     | Description                   |
| ----------- | ----------------------------- |
| Red dots    | Orders not yet picked         |
| Green dots  | Orders picked and in delivery |
| 🏭          | Warehouses                    |
| 🚚          | Vehicles                      |

---

## Metrics

The system tracks:

* Reward
* Score
* Delivery Rate
* Vehicle-wise delivery count
* Time progression

---

## Routing Logic

The baseline agent implements:

* Nearest-neighbor assignment
* Capacity-aware batching
* Greedy route optimization
* Pickup-before-delivery constraint

---

## Simulation Logic

Each vehicle:

1. Moves to warehouse for pickup
2. Picks assigned orders
3. Delivers orders to customers
4. Updates routes dynamically

---

### Reward is influenced by:

* Distance traveled
* On-time delivery
* Late delivery penalties
* Idle penalties

---

## Offline Evaluation

```
python scripts/run_baseline.py
```

---

## Future Improvements

* Reinforcement Learning integration (DQN / PPO)
* Traffic simulation
* Dynamic order generation
* Multi-warehouse optimization
* Route visualization
* Real-time updates

---

## Technologies Used

* Python
* Flask
* Pydantic
* Leaflet.js
* Chart.js

---

## Notes

* Intended for simulation and research purposes
* Uses Flask development server

---

## License

This project is for educational and research purposes.

```
```

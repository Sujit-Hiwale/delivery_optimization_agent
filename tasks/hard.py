import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from env.environment import DeliveryEnv

def create_env(num_vehicles=3):
    return DeliveryEnv(num_vehicles=num_vehicles)
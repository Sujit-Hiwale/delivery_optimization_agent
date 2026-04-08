from env.models import Action


def distance(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2


def nearest_neighbor_route(start, points):
    route = []
    current = start
    remaining = points[:]

    while remaining:
        next_point = min(remaining, key=lambda p: distance(current, p))
        route.append(next_point)
        current = p = next_point
        remaining.remove(next_point)

    return route


def baseline_agent(obs):
    assignments = {}

    remaining_orders = [o for o in obs.orders if not o.delivered]

    for v in obs.vehicles:
        if not remaining_orders:
            assignments[v.id] = []
            continue

        # Step 1: assign closest orders
        sorted_orders = sorted(
            remaining_orders,
            key=lambda o: distance(v.location, o.location)
        )

        selected = sorted_orders[:v.capacity]

        # Step 2: create pickup + delivery points
        route_points = []

        for o in selected:
            if not getattr(o, "picked", False):
                route_points.append(o.pickup)   # go to warehouse
            route_points.append(o.location)     # then deliver

        # Step 3: optimize route
        optimized = nearest_neighbor_route(v.location, route_points)

        # Step 4: map back to order IDs
        ordered_ids = []
        for point in optimized:
            for o in selected:
                if (not o.picked and point == o.pickup) or point == o.location:
                    if o.id not in ordered_ids:
                        ordered_ids.append(o.id)

        assignments[v.id] = ordered_ids

        for o in selected:
            remaining_orders.remove(o)

    return Action(assignments=assignments)
import heapq
from core.cost_model import compute_cost
from math import radians, sin, cos, sqrt, asin

def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def astar(start, goal, cities, roads, city_info, county_cost):
    max_pop = max(city['population'] for city in city_info.values())
    open_set = [(haversine(cities[start], cities[goal]), 0, start, [])]
    visited = set()
    while open_set:
        f, g, current, path = heapq.heappop(open_set)
        if current in visited:
            continue
        path = path + [current]
        if current == goal:
            return path, g
        visited.add(current)
        for neighbor, base_dist in roads.get(current, []):
            if neighbor in visited:
                continue
            cost = compute_cost(current, neighbor, base_dist, city_info, county_cost, max_pop)
            h = haversine(cities[neighbor], cities[goal])
            heapq.heappush(open_set, (
                g + cost + h,
                g + cost,
                neighbor,
                path
            ))
    return [], float('inf')

from data.city_data import cities, roads, city_info, county_cost_per_mile
from core.a_star import astar

def run():
    start = 'San Jose'
    goals = ['Fremont', 'Palo Alto', 'Sunnyvale', 'Cupertino']
    for goal in goals:
        path, cost = astar(start, goal, cities, roads, city_info, county_cost_per_mile)
        print(f"{start} → {goal} ：Path = {path}, Cost = {round(cost, 2)} km")

if __name__ == "__main__":
    run()

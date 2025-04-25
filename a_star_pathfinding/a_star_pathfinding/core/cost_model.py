def compute_cost(from_city, to_city, base_distance, city_info, county_cost_dict, max_pop, alpha=0.3):
    pop = city_info[to_city]['population']
    county = city_info[from_city]['county']
    cost_factor = county_cost_dict[county] / 200000
    pop_factor = 1 - alpha * (pop / max_pop)
    return base_distance * (1 + cost_factor) * pop_factor

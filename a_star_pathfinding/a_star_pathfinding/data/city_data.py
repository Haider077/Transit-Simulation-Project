cities = {
    'San Jose': (37.3382, -121.8863),
    'Santa Clara': (37.3541, -121.9552),
    'Sunnyvale': (37.3688, -122.0363),
    'Cupertino': (37.3229, -122.0322),
    'Palo Alto': (37.4419, -122.1430),
    'Fremont': (37.5483, -121.9886)
}

city_info = {
    'San Jose': {'population': 971233, 'county': 'Santa Clara'},
    'Santa Clara': {'population': 127647, 'county': 'Santa Clara'},
    'Sunnyvale': {'population': 155805, 'county': 'Santa Clara'},
    'Cupertino': {'population': 60381, 'county': 'Santa Clara'},
    'Palo Alto': {'population': 68572, 'county': 'Santa Clara'},
    'Fremont': {'population': 230504, 'county': 'Alameda'}
}

roads = {
    'San Jose': [('Santa Clara', 7.0), ('Cupertino', 13.5)],
    'Santa Clara': [('Sunnyvale', 6.3)],
    'Sunnyvale': [('Palo Alto', 9.1)],
    'Cupertino': [('Palo Alto', 10.5)],
    'Palo Alto': [('Fremont', 16.0)]
}

county_cost_per_mile = {
    'Santa Clara': 163020,
    'Alameda': 148423
}

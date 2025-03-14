import pandas as pd
import requests
import dotenv
import os
from urllib.parse import quote

from optimal_route import best_k_city_tsp

dotenv.load_dotenv('.env')


API_KEY = os.getenv("GOOGLE_API_KEY")


# function to read and parse csv into a list of column values


def get_column_values(filepath, column_to_parse):
    try:
        df = pd.read_csv(filepath)[column_to_parse]
        return [val for val in df]

    except:
        raise Exception("File or column does not exist!")

# function that uses Distance Matrix API (Google) to return distance from point A to a list of points.


def get_distances(start: str, addresses: list[str]):
    encoded_start = quote(start)
    encoded_addresses = list(map(lambda x: quote(x), addresses))
    response = requests.get(os.getenv('API_URL').format(
        origin=encoded_start, destinations="|".join(encoded_addresses), api_key=API_KEY))
    rows = response.json()['rows']
    elements = rows[0]['elements']
    return [float(elem['duration']['value']) for elem in elements]


def create_adjacency_matrix(start, addresses):
    n = len(addresses) + 1
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    distances_from_start = get_distances(start=start, addresses=addresses)

    for i in range(n-1):
        matrix[0][i+1] = distances_from_start[i]
        matrix[i+1][0] = distances_from_start[i]

    for i in range(1, n):
        distances_from_current = get_distances(
            start=addresses[i-1], addresses=addresses)

        for j in range(i+1, n):
            matrix[i][j] = distances_from_current[j-1]
            matrix[j][i] = distances_from_current[j-1]

    return matrix


start_address = '4029 Alia Dr, Warren, MI 48092'
addresses = get_column_values("sample.csv", 'Address')
adj_matrix = create_adjacency_matrix(start_address, addresses)

k = 2
best_subset, min_cost, best_path = best_k_city_tsp(adj_matrix, k, 0)

# best_subset_verbose = [start_address if node ==
#                        0 else addresses[node] for node in best_path]
# print(f"Best subset of cities to visit: {best_subset_verbose}")
minutes, seconds = divmod(min_cost, 60)
print(
    f"Minimum travel time: {minutes:.0f} minutes {seconds:.0f} seconds")
best_path_verbose = " -> ".join([start_address if node ==
                                 0 else addresses[node] for node in best_path])+" -> "+start_address
print(f"Optimal path: {best_path_verbose}")

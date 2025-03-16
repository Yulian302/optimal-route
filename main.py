from pandas import read_csv
import requests
from dotenv import load_dotenv
from os import getenv
from urllib.parse import quote
from io import BytesIO

load_dotenv('.env')


API_KEY = getenv("GOOGLE_API_KEY")


# function to read and parse csv into a list of column values


def get_column_values(contents, column_to_parse):
    try:
        df = read_csv(BytesIO(contents))[column_to_parse]
        return [val for val in df]

    except:
        raise Exception("File or column does not exist!")

# function that uses Distance Matrix API (Google) to return distance from point A to a list of points.


def get_distances(start: str, addresses: list[str]):
    encoded_start = quote(start)
    encoded_addresses = list(map(lambda x: quote(x), addresses))
    response = requests.get(getenv('API_URL').format(
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

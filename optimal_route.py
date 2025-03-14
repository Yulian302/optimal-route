from functools import lru_cache
import itertools


def tsp(graph, cities):
    """
    Solves TSP for a given subset of cities using Dynamic Programming (Bitmasking).

    :param graph: Full N x N distance matrix.
    :param cities: List of selected K city indices.
    :return: (Minimum Cost, Optimal Path)
    """
    k = len(cities)

    reduced_graph = [[graph[cities[i]][cities[j]]
                      for j in range(k)] for i in range(k)]

    @lru_cache(None)
    def dp(mask, last):
        if mask == (1 << k) - 1:
            return reduced_graph[last][0], [cities[last]]

        min_cost = float('inf')
        best_path = []

        for next_city in range(k):
            if not (mask & (1 << next_city)):
                cost, path = dp(mask | (1 << next_city), next_city)
                total_cost = reduced_graph[last][next_city] + cost

                if total_cost < min_cost:
                    min_cost = total_cost
                    best_path = [cities[last]] + path

        return min_cost, best_path

    min_cost, path = dp(1, 0)
    return min_cost, path


def best_k_city_tsp(graph, k, start_city=0):
    """
    Selects the best K cities out of N, then solves TSP among them.

    :param graph: Full N x N distance matrix.
    :param k: Number of cities to visit (excluding start city).
    :param start_city: The index of the starting city.
    :return: (Best Subset of K Cities, Minimum Cost, Optimal Path)
    """
    n = len(graph)
    min_cost = float('inf')
    best_path = []
    best_subset = []

    city_indices = list(range(n))
    city_indices.remove(start_city)
    possible_subsets = itertools.combinations(city_indices, k)

    for subset in possible_subsets:
        selected_cities = [start_city] + list(subset)
        cost, path = tsp(graph, selected_cities)

        if cost < min_cost:
            min_cost = cost
            best_path = path
            best_subset = selected_cities

    return best_subset, min_cost, best_path

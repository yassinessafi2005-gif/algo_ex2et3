"""Exercice 3 — TSP par recherche tabou et recuit simulé (5 itérations)."""

import math
import random

N = 8
# Graphe non orienté : les liaisons absentes du tableau ne sont pas permises.
EDGES = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9, (7, 8): 13,
}
DIST = {**EDGES, **{(b, a): cost for (a, b), cost in EDGES.items()}}
INITIAL = (1, 2, 3, 4, 5, 6, 7, 8)


def tour_cost(tour):
    cycle = tour + (tour[0],)
    try:
        return sum(DIST[(cycle[i], cycle[i + 1])] for i in range(N))
    except KeyError:
        return math.inf


def two_opt_neighbors(tour):
    """Inversion d'un segment, en gardant la ville 1 en première position."""
    for i in range(1, N - 1):
        for j in range(i + 1, N):
            candidate = tour[:i] + tuple(reversed(tour[i:j + 1])) + tour[j + 1:]
            if math.isfinite(tour_cost(candidate)):
                yield candidate


def tabu_tsp(max_iterations=20, tenure=5):
    current = INITIAL
    best = current
    best_cost = tour_cost(best)
    tabu = {}
    history = []

    for iteration in range(max_iterations):
        candidates = []
        for candidate in two_opt_neighbors(current):
            cost = tour_cost(candidate)
            if tabu.get(candidate, -1) > iteration and cost >= best_cost:
                continue
            candidates.append((cost, candidate))
        if not candidates:
            break

        cost, current = min(candidates, key=lambda item: (item[0], item[1]))
        tabu[current] = iteration + tenure
        if cost < best_cost:
            best, best_cost = current, cost
        history.append((iteration + 1, current, cost, best_cost))

    return best, best_cost, history


def simulated_annealing_tsp(iterations=5, seed=7):
    rng = random.Random(seed)
    current = INITIAL
    current_cost = tour_cost(current)
    best = current
    best_cost = current_cost
    # Température empirique : 5 % du coût initial, puis baisse de 1 par tour.
    temperature = max(1.0, 0.05 * current_cost)
    history = []

    for step in range(1, iterations + 1):
        candidate = rng.choice(list(two_opt_neighbors(current)))
        candidate_cost = tour_cost(candidate)
        delta = candidate_cost - current_cost
        accepted = delta <= 0 or rng.random() < math.exp(-delta / temperature)
        if accepted:
            current, current_cost = candidate, candidate_cost
        if current_cost < best_cost:
            best, best_cost = current, current_cost
        history.append((step, temperature, candidate, candidate_cost, accepted,
                        current, current_cost, best, best_cost))
        temperature = max(1.0, temperature - 1.0)

    return best, best_cost, history


def show_tour(tour):
    return "-".join(map(str, tour + (tour[0],)))


def main():
    print("EXERCICE 3 — Recherche tabou")
    tour, cost, history = tabu_tsp()
    print("Tour initial:", show_tour(INITIAL), "coût =", tour_cost(INITIAL))
    for iteration, state, state_cost, best_cost in history:
        print(f"{iteration:2d}: {show_tour(state)} | coût={state_cost} | meilleur={best_cost}")
    print("Meilleur tour tabou:", show_tour(tour), "coût =", cost)

    print("\nEXERCICE 3 — Recuit simulé (5 itérations, seed=7)")
    tour, cost, history = simulated_annealing_tsp()
    for step, temperature, proposal, proposal_cost, accepted, state, state_cost, best, best_cost in history:
        decision = "acceptée" if accepted else "rejetée"
        print(f"{step}: T={temperature:.2f}, proposition={show_tour(proposal)} "
              f"({proposal_cost}), {decision}, état={show_tour(state)} ({state_cost}), "
              f"meilleur={show_tour(best)} ({best_cost})")
    print("Meilleur tour recuit:", show_tour(tour), "coût =", cost)


if __name__ == "__main__":
    main()

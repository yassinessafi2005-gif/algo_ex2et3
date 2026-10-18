"""Exercice 2 — problème de transport résolu par recherche tabou."""

SUPPLIES = (8, 9)
DEMANDS = (4, 5, 8)
COSTS = ((5, 3, 4), (6, 7, 2))


def transport_cost(x):
    return sum(x[i][j] * COSTS[i][j] for i in range(2) for j in range(3))


def transport_neighbors(x):
    """Génère les allocations voisines par cycle 2x2 réalisable."""
    seen = set()
    for j1 in range(3):
        for j2 in range(j1 + 1, 3):
            limit = min(x[0][j2], x[1][j1])
            for quantity in range(1, limit + 1):
                y = [list(x[0]), list(x[1])]
                y[0][j1] += quantity
                y[1][j2] += quantity
                y[0][j2] -= quantity
                y[1][j1] -= quantity
                candidate = tuple(tuple(row) for row in y)
                if candidate not in seen:
                    seen.add(candidate)
                    yield candidate

            limit = min(x[0][j1], x[1][j2])
            for quantity in range(1, limit + 1):
                y = [list(x[0]), list(x[1])]
                y[0][j1] -= quantity
                y[1][j2] -= quantity
                y[0][j2] += quantity
                y[1][j1] += quantity
                candidate = tuple(tuple(row) for row in y)
                if candidate not in seen:
                    seen.add(candidate)
                    yield candidate


def tabu_transport(max_iterations=20, tenure=3):
    # Solution initiale réalisable par la méthode du coin nord-ouest.
    current = ((4, 4, 0), (0, 1, 8))
    best = current
    best_cost = transport_cost(best)
    tabu = {}
    history = []

    for iteration in range(max_iterations):
        candidates = []
        for candidate in transport_neighbors(current):
            cost = transport_cost(candidate)
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


def main():
    allocation, cost, history = tabu_transport()
    print("EXERCICE 2 — Recherche tabou")
    print("Allocation (lignes D1,D2; colonnes M1,M2,M3):", allocation)
    print("Coût total:", cost)
    print("Itérations:", len(history))


if __name__ == "__main__":
    main()

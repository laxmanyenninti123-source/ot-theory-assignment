import numpy as np

# --------------------------------------------------
# MODI METHOD
# --------------------------------------------------

cost = np.array([
    [2, 4, 8],
    [6, 1, 2],
    [10, 11, 8]
], dtype=float)

# Initial solution obtained using VAM
allocation = np.array([
    [20, 0, 0],
    [0, 10, 20],
    [10, 15, 0]
], dtype=float)

m, n = cost.shape


def find_cycle(allocation, entering):
    """
    Find a closed loop for the entering cell.
    """

    basics = {
        (i, j)
        for i in range(m)
        for j in range(n)
        if allocation[i, j] > 0
    }

    def search(path):

        current = path[-1]
        i, j = current

        # Move horizontally / vertically alternately
        if len(path) % 2 == 1:

            candidates = [
                (i, col)
                for col in range(n)
                if ((i, col) in basics or
                    (i, col) == entering)
                and (i, col) != current
            ]

        else:

            candidates = [
                (row, j)
                for row in range(m)
                if ((row, j) in basics or
                    (row, j) == entering)
                and (row, j) != current
            ]

        for cell in candidates:

            if cell == entering and len(path) >= 4:
                return path + [entering]

            if cell in path:
                continue

            result = search(path + [cell])

            if result:
                return result

        return None

    return search([entering])


iteration = 1

while True:

    # Find basic cells
    basic_cells = [
        (i, j)
        for i in range(m)
        for j in range(n)
        if allocation[i, j] > 0
    ]

    # --------------------------------------------------
    # Calculate u and v
    # --------------------------------------------------

    u = [None] * m
    v = [None] * n

    u[0] = 0

    changed = True

    while changed:

        changed = False

        for i, j in basic_cells:

            if u[i] is not None and v[j] is None:
                v[j] = cost[i, j] - u[i]
                changed = True

            elif v[j] is not None and u[i] is None:
                u[i] = cost[i, j] - v[j]
                changed = True

    # --------------------------------------------------
    # Calculate opportunity costs
    # Delta = Cij - (Ui + Vj)
    # --------------------------------------------------

    delta = np.full((m, n), np.nan)

    for i in range(m):
        for j in range(n):

            if (i, j) not in basic_cells:
                delta[i, j] = (
                    cost[i, j] - (u[i] + v[j])
                )

    print("\n========================================")
    print("MODI ITERATION", iteration)
    print("========================================")

    print("\nCurrent Allocation:")
    print(allocation)

    print("\nU values:")
    print(u)

    print("\nV values:")
    print(v)

    print("\nOpportunity Cost (Delta):")
    print(delta)

    minimum_delta = np.nanmin(delta)

    # --------------------------------------------------
    # Optimality test
    # --------------------------------------------------

    if minimum_delta >= 0:

        print("\nAll Delta values are >= 0.")
        print("Therefore, the solution is OPTIMAL.")

        break

    # --------------------------------------------------
    # Select entering cell
    # --------------------------------------------------

    entering = np.unravel_index(
        np.nanargmin(delta),
        delta.shape
    )

    print(
        "\nEntering Cell:",
        f"S{entering[0] + 1} -> D{entering[1] + 1}"
    )

    # Find closed loop
    cycle = find_cycle(allocation, entering)

    print("Closed Loop:", [
        f"({i + 1},{j + 1})"
        for i, j in cycle
    ])

    # --------------------------------------------------
    # + and - positions
    # --------------------------------------------------

    minus_cells = cycle[1:-1:2]

    theta = min(
        allocation[i, j]
        for i, j in minus_cells
    )

    print("Theta =", theta)

    # Update allocation
    for k, (i, j) in enumerate(cycle[:-1]):

        if k % 2 == 0:
            allocation[i, j] += theta
        else:
            allocation[i, j] -= theta

    iteration += 1


# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

total_cost = np.sum(allocation * cost)

print("\n========================================")
print("FINAL OPTIMAL TRANSPORTATION PLAN")
print("========================================")

print(allocation)

print("\nMinimum Transportation Cost =",
      total_cost)

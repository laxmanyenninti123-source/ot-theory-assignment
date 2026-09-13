import numpy as np

# --------------------------------------------------
# VOGEL'S APPROXIMATION METHOD (VAM)
# --------------------------------------------------

cost = np.array([
    [2, 4, 8],
    [6, 1, 2],
    [10, 11, 8]
], dtype=float)

supply = [20, 30, 25]
demand = [30, 25, 20]

m, n = cost.shape

allocation = np.zeros((m, n))

remaining_supply = supply.copy()
remaining_demand = demand.copy()

active_rows = set(range(m))
active_cols = set(range(n))

print("INITIAL COST TABLE")
print(cost)

while active_rows and active_cols:

    # Calculate row penalties
    row_penalty = {}

    for i in active_rows:
        values = sorted(
            cost[i, j] for j in active_cols
        )

        if len(values) >= 2:
            row_penalty[i] = values[1] - values[0]
        else:
            row_penalty[i] = values[0]

    # Calculate column penalties
    col_penalty = {}

    for j in active_cols:
        values = sorted(
            cost[i, j] for i in active_rows
        )

        if len(values) >= 2:
            col_penalty[j] = values[1] - values[0]
        else:
            col_penalty[j] = values[0]

    max_row_penalty = (
        max(row_penalty.values())
        if row_penalty else -1
    )

    max_col_penalty = (
        max(col_penalty.values())
        if col_penalty else -1
    )

    # Select row or column with maximum penalty
    if max_row_penalty >= max_col_penalty:

        row = max(
            row_penalty,
            key=lambda x: (
                row_penalty[x],
                -min(cost[x, j] for j in active_cols)
            )
        )

        col = min(
            active_cols,
            key=lambda j: (cost[row, j], j)
        )

        selected_penalty = row_penalty[row]

        print("\nSelected Row:", row + 1)
        print("Penalty:", selected_penalty)

    else:

        col = max(
            col_penalty,
            key=lambda x: (
                col_penalty[x],
                -min(cost[i, x] for i in active_rows)
            )
        )

        row = min(
            active_rows,
            key=lambda i: (cost[i, col], i)
        )

        selected_penalty = col_penalty[col]

        print("\nSelected Column:", col + 1)
        print("Penalty:", selected_penalty)

    # Allocate maximum possible quantity
    quantity = min(
        remaining_supply[row],
        remaining_demand[col]
    )

    allocation[row, col] = quantity

    print(
        "Allocation:",
        f"S{row + 1} -> D{col + 1} = {quantity}"
    )

    remaining_supply[row] -= quantity
    remaining_demand[col] -= quantity

    # Remove satisfied row/column
    if remaining_supply[row] == 0:
        active_rows.remove(row)

    if remaining_demand[col] == 0:
        active_cols.remove(col)


# Calculate total transportation cost
total_cost = np.sum(allocation * cost)

print("\n========================================")
print("VAM INITIAL BASIC FEASIBLE SOLUTION")
print("========================================")

print(allocation)

print("\nTotal Transportation Cost =", total_cost)

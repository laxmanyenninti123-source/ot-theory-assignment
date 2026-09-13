import numpy as np

# --------------------------------------------------
# BIG-M SIMPLEX METHOD
# --------------------------------------------------

M = 1000000

# Variables:
# x1, x2, s1, s2, a2
variable_names = ["x1", "x2", "s1", "s2", "a2"]

# Objective coefficients
C = np.array([3, 5, 0, 0, -M], dtype=float)

# Constraint coefficient matrix
A = np.array([
    [1, 1, 1, 0, 0],
    [1, 3, 0, -1, 1]
], dtype=float)

# RHS
b = np.array([4, 3], dtype=float)

# Initial basic variables: s1 and a2
basis = [2, 4]

# Create tableau
tableau = np.column_stack((A, b))

iteration = 0

while True:

    # Cost coefficients of basic variables
    CB = np.array([C[i] for i in basis])

    # Zj values
    Zj = CB @ tableau[:, :-1]

    # Z value
    Z = CB @ tableau[:, -1]

    # Cj - Zj
    Cj_Zj = C - Zj

    print("\n----------------------------------------")
    print("Iteration:", iteration)
    print("----------------------------------------")

    print("Basic Variables:",
          [variable_names[i] for i in basis])

    print("\nTableau:")
    print(np.round(tableau, 4))

    print("\nCj - Zj:")
    print(np.round(Cj_Zj, 4))

    print("Z =", round(Z, 4))

    # Optimality condition
    if np.max(Cj_Zj) <= 0:
        break

    # Entering variable
    entering = int(np.argmax(Cj_Zj))

    # Ratio test
    ratios = []

    for i in range(len(b)):
        if tableau[i, entering] > 0:
            ratio = tableau[i, -1] / tableau[i, entering]
            ratios.append((ratio, i))

    if not ratios:
        print("Solution is unbounded.")
        break

    # Leaving variable
    _, leaving = min(ratios)

    print("\nEntering Variable:",
          variable_names[entering])

    print("Leaving Variable:",
          variable_names[basis[leaving]])

    # Pivot
    pivot = tableau[leaving, entering]

    tableau[leaving, :] /= pivot

    for i in range(len(b)):
        if i != leaving:
            tableau[i, :] -= (
                tableau[i, entering] *
                tableau[leaving, :]
            )

    basis[leaving] = entering

    iteration += 1


# --------------------------------------------------
# FINAL SOLUTION
# --------------------------------------------------

solution = np.zeros(len(C))

for i, variable in enumerate(basis):
    solution[variable] = tableau[i, -1]

print("\n========================================")
print("FINAL OPTIMAL SOLUTION")
print("========================================")

for i in range(len(variable_names)):
    print(variable_names[i], "=", round(solution[i], 4))

print("Maximum Z =", round(Z, 4))

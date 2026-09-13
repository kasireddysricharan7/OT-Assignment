M = 10**6
z_coeff = [3, 5, 0, 0, -M]
RHS = [10, 8]
basic_coeff = [0, -M]
table = [
    [2, 1, 1, 0, 0],
    [1, 2, 0, -1, 1]
]

dev = []
for j in range(len(z_coeff)):
    reduced_cost = z_coeff[j] - sum(basic_coeff[i] * table[i][j] for i in range(len(basic_coeff)))
    dev.append(reduced_cost)

z = sum(RHS[i] * basic_coeff[i] for i in range(len(RHS)))

while True:
    if max(dev) <= 0:
        break

    pivot_col = dev.index(max(dev))

    ratios = []
    for i in range(len(RHS)):
        pivot_value = table[i][pivot_col]
        if pivot_value > 0:
            ratios.append(RHS[i] / pivot_value)
        else:
            ratios.append(float("inf"))

    if all(value == float("inf") for value in ratios):
        raise ValueError("No feasible pivot row found for the selected entering column.")

    pivot_row = ratios.index(min(ratios))

    pivot = table[pivot_row][pivot_col]

    for j in range(len(table[pivot_row])):
        table[pivot_row][j] /= pivot
    RHS[pivot_row] /= pivot

    for i in range(len(table)):
        if i == pivot_row:
            continue

        factor = table[i][pivot_col]
        if factor == 0:
            continue

        for j in range(len(table[i])):
            table[i][j] -= factor * table[pivot_row][j]

        RHS[i] -= factor * RHS[pivot_row]

    basic_coeff[pivot_row] = z_coeff[pivot_col]

    dev = []
    for j in range(len(z_coeff)):
        reduced_cost = z_coeff[j] - sum(basic_coeff[i] * table[i][j] for i in range(len(basic_coeff)))
        dev.append(reduced_cost)

    z = sum(RHS[i] * basic_coeff[i] for i in range(len(RHS)))

print("Optimal solution found:")
print("Basic coefficients:", basic_coeff)
print("Optimal objective function value:", z)
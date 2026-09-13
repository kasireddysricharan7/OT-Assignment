cost = [
    [10, 0, 20, 11],
    [12, 8, 9, 20],
    [0, 14, 16, 18]
]

supply = [15, 25, 10]
demand = [5, 20, 15, 10]

allocation = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

remaining_supply = supply.copy()
remaining_demand = demand.copy()


# ---------------- VAM ----------------

while sum(remaining_supply) > 0:

    row_penalty = [None, None, None]

    for i in range(len(cost)):

        values = []

        if remaining_supply[i] > 0:

            for j in range(len(cost[0])):

                if remaining_demand[j] > 0:
                    values.append(cost[i][j])

        if len(values) >= 2:
            values.sort()
            row_penalty[i] = values[1] - values[0]

        elif len(values) == 1:
            row_penalty[i] = values[0]


    col_penalty = [None, None, None, None]

    for j in range(len(cost[0])):

        values = []

        if remaining_demand[j] > 0:

            for i in range(len(cost)):

                if remaining_supply[i] > 0:
                    values.append(cost[i][j])

        if len(values) >= 2:
            values.sort()
            col_penalty[j] = values[1] - values[0]

        elif len(values) == 1:
            col_penalty[j] = values[0]


    max_row_penalty = -1
    selected_row = -1

    for i in range(len(row_penalty)):

        if row_penalty[i] is not None:

            if row_penalty[i] > max_row_penalty:
                max_row_penalty = row_penalty[i]
                selected_row = i


    max_col_penalty = -1
    selected_col = -1

    for j in range(len(col_penalty)):

        if col_penalty[j] is not None:

            if col_penalty[j] > max_col_penalty:
                max_col_penalty = col_penalty[j]
                selected_col = j


    if max_row_penalty >= max_col_penalty:

        row = selected_row
        cheapest_col = -1
        cheapest_cost = float("inf")

        for j in range(len(cost[0])):

            if remaining_demand[j] > 0:

                if cost[row][j] < cheapest_cost:
                    cheapest_cost = cost[row][j]
                    cheapest_col = j

        col = cheapest_col

    else:

        col = selected_col
        cheapest_row = -1
        cheapest_cost = float("inf")

        for i in range(len(cost)):

            if remaining_supply[i] > 0:

                if cost[i][col] < cheapest_cost:
                    cheapest_cost = cost[i][col]
                    cheapest_row = i

        row = cheapest_row


    amount = min(remaining_supply[row], remaining_demand[col])

    allocation[row][col] = amount

    remaining_supply[row] -= amount
    remaining_demand[col] -= amount


print("Initial Basic Feasible Solution using VAM:")

for i in range(len(allocation)):
    print(allocation[i])

initial_cost = 0

for i in range(len(cost)):

    for j in range(len(cost[0])):

        initial_cost += allocation[i][j] * cost[i][j]

print("Initial transportation cost:", initial_cost)

choice = int(input("Do you want to apply MODI? (1 for Yes, 0 for No): "))


if choice == 1:

    # ---------------- MODI ----------------

    while True:

        basic = []

        for i in range(len(allocation)):

            for j in range(len(allocation[0])):

                if allocation[i][j] > 0:
                    basic.append((i, j))

        u = [None, None, None]
        v = [None, None, None, None]

        u[0] = 0

        changed = True

        while changed:

            changed = False

            for i, j in basic:

                if u[i] is not None and v[j] is None:

                    v[j] = cost[i][j] - u[i]
                    changed = True

                elif v[j] is not None and u[i] is None:

                    u[i] = cost[i][j] - v[j]
                    changed = True

        dev = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        for i in range(len(cost)):

            for j in range(len(cost[0])):

                if allocation[i][j] == 0:

                    dev[i][j] = cost[i][j] - (u[i] + v[j])

        min_dev = 0
        entering_row = -1
        entering_col = -1

        for i in range(len(cost)):

            for j in range(len(cost[0])):

                if allocation[i][j] == 0:

                    if dev[i][j] < min_dev:

                        min_dev = dev[i][j]
                        entering_row = i
                        entering_col = j

        if min_dev >= 0:
            break

        start = (entering_row, entering_col)

        basic_set = set(basic)

        def find_loop(current, path, move_row):

            i, j = current

            if move_row:

                for col in range(len(cost[0])):

                    if col == j:
                        continue

                    next_cell = (i, col)

                    if next_cell in basic_set or next_cell == start:

                        if next_cell == start and len(path) >= 4:
                            return path + [start]

                        if next_cell not in path:

                            result = find_loop(
                                next_cell,
                                path + [next_cell],
                                False
                            )

                            if result is not None:
                                return result

            else:

                for row in range(len(cost)):

                    if row == i:
                        continue

                    next_cell = (row, j)

                    if next_cell in basic_set or next_cell == start:

                        if next_cell == start and len(path) >= 4:
                            return path + [start]

                        if next_cell not in path:

                            result = find_loop(
                                next_cell,
                                path + [next_cell],
                                True
                            )

                            if result is not None:
                                return result

            return None


        loop = find_loop(start, [start], True)

        if loop is None:
            loop = find_loop(start, [start], False)

        loop = loop[:-1]

        plus_cells = []
        minus_cells = []

        for k in range(len(loop)):

            if k % 2 == 0:
                plus_cells.append(loop[k])

            else:
                minus_cells.append(loop[k])

        theta = float("inf")

        for i, j in minus_cells:

            if allocation[i][j] < theta:
                theta = allocation[i][j]

        for i, j in plus_cells:
            allocation[i][j] += theta

        for i, j in minus_cells:
            allocation[i][j] -= theta

    total_cost = 0

    for i in range(len(cost)):

        for j in range(len(cost[0])):

            total_cost += allocation[i][j] * cost[i][j]


    print()
    print("Optimal allocation using MODI:")

    for i in range(len(allocation)):
        print(allocation[i])

    print("Minimum transportation cost:", total_cost)


else:

    print()
    print("VAM completed. MODI was not applied.")
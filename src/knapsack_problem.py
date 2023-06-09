from pulp import *

# Create the problem instance
problem = LpProblem("Knapsack Problem", LpMaximize)

# Decision variables
items = range(5)  # Number of items
selected = LpVariable.dicts("Selected", items, cat="Binary")

# Objective function: Maximize the total value
problem += lpSum(selected[i] * [8, 12, 6, 14, 10][i] for i in items)

# Constraint: Total weight should not exceed the knapsack capacity
problem += lpSum(selected[i] * [4, 5, 3, 7, 6][i] for i in items) <= 15

# Solve the problem
problem.solve()

# Print the optimal solution
print("Optimal Solution:")
for i in items:
    if selected[i].value() == 1:
        print(f"Item {i + 1} is selected")

# Print the maximum value
print("Maximum Value:", value(problem.objective))
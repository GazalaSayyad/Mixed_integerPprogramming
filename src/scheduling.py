from pulp import *

# Define shift names and their requirements
shifts = ["Shift 1", "Shift 2", "Shift 3", "Shift 4", "Shift 5"]
shift_requirements = [8, 6, 9, 7, 5]  # Number of workers required for each shift

# Define the cost per worker for each shift
shift_costs = [100, 120, 110, 115, 105]  # Cost per worker for each shift

# Create the problem instance
problem = LpProblem("Staffing Problem", LpMinimize)

# Decision variables
workers = LpVariable.dicts("Workers", shifts, lowBound=0, cat="Integer")

# Objective function: Minimize the total labor costs
problem += lpSum(workers[shift] * shift_costs[i] for i, shift in enumerate(shifts))

# Constraints: Ensure sufficient coverage for each shift
for i, shift in enumerate(shifts):
    problem += workers[shift] >= shift_requirements[i]

# Solve the problem
problem.solve()

# Print the optimal solution
print("Optimal Solution:")
for shift in shifts:
    print(f"{shift}: {int(workers[shift].value())} workers")

# Print the minimum cost
print("Minimum Cost:", value(problem.objective))

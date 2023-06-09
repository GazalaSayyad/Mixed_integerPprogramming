from pulp import *

# Define shift names and their requirements
shifts = ["Shift 1", "Shift 2", "Shift 3", "Shift 4", "Shift 5"]
shift_requirements = [8, 6, 9, 7, 5]  # Number of workers required for each shift

# Define the cost per worker for each shift
shift_costs = [100, 120, 110, 115, 105]  # Cost per worker for each shift

# Define the limit on assigning workers to shifts
max_shifts_per_worker = 2

# Define the Dothraki worker availability and cost
dothraki_worker_limit = 10
dothraki_worker_cost = 40

# Define the interpersonal conflicts
interpersonal_conflicts = [(1, 3), (1, 4), (2, 3), (2, 4), (1, 2), (5, 3), (5, 4)]

# Create the problem instance
problem = LpProblem("Staffing Problem", LpMinimize)

# Decision variables
workers = LpVariable.dicts("Workers", (shifts, range(dothraki_worker_limit + 1)), lowBound=0, cat="Integer")
dothraki_workers = LpVariable.dicts("Dothraki_Workers", shifts, lowBound=0, cat="Integer")

# Objective function: Minimize the total labor costs
problem += lpSum(workers[shift][worker] * shift_costs[i] for i, shift in enumerate(shifts) for worker in range(dothraki_worker_limit + 1)) + \
           lpSum(dothraki_workers[shift] * dothraki_worker_cost for shift in shifts)

# Constraints: Ensure sufficient coverage for each shift
for i, shift in enumerate(shifts):
    problem += lpSum(workers[shift][worker] for worker in range(dothraki_worker_limit + 1)) + dothraki_workers[shift] >= shift_requirements[i]

# Constraints: Limit on assigning workers to shifts
for worker in range(dothraki_worker_limit + 1):
    problem += lpSum(workers[shift][worker] for shift in shifts) <= max_shifts_per_worker

# Constraints: Interpersonal conflicts
for conflict in interpersonal_conflicts:
    for shift in shifts:
        problem += workers[shift][conflict[0]] + workers[shift][conflict[1]] <= 1

# Solve the problem
problem.solve()

# Print the optimal solution
print("Optimal Solution:")
for shift in shifts:
    for worker in range(dothraki_worker_limit + 1):
        if workers[shift][worker].value() > 0:
            print(f"{shift}: Worker {worker} - {int(workers[shift][worker].value())} workers")
    if dothraki_workers[shift].value() > 0:
        print(f"{shift}: Dothraki Workers - {int(dothraki_workers[shift].value())} workers")

# Print the minimum cost
print("Minimum Cost:", value(problem.objective))

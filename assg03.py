import sys
import math
import heapq

N = 3

K = 5

assignments = {
    1:  {"cost": 2, "deps": []},
    2:  {"cost": 3, "deps": [1]},
    3:  {"cost": 4, "deps": [1]},
    4:  {"cost": 2, "deps": [2]},
    5:  {"cost": 5, "deps": [2, 3]},
    6:  {"cost": 3, "deps": [3]},
    7:  {"cost": 4, "deps": []},
    8:  {"cost": 1, "deps": [4, 7]},
    9:  {"cost": 2, "deps": [5]},
    10: {"cost": 3, "deps": [6, 8]},
}


ALL = frozenset(assignments.keys())



def llm_type(a):
    return "chatgpt" if a % 2 == 0 else "gemini"


def deps_satisfied(a, completed):
    return all(d in completed for d in assignments[a]["deps"])


def heuristic(completed, P1, P2):
    rem_cg = 0
    rem_gm = 0

    for a in assignments:
        if a not in completed:
            if llm_type(a) == "chatgpt":
                rem_cg += assignments[a]["cost"]
            else:
                rem_gm += assignments[a]["cost"]

    h1 = math.ceil(rem_cg / max(1, P1)) + math.ceil(rem_gm / max(1, P2))
    h2 = len(assignments) - len(completed)
    return max(h1, h2)

def successors(state, P1, P2, case):
    day, completed = state
    succ = []

    available = [
        a for a in assignments
        if a not in completed and deps_satisfied(a, completed)
    ]

    if case == "A":
        max_assignments = N          
    else:
        max_assignments = len(available)

    used = 0
    cg_used = 0
    gm_used = 0

    for a in available:
        if used >= max_assignments:
            break

        cost = assignments[a]["cost"]

        if cost > K:
            continue

        if llm_type(a) == "chatgpt":
            if cg_used + cost <= P1:
                cg_used += cost
                used += 1
                succ.append((day + 1, completed | {a}))
        else:
            if gm_used + cost <= P2:
                gm_used += cost
                used += 1
                succ.append((day + 1, completed | {a}))

    return succ




def dfs(P1, P2, case):
    stack = [(1, frozenset())]
    visited = set()
    nodes = 0
    best = float("inf")

    while stack:
        day, completed = stack.pop()
        nodes += 1

        if day >= best:
            continue

        if completed == ALL:
            best = min(best, day - 1)
            continue

        if (day, completed) in visited:
            continue
        visited.add((day, completed))

        for s in successors((day, completed), P1, P2, case):
            stack.append(s)

    return best, nodes

def dfbb(P1, P2, case):
    best = float("inf")
    nodes = 0

    def dfs_bb(day, completed):
        nonlocal best, nodes
        nodes += 1

        if day + heuristic(completed, P1, P2) >= best:
            return

        if completed == ALL:
            best = min(best, day - 1)
            return

        for s in successors((day, completed), P1, P2, case):
            dfs_bb(*s)

    dfs_bb(1, frozenset())
    return best, nodes

def astar(P1, P2, case):
    pq = []
    heapq.heappush(pq, (0, 1, frozenset()))
    visited = set()
    nodes = 0

    while pq:
        f, day, completed = heapq.heappop(pq)
        nodes += 1

        if completed == ALL:
            return day - 1, nodes

        if (day, completed) in visited:
            continue
        visited.add((day, completed))

        for nd, nc in successors((day, completed), P1, P2, case):
            g = nd
            h = heuristic(nc, P1, P2)
            heapq.heappush(pq, (g + h, nd, nc))

    return float("inf"), nodes

def best_subscription(m, c1, c2, case):
    best_cost = float("inf")
    best_pair = None

    for P1 in range(1, N * K + 1):
        for P2 in range(1, N * K + 1):
            days, _ = astar(P1, P2, case)
            if days <= m:
                cost = P1 * c1 + P2 * c2
                if cost < best_cost:
                    best_cost = cost
                    best_pair = (P1, P2)

    return best_pair, best_cost

if len(sys.argv) < 5:
    print("Usage:")
    print("python assg03.py <c1> <c2> <m> <A|B>")
    sys.exit(1)

c1 = int(sys.argv[1])  
c2 = int(sys.argv[2])   
m = int(sys.argv[3])    
case = sys.argv[4]      

P1 = N * K
P2 = N * K

print("\n========= CASE", case, "=========\n")
print("Students (N):", N)
print("Per-student prompt limit (K):", K)

print("\nDFS:")
d, n = dfs(P1, P2, case)
print("Days:", d, "Nodes:", n)

print("\nDFBB:")
d, n = dfbb(P1, P2, case)
print("Days:", d, "Nodes:", n)

print("\nA*:")
d, n = astar(P1, P2, case)
print("Days:", d, "Nodes:", n)

print("\nBest Subscription for m =", m)
sub, cost = best_subscription(m, c1, c2, case)
if sub:
    print("ChatGPT prompts/day:", sub[0])
    print("Gemini prompts/day:", sub[1])
    print("Daily cost:", cost)
else:
    print("No feasible subscription")

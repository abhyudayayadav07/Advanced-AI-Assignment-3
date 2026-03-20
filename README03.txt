Guide on How to compile the 'assg03.py' program on your system.

Step 1 :  Open the file 'assg03.py' on your VS Code.

Step 2 :  On the panel, go to the terminal and type ' python assg03.py <c1> <c2> <m> ', where Cost per ChatGPT prompt (c1), Cost per Gemini prompt (c2), Number of days (m), Case type (A or B).

Step 3 : You will see output as follows (sample output) :

Sample Output : 

YES: All assignments can be completed in 4 days

DFS:
Days required: 4
Nodes expanded: 412

DFBB:
Days required: 4
Nodes expanded: 86

A*:
Days required: 4
Nodes expanded: 23


Given:

Number of students (N)

Prompt limit per student (K)

Assignment dependencies

The program found at least one valid schedule that:

Respects all dependencies

Respects prompt limits

Completes all assignments in ≤ 4 days

---------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------

After confirming feasibility, the program runs three different search algorithms to find the schedule:

DFS (Depth First Search)

DFBB (Depth First Branch and Bound)

A* (A-star)

Each algorithm explores the state space differently.

---------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------

What DFS does

DFS goes deep first into one possible schedule

It explores many wrong or inefficient schedules

It does not use any heuristic


Interpretation

DFS found a valid schedule in 4 days

To find it, DFS explored 412 different states

A state = partial schedule (which assignments done, which day, remaining prompts, etc.)



Why 412 is large

DFS tries many useless combinations

No pruning

Exponential branching due to:

Multiple students

Multiple assignments per day

Dependency constraints


--------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------

What DFBB does

DFS + Branch and Bound

Uses an upper bound on best solution

Prunes branches that cannot improve the current best



Interpretation

Still finds the optimal 4-day solution

Explores only 86 states



Why much smaller than DFS

Once DFBB finds a 4-day solution:

Any branch that cannot finish in ≤ 4 days is discarded

Huge parts of the search tree are skipped

This shows intelligent pruning


----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------

What A* does

1.Uses a heuristic function

2.Always expands the most promising state first

Typical heuristic:

h(n) = ceil(remaining_prompts / total_daily_capacity)


Interpretation

A* also finds the optimal 4-day schedule


Why A* is best

It avoids bad paths early

Guided search instead of blind search

Near-optimal path is explored first
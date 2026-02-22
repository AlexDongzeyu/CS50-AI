# **CS50 AI Crossword Project**
# **1. Planning**

**1.1 Key Terms Definitions**

The following key terms are defined to fully understand the concepts and mathematical variables discussed in this document:

- **Constraint Satisfaction Problem (CSP):** A problem defined by a set of variables, a domain of possible values for each variable, and a set of constraints. The goal is to find an assignment of values to all variables that satisfies every constraint at the same time.

- **Node Consistency (Unary Constraint):** The state at which every value in a variable's domain satisfies the variable's unary constraint. In this project, a word's length must exactly equal the variable's length in the crossword grid.

- **Arc Consistency (Binary Constraint):** The state at which every value in a variable's domain satisfies its binary constraints with every neighboring variable. For intersecting crossword variables, the character at $X$'s overlap index must equal the character at $Y$'s overlap index.

- **AC-3 Algorithm:** An inference algorithm that enforces arc consistency across the entire CSP. It maintains a queue of arcs (pairs of variables) and removes values from domains that violate binary constraints until no further changes can be made.

- **Backtracking Search:** A recursive search algorithm that builds an assignment one variable at a time. If the algorithm reaches a point where no valid value can be assigned to a variable without violating a constraint, it goes back to the previous decision and tries a different value.

- **Heuristics:** Rules of thumb used to guide the search toward a solution faster by deciding which variable to assign next and which value to try first. This project uses three: Minimum Remaining Values (MRV), Degree Heuristic, and Least Constraining Value (LCV).

- **Minimum Remaining Values (MRV):** A variable-ordering heuristic that selects the unassigned variable with the fewest remaining values in its domain. The idea is that by targeting the most constrained variable first, we detect failures as early as possible and avoid unnecessary backtracking later.

- **Degree Heuristic:** A tiebreaker used when two variables share the same MRV count. It selects the variable with the highest degree, meaning it is involved in the most constraints with other unassigned variables. By choosing this variable, a single assignment constrains multiple other variables at once.

- **Least Constraining Value (LCV):** A value-ordering heuristic that selects the word that eliminates the fewest options from neighboring variables' domains. This keeps as many choices open as possible for future assignments.

**1.2 Concept & Rules (How Crossword Generation Works)**

Before defining the goal, it is important to understand the rules of the crossword generation algorithm. Crossword generation determines the placement of words based on a strict set of structural constraints.

- **Rule 1:** Each contiguous sequence of blank cells in the grid defines a variable. Every variable has a fixed length and direction (across or down) determined by the structure file.

- **Rule 2:** The initial domain for every variable is the complete vocabulary list provided in the words file. Any word whose length does not match the variable's length is immediately removed, enforcing node consistency before the search begins.

- **Rule 3:** If variable $X$ and variable $Y$ share an intersecting cell, the character at $X$'s overlap index must equal the character at $Y$'s overlap index. Any word that violates this for any value in the neighboring domain is removed from the domain, enforcing arc consistency.

- **Rule 4:** All assigned words must be unique across the entire board. The algorithm cannot reuse a word already placed in a different variable, even if it satisfies all other constraints.

**1.3 Goal:**

Engineer a knowledge-based AI agent capable of determining the optimal word assignments for all empty variables within a crossword structure. The solution will implement two distinct methodologies: simplifying the domain via Inference (AC-3 Algorithm) and determining exact assignments via Search (Recursive Backtracking with Heuristics).

**1.4 Success Criteria**

To evaluate the effectiveness and accuracy of the algorithm, the following success criteria must be met:

- The model must return a complete assignment dictionary where every variable is paired with a unique, valid word. It must accurately handle intersecting variables, treating them as binary constraints to prevent character conflicts at shared cells.
- The `ac3` function must yield domains that are fully arc-consistent before the search begins, significantly reducing the number of possibilities the backtracking algorithm needs to explore.
- The `backtrack` function must correctly solve complex grid structures using recursion. The recursion must terminate and return a complete solution when every variable in the CSP has been assigned a value.
- The implementation must utilize reusable heuristic functions (MRV, Degree, and LCV) to enforce consistent and optimal decision-making throughout the search.

**1.5 Project Requirements**

The technical boundaries and expected inputs/outputs for this project are outlined below:

- **Input:** Two text files — a structure file (defining the grid layout using `#` for blocked cells and `_` for open cells) and a words file (defining the full vocabulary domain, one word per line).
- **Processing:** Parsing structural overlaps to identify intersections, building an arc queue for consistency enforcement, pruning domains via AC-3, and executing a recursive depth-first search guided by MRV, Degree, and LCV heuristics.
- **Output:** A formatted console printout of the solved crossword grid and an optional exported `.png` image of the completed puzzle.

# **2. Analysis**

**2.1 Tools and Resources**

The following software tools and libraries were utilized to develop, test, and document this project, each serving a specific necessary function:

- **Python 3.12 via VS Code**: The primary programming language and integrated development environment (IDE) used to write and execute the algorithmic logic.
- **Libraries**
    - **copy**: Specifically `copy.deepcopy()`, used to create a separate copy of the domains so that words can be removed during iteration without causing a runtime error.
    - **collections.deque**: Used to maintain the queue for the AC-3 algorithm, allowing arcs to be added from the right and removed from the left efficiently.
    - **PIL (Pillow)**: Used to generate the graphical output of the completed crossword assignment.
- **Git/GitHub**: Used for version control.
- **draw.io**: Used to construct the algorithm flowchart.

**2.2 Development Timeline**

The development of this project followed a structured timeline:

1. **Initialization:** Setup Git repo and analyze the `Crossword` and `Variable` classes.
2. **Logic for node consistency:** Implement `enforce_node_consistency` to remove words of incorrect lengths.
3. **Logic for arc consistency:** Implement `revise` and `ac3` to remove words that violate the character overlap rules.
4. **Validation:** Implement `assignment_complete` and `consistent` to check that all variables are assigned and all constraints are satisfied.
5. **Optimization:** Implement `order_domain_values` (LCV) and `select_unassigned_variable` (MRV and Degree heuristics).
6. **Search Integration:** Implement `backtrack` using the recursive search tree.
7. **Verification:** Run model checks on all structures and document results.

**2.3 Troubleshooting Techniques**

The following troubleshooting techniques are applied when unexpected results occur:

- If a `RuntimeError` occurs (dictionary changed size during iteration), we must verify that a deep copy of the domain is being looped over while the original domain is being modified.
- If the AC-3 algorithm runs endlessly, we should check if neighbor arcs are only added back to the queue when `revise()` returns `True`.
- If the output contains duplicate words, we must verify that the `consistent()` function checks `len(assignment.values()) == len(set(assignment.values()))`.

**2.4 General Logic Analysis**

Translating the crossword structure into logic, we need to analyze the relationship between Unary Constraints, Binary Constraints, and Heuristics. After analysis, we can derive the constraint formula below:

For any overlapping variables $X$ and $Y$ with intersection indices $i$ and $j$:

$$Constraint(X, Y) = \{ (x, y) \in D_X \times D_Y \mid x[i] = y[j] \}$$

To enforce this formula, we analyze the algorithm's behavior through two mutually exclusive search states.
 1. The Inference term (`ac3`) accounts for the elimination of words that cannot satisfy the overlap constraint. Since $x[i]$ must equal $y[j]$, any word $x$ that has no valid counterpart $y$ in domain $D_Y$ is removed entirely from domain $D_X$.
 2. The Heuristic term (MRV and LCV) accounts for the order in which variables and values are explored in the search tree. By selecting the variable with the fewest remaining values first, the algorithm detects dead ends sooner and avoids unnecessary backtracking.

This table below shows how the algorithm's behavior divides into two distinct states:
| Independent Variable (Behavior) | Logic State | Algorithmic Tool | Resulting Action |
|:---:|:---:|:---:|:---:|
| Node Consistency | Check word length | `len(word) == var.length` | Removes words of incorrect length |
| Arc Consistency | Check overlap characters | `x_word[i] == y_word[j]` | Removes words with no valid counterpart |
| Backtrack Search | Explore valid assignments | `select_unassigned_variable()` | Recursively builds the board |

**2.5 Structure 0 Analysis (Standard Case)**

**Structure:** A small grid where two variables intersect exactly once.

We know that Variable 1 (Across) and Variable 2 (Down) overlap at one shared cell. Since Variable 1 is assigned first, the character at its overlap index directly restricts what words are valid for Variable 2. If Variable 1 is assigned "FIVE", then Variable 2 must contain the letter "I" at its overlap index. Therefore, we expect AC-3 alone to fully narrow the domains in this structure.

| Variable | Intersects With... | Expected Action | Logic |
|:---:|:---:|:---:|:---:|
| V1 (Across, Len 4) | V2 | Restricts V2 Domain | Forces V2 to match character at overlap |
| V2 (Down, Len 5) | V1 | Restricts V1 Domain | Forces V1 to match character at overlap |

**2.6 Structure 1 Analysis (Heuristic Optimization)**

**Structure:** A medium grid with multiple intersections and varying variable lengths.

This structure represents a search space with many potential word combinations. We observe that central hub variables intersect with 3 or 4 other variables, while edge variables only intersect with 1. Because the central hub restricts the most other variables at once, the Degree Heuristic should select it first to collapse the search space as quickly as possible.

| Variable Type | Intersections | Selection Priority | Logic |
|:---:|:---:|:---:|:---:|
| Hub Node | 4 | Highest (Degree Heuristic) | Restricts the most variables at once |
| Standard Node | 2 | Moderate | Evaluated mid-search |
| Edge Node | 1 | Lowest | Least constrained, filled last |

**2.7 Structure 2 Analysis (Deep Recursion Case)**

**Structure:** A large grid where AC-3 alone cannot fully solve the board.

In a standard inference pass, AC-3 will reduce several domains down to 2 or 3 remaining words but cannot narrow them further. To resolve this, we apply backtracking recursion. If an assignment leads to a contradiction, the algorithm returns `None`, removes the assignment, and tries the next word in the domain.

| Case | Tree State | Standard Logic | Corrected Logic (Backtrack) | Verification |
|:---:|:---:|:---:|:---:|:---:|
| 1 | Valid Assignment | Proceeds deeper | Adds to dict, calls `backtrack()` | Valid |
| 2 | Invalid Assignment | Fails completely | Returns `None`, removes key, tries next | Valid |

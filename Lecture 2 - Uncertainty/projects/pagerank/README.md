# **CS50 AI PageRank Project**
# **1. Planning**

**1.1 Key Terms Definitions**
- **Random Surfer Model (model):** A stochastic model simulating the behavior of an internet surfer who randomly clicks on links. It assumes that if a user is on a page with many links, they are equally likely to click any of them (if a page has L links, the probability of the surfer clicking any specific link is $1/L$).

- **Markov Chain:** A mathematical model that undergoes transitions from one state (web page) to another according to certain probabilistic rules. The next state depends only on the current state (state attained in the previous event).

- **Damping Factor ($d$):** A probability factor (typically 0.85) representing the likelihood that a user continues clicking links. On the other hand, probability $1-d$ (0.15) represents the likelihood that the user "teleports" to a completely random page in the corpus.

- **Convergence:** The state at which the calculated PageRank values stabilize, changing by no more than a specified threshold (0.001) between iterations.

- **Sink Node (Dead End):** A web page that has no outgoing links (a "Dead End").

**1.2 Goal:**

Engineer a knowledge-based AI agent capable of determining the importance (PageRank) of web pages within a corpus. The solution will implement two distinct methodologies: approximating rank via Sampling (Markov Chain) and calculating exact rank via Iteration (Recursive Formula).

**1.3 Success Criteria**
- The model must return a probability distribution that always sums to 1. It must accurately handle "Sink Nodes" (pages with no outgoing links), treating them as linking to all pages to prevent probability loss.
- The sample pagerank function must yield results statistically consistent within approximately 0.05 margin with the iterative approach.
- The iterate pagerank function must correctly handle Corpus 2 using recursion and dead ends. The iteration loop must achieve convergence (terminate) when the maximum change in any page rank is $< 0.001$.
- The implementation should utilize a reusable function to enfore the damping factor rules consistently.

**1.4 Project Requirements**
- **Input:** A directory (corpus) containing HTML files.
- **Processing:** Parsing HTML structure, building an adjacency dictionary, and then calculating probabilities.
- **Output:** A sorted console printout of pages and their calculated PageRank values (e.g., 1.html: 0.2202).

# **2. Analysis**

**2.1 Tools and Resources**
- **Python via VS Code**: Main programming language.
- **Libraries**
    - os, sys, re: For corpus parsing the HTML corpus structure.
    - random: For weighted sampling in the Markov Chain
- **Git/Github**: Version control.
- **draw.io**: Constructing flowcharts.

**2.2 Development Timeline**
1. **Initialization:** Setup Git repo and analyze the crawl() function.
2. **Logic for probability:** Implement transition_model function to return a dictionary of probabilities summing to 1.
3. **Sampling pagerank:** Implement sample_pagerank using weighted random selection (random.choices).
4. **Iterate pagerank** Implement iterate_pagerank using the recursive formula.
5. **Refinement:** Handle the Sink Node edge case in Corpus 2.
6. **Verification:** Run model checks on all corpora and document results.

**2.3 Troubleshooting Techniques**
- If PageRank values do not sum to 1, we must verify that the teleportation probability $\frac{1-d}{N}$ is added to every page.
- If the iterative algorithm runs endlessly, we should check if abs() is being used when calculating the difference between old and new ranks.
- If Corpus 2 results are unexpectedly low (e.g., 0.05), we must verify that the Sink Nodes are explicitly handled in the loop.

**2.4 General Logic Analysis**

Translating the web structure into logic, we need to analyze the relationship between the Damping Factor, the Links, and the Probability. After analysis, we can derive the formula below:

$$
PR(p) = \frac{1 - d}{N} + d \sum_{i} \frac{PR(i)}{NumLinks(i)}
$$

To derive this formula, we analyze the probability of a random surfer arriving at page p through two mutually exclusive events.
 1. The Teleportation term ($\frac{1-d}{N}$) accounts for the $1-d$ (15%) probability that a user types a random URL directly. Since they can choose any of the N pages in the corpus with equal likelihood, the probability for landing on page p via teleportation is $\frac{1}{N}$. 
 2. The Surfing term ($d \sum \dots$) accounts for the $d$ (85%)probability that a user follows a link. For a user to arrive at page $p$ by clicking, they must currently be on a page $i$ that links to $p$. The probability they are on page $i$ is $PR(i)$. The probability they choose the specific link to $p$ is $\frac{1}{NumLinks(i)}$. We sum this probability for all pages $i$ that link to $p$.

This table below shows how the user's behavior into two distinct states:
| Behavior | Detailed Action | Formula Term | Probability |
|:---:|:---:|:---:|:---:|
| Teleport | User types a random URL | $\frac{1-d}{N}$ | 0.15 / Total Pages |
| Surf | User clicks a specific link | $d \times \frac{PR(i)}{NumLinks(i)}$ | 0.85 / Link Count |

**2.5 Corpus 0 Analysis (Standard Case)**

**Structure:** A small network where every page has at least one link. 

We know that page 2 is linked to by page 1 and page 3. Since page 1 and 3 are also linked to each other, they feed probability into page 2. Page 4 is only linked to by page 2. Therefore, we expect Page 2 to have the highest rank.

| Page | Links To... | Expected Rank | Logic |
|:---:|:---:|:---:|:---:|
| 1.html | 2 | Moderate | Receives link from 2 |
| 2.html | 1, 3 | Highest | Receives links from 1 and 3 |
| 3.html| 2, 4 | Moderate | Receives link from 2 |
| 4.html | 2 | Lowest | Only receives link from 3 |

**2.6 Corpus 1 Analysis**

**Structure:** bfs to dfs to search to bfs.

This corpus represents a recursion with probabilities flows in a loop. We observe that games, minesweeper, and tictactoe are the leaf nodes being fed by search. However, search itself is fed by dfs, which is fed by bfs. Because search is the hub that feeds the leaf nodes and recycles probability back to bfs, it should hold significant weight.


| Page | Links To... | Logic | Conclusion |
|:---:|:---:|:---:|:---:|
| bfs.html | dfs | Feeds Loop | Valid |
| dfs.html | minimax, search | Feeds Loop | Valid |
| search.html | bfs, games, etc. | Hub Node | High Rank |
| games.html | None | Leaf Node | Moderate |

**2.7 Corpus 2 Analysis (Sink Node Edge Case)**

**Structure:** recursion.html has no outgoing links.
In a standard formula, NumLinks(i) would be 0, leading to a loss of probability (division by zero and logic skip). To fix this, we can apply the rule that if len(links) == 0, treat as len(links) == N.


| Case | Page Type | Standard Logic Result | Corrected Logic Result | Conclusion |
|:---:|:---:|:---:|:---:|:---:|
| 1 | Standard Page | Sums incoming weights | Sums incoming weights | Valid |
| 2 | Sink Node | Probability Leaks (0.05) | Redistributes Weight (about 0.33) | Valid |


# **3. Design**

1. The model parses the HTML directory into a dictionary of sets.
2. The transition_model function calculates the probability distribution for the next state, ensuring that the sink nodes return a uniform distribution.
3. The sample_pagerank function iterates N times, tracking visit counts to approximate the rank.
4. The iterate_pagerank function applies the recursive formula, treating sink nodes as linking to all pages, until the delta is < 0.001.

The flowchart below include more details about the design segament:
![Local Image](./PageRank_Flowchart.png)


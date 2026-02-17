# **CS50 AI PageRank Project**
# **1. Planning**

**1.1 Key Terms Definitions**
- **Random Surfer Model:** A stochastic model simulating the behavior of an internet user who clicks on links at random. It assumes that if a user is on a page with many links, they are equally likely to click any of them.

- **Markov Chain:** A mathematical system that undergoes transitions from one state (web page) to another according to certain probabilistic rules. The next state depends only on the current state.

- **Damping Factor ($d$):** A probability factor (typically 0.85) representing the likelihood that a user continues clicking links. With probability $1-d$, the user "teleports" to a completely random page in the corpus.

- **Convergence:** The point at which the calculated PageRank values stabilize, changing by no more than a specified threshold (0.001) between iterations.

- **Sink Node (Dead End):** A webpage that has no outgoing links to other pages.

**1.2 Goal:**

Engineer an AI algorithm capable of determining the importance (PageRank) of web pages within a corpus using Python. The solution implements two different approaches of sampling: approximating rank by simulating a random surfer visiting 10,000 pages (Markov Chain); and iteration: calculating exact rank using a recursive mathematical formula until its numerial convergence.

**1.3 Success Criteria**
- The model must return a probability distribution that always sums to 1, regardless of whether the page has links or is a sink node.
- The sample pagerank function that uses $N=10,000$ must yield results within approximately 0.05 of the iterative approach.
- The iterate pagerank function must correctly handle Corpus 2 using recursion and dead ends. It must not output $\approx 0.05$ for recursion.html, which is a known failure mode; it must yield the correct probability of approximately 0.33.
- The iteration loop must terminate when the maximum change in any page rank is $< 0.001$.

**1.4 Project Requirements**
- **Input:** A directory (corpus) containing HTML files.
- **Processing:** Parsing HTML structure, building an adjacency dictionary, and then calculating probabilities.
- **Output:** A sorted list of pages and their calculated PageRank values (e.g., 1.html: 0.2202).


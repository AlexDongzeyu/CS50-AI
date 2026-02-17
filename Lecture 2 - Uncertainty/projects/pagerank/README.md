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

# **2. Analysis**

**2.1 Tools and Resources**
- **Python via VS Code**: Main programming language.
- **Harvard logic.py library**: Provides dunctions such as And, Or, Not, and model_check.
- **Git/Github**: Version control.
- **draw.io**: Making flowcharts.

**2.2 Development Timeline**
1. **Initialization:** Setup Git repo and analyze the logic.py.
2. **Abstraction:** Create a function to handle the "XOR" game rule (One can be either Knight or Knave).
3. **Puzzles 0 & 1:** Implement direct Biconditional statements.
4. **Puzzle 2:** Implement "Same vs Different" logic using logic gates.
5. **Puzzle 3:** Implement nested Biconditionals for "He said that..." statements.
6. **Verification:** Run model_check and document results.

**2.3 Troubleshooting Techniques**
- If the output is empty, it means the KB contains a contradiction (e.g., asserting A and Not A). We should comment out individual sentences to isolate the conflicting rule.
- If the output lists a character as both Knight and Knave, the game rules are missing. We should verify validate_game_logic is being called.
- If Puzzle 3 loops infinitely, check parenthesis balance in nested Biconditionals.

**2.4 General Logic Analysis**

Translating English into logic, we need to analyze the relationship between a speakek, their statement, and the reality. The chart below shows the two valid states of the model.

| Character (C) | Type | Always tells truth? | Statement (S) Truth | Formula|
|:---:|:---:|:---:|:---:|:---:|
| Knight | True | Yes | True | $C \land S$ |
| Knave | False | No | False | $\neg C \land \neg S$ |

In both valid states, C and S share the same truth value, allowing us to use a biconditional operator: $$C \iff S$$ This is becasue a character is a Knight if and only if their statement is true.

**2.5 Puzzle 0 Analysis**

**Statement:** A says "I am both a Knight and a Knave."

We know that a Knight cannot lie, and a Knave cannot tell the truth. Since "Knight AND Knave" is logically impossible (False), if A were a Knight, he would be telling a lie (Impossible as Knight cannot lie). Therefore, A must be a Knave. The following table is the truth table of this puzzle.

| Case | A is... | Statement Truth Value | Logic Check | Conclusion |
|:---:|:---:|:---:|:---:|:---:|
| 1 | Knight (True) | True AND False = False | Contradiction (Knight said False) | Impossible |
| 2 | Knave (False) | True AND False = False | Consistent (Knave said False) | Valid |

**2.6 Puzzle 1 Analysis**

**Statement:** A says "We are both Knaves."

If A is a Knight, he is telling the truth, so he is a Knave which contradicts. Thus, A must be a Knave. Since A is a Knave, his statement "We are both Knaves" must be False. For "A and B are Knaves" to be False (when we already know A is a Knave), B must be a Knight. The following table is the truth table of this puzzle.

| Case | A | B | Statement Truth Value | Logic Check | Conclusion |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Knight | Knight | False | Contradiction (Knight said False) | Impossible |
| 2 | Knight | Knave | False | Contradiction (Knight said False) | Impossible|
| 3 | Knave | Knight | False | Consistent (Knave said False) | Valid |
| 4 | Knave | Knave | True | Contradiction (Knave said True) | Impossible |

**2.7 Puzzle 2 Analysis**

**Statement A:** "Same kind" $A \iff (A \land B) \lor (\neg A \land \neg B)$

**Statement B:** "Different kinds" $B \iff (A \land \neg B) \lor (\neg A \land B)$

A and B claim opposite things. Therefore, one must be telling the truth and one must be lying. If one lies and one truths, they are of "Different Kinds". This makes B's statement ("Different kinds") True. Since B told the truth, B is a Knight. Since they are different, A is a Knave. The following table is the truth table of this puzzle.

| Case | A | B | A's Statment | B's Statement | Logic Check | Conclusion |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Knight | Knight | True | False | B is Knight but said False | Impossible |
| 2 | Knight | Knave | False | True | A is Knight but said False | Impossible |
| 3 | Knave | Knight | False | True | A is Knave and said False; B is Knight and said True | Valid |
| 4 | Knave | Knave | True | False | A is Knave but said True | Impossible |

**2.8 Puzzle 3 Analysis**

**Statement:** B says "A said 'I am a knave'."

We first check the inner statement asking ourselves Can A say "I am a Knave"? If A is a Knight he speaks the truth meaning he is a knave which contradicts. If A is a Knave, he speaks a lie meaning that he is a knight which contradicts. Therefore, A can never say "I am a Knave." Since A could not have said that, B is lying about what A said. Therefore, B is a Knave. Since B is a Knave, his statement "C is a Knave" is False. Therefore, C is a Knight. Since C is a Knight, his statement "A is a Knight" is True. Therefore A is a Knight. The following table is the truth table of this puzzle.

| Character | Is Knight? | Statement | Is Statement True? | Conclusion |
|:---:|:---:|:---:|:---:|:---:|
| A | Knight | "I am Knight" | True | Valid |
| B | Knave | "A said 'I am Knave'" | False | Valid (Lied about A) |
| C | Knave | "A is Knight" | True | Valid |

# **3. Design**

1. The agent instantiates the symbols for each character.
2. For better scalability, we use a generator function called validate_game_logic to apply the game rule (the exclusive OR) to all characters.
3. The English clues are parsed into biconditionals. Direct statements become $speaker \iff statement$, meta-statements (statements about statements) become nested biconditionals $speaker \iff (target \iff statement)$.
4. The model_check function will iterate through every possibilities in the truth table. If a symbol is true in every scenarios where the Knowledge Base is true, it is output as a confirmed identity.

The flowchart below include more details about the design segament:
![Local Image](./design_flowchart.png)

# **4. Testing**
| Test Case | Description | Expected Outcome | Pass/Fail |
|:---:|:---:|:---:|:---:|
| 1 | Run Puzzle 0 | A is a Knave | Pass |
| 2 | Run Puzzle 1 | A is a Knave, B is a Knight | Pass |
| 3 | Run Puzzle 2 | A is a Knave, B is a Knight | Pass | 
| 4 | Run puzzle 3 | A is a Knight, B is a Knave, C is a Knight | Pass |
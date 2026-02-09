# **CS50 AI Knights and Knaves Project**
# **1. Planning**

**1.1 Key Terms Definitions**
- **Knowledge-Based Agent:** A system that reasons based on the internally given knowledge (sentences) to derive new information.

- **Knowledge Base (KB):** A set of sentences known to be true by the agent. In this project, the KB consists of the "Game Rules" (One can be either Knight or Knave) and the given "Puzzle Clues."

- **Entailment ($KB \vDash \alpha$):** The relationship where, if the Knowledge Base is true, then the conclusion ($\alpha$) must also be true.

- **Model Checking:** The algorithm that is being used to enumerate all possibilities (truth tables) to verify entailment.

- **Biconditional ($\iff$):** A logical connective indicating that two statements have the exact same truth value (True/True or False/False).

**1.2 Goal:**

Engineer a knowledge-based agent that is capable of solving the logical  based on the Raymond Smullyan "Knights and Knaves" puzzles. The agent would be reason using the propositional logic to infer the state of various characters (Knight/Truth-teller or Knave/Liar) based on limited initial sentences as constrained clues.

**1.3 Success Criteria**
- The agent must accurately and strictly adhere to the laws of identity without any contradictions (e.g., One cannot be both Knight and Knave).
- The agent must yield exactly one valid model per symbol for puzzles 0, 1, 2, and 3.
-  The implementation should utilize some reusable functions to enfore the given rules and logic gates (e.g. XOR). This avoids redundancy. 
- The agent should successfully check that $KB \vDash \alpha$ based on the given cases in all puzzles.
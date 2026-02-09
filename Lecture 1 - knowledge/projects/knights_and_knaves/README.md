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

**1.4 Project Requirements**
- **Input:** Implicit rules derived from 4 specific logic puzzles.
- **Processing:** Converting English statements into logical connectives (And, Or, Not, Biconditional) via the logic.py library.
- **Output:** Console printout of the definitive status (Knight or Knave) of every character involved.

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

In both valid states, C and S share the same truth value, allowing us to use a biconditional operator: $$ C \iff S$$ This is becasue a character is a Knight if and only if their statement is true.

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

**Statement A:** "Same kind" ($A \iff (A \land B) \lor (\neg A \land \neg B)$)

**Statement B:** "Different kinds" ($B \iff (A \land \neg B) \lor (\neg A \land B)$)

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
3. The English clues are parsed into biconditionals. Direct statements become $ speaker \iff statement$, meta-statements (statements about statements) become nested biconditionals $ speaker \iff (target \iff statement)$.
4. The model_check function will iterate through every possibilities in the truth table. If a symbol is true in every scenarios where the Knowledge Base is true, it is output as a confirmed identity.

The flowchart below include more details about the design segament:
![Local Image](design_flowchart.png)

# **4. Testing**
| Test Case | Description | Expected Outcome | Pass/Fail |
|:---:|:---:|:---:|:---:|
| 1 | Run Puzzle 0 (A says "I am both"). | Agent identifies A as a Knave. | True | Valid |
| 2 | Run Puzzle 2 ("Same kind" vs "Different"). | Agent identifies A as Knave, B as Knight. | False | Valid (Lied about A) |
| 3 | Run Puzzle 3 (B claims A said "I am a Knave"). | "A is Knight" | True | Valid |
| 4 | Run all puzzles sequentially. | "A is Knight" | True | Valid |
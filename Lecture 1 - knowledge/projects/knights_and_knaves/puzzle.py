from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

def validate_game_logic(characters):
    """
    Generates fundamental game knowledge base
    Enforces Exclusive OR; A character must be a knight OR a knave, but never both.
    Logic: Knight <-> Not Knave
    """
    knowledge = []
    for knight, knave in characters:
        knowledge.append(Biconditional(knight, Not(knave)))
    return knowledge

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
     # Game Rules
    *validate_game_logic([(AKnight, AKnave)]),

    # Clue: A says A is Knight AND A is Knave
    # If A is knight, statement is True. If A is knave, statement is False.
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Game Rules
    *validate_game_logic([(AKnight, AKnave), (BKnight, BKnave)]),

    # Clue: A says A is knave AND B is knave
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Game Rules
    *validate_game_logic([(AKnight, AKnave), (BKnight, BKnave)]),

    # Clue 1: A says "Same kind." Both knight OR both knave
    Biconditional(AKnight, Or(
        And(AKnight, BKnight),
        And(AKnave, BKnave)
    )),

    # Clue 2: B says "Different kinds." One knight AND one knave
    #XOR logic
    Biconditional(BKnight, Or(
        And(AKnight, BKnave),
        And(AKnave, BKnight)
    ))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Game Rules
    *validate_game_logic([(AKnight, AKnave), (BKnight, BKnave), (CKnight, CKnave)]),

    # Clue 1: A says "I am a Knight" OR "I am a Knave"
    # We represent the existence of the speech act itself
    Or(
        Biconditional(AKnight, AKnight), # Logic if A said "I am Knight"
        Biconditional(AKnight, AKnave)   # Logic if A said "I am Knave"
    ),

    # Clue 2: B says "A said 'I am a knave'."
    # B asserts that the event A said "I am a knave" is true.
    # As defined above, A said "I am a knave" == Biconditional(AKnight, AKnave)
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),

    # Clue 3: B says "C is a knave."
    Biconditional(BKnight, CKnave),

    # Clue 4: C says "A is a knight."
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

IN_FILE = "02/input.txt"


def score_game(move):
    score = 0
    if move[1] == "X":  # rock
        if move[0] == "A":  # rock
            score += 3
        elif move[0] == "B":  # paper
            score += 0
        elif move[0] == "C":  # scissors
            score += 6
        score += 1
    elif move[1] == "Y":  # paper
        if move[0] == "A":  # rock
            score += 6
        elif move[0] == "B":  # paper
            score += 3
        elif move[0] == "C":  # scissors
            score += 0
        score += 2
    elif move[1] == "Z":  # scisors
        if move[0] == "A":  # rock
            score += 0
        elif move[0] == "B":  # paper
            score += 6
        elif move[0] == "C":  # scissors
            score += 3
        score += 3
    return score


if __name__ == "__main__":
    total_score = 0
    with open(IN_FILE) as f:
        for turn in f:
            moves = turn.split()
            total_score += score_game(moves)

    print(total_score)

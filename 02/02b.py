IN_FILE = "02/input.txt"


def score_game(move):
    score = 0
    if move[1] == "X":  # lose
        if move[0] == "A":  # rock
            score += 3  # so play scissors
        elif move[0] == "B":  # paper
            score += 1  # so play rock
        elif move[0] == "C":  # scissors
            score += 2  # so play paper
        score += 0
    elif move[1] == "Y":  # draw
        if move[0] == "A":  # rock
            score += 1  # so play rock
        elif move[0] == "B":  # paper
            score += 2  # so play paper
        elif move[0] == "C":  # scissors
            score += 3  # so play scissors
        score += 3
    elif move[1] == "Z":  # win
        if move[0] == "A":  # rock
            score += 2  # so play paper
        elif move[0] == "B":  # paper
            score += 3  # so play scissors
        elif move[0] == "C":  # scissors
            score += 1  # so play rock
        score += 6
    return score


if __name__ == "__main__":
    total_score = 0
    with open(IN_FILE) as f:
        for turn in f:
            moves = turn.split()
            total_score += score_game(moves)

    print(total_score)

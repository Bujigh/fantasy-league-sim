from tabulate import tabulate

import random
import debug


polish_var = 10


class Game():
    def __init__(self, team_a, team_b, score_a, score_b):
        self.team_a = team_a
        self.team_b = team_b
        self.score_a = score_a
        self.score_b = score_b


def clear_scores(games_list):
    for game in games_list:
        game.score_a = 0
        game.score_b = 0

# Define a function to create and append Game objects to a list


def add_game(team_a, team_b, score_a, score_b, games_list):
    game = Game(team_a, team_b, score_a, score_b)
    games_list.append(game)


def print_games(games_list):
    table = [(game.team_name_a, game.score_a, '-', game.score_b,
              game.team_name_b) for game in games_list]
    headers = ['Team A', '', '', '', 'Team B']
    print(tabulate(table, headers=headers))


def score_simulator(team_a_power, team_b_power):

    win_a = team_a_power * 100 / (team_a_power + team_b_power)
    win_b = 100 - win_a

    white_balls = int(win_a * 33 / 50) + 1
    black_balls = int(win_b * 33 / 50) + 1
    grey_balls = 100 - white_balls - black_balls

    grey_balls_dif = (abs(win_a - win_b) * grey_balls) / 100

    grey_balls -= grey_balls_dif + polish_var
    grey_balls = int(grey_balls)

    white_balls += win_a * grey_balls_dif / 100 + win_a * polish_var / 100
    black_balls += win_b * grey_balls_dif / 100 + win_b * polish_var / 100

    bigger = white_balls
    lower = black_balls

    if black_balls > white_balls:
        bigger = black_balls
        lower = white_balls

    bigger += (abs(win_a - win_b) * lower) / 100
    lower -= (abs(win_a - win_b) * lower) / 100

    total = int(white_balls) + int(black_balls) + grey_balls

    if total > 100:
        dif = total - 100
        grey_balls -= dif
    elif total < 100:
        dif = 100 - total
        bigger += dif

    if black_balls > white_balls:
        black_balls = int(bigger)
        white_balls = int(lower)
    else:
        black_balls = int(lower)
        white_balls = int(bigger)

    if debug.debug_print_chances:
        print(
            f"Home Team Chance: {white_balls}, Away Team Chance: {black_balls}, Draw Chance: {grey_balls}")

    # randomly choose a ball
    ball = random.choices(['white', 'black', 'grey'], weights=[
                          white_balls, black_balls, grey_balls])[0]

    # simulate the game based on the color of the ball
    if ball == 'white':
        # choose a random score for team A
        team_a_score = random.randint(1, 10)
        team_b_score = random.randint(0, team_a_score - 1)
    elif ball == 'black':
        # choose a random score for team B
        team_b_score = random.randint(1, 10)
        team_a_score = random.randint(0, team_b_score - 1)
    else:
        # game ends in a draw
        team_a_score = random.randint(0, 10)
        team_b_score = team_a_score

    # return the scores of the two teams
    return (team_a_score, team_b_score)


def match_simulator(team_a_power, team_b_power):
    # simulate the initial game
    team_a_score, team_b_score = score_simulator(team_a_power, team_b_power)
    ot = 0

    if team_a_score == team_b_score:
        # simulate overtime until there is a winner
        ot = 1

        if debug.debug_print_ot:
            print_ot(ot)

        while True:
            team_a_score_ot, team_b_score_ot = score_simulator(
                team_a_power, team_b_power)
            if team_a_score_ot > team_b_score_ot:
                team_a_score += 1
                break
            elif team_a_score_ot < team_b_score_ot:
                team_b_score += 1
                break

    # return the final scores of the two teams
    return (team_a_score, team_b_score, ot)


def print_ot(ot):
    if ot:
        print("After OT")

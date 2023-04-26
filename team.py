import random
import time
from tabulate import tabulate

class Team:
    def __init__(self, name, power):
        self.name = name
        self.power = power
        self.positions = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    
    def add_position(self, position):
        if position in self.positions:
            self.positions[position] += 1

class Game():
    def __init__(self, team_name_a, team_name_b, score_a, score_b):
        self.team_name_a = team_name_a
        self.team_name_b = team_name_b
        self.score_a = score_a
        self.score_b = score_b
        
def clear_scores(games_list):
    for game in games_list:
        game.score_a = 0
        game.score_b = 0

def switch_teams(games):
    for game in games:
        temp = game.team_name_a
        game.team_name_a = game.team_name_b
        game.team_name_b = temp

# Define a function to create and append Game objects to a list
def add_game(team_name_a, team_name_b, score_a, score_b, games_list):
    game = Game(team_name_a, team_name_b, score_a, score_b)
    games_list.append(game)



# Define a function to print the list of Game objects
def print_games(games_list):
    table = [(game.team_name_a, game.score_a, '-', game.score_b, game.team_name_b) for game in games_list]
    headers = ['Team A', '', '', '', 'Team B']
    print(tabulate(table, headers=headers))

def group_games(games_list):
    game_sets = {}

    for game in games_list:
        team_name_a = game.team_name_a
        team_name_b = game.team_name_b
        if team_name_a or team_name_b in [game.team_name_a, game.team_name_b]:
            game_sets.append(game)

    # Return the list of game sets
    return game_sets

def reset_team_data(teams):
    for team in teams:
        team.positions = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

def game_simulator(team_a_power, team_b_power):

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

    

    if debug > 2:
        print(f"White balls: {white_balls}, black balls: {black_balls}, grey balls: {grey_balls}")

    # randomly choose a ball 
    ball = random.choices(['white', 'black', 'grey'], weights=[white_balls, black_balls, grey_balls])[0]

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


def match_simulator(team_a_power, team_b_power, ot):
    # simulate the initial game
    team_a_score, team_b_score = game_simulator(team_a_power, team_b_power)
    ot = 0

    if team_a_score == team_b_score:
        # simulate overtime until there is a winner
        ot = 1
        if debug > 1:
            print("After OT")
        while True:
            team_a_score_ot, team_b_score_ot = game_simulator(team_a_power, team_b_power)
            if team_a_score_ot > team_b_score_ot:
                team_a_score += 1
                break
            elif team_a_score_ot < team_b_score_ot:
                team_b_score += 1
                break
    else:
        if debug > 1:
            print("Regular Time")

    # return the final scores of the two teams
    
    return (team_a_score, team_b_score, ot)



def print_team_order(points, teams):
    # sort the teams based on their total points
    sorted_teams = sorted(teams, key=lambda team: points[team.name], reverse=True)

    
    # print the order of the teams
    #print("Team\t\tPoints")
    for i, team in enumerate(sorted_teams):
        team.add_position(i+1)
        #print(f"{i+1}. {team.name}\t\t{points[team.name]}")
    
    if debug:
        print("Power          Team              Points")
        print("---------------------------------------")
        for i, team in enumerate(sorted_teams):
            print("{:<10}{:<20}{:>5}".format(team.power, team.name, points[team.name]))

def simulate_championship(teams):
    n = len(teams)
    matches = {}
    points = {team.name: 0 for team in teams}
    games_list = []
    no_games = 0

    # generate all unique pairs of teams
    for i in range(len(teams)):
        for j in range(len(teams)):
            if i != j:
                # simulate home and away matches between each pair of teams
                team_a = teams[i]
                team_b = teams[j]
                score_a = 0
                score_b = 0

                
                # simulate home and away matches
                ot = 0
                score_a, score_b, ot = match_simulator(team_a.power, team_b.power, ot)
                if debug > 2:
                    print(f"{team_a.name} vs. {team_b.name}: {score_a} - {score_b}")
                    print()
                add_game(team_a.name, team_b.name, score_a, score_b, games_list)
                no_games += 1
                # calculate points earned by each team
                if ot == 0:
                    if score_a > score_b:
                        points[team_a.name] += 3
                    elif score_b > score_a:
                        points[team_b.name] += 3
                elif ot == 1:
                    if score_a > score_b:
                        points[team_a.name] += 2
                        points[team_b.name] += 1
                    elif score_b > score_a:
                        points[team_b.name] += 2
                        points[team_a.name] += 1

                # store the results of the matches in a dictionary
                matches[(team_a.name, team_b.name)] = (score_a, score_b)


    # create a list of points earned by each team
    points_list = [points[team.name] for team in teams]

    
    if debug > 1:
        print_games(games_list)
        print(no_games)
        print(len(teams))

    games_list.clear()
    
    print_team_order(points, teams)
    # return the dictionary of matches and points earned by each team
    return matches, points, points_list

def print_team_data(teams):
    # Define the column headers and their widths
    headers = ['Team', 'Power', '1st Place', '2nd Place', '3rd Place', '4th Place', '5th Place', '6th Place', '7th Place', '8th Place']
    widths = [30, 6, 10, 10, 10, 10, 10, 10, 10, 10]

    # Print the headers
    print('  '.join([f"{header:<{widths[i]}}" for i, header in enumerate(headers)]))


    sorted_teams = sorted(teams, key=lambda team: team.positions[1], reverse=True)



    # Print the team data rows
    for team in sorted_teams:
        row_data = [
            f"{team.name:<{widths[0]}}",
            f"{team.power:<{widths[1]}}",
            f"{team.positions[1]:<{widths[2]}}",
            f"{team.positions[2]:<{widths[3]}}",
            f"{team.positions[3]:<{widths[4]}}",
            f"{team.positions[4]:<{widths[5]}}",
            f"{team.positions[5]:<{widths[6]}}",
            f"{team.positions[6]:<{widths[7]}}",
            f"{team.positions[7]:<{widths[8]}}",
            f"{team.positions[8]:<{widths[9]}}"
        ]
        print('  '.join(row_data))



# create instances of Team class
team_steaua = Team("Steaua", 90)
team_fc_cojeasca = Team("FC Cojeasca", 85)
team_avantul_prabusirea = Team("Avantul Prabusirea", 87)
team_fc_scuipa_n_dunare = Team("FC Scuipa-n Dunare", 71)
team_dunarea_galati = Team("Dunarea Galati", 73)
team_sportul_ghetau = Team("Sportul Ghetau", 69)
team_gloria_catar = Team("Gloria Catar", 55)
team_echipa_forta = Team("Echipa Forta", 51)

# store teams in a list
teams = [team_gloria_catar, team_steaua, team_fc_cojeasca, team_avantul_prabusirea, team_fc_scuipa_n_dunare,
         team_dunarea_galati, team_sportul_ghetau, team_echipa_forta]



debug = 3
polish_var = 10

start_time = time.time()

# for i in range(0, 5):
#     for i in range(1,10000):
#         simulate_championship(teams)
#     print_team_data(teams)
#     reset_team_data(teams)
#     print()

simulate_championship(teams)

end_time = time.time()
runtime = end_time - start_time
print()
print(f"Program runtime: {runtime} seconds")


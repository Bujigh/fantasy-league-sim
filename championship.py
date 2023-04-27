import games
import debug
import team
import random

def print_ot():
    print(" | After OT")

def print_team_standings(points, teams):
    # sort the teams based on their total points
    sorted_teams = sorted(
        teams, key=lambda team: points[team.name], reverse=True)

    # print the order of the teams
    # print("Team\t\tPoints")
    for i, team in enumerate(sorted_teams):
        team.add_position(i+1)
        # print(f"{i+1}. {team.name}\t\t{points[team.name]}")

        print("Power          Team              Points")
        print("---------------------------------------")
        for i, team in enumerate(sorted_teams):
            print("{:<10}{:<20}{:>5}".format(
                team.power, team.name, points[team.name]))
            
def generate_fixtures(teams):

    team_list = teams
    num_teams = len(team_list)
    num_games_round = int(num_teams/2)
    fixtures = []

    # Generate the first round robin
    fixtures = []
    for i in range(num_teams-1):
        for j in range(num_teams//2):
            games.add_game(team_list[j], team_list[num_teams-j-1], 0, 0, fixtures)
        
        # Rotate the teams for the next round robin
        teams.insert(1, team_list.pop())
        
    # Generate the return fixtures
    for i in range(len(fixtures)):
            games.add_game(fixtures[i].team_b, fixtures[i].team_a, 0, 0, fixtures)

    for i in range(0, len(fixtures), num_games_round):
        group = fixtures[i:i+num_games_round]
        random.shuffle(group)
        fixtures[i:i+num_games_round] = group

    return fixtures


def print_team_championship_data(teams):
    # Define the column headers and their widths
    headers = ['Team', 'Power', '1st Place', '2nd Place', '3rd Place',
               '4th Place', '5th Place', '6th Place', '7th Place', '8th Place']
    widths = [30, 6, 10, 10, 10, 10, 10, 10, 10, 10]

    # Print the headers
    print('  '.join([f"{header:<{widths[i]}}" for i,
          header in enumerate(headers)]))

    sorted_teams = sorted(
        teams, key=lambda team: team.positions[1], reverse=True)

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


def simulate_championship(teams):
    matches = {}
    points = {team: 0 for team in teams}
    games_list = []
    games_per_round = int(len(teams)/2)

    games_list = generate_fixtures(teams)
    
    for i in range(len(games_list)):

        games_list[i].score_a, games_list[i].score_b, ot = games.match_simulator(games_list[i].team_a.power, games_list[i].team_b.power)

        if debug.debug_print_games:
            
            if i % games_per_round == 0:
                print()
                print(f"Round {int((i + 1) / games_per_round) + 1}")
            

        if ot == 0:
            if games_list[i].score_a > games_list[i].score_b:
                points[games_list[i].team_a] += 3
            elif games_list[i].score_b > games_list[i].score_a:
                points[games_list[i].team_b] += 3
            if debug.debug_print_games:
                print(f"{games_list[i].team_a.name} vs. {games_list[i].team_b.name}: {games_list[i].score_a} - {games_list[i].score_b}")
        elif ot == 1:
            if games_list[i].score_a > games_list[i].score_b:
                points[games_list[i].team_a] += 2
                points[games_list[i].team_b] += 1
            elif games_list[i].score_b > games_list[i].score_a:
                points[games_list[i].team_b] += 2
                points[games_list[i].team_a] += 1
            if debug.debug_print_games:
                print(f"{games_list[i].team_a.name} vs. {games_list[i].team_b.name}: {games_list[i].score_a} - {games_list[i].score_b}", end=" ")  
                print_ot() 
        

    teams = team.sort_teams(teams, points)

    team.add_team_position(teams)

    if debug.debug_print_standings:
        team.print_team_order(points, teams)

    games_list.clear()

    # return the dictionary of matches and points earned by each team
    return teams[0], points[teams[0]]

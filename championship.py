import games
import debug
import team


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

    #generate all games
    # generate all unique pairs of teams
    for i in range(len(teams)):
        for j in range(len(teams)):
            if i != j:
                # simulate home and away matches between each pair of teams
                team_a = teams[i]
                team_b = teams[j]
                score_a = 0
                score_b = 0

                games.add_game(team_a, team_b, score_a, score_b, games_list)


    #create the fixtures
    
    
    for i in range(len(games_list)):

        games_list[i].score_a, games_list[i].score_b, ot = games.match_simulator(games_list[i].team_a.power, games_list[i].team_b.power)

        if debug.debug_print_games:
            print(f"{games_list[i].team_a.name} vs. {games_list[i].team_b.name}: {games_list[i].score_a} - {games_list[i].score_b}")
            print()

        if ot == 0:
            if games_list[i].score_a > games_list[i].score_b:
                points[games_list[i].team_a] += 3
            elif games_list[i].score_b > games_list[i].score_a:
                points[games_list[i].team_b] += 3
        elif ot == 1:
            if games_list[i].score_a > games_list[i].score_b:
                points[games_list[i].team_a] += 2
                points[games_list[i].team_b] += 1
            elif games_list[i].score_b > games_list[i].score_a:
                points[games_list[i].team_b] += 2
                points[games_list[i].team_a] += 1
               
        

    teams = team.sort_teams(teams, points)

    team.add_team_position(teams)

    if debug.debug_print_standings:
        team.print_team_order(points, teams)

    games_list.clear()

    # return the dictionary of matches and points earned by each team
    return teams[0]

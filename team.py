import debug

class Team:
    def __init__(self, name, power):
        self.name = name
        self.power = power
        self.positions = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

    def add_position(self, position):
        if position in self.positions:
            self.positions[position] += 1


def create_teams():

    filename = "teams.txt"

    with open(filename, 'r') as file:
        lines = file.readlines()
    teams = []
    for line in lines:
        name, power = line.strip().split(' - ')
        team = Team(name, int(power))
        teams.append(team)
    return teams


def reset_team_data(teams):
    for team in teams:
        team.positions = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

def print_team_order(points, teams):
    print("Power             Team                 Points")
    print("----------------------------------------------")
    for i, team in enumerate(teams):
        print("{:<10}{:<8}{:<20}{:>5}".format(team.power, i+1, team.name, points[team]))


def add_team_position(sorted_teams):
    for i, team in enumerate(sorted_teams):
        team.add_position(i+1)

def sort_teams(teams, points):
    sorted_teams = sorted(teams, key=lambda team: points[team], reverse=True)

    return sorted_teams

from tabulate import tabulate
from team import create_teams, reset_team_data
from championship import simulate_championship, print_team_championship_data
import debug

run_type = 1

def run():
    teams = []
    teams = create_teams()

    if run_type == 0:
        simulate_championship(teams)

    if run_type == 1:
        for i in range(0, 100000):
            simulate_championship(teams)
        
        print_team_championship_data(teams)


        

from tabulate import tabulate
from team import create_teams
from championship import simulate_championship
import debug

run_type = 0

def run():
    if run_type == 0:

        teams = []

        teams = create_teams()

        team = simulate_championship(teams)

        

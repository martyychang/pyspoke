import argparse
import csv
import json
import os

def flatten_team(team):
    return {
        'id': team['id'],
        'name': team['name'],
        'createdAt': team['createdAt'],
        'updatedAt': team['updatedAt'],
        'owner': team['owner'],
        'email': team['email'],
        'permalink': team['permalink']
    }

# Parse arguments from the command line
parser = argparse.ArgumentParser(description='Convert a team data file into CSV.')
parser.add_argument('--json', type=str, required=True,
                    help='The path to the JSON file containing team data')

args = parser.parse_args()

# Read the JSON file
teams_json = None
with open(args.json, 'r') as f:
    teams_json = f.read()

# Load the JSON into a Python object
teams = json.loads(teams_json)

# Flatten the teams JSON
flat_teams = map(flatten_team, teams)

# Write the CSV file
teams_csv_file = args.json + '.csv'
teams_csv_field_names = [
    'id',
    'name',
    'createdAt',
    'updatedAt',
    'owner',
    'email',
    'permalink'
]

with open(teams_csv_file, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=teams_csv_field_names)
    writer.writeheader()
    for team in flat_teams:
        writer.writerow(team)
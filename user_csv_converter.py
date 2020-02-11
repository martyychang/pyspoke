import argparse
import csv
import json
import os

DRIFT_ORG = 'drift'

def flatten_user(user):

    # Flatten the "profile" field
    user['profileIsManager'] = user['profile']['isManager']
    del user['profile']

    # Flatten the "memberships" field for the "drift" org
    drift_membership = {}
    for membership in user['memberships']:
        if membership['org'] == DRIFT_ORG:
            drift_membership = membership
    del user['memberships']
    
    user['membershipStatus'] = drift_membership['status']
    user['membershipRole'] = drift_membership['role']

    # Return the flattened user
    return user

# Parse arguments from the command line
parser = argparse.ArgumentParser(description='Convert a user data file into CSV.')
parser.add_argument('--json', type=str, required=True,
                    help='The path to the JSON file containing user data')

args = parser.parse_args()

# Read the JSON file
users_json = None
with open(args.json, 'r') as f:
    users_json = f.read()

# Load the JSON into a Python object
users = json.loads(users_json)

# Flatten the users JSON
flat_users = map(flatten_user, users)

# Write the CSV file
users_csv_file = args.json + '.csv'
users_csv_field_names = [
    'id',
    'displayName',
    'email',
    'isEmailVerified',
    'isProfileCompleted',
    'formattedPhoneNumber',
    'profileIsManager',
    'createdAt',
    'membershipStatus',
    'membershipRole'
]

with open(users_csv_file, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=users_csv_field_names)
    writer.writeheader()
    for user in flat_users:
        writer.writerow(user)
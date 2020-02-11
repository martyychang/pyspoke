import argparse
import csv
import json
import os

def flatten_request_type(request_type):
    return {
        'id': request_type['id'],
        'status': request_type['status'],
        'title': request_type['title'],
        'team': request_type['team']
    }

# Parse arguments from the command line
parser = argparse.ArgumentParser(description='Convert a request type data file into CSV.')
parser.add_argument('--json', type=str, required=True,
                    help='The path to the JSON file containing request type data')

args = parser.parse_args()

# Read the JSON file
request_types_json = None
with open(args.json, 'r') as f:
    request_types_json = f.read()

# Load the JSON into a Python object
request_types = json.loads(request_types_json)

# Flatten the JSON objects
flat_request_types = map(flatten_request_type, request_types)

# Write the CSV file
request_types_csv_file = args.json + '.csv'
request_types_csv_field_names = [
    'id',
    'status',
    'title',
    'team'
]

with open(request_types_csv_file, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=request_types_csv_field_names)
    writer.writeheader()
    for request_type in flat_request_types:
        writer.writerow(request_type)
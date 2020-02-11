import argparse
import csv
import json
import os

def flatten_tag(tag):
    return tag

# Parse arguments from the command line
parser = argparse.ArgumentParser(description='Convert a tag data file into CSV.')
parser.add_argument('--json', type=str, required=True,
                    help='The path to the JSON file containing tag data')

args = parser.parse_args()

# Read the JSON file
tags_json = None
with open(args.json, 'r') as f:
    tags_json = f.read()

# Load the JSON into a Python object
tags = json.loads(tags_json)

# Flatten the JSON objects
flat_tags = map(flatten_tag, tags)

# Write the CSV file
tags_csv_file = args.json + '.csv'
tags_csv_field_names = [
    'id',
    'status',
    'color',
    'text',
    'org'
]

with open(tags_csv_file, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=tags_csv_field_names)
    writer.writeheader()
    for tag in flat_tags:
        writer.writerow(tag)
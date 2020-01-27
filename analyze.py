import json

# Read the file
json_file = '/Users/mchang/Downloads/output'

requests_json = None
with open(json_file, 'r') as f:
    requests_json = f.read()

requests = json.loads(requests_json)

print(len(requests))

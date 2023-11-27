import json, subprocess

path = 'test/test_1'
pids = f'{path}/pids.json'

with open(pids, 'r') as file:
    data = json.load(file)

test_process_pid = data['servers']['test']

subprocess.run(['kill', str(test_process_pid)])

data['servers']['test'] = ''

with open(pids, 'w') as file:
    json.dump(data, file, indent=4)
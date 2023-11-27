import json, subprocess

path = 'test/test_1'
pids = f'{path}/pids.json'

with open(pids, 'r') as file:
    data = json.load(file)

test_process = subprocess.Popen(['python', f'{path}/mockup_test.py'])

data['servers']['test'] = test_process.pid

with open(pids, 'w') as file:
    json.dump(data, file, indent=4)
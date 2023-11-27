import subprocess

print('start pyhton')

p = subprocess.Popen(['python', 'test/test_1/run.py'])
subprocess.run(['python', 'test/test_1/stop.py'])

print(p.pid)


import subprocess, json, os, argparse

print('start pyhton\n')

ADMIN_PATH = '/var/admin'
WEBS_PATH = '/var/web'
CFG_FILE = 'servers.json'

def get_args():
    parser = argparse.ArgumentParser(description='Správa serverů.')

    # Vytvoření vzájemně se vylučující skupiny pro první argument
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('servers', nargs='*', help='Jména serverů', default=[])
    group.add_argument('-a', '--all', action='store_true', help='Všechny servery')
    group.add_argument('--self', action='store_true', help='Vlastní server')

    # Definování druhého povinného argumentu pro akce
    parser.add_argument('action', choices=['stop', 'update', 'run', 'reset', 'redeploy'], help='Akce k provedení')

    return parser.parse_args()

args = get_args()

servers_to_config = args.servers

print(args)

print(f'servers_to_config: {servers_to_config} {args.action} {args.self} {args.all}\n')

if args.self:
    with open(os.path.join(ADMIN_PATH, CFG_FILE), 'r') as cfg_file:
        data = json.load(cfg_file)
    
    if args.action == 'update':
        subprocess.run(data['servers']['this']['commands']['update'], shell=True, cwd=ADMIN_PATH)

# for sub_dir_name in filter(lambda i: os.path.isdir(i), os.listdir(WEBS_PATH)):
#     sub_dir_path = os.path.join(WEBS_PATH, sub_dir_name)

#     if CFG_FILE in os.listdir(sub_dir_path):
#         with open(os.path.join(sub_dir_path, CFG_FILE), 'r') as cfg_file:
#             data = json.load(cfg_file)

#         for server in data['servers']:
#             print(server)
#             if server == 'test':
#                 subprocess.run(data['servers'][server]['commands']['start'], shell=True)

# subprocess.run(['python', 'test/test_1/run.py'])
# subprocess.run(['python', 'test/test_1/stop.py'])

# print(p.pid)


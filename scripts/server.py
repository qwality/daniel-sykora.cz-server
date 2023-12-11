import subprocess, json, os, argparse

print('p: server config script:\n')

ADMIN_PATH = '/var/admin'
WEBS_PATH = '/var/web'
CFG_FILE = 'servers.json'

def get_args():
    parser = argparse.ArgumentParser(description='Správa serverů.')

    server_group = parser.add_mutually_exclusive_group(required=True)
    server_group.add_argument('-a', '--all', action='store_true', help='Všechny servery')
    server_group.add_argument('--self', action='store_true', help='Vlastní server')
    server_group.add_argument('-s', '--servers', nargs='+', help='Jména serveru')

    services_group = parser.add_mutually_exclusive_group(required=True)
    services_group.add_argument('-f', '--full', action='store_true', help='Všechny servery')
    services_group.add_argument('-l', '--services', nargs='+', help='Jména serveru')

    # parser.add_argument('-d', '--do', action='store_true', required=True)

    actions_group = parser.add_mutually_exclusive_group(required=True)
    for action in ['stop', 'update', 'run', 'reset', 'redeploy']:
        actions_group.add_argument(f'--{action}', action='store_true', help=action)

    args = parser.parse_args()

    class my_args:
        def __init__(self, args):
            self.servers = args.servers if not (args.all or args.self) else [] if not args.self else ['self']
            self.services = args.services if not args.full else []
            self.action = 'stop' if args.stop else 'update' if args.update else 'run' if args.run else 'reset' if args.reset else 'redeploy'

    args = my_args(args)

    print(f'\tp: servers: {args.servers}, services: {args.services}, action: {args.action}')

    return args

args = get_args()

servers_to_config = args.servers
services_to_config = args.services
action = args.action

if servers_to_config and len(servers_to_config) >= 1 and servers_to_config[0] == 'self':
    print(f'\tp: updating admin')
    with open(os.path.join(ADMIN_PATH, CFG_FILE), 'r') as cfg_file:
        data = json.load(cfg_file)
    
    if action == 'update':
        subprocess.run(data['servers']['this']['commands']['update'], shell=True, cwd=ADMIN_PATH)
        print('\t\tp: admin updated')
    elif action == 'run':
        subprocess.run(data['servers']['nginx']['commands']['start'], shell=True, cwd=ADMIN_PATH)
        print('\t\tp: admin started')
    elif action == 'stop':
        subprocess.run(data['servers']['nginx']['commands']['stop'], shell=True, cwd=ADMIN_PATH)
        print('\t\tp: admin stopped')
    elif action == 'reset':
        subprocess.run(data['servers']['nginx']['commands']['restart'], shell=True, cwd=ADMIN_PATH)
        print('\t\tp: admin reseted')
    elif action == 'redeploy':
        subprocess.run(data['servers']['this']['commands']['update'], shell=True, cwd=ADMIN_PATH)
        subprocess.run(data['servers']['nginx']['commands']['restart'], shell=True, cwd=ADMIN_PATH)
        print('\t\tp: admin redeployed')

else:
    # print(f'will check: {list(filter(lambda i: os.path.isdir(os.path.join(WEBS_PATH, i)), os.listdir(WEBS_PATH)))}')
    for sub_dir_name in filter(lambda i: os.path.isdir(os.path.join(WEBS_PATH, i)), os.listdir(WEBS_PATH)):
        sub_dir_path = os.path.join(WEBS_PATH, sub_dir_name)
        # print(f'\tp: checking {sub_dir_path}')

        if CFG_FILE in os.listdir(sub_dir_path) and (servers_to_config == [] or sub_dir_name in servers_to_config):
            print(f'\tp: updating {sub_dir_name}')

            with open(os.path.join(sub_dir_path, CFG_FILE), 'r') as cfg_file:
                data = json.load(cfg_file)

            if action == 'update' or action == 'redeploy':
                subprocess.run(data['servers']['this']['commands']['update'], shell=True, cwd=sub_dir_path)
                print(f'\t\tp: {sub_dir_name} updated')

            for service in filter(lambda i: i != 'this', data['servers']):
                print(f'\t\t\tp: updating {service} vs: {services_to_config}')

                if service not in services_to_config and services_to_config != []:
                    continue

                if action == 'run':
                    subprocess.run(data['servers'][service]['commands']['run'], shell=True, cwd=sub_dir_path)
                    print(f'\t\tp: {service} started')
                elif action == 'stop':
                    subprocess.run(data['servers'][service]['commands']['stop'], shell=True, cwd=sub_dir_path)
                    print(f'\t\tp: {service} stopped')
                elif action == 'reset' or action == 'redeploy':
                    subprocess.run(data['servers'][service]['commands']['run'], shell=True, cwd=sub_dir_path)
                    subprocess.run(data['servers'][service]['commands']['stop'], shell=True, cwd=sub_dir_path)
                    print(f'\t\tp: {service} reseted')


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

    parser.add_argument('-d', '--do', action='store_true', required=True)

    actions_group = parser.add_mutually_exclusive_group(required=True)
    actions_group.add_argument('--stop', action='store_true', help='stop')
    actions_group.add_argument('--update', action='store_true', help='update')
    actions_group.add_argument('--run', action='store_true', help='run')
    actions_group.add_argument('--reset', action='store_true', help='reset')
    actions_group.add_argument('--redeploy', action='store_true', help='redeploy')

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

if args.servers and len(args.servers) >= 1 and args.servers[0] == 'self':
    print(f'\tp: updating admin')
    with open(os.path.join(ADMIN_PATH, CFG_FILE), 'r') as cfg_file:
        data = json.load(cfg_file)
    
    if args.action == 'update':
        subprocess.run(data['servers']['this']['commands']['update'], shell=True, cwd=ADMIN_PATH)
        print('\t\tp: admin updated')
    elif args.action == 'run':
        subprocess.run(data['servers']['nginx']['commands']['start'], shell=True, cwd=ADMIN_PATH)
        print('\t\tp: admin started')
    elif args.action == 'stop':
        subprocess.run(data['servers']['nginx']['commands']['stop'], shell=True, cwd=ADMIN_PATH)
        print('\t\tp: admin stopped')
    elif args.action == 'reset':
        subprocess.run(data['servers']['nginx']['commands']['restart'], shell=True, cwd=ADMIN_PATH)
        print('\t\tp: admin reseted')
    elif args.action == 'redeploy':
        subprocess.run(data['servers']['this']['commands']['update'], shell=True, cwd=ADMIN_PATH)
        subprocess.run(data['servers']['nginx']['commands']['restart'], shell=True, cwd=ADMIN_PATH)
        print('\t\tp: admin redeployed')

else:
    # print(f'will check: {list(filter(lambda i: os.path.isdir(os.path.join(WEBS_PATH, i)), os.listdir(WEBS_PATH)))}')
    for sub_dir_name in filter(lambda i: os.path.isdir(os.path.join(WEBS_PATH, i)), os.listdir(WEBS_PATH)):
        sub_dir_path = os.path.join(WEBS_PATH, sub_dir_name)
        # print(f'\tp: checking {sub_dir_path}')

        if CFG_FILE in os.listdir(sub_dir_path) and (args.servers == [] or sub_dir_name in servers_to_config):
            print(f'\tp: updating {sub_dir_name}')

            with open(os.path.join(sub_dir_path, CFG_FILE), 'r') as cfg_file:
                data = json.load(cfg_file)

            if args.action == 'update' or args.action == 'redeploy':
                subprocess.run(data['servers']['this']['commands']['update'], shell=True, cwd=sub_dir_path)
                print(f'\t\tp: {sub_dir_name} updated')

            for server in filter(lambda i: i != 'this', data['servers']):
                print(f'\t\t\tp: updating {server} vs: {args.services}')

                if server not in args.services or args.services == []:
                    break

                if args.action == 'run':
                    subprocess.run(data['servers'][server]['commands']['run'], shell=True, cwd=sub_dir_path)
                    print(f'\t\tp: {server} started')
                elif args.action == 'stop':
                    subprocess.run(data['servers'][server]['commands']['stop'], shell=True, cwd=sub_dir_path)
                    print(f'\t\tp: {server} stopped')
                elif args.action == 'reset' or args.action == 'redeploy':
                    subprocess.run(data['servers'][server]['commands']['run'], shell=True, cwd=sub_dir_path)
                    subprocess.run(data['servers'][server]['commands']['stop'], shell=True, cwd=sub_dir_path)
                    print(f'\t\tp: {server} reseted')


import subprocess, json, os, argparse

print('p: server config script:\n')

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

print(f'\tp: updating \'{'admin' if args.self else servers_to_config if args.all else servers_to_config[0]}\' with action \'{args.action}\'')

if args.self:
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

        if CFG_FILE in os.listdir(sub_dir_path) and (args.all or sub_dir_name in servers_to_config):
            print(f'\tp: updating {sub_dir_name}')
            with open(os.path.join(sub_dir_path, CFG_FILE), 'r') as cfg_file:
                data = json.load(cfg_file)

            if args.action == 'update' or args.action == 'redeploy':
                subprocess.run(data['servers']['this']['commands']['update'], shell=True, cwd=sub_dir_path)
                print(f'\t\tp: {sub_dir_name} updated')

            for server in filter(lambda i: i != 'this', data['servers']):
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


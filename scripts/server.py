import subprocess, json, os, argparse

print('p: server config script:\n')

ADMIN_PATH = '/var/admin'
WEBS_PATH = '/var/web'
CFG_FILE = 'servers.json'
ACTIONS = ['stop', 'update', 'run', 'reset', 'redeploy']

def get_args() -> tuple[list[str], list[str], str]:
    '''Získá argumenty z příkazové řádky.
    Vrací tuple obsahující jména serverů, služeb a akci.'''
    parser = argparse.ArgumentParser(description='Správa serverů.')

    server_group = parser.add_mutually_exclusive_group(required=True)
    server_group.add_argument('-a', '--all', action='store_true', help='Všechny servery')
    server_group.add_argument('--self', action='store_true', help='Vlastní server')
    server_group.add_argument('-s', '--servers', nargs='+', help='Jména serveru')

    services_group = parser.add_mutually_exclusive_group(required=True)
    services_group.add_argument('-f', '--full', action='store_true', help='Všechny servery')
    services_group.add_argument('-l', '--services', nargs='+', help='Jména serveru')

    actions_group = parser.add_mutually_exclusive_group(required=True)
    for action in ACTIONS:
        actions_group.add_argument(f'--{action}', action='store_true', help=action)

    args = parser.parse_args()

    return (
        args.servers if not (args.all or args.self) else [] if not args.self else ['self'],
        args.services if not args.full else [],
        next((action for action in ACTIONS if getattr(args, action)))
    )

def load_cfg( path: str ) -> dict:
    '''Načte konfigurační soubor na dané cestě.'''
    with open(path, 'r') as cfg_file:
        return json.load(cfg_file)

servers_to_config, services_to_config, action = get_args()

print(f'\tp: servers: {servers_to_config}, services: {services_to_config}, action: {action}')

if servers_to_config and servers_to_config[0] == 'self':
    '''Pokud se jedná o --self, tak se provede akce na tomto serveru.'''
    
    data = load_cfg(os.path.join(ADMIN_PATH, CFG_FILE))['servers']

    {
        'update':   lambda: subprocess.run(data['this'] ['commands']['update'], shell=True, cwd=ADMIN_PATH),
        'run':      lambda: subprocess.run(data['nginx']['commands']['start'], shell=True, cwd=ADMIN_PATH),
        'stop':     lambda: subprocess.run(data['nginx']['commands']['stop'], shell=True, cwd=ADMIN_PATH),
        'reset':    lambda: subprocess.run(data['nginx']['commands']['restart'], shell=True, cwd=ADMIN_PATH),
        'redeploy': lambda: subprocess.run(data['this'] ['commands']['update'], shell=True, cwd=ADMIN_PATH)
                            and subprocess.run(load_cfg(os.path.join(ADMIN_PATH, CFG_FILE))['servers']['nginx']['commands']['restart'], shell=True, cwd=ADMIN_PATH)
    }[action]() # selfcalling dict switch struct

else:
    '''Pokud se jedna o servers_to_config'''
    for web in filter(lambda i: os.path.isdir(os.path.join(WEBS_PATH, i)), os.listdir(WEBS_PATH)):
        '''pro kazdou slozku v /var/web která je složkou'''
        web_path = os.path.join(WEBS_PATH, web)

        if CFG_FILE in os.listdir(web_path) and (not servers_to_config or web in servers_to_config):
            '''pokud je v ní konfigurační soubor a je to server, který chceme konfigurovat'''

            data = load_cfg(os.path.join(web_path, CFG_FILE))['servers']

            if action in ['update', 'redeploy']:
                subprocess.run(data['this']['commands']['update'], shell=True, cwd=web_path)
                data = load_cfg(os.path.join(web_path, CFG_FILE))['servers']

            if action not in ['update']:
                for service in filter(lambda s: s != 'this' and not (services_to_config and s not in services_to_config) , data):
                    print(f'\t\t\tp: updating {service} vs: {services_to_config}')

                    {
                        'run':      lambda: subprocess.run(     data[service]['commands']['run'], shell=True, cwd=web_path),
                        'stop':     lambda: subprocess.run(     data[service]['commands']['stop'], shell=True, cwd=web_path),
                        'reset':    lambda: subprocess.run(     data[service]['commands']['stop'], shell=True, cwd=web_path)
                                            and subprocess.run( data[service]['commands']['run'], shell=True, cwd=web_path),
                        'redeploy': lambda: subprocess.run(     data[service]['commands']['stop'], shell=True, cwd=web_path)
                                            and subprocess.run( data[service]['commands']['run'], shell=True, cwd=web_path)
                    }[action]() # selfcalling dict switch struct
                        


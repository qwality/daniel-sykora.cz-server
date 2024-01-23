# Server Control Panel

## Úvod
Tento repozitář je určen pro správu serverů na VPS (Virtual Private Server). Jeho hlavním účelem je poskytnout sadu skriptů pro jednoduchou aktualizaci a správu webových aplikací a služeb.

## Instalace a konfigurace
- Hlavní skript projektu je `./qwality-server`. Je doporučeno nastavit pro tento soubor spustitelné oprávnění pomocí příkazu `chmod +x` nebo pomoci `python qwality-server --install`.
- Pro snadné používání skriptu z jakéhokoli umístění je skript přidán do proměnné `PATH` v souboru `~/.bashrc` následujícím příkazem:
  ```bash
  export PATH="$PATH:/var/admin/"
  ```
  nebo `python qwality-server --install`
- Po této konfiguraci lze skript `qwality-server` spouštět z jakéhokoli umístění v systému.

## Použití

1. **První argument [OPTIONS]**:
    - `--cfg-file` | `-cfg` nazev konfiguracniho souboru, defaultni je `server`
    - `--cfg-format` | `-format` format konfiguracniho souboru, defaultni je `yaml`
    - `--webs-path` | `-webs` cesta k webum/serverum defaultni je ` `
    - `--admin-path` | `-admin` cesta k admin defaultni je ` `
    - `--verbose` | `-v` prida nejake vystupy
    - `--install` nainstaluje program a ignoruje dalsi argumenty, pokud je instalace neuspesna tak vytiskne commandy ktere by mely pomoct
    - `--help` | `-h` help

2. **Druhý argument [ACTION]**:
    - `run`
    - `stop`
    - `update` aplikuje se pouze na root serveru
    - `reser`
    - `redeploy`

3. **Třetí argument [SERVERY]**:
   - funguje zde automaticke doplnovani, ktere vyhledava servery na `--webs-path`
   - `all` vsechny servery
   - `self` this.server / admin (nejspise nginx)

4. **Oddelovac [`/`]**
5. **Paty argument [SERVICES]**:
    - funguje zde automaticke zadavani zalozene na spolecnych servicech zadanych serveru
    - `all` i presto ze nemusi mit spolecne servicy all toto chovani prepise a provede akci na vsechny servicy zadanych serveru

## Konfigurace webů
- Každý web, který chcete spravovat pomocí této utility, musí obsahovat v kořenovém adresáři soubor `server.yaml` nebo jinak nazvany pokud je tak nastaveno v `--cfg-file` a `--cfg-format`
- Příklad struktury souboru `servers.json`:
  ```json
  {
      "servers": {
          "this": {
              "commands": {
                  "update": "Aktualizuje kořenový adresář webu, obvykle provádí pull celého repozitáře z Gitu."
              }
          },
          "service": {
              "commands": {
                  "run": "...",
                  "stop": "..."
              }
          }
      }
  }
  ```

## Další informace
- Tento repozitář také obsahuje konfiguraci pro Nginx. Při příkazu `redeploy self` dojde k resetování Nginx.
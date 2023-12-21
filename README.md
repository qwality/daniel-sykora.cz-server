# Server Control Panel

## Úvod
Tento repozitář je určen pro správu serverů na VPS (Virtual Private Server). Jeho hlavním účelem je poskytnout sadu skriptů pro jednoduchou aktualizaci a správu webových aplikací a služeb.

## Instalace a konfigurace
- Hlavní skript projektu je umístěn v `scripts/server`. Je doporučeno nastavit pro tento soubor spustitelné oprávnění pomocí příkazu `chmod +x`.
- Pro snadné používání skriptu z jakéhokoli umístění je skript přidán do proměnné `PATH` v souboru `~/.bashrc` následujícím příkazem:
  ```bash
  export PATH="$PATH:/var/admin/scripts/"
  ```
- Po této konfiguraci lze skript `server` spouštět z jakéhokoli umístění v systému.

## Použití
Skript `server` přijímá argumenty, které určují jeho chování:

1. **První argument**:
   - `--self`: Aktualizuje tuto utility včetně Nginx.
   - `-a`: Aktualizuje všechny weby umístěné v `/var/web`.
   - `-s`: Specifikuje seznam webů k aktualizaci (za `-s` následuje seznam webů).

2. **Druhý argument**:
   - `-f`: Aplikuje příkaz na všechny služby.
   - `-l`: Specifikuje seznam služeb (za `-l` následuje seznam služeb).

3. **Třetí argument**:
   - `--stop`: Zastaví službu.
   - `--update`: Aktualizuje službu.
   - `--run`: Spustí službu.
   - `--reset`: Restartuje službu (kombinace `stop` a `run`).
   - `--redeploy`: Přeinstaluje službu (kombinace `update`, `stop` a `run`).

## Konfigurace webů
- Každý web, který chcete spravovat pomocí této utility, musí obsahovat v kořenovém adresáři soubor `servers.json`.
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
- Tento repozitář také obsahuje konfiguraci pro Nginx. Při příkazu `redeploy --self` dojde k resetování Nginx.
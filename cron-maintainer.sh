#!/usr/bin/env bash

# source ~/.bashrc

nvm -v
node -v
rails -v

status_1=$(qwality-server -q status daniel-sykora.cz)
status_2=$(qwality-server -q status rails-redmine)

if [[ $status_1 != "OK" ]]; then
    qwality-server redeploy daniel-sykora.cz
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - daniel-sykora.cz is OK"
fi

if [[ $status_2 != "OK" ]]; then
    qwality-server redeploy rails-redmine
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - rails-redmine is OK"
fi
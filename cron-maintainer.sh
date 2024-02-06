#!/usr/bin/env bash

status_1=$(qwality-server -q status daniel-sykora.cz)
status_2=$(qwality-server -q status rails-redmine)

if [[ $status_1 != "OK"]]; then
    qwality-server run danie-sykora.cz
fi

if [[ $status_2 != "OK"]]; then
    qwality-server run rails-redmine
fi
#!/bin/bash
# uvicorn 'main:app' --host '0.0.0.0' --port '80' &
uvicorn main:app --host 0.0.0.0 --port 443 --ssl-keyfile $SSL/privkey.pem --ssl-certfile $SSL/fullchain.pem &

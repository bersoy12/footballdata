#!/bin/sh
superset fab create-admin --username berkay --firstname berkay --lastname ersoy --email admin@superset.com --password admin
superset db upgrade
superset init
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger
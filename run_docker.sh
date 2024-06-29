#!/bin/bash

# run docker container of mysql
# docker run --name <cotainer name> -e MYSQL_ROOT_PASSWORD=<root password> -e MYSQL_DATABASE=new_nm_api -p 3307:3306 -d mysql:5.6.33

# Create a network
# docker network create new_nm

# add mysql container to the network
# docker network connect new_nm <mysql_container_nameorid>

docker run \
    --rm \
    -v .:/usr/src/app \
    -p 8000:8000 \
    -e DJANGO_SETTINGS_MODULE=new_nm_api.local \
    --network new_nm \
    --name new_nm_api_local \
    new_nm_api

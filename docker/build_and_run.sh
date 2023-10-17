#!/bin/bash

docker-compose -f /home/debian/ws2022-gruppe5/docker/docker-compose.yml down
docker-compose -f /home/debian/ws2022-gruppe5/docker/docker-compose.yml build
docker-compose -f /home/debian/ws2022-gruppe5/docker/docker-compose.yml up -d




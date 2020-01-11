#!/bin/bash

# dos2unix
dos2unix frontend/entrypoint.sh

# Start singular development server
docker-compose up --build -d singular_frontend
docker-compose up --build -d singular_backend



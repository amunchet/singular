#!/bin/sh

# Starts up the production version of singular server

# Step 1: Compile the vue to dist in src
docker-compose up -d singular_frontend
docker exec singular_singular_frontend_1 sh -c "cd /data && npm run build"
docker cp singular_singular_frontend_1:/data/dist frontend
docker stop singular_singular_frontend_1 && docker rm singular_singular_frontend_1
# Step 2: Start nginx with dist for frontend

# Step 3: Start backend with gunicorn
docker-compose up --build -d singular_backend

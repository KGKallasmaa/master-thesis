docker login --username=rocketnow
docker-compose build
docker login docker.io
docker push master_thesis_server
docker system prune -a
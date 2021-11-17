docker login --username=rocketnow
docker-compose build
docker login docker.io
docker tag server_master_thesis_server:latest rocketnow/server_master_thesis_server:latest
docker push rocketnow/server_master_thesis_server:latest
docker system prune -a

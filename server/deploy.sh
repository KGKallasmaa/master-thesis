docker login --username=rocketnow
docker-compose build
docker login docker.io
docker tag master_thesis_server:latest rocketnow/master_thesis_server:latest
docker push rocketnow/master_thesis_server:latest
docker system prune -a

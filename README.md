# Demo flask redis dockerized templates

Example of how to handle background processes with Flask, Redis Queue, and Docker

### Quick Start

Spin up the containers:

```sh
$ docker-compose up --build -V --scale worker=4
```

Spin up the containers in background:

```sh
$ docker-compose up -d --build -V --scale worker=4
```


Stop all containers and workers:

```sh
$ docker-compose down -v
```

Open your browser to http://localhost:5004

Open redis dashboard in http://localhost:9181/

Show logs from worker containers:
```sh
docker-compose logs --tail=0 -f master
docker-compose logs --tail=0 -f worker
```

You can view a list of all the allocated volumes in your system with
```sh
docker volume ls
```

If you prefer a more automatic cleanup, the following command will remove any unused images or volumes, and any stopped containers that are still in the system.
```sh
docker system prune --volumes
```

## Some important docker commands:
Below command will remove the following:
  - all stopped containers
  - all networks not used by at least one container
  - all dangling images
  - all dangling build cache
```sh
docker system prune
```
Below command will remove the following:
  - all stopped containers
  - all networks not used by at least one container
  - all images without at least one container associated to them
  - all build cache
```sh
docker system prune --all --force
```
Below command will remove all docker images:
```sh
docker rmi --force $(docker images --all --quiet)
```

# Contribution

## Pre-commit
Following command will help to remove trailing-whitespace, check case conflict, check added large files,
check merge conflict by using isort, black and flake8 automation tools.
```sh
python3 pre-commit-2.15.0.pyz run  -a
```

## Delete __pycache__ files
```sh
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
```

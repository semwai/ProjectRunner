[![Python](https://github.com/semwai/ProjectRunner/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/semwai/ProjectRunner/actions/workflows/ci.yml)

### Clear docker 
`docker kill $(docker ps -a -q)`\
`docker rm $(docker ps -a -q)`\
`docker volume prune -f`

### Build (default arm)

```bash
docker build -t semwai/backend:0.6.1-arm . 
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock -p 8000:8000 semwai/backend:0.6.1-arm
```
### Buildx (for intel)
```bash
docker buildx build --platform linux/amd64 -t semwai/backend:0.6.1-amd64 . 
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock -p 8000:8000 semwai/backend:0.6.1-amd64

```
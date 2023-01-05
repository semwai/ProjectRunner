[![Python](https://github.com/semwai/ProjectRunner/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/semwai/ProjectRunner/actions/workflows/ci.yml)

### Clear docker 
`docker kill $(docker ps -a -q)`\
`docker rm $(docker ps -a -q)`\
`docker volume prune -f`

### Build (default arm)

```bash
docker build -t semwai/backend:0.7.0-arm . 
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock 
-p 8000:8000 
-e SECRET_KEY=<RANDOM_KEY>
-e GOOGLE_CLIENT_ID=<PUBLIC_KEY>
semwai/backend:0.7.0-arm
```
### Buildx (for intel)
```bash
docker buildx build --platform linux/amd64 -t semwai/backend:0.7.0-amd64 . 
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock 
-p 8000:8000 
-e SECRET_KEY=<RANDOM_KEY>
-e GOOGLE_CLIENT_ID=<PUBLIC_KEY>
semwai/backend:0.7.0amd64

```
### Clear docker 
`docker kill $(docker ps -a -q)`\
`docker rm $(docker ps -a -q)`\
`docker volume prune -f`

### Build (default arm)

```bash
docker build -t semwai/backend:0.6.0-arm . 
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock -p 8000:8000 semwai/backend:0.6.0-arm
```
### Buildx (for intel)
```bash
docker buildx build --platform linux/amd64 -t semwai/backend:0.6.0-amd64 . 
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock -p 8000:8000 semwai/backend:0.6.0-amd64

```
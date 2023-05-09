[![Python](https://github.com/semwai/ProjectRunner/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/semwai/ProjectRunner/actions/workflows/ci.yml)

### Clear docker 
`docker kill $(docker ps -a -q)`\
`docker rm $(docker ps -a -q)`\
`docker volume prune -f`

### Build (default arm)

```bash
docker build -t semwai/backend:0.8.2-arm .
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock \
-p 8000:8000 \
-e SECRET_KEY=<RANDOM_KEY> \
-e GOOGLE_CLIENT_ID=<PUBLIC_KEY> \
-e FRONTEND_URL=<https://your_frontend_url_for_cors> \
-e DB=postgresql://root:1234@localhost/coderunner \
semwai/backend:0.8.2-arm
```
### Buildx (for intel)
```bash
docker buildx build --platform linux/amd64 -t semwai/backend:0.8.2-amd64 .
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock \
-p 8000:8000 \
-e SECRET_KEY=<RANDOM_KEY> \
-e GOOGLE_CLIENT_ID=<PUBLIC_KEY> \
-e FRONTEND_URL=<https://your_frontend_url_for_cors> \
-e DB=postgresql://root:1234@localhost/coderunner \
semwai/backend:0.8.2-amd64

```

```bash
docker run -d --name postgre -p 5432:5432 -e POSTGRES_DB=coderunner -e POSTGRES_USER=root -e POSTGRES_PASSWORD=1234  bitnami/postgresql
docker run -d --name pgadmin -p 5500:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin  dpage/pgadmin4
```


[google key console](https://console.cloud.google.com/apis/credentials?authuser=1&hl=ru&project=gold-box-368621)
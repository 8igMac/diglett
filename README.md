# Diglett
An online speaker verification server.

# Development
```sh
$ uvicorn server:app --reload
```

# Build
```sh
$ docker build -t diglett .
```

# Deployment
```sh
$ docker run -d --restart unless-stopped --name diglett -p 3210:80 diglett:latest
```

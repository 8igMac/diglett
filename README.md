# Diglett
An online speaker verification server.

# Development
1. Create your own `.env` to store sensitive information. (You can copy `example.env`
and modify the content as you needed.) 
```sh
$ cp example.env .env
# Edit .env
```
2. Run the development server.
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

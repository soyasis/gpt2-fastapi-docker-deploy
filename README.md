# NLP with PyTorch: How-to Generator
This project containes a GPT-2 transformer faine-tunned on WikiHow.com entries related to cultural practices.
You can test the model, which is currenlty deployed on a DigitalOcean instace here: http://how-to-generator.herokuapp.com/

The ideation and UI has been done in collaboration with Johanna K. Michel

## Steps to Deploy Model served via FastAPI using docker
Ref: https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker


### 1. Dockerize FastAPI App
- Add Docker file
`vim Dockerfile` and paste:
```
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
```

### 2. Create Docker Image
- Build docker image
`docker build -t myimage ./`

- Run Docker image locally (for testing)
`docker run -p 4000:80 myimage`

### 3. Push to Docker Hub
- Login to Docker
`docker login`

- Tag image and Push
`docker tag myimage plasticfruits/reponame:latest`
`docker push plasticfruits/reponame:latest`

### 4. Setup Container and run
*For large models minimum 4GB of RAM*
- Create RancheraOS and SSH
`ssh rancher@your_droplet_ip`

- pull Docker Image
`docker pull plasticfruits/how-to-qa`

- Check docker image info
`docker images`

- Run Container
`docker run -d --name mycontainer -p 80:80 plasticfruits/how-to-qa`

- Check if container is running
`docker ps`
`docker ps -a` for all containers

- Check logs
`docker container logs mycontainer`

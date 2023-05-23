PORT=5000
APP=app
PYTHON=python3.10

# Install pipenv
pipenv:
	$(PYTHON) -m pip install --user pipenv 

# Install dependencies
prep:
	$(PYTHON) -m pipenv install

# Activate pipenv
shell:
	$(PYTHON) -m pipenv shell

# Run flask app
run:
	$(PYTHON) -m pipenv run flask --app $(APP) run -h localhost -p $(PORT)

IMAGE_NAME=bangkit-sleep-app-be-image
IMAGE_TAG=latest
CONTAINER_NAME=bangkit-sleep-app-be
REBUILD=false

# Build docker image
docker-build:
	$(REBUILD) && make docker-clean || echo "skipping clean up procedure"
	docker images | grep $(IMAGE_NAME) || docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

# Run docker container
docker-run:
	docker ps -a | grep $(CONTAINER_NAME) || docker run -dp $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME):$(IMAGE_TAG)
	docker ps | grep $(CONTAINER_NAME) || docker start $(CONTAINER_NAME)

# Stop docker container
docker-stop:
	docker stop $(CONTAINER_NAME)

# Remove the docker container and docker image
docker-clean:
	make docker-stop && docker rm $(CONTAINER_NAME) && docker rmi $(IMAGE_NAME)

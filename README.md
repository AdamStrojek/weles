# Weles

Simple POC file storge app written in Django, Django REST Framework to work on AWS

## Setup environment

To setup fully working environment follow this steps:

### Create new `.env` file in main folder of project
This file is added to gitignore list, so it will not be commited to ensure that all secrets will remain secrets. In file
`env.example` you always should have the newest version of all available settings variables. For development process
you can just simply copy this file

```shell script
$ cp env.example .env
```

### Start docker-compose project
Even though each microservice is separated container to help in set up development environment docker-compose scripts were
created. This allow to start project fast, after installing docker and docker-compose, with simple command

```shell script
$ docker-compose up
```

For docker and docker-compose installation please consult with [official documentation](https://docs.docker.com/install/)

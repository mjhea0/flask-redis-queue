# Flask Redis Queue

Example of how to handle background processes with Flask, Redis Queue, and Docker

## Quick Start

### Basics

1. Create and activate a virtualenv
1. Install the requirements

### Set Environment Variables

Update *project/server/config.py*, and then run:

```sh
$ export APP_SETTINGS="project.server.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.server.config.ProductionConfig"
```

### Run the Application

```sh
$ python manage.py runserver
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)


### Test

Without coverage:

```sh
$ python manage.py test
```

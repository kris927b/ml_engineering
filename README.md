# neurons

## Installation

The project uses poetry as the package manager so simply run:

```
$ poetry install 
```

## Prerequisites

The API makes use of the OpenAI API, thus you need to specify an API key in an ENV file placed in the root directory.

```
OPENAI_SECRET=sk-proj-XXXXXX
```

## Running just the backend

To run just the backend/API run:

```
$ poetry run langchain serve --port 8100
```

Then access the API on `http://localhost:8100`


## Running both bakcend and frontend

To run both the backend and the frontend use docker:

```
$ docker-compose -f docker/docker-compose.yml up --build
```


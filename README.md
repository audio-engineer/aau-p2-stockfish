# ChessTeacher Stockfish

This containerized Python application is a REST API
built using FastAPI that serves [Stockfish](https://stockfishchess.org/) engine responses using
[py-stockfish/stockfish](https://github.com/py-stockfish/stockfish) as a wrapper.

The Stockfish software is licensed under GPL v3.
The full source code for the version of the software used in this project can be found here:
[official-stockfish/Stockfish](https://github.com/official-stockfish/Stockfish/tree/sf_16.1).

To build it, run:

```shell
docker build -t audio-engineer/chess-teacher-stockfish:latest .
```

Or, if you are using PyCharm, run the `Build` run configuration.

## Documentation

API documentation can be found at [localhost:8000/docs](http://localhost:8000/docs) and
[localhost:8000/redoc](http://localhost:8000/redoc).

## Local Development

```shell
docker compose up -d
```

```shell
docker exec -it chess-teacher-stockfish-python-1 /bin/sh
```

```shell
fastapi dev --host 0.0.0.0 src/chess_teacher_stockfish/main.py
```

To run the linters in the `python` service container:

```shell
pylint src/ && flake8 && ruff check
```

To run the testing suite in the `python` service container:

```shell
python -m pytest --cov=src.chess_teacher_stockfish
```

```shell
docker compose down
```

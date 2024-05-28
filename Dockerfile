FROM alpine:latest AS stockfish_builder

RUN apk add -U --no-cache git g++ make && \
    git clone --depth 1 --branch sf_16.1 https://github.com/official-stockfish/Stockfish.git

WORKDIR /Stockfish/src/

RUN make -j build

FROM python:alpine AS development

WORKDIR /usr/src/chess-teacher-stockfish/

COPY ./poetry.lock ./poetry.toml ./pyproject.toml ./README.md ./

RUN apk add -U --no-cache libstdc++ git && \
    pip install --no-cache-dir poetry && \
    poetry install

COPY --from=stockfish_builder /Stockfish/src/stockfish /usr/local/bin/

EXPOSE 8000

FROM development AS production_builder

RUN poetry export --without-hashes -o requirements.txt

FROM python:alpine AS production

WORKDIR /usr/src/chess-teacher-stockfish/

COPY --from=stockfish_builder /Stockfish/src/stockfish /usr/local/bin/
COPY --from=production_builder /usr/src/chess-teacher-stockfish/requirements.txt ./

RUN apk add -U --no-cache libstdc++ git && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src/ ./src/

EXPOSE 8000

CMD ["fastapi", "run", "--host", "0.0.0.0", "src/chess_teacher_stockfish/main.py"]

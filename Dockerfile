FROM alpine:latest AS builder

RUN apk add -U --no-cache git g++ make && \
    git clone --depth 1 --branch sf_16.1 https://github.com/official-stockfish/Stockfish.git

WORKDIR /Stockfish/src/

RUN make -j build

FROM python:alpine

WORKDIR /usr/src/chess-teacher-stockfish/

COPY ./poetry.lock ./poetry.toml ./pyproject.toml ./

RUN apk add -U --no-cache libstdc++ git && \
    pip install --no-cache-dir poetry && \
    poetry install

COPY --from=builder /Stockfish/src/stockfish /usr/local/bin/
COPY --from=builder /Stockfish/Copying.txt /usr/share/doc/stockfish/COPYING

COPY app/ app/
COPY --chmod=744 ./entrypoint.sh /

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

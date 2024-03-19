FROM alpine:latest AS builder

RUN apk add -U --no-cache git g++ make && \
    git clone --depth 1 --branch sf_16.1 https://github.com/official-stockfish/Stockfish.git

WORKDIR /Stockfish/src/

RUN make -j build

FROM python:alpine

WORKDIR /usr/src/app/

COPY ./requirements.txt ./

RUN apk add -U --no-cache libstdc++ git && \
    pip install --no-cache-dir -r requirements.txt

COPY ./ ./

COPY --from=builder --chown=stockfish:stockfish /Stockfish/src/stockfish /usr/local/bin/
COPY --from=builder --chown=stockfish:stockfish /Stockfish/src/*.nnue /usr/local/bin/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

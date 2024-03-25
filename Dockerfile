FROM alpine:latest AS stockfish_builder

RUN apk add -U --no-cache git g++ make && \
    git clone --depth 1 --branch sf_16.1 https://github.com/official-stockfish/Stockfish.git

WORKDIR /Stockfish/src/

RUN make -j build

FROM python:alpine AS development

WORKDIR /usr/src/chess-teacher-stockfish/

COPY ./poetry.lock ./poetry.toml ./pyproject.toml ./

RUN apk add -U --no-cache libstdc++ git && \
    pip install --no-cache-dir poetry && \
    poetry install

COPY --from=stockfish_builder /Stockfish/src/stockfish /usr/local/bin/

COPY ./src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.chess_teacher_stockfish.main:app", "--host", "0.0.0.0", "--reload"]

FROM development AS production_builder

COPY ./README.md ./

RUN poetry build

FROM python:alpine

COPY --from=stockfish_builder /Stockfish/src/stockfish /usr/local/bin/
COPY --from=stockfish_builder /Stockfish/Copying.txt /usr/share/doc/stockfish/COPYING
COPY --from=production_builder /usr/src/chess-teacher-stockfish/dist/*.whl ./
COPY --chmod=744 ./entrypoint.sh /

RUN apk add -U --no-cache libstdc++ git && \
    pip install --no-cache-dir *.whl

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000

CMD ["uvicorn", "chess_teacher_stockfish.main:app", "--host", "0.0.0.0", "--reload"]

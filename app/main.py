import os

from fastapi import FastAPI
from stockfish import Stockfish
from fastapi.responses import PlainTextResponse

app = FastAPI()
stockfish = Stockfish()


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    with open(os.path.join(os.path.dirname(__file__), "robots.txt"), encoding="utf-8") as f:
        return f.read()


@app.get("/about", response_class=PlainTextResponse)
def robots():
    with open("/usr/share/doc/stockfish/COPYING", encoding="utf-8") as f:
        return f.read()


@app.get("/")
def read_root():
    return {"data": {"best-move": stockfish.get_top_moves(3)}}

"""Module that provides the main entry point for the API"""

import os

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from stockfish import Stockfish

app = FastAPI()
stockfish = Stockfish()


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    """Opens and prints the robots.txt file"""
    with open(
        os.path.join(os.path.dirname(__file__), "robots.txt"), encoding="utf-8"
    ) as f:
        return f.read()


@app.get("/about", response_class=PlainTextResponse)
def about():
    """Opens and prints Stockfish's license page"""
    with open("/usr/share/doc/stockfish/COPYING", encoding="utf-8") as f:
        return f.read()


@app.get("/")
def read_root():
    """Returns the three best moves"""
    return {"data": {"best-move": stockfish.get_top_moves(3)}}

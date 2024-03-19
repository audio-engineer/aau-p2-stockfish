from fastapi import FastAPI
from stockfish import Stockfish

app = FastAPI()
stockfish = Stockfish()


@app.get("/")
def read_root():
    return {"data": {"best-move": stockfish.get_top_moves(3)}}

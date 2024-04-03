"""Module that provides the main entry point for the API"""

import os
from typing import Generic, TypeVar, Optional, List
from math import floor
from inflection import underscore
from stockfish import Stockfish
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, ConfigDict, TypeAdapter, ValidationError
from pydantic.alias_generators import to_camel

# Creating the FastAPI instance and setting up metadata for the API
DESCRIPTION = """
## Software in Use
- [Stockfish](https://stockfishchess.org/)
  - [GNU GPLv3](https://opensource.org/license/gpl-3-0)
- [py-stockfish](https://github.com/py-stockfish/stockfish)
"""

app = FastAPI(
    title="ChessTeacher Stockfish API",
    description=DESCRIPTION,
    summary="An API for evaluating chess positions and moves using Stockfish",
)

# Stockfish setup
stockfish = Stockfish()
stockfish.set_depth(8)
stockfish.resume_full_strength()
stockfish.set_turn_perspective(False)

DataT = TypeVar("DataT")


class CamelCaseAliasBaseModel(BaseModel):
    """Extending this class automatically generates camel case aliases"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class DataResponse(CamelCaseAliasBaseModel, Generic[DataT]):
    """Default top-level member for all response types"""

    data: Optional[DataT] = None


class TopMove(CamelCaseAliasBaseModel):
    """Represents a top move as defined by the get_top_moves method using the
    verbose setting"""

    move: str
    centipawn: int | None
    mate: int | None
    time: str
    nodes: str
    multi_pv_line: str
    nodes_per_second: str
    selective_depth: str
    wdl: str


class TopThreeMovesResponse(CamelCaseAliasBaseModel):
    """Response object containing the top three moves from the start position"""

    top_three_moves: list[TopMove]


class EvaluatePositionRequest(CamelCaseAliasBaseModel):
    """Request object for the /evaluate-position endpoint"""

    fen: str
    time_to_analyze: int = Field(default=1000)


class AnalyzeMoveRequest(EvaluatePositionRequest):
    """Request object for the /analyze-move endpoint"""

    move: str


class EvaluatePositionResponse(CamelCaseAliasBaseModel):
    """Response object containing the Stockfish evaluation of the current position,
    the win/draw/loss statistics and the top three moves"""

    evaluation: dict[str, str | int]
    wdl_stats: list[int] | None
    top_three_moves: list[TopMove]


class AnalyzeMoveResponse(CamelCaseAliasBaseModel):
    """Response object containing the data whether the move will be a capture, the
    evaluation after the move and the absolute change in evaluation after the move"""

    is_move_capture: Stockfish.Capture
    evaluation_after_move: float
    absolute_evaluation_change: float


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    """Opens and prints the robots.txt file"""

    with open(
        os.path.join(os.path.dirname(__file__), "robots.txt"), encoding="utf-8"
    ) as f:
        return f.read()


@app.post("/evaluate-position")
async def evaluate_position(
    evaluate_position_request: EvaluatePositionRequest,
) -> DataResponse[EvaluatePositionResponse]:
    """Evaluates the current position and returns the result and statistics about
    win/draw/loss for the side to move"""

    fen = evaluate_position_request.fen

    if not stockfish.is_fen_valid(fen):
        raise HTTPException(status_code=400, detail="Invalid FEN")

    stockfish.set_fen_position(fen)

    top_three_moves = stockfish.get_top_moves(3, True)
    top_three_moves_snake_case = [
        {underscore(key): value for (key, value) in top_move.items()}
        for top_move in top_three_moves
    ]

    try:
        top_three_moves = TypeAdapter(List[TopMove]).validate_python(
            top_three_moves_snake_case
        )
    except ValidationError as error:
        raise HTTPException(status_code=400, detail=error) from error

    return DataResponse[EvaluatePositionResponse](
        data=(
            EvaluatePositionResponse(
                evaluation=stockfish.get_evaluation(
                    floor(evaluate_position_request.time_to_analyze)
                ),
                wdl_stats=stockfish.get_wdl_stats(),
                top_three_moves=top_three_moves,
            )
        )
    )


@app.post("/analyze-move")
async def analyze_move(
    analyze_move_request: AnalyzeMoveRequest,
) -> DataResponse[AnalyzeMoveResponse]:
    """Analyzes whether the move will be a capture and the quality of the given move"""

    fen = analyze_move_request.fen
    move = analyze_move_request.move

    if not stockfish.is_fen_valid(fen):
        raise HTTPException(status_code=400, detail="Invalid FEN")

    stockfish.set_fen_position(fen)

    if not stockfish.is_move_correct(move):
        raise HTTPException(status_code=400, detail="Invalid move")

    is_move_capture = stockfish.will_move_be_a_capture(move)

    evaluation_before_move = stockfish.get_static_eval()
    stockfish.make_moves_from_current_position([move])
    evaluation_after_move = stockfish.get_static_eval()
    absolute_evaluation_change = evaluation_after_move - evaluation_before_move

    return DataResponse[AnalyzeMoveResponse](
        data=AnalyzeMoveResponse(
            is_move_capture=is_move_capture,
            evaluation_after_move=evaluation_after_move,
            absolute_evaluation_change=absolute_evaluation_change,
        )
    )

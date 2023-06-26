from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
import requests
import os
from datetime import datetime

board_bp = Blueprint("board_bp",  __name__, url_prefix="/boards")

@board_bp.route("", methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    if not "title" in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    return make_response({"board": new_board.to_dict()}, 201)



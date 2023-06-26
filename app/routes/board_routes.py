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

@board_bp.route("", methods=["GET"])
def get_boards():
    sort_direction_title = request.args.get("sort", default="desc")
    if sort_direction_title == "asc":
        all_boards = Board.query.order_by(Board.title.asc())
    else:
        all_boards = Board.query.order_by(Board.title.desc())
    
    sort_direction_owner = request.args.get("sort", default="desc")
    if sort_direction_owner == "asc":
        all_boards = Board.query.order_by(Board.owner.asc())
    else:
        all_boards = Board.query.order_by(Board.owner.desc())

    response = [board.to_dict() for board in all_boards]
    return jsonify(response), 200

@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_item(Board, board_id)
    return make_response({"task": board.to_dict()}, 200)

@board_bp.route("/<board_id>", methods=["PUT"])
def update_task(board_id):
    board = validate_item(Board, board_id)
    
    request_data = request.get_json()

    board.title = request_data["title"]
    board.owner = request_data["owner"]

    db.session.commit()

    return make_response({"board": board.to_dict()}, 200)

@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_one_task(board_id):
    task = validate_item(Board, board_id)
    
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}, 200)

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    return model.query.get_or_404(item_id, description=f"{model.__name__} with id {item_id} not found")


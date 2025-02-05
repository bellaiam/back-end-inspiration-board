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
    if "title" not in request_body:
        return ({"details": "Invalid data"}, 400)
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
    return make_response({"board": board.to_dict()}, 200)

#UNSURE WHY WE HAVE TWO OF THESE...
# @board_bp.route("/<board_id>", methods=["PUT"])
# def update_board(board_id):
#     board = validate_item(Board, board_id)
    
#     request_data = request.get_json()

#     board.title = request_data["title"]
#     board.owner = request_data["owner"]

#     db.session.commit()

#     return make_response({"board": board.to_dict()}, 200)

@board_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board = validate_item(Board, board_id)
    request_body = request.get_json()
    if not "title" in request_body:
        return make_response({"details": "Invalid data"}, 400)
    board = Board.from_dict(request_body)

    db.session.commit()
    return {"board": board.to_dict()}, 200

@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_one_card(board_id):
    board = validate_item(Board, board_id)
    
    db.session.delete(board)
    db.session.commit()
    return make_response({"details": f"Board {board.board_id} \"{board.title}\" successfully deleted"}, 200)

def validate_item(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {item_id}"}, 400))
    
    return model.query.get_or_404(item_id, description=f"{model.__name__} with id {item_id} not found")

#NESTED ROUTES
@board_bp.route("/<board_id>/cards", methods= ["POST"])
def post_cards_under_board(board_id):
    board = validate_item(Board, board_id)

    request_body = request.get_json()
    if "message" not in request_body:
        return ({"details": "Invalid data"}, 400)
    new_card = Card.from_dict(request_body)

    board.cards.append(new_card)  # Associate the card with the board
    #requests.post("https://slack.com/api/chat.postMessage", json={"channel": "task-notifications", "text": f"Someone created a new card {new_card.message}"}, headers={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"})

    db.session.add(new_card)
    db.session.commit()
    temp1 = {"channel": "task-notifications", "text": f"Someone created a new card {new_card.message}"}
    headers = {"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
    requests.post("https://slack.com/api/chat.postMessage", json=temp1, headers=headers)
    # print(temp1, headers)
    # return {"board_id": board.board_id, "card_id": new_card.card_id, "card": new_card.to_dict()}, 201
    return {"card": new_card.to_dict()}, 201

@board_bp.route("/<board_id>/cards", methods = ["GET"])
def get_cards_of_one_board(board_id):
    board = validate_item(Board, board_id)

    sort_query = request.args.get("sort")

    if sort_query is None:
        all_cards = Card.query.filter_by(board_id=board_id).all()
    elif sort_query == "by_id":
        all_cards = Card.query.filter_by(board_id=board_id).order_by(Card.card_id).all()
    elif sort_query == "alpha":
        all_cards = Card.query.filter_by(board_id=board_id).order_by(Card.message).all()
    elif sort_query == "likes":
        all_cards = Card.query.filter_by(board_id=board_id).order_by(Card.likes_count).all()

    cards_to_dict = [card.to_dict() for card in all_cards]
    return jsonify(id=board.board_id, title=board.title, owner=board.owner, cards=cards_to_dict), 200
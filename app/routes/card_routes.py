from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
import requests
from datetime import datetime
import os
from app.routes.board_routes import validate_item

card_bp = Blueprint("card_bp",  __name__, url_prefix="/cards")


@card_bp.route("", methods=["POST"])
def create_new_card():
    request_body = request.get_json()
    if "message" not in request_body:
        return ({"details": "Invalid data"}, 400)
    new_card = Card.from_dict(request_body)
    # new_card.likes_count=0
    # new_card.date_created="Sat, 01 Jan 2011 00:00:00 GMT"

    db.session.add(new_card)
    db.session.commit()
    # requests.post("https://slack.com/api/chat.postMessage", json={"channel": "task-notifications", "text": f"Someone created a new card {new_card.message}"}, headers={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"})
    return make_response({"card": new_card.to_dict()}, 201)

@card_bp.route("", methods=["GET"])
def get_cards():
    response = []

    all_cards = Card.query.all()

    response = [card.to_dict() for card in all_cards]
    return jsonify(response), 200

@card_bp.route("/<card_id>", methods=["GET"])
def get_card_by_id(card_id):
    card = validate_item(Card, card_id)
    return {"card": card.to_dict()}, 200

@card_bp.route("/<card_id>", methods=["PUT"])
def update_card(card_id):
    card = validate_item(Card, card_id)
    request_body = request.get_json()
    if not "message" in request_body:
        return make_response({"details": "Invalid data"}, 400)
    card = Card.from_dict(request_body)

    db.session.commit()
    return make_response({"card": card.to_dict()}, 200)

@card_bp.route("/<card_id>/likes_count", methods=["PATCH"])
def update_card_likes(card_id):
    card = validate_item(Card, card_id)
    request_body = request.get_json()
    if "likes_count" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    card.likes_count = request_body['likes_count']

    db.session.commit()
    return make_response({"card": card.to_dict()}, 200)

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):

    card = validate_item(Card, card_id)
    db.session.delete(card)
    db.session.commit()
    return {"details": f'Card {card_id} successfully deleted'}, 200


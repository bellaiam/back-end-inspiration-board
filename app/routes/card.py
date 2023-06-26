from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
import requests
from datetime import datetime
import os
from app.routes.board import validate_item

card_bp = Blueprint("card_bp",  __name__, url_prefix="/cards")


@card_bp.route("", methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    if not "message" in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_card = Card.from_dict(request_body)

    db.session.add(new_card)
    db.session.commit()

    return make_response({"card": new_card.to_dict()}, 201)
import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card
from datetime import datetime
from flask.signals import request_finished


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

# This fixture gets called in every test that
# references "one_board"
# This fixture creates a board and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(
        title="Happy Board", owner="Bella")
    db.session.add(new_board)
    db.session.commit()

# This fixture gets called in every test that
# references "three_cards"
# This fixture creates three cards and saves
# them in the database
@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Card(
            message="1st Card", likes_count=1,date_created="06/28/2023" ),
        Card(
            message="2nd Card", likes_count=2,date_created="06/28/2023"),
        Card(
            message="3rd Card", likes_count=3,date_created="06/28/2023")
    ])
    db.session.commit()

# This fixture gets called in every test that
# references "one_card"
# This fixture creates a card and saves it in the database
@pytest.fixture
def one_card(app):
    new_card = Card(message="Happy Card", likes_count=1,date_created="06/28/2023")
    db.session.add(new_card)
    db.session.commit()

# This fixture gets called in every test that
# references "one_task_belongs_to_one_goal"
# This fixture creates a task and a goal
# It associates the goal and task, so that the
# goal has this task, and the task belongs to one goal
@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    card = card.query.first()
    board = Board.query.first()
    board.tasks.append(card)
    db.session.commit()
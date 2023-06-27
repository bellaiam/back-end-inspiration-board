from app import db
class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String)
    owner = db.Column(db.String)

    card_id = db.Column(db.Integer, db.ForeignKey('card.card_id'), nullable=True)
    card = db.relationship("Card", back_populates="boards")


    def to_dict(self):
        return {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }

    @classmethod
    def from_dict(cls, board_data):
        return cls(
            title=board_data["title"],
            owner=board_data["owner"]
        )
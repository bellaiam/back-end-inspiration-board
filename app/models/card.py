from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    day_created = db.Column(db.DateTime, nullable=True)

    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)
    board = db.relationship("Board", back_populates="cards")


    def to_dict(self):
        card_dict = {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
            "day_created": self.day_created
        }
        if self.board_id:
            card_dict["board_id"] = self.board_id
        return card_dict


    @classmethod
    def from_dict(cls, card_data):
        return cls(
            message=card_data["message"],
            likes_count=card_data["likes_count"],
            day_created=card_data["day_created"]
        )
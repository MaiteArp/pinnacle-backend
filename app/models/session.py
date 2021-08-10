from app import db

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)
    user = db.relationship('User', lazy=True)


    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }
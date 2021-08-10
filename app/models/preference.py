from app import db

class Preference(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    key = db.Column(db.String, primary_key=True)
    value = db.Column(db.String)


    def to_json(self):
        return {
            "user_id": self.user_id,
            "key": self.key,
            "value": self.value,
        }

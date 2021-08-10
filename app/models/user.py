from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    coins = db.Column(db.Integer, default=0)
    best_time = db.Column(db.Interval)
    


    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            # "password": self.password,
            "coins": self.coins,
            "best_time": self.best_time,
        }

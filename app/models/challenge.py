from app import db

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    challenger_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('user.id')) #user will send challenge to 'user name' I'll have to match to user id
    challenger = db.relationship('User', foreign_keys="Challenge.challenger_id")
    destination = db.relationship('User', foreign_keys="Challenge.destination_id")

    winner = db.Column(db.Integer)# turn this to string
    
    cha_time = db.Column(db.Integer)# repsonse time
    sent_time = db.Column(db.Integer)
    # store incorrect questions

    def to_json(self):
        return {
            "id": self.id,
            
            "challenger_id": self.challenger_id,
            "destination_id": self.destination_id,
            "winner": self.winner,
            
            "cha_time": self.cha_time,
            "sent_time": self.sent_time,
        }
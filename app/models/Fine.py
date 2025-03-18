from app import db

class Fine(db.Model):
    __tablename__ = 'fines'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum('Unpaid', 'Paid'), default='Unpaid')

    user = db.relationship('User', backref=db.backref('fines', lazy=True))

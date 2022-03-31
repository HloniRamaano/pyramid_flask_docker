from app import db
from sqlalchemy.dialects.postgresql import JSON


class List(db.Model):
    __tablename__ = 'list'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String())

    def __init__(self, item):
        self.item = item

    def __repr__(self):
        return '<id {}>'.format(self.id)
from .db import db

class ProductModel(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"ProductModel(name = {self.name}, desc = {self.desc}, is_available = {self.is_available})"
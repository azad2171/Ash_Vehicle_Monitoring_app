from database import db


class Silo(db.Model):
    __tablename__ = "silo"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    capacity_mt = db.Column(db.Float)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Silo {self.name}>"

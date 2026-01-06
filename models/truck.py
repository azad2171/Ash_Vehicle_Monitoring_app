from datetime import datetime
from database import db


class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    truck_number = db.Column(db.String(50), unique=True, nullable=False)
    qr_code = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

from datetime import datetime
from database import db


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    truck_id = db.Column(db.Integer, db.ForeignKey("truck.id"), nullable=False)

    gate_in_time = db.Column(db.DateTime, nullable=False)
    gate_out_time = db.Column(db.DateTime)

    empty_weight = db.Column(db.Float)  # tons
    loaded_weight = db.Column(db.Float)  # tons
    ash_quantity = db.Column(db.Float)  # tons

    turnaround_minutes = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

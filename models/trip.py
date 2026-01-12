from database import db


class Trip(db.Model):
    __tablename__ = "trip"

    id = db.Column(db.Integer, primary_key=True)

    truck_id = db.Column(db.Integer, db.ForeignKey("truck.id"), nullable=False)

    trip_type = db.Column(db.String(20))

    silo_id = db.Column(db.Integer, db.ForeignKey("silo.id"), nullable=True)
    party_id = db.Column(db.Integer, db.ForeignKey("party.id"), nullable=True)

    gate_in_time = db.Column(db.DateTime)
    gate_out_time = db.Column(db.DateTime)

    empty_weight = db.Column(db.Float)
    loaded_weight = db.Column(db.Float)
    ash_quantity = db.Column(db.Float)

    turnaround_minutes = db.Column(db.Float)
    status = db.Column(db.String(20))
    remarks = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)

    # Relationships
    truck = db.relationship("Truck", backref="trips")
    silo = db.relationship("Silo")
    party = db.relationship("Party")

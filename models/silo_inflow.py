from datetime import datetime
from database import db


class SiloInflow(db.Model):
    __tablename__ = "silo_inflow"

    id = db.Column(db.Integer, primary_key=True)

    silo_id = db.Column(db.Integer, db.ForeignKey("silo.id"), nullable=False)

    quantity_mt = db.Column(db.Float, nullable=False)

    inflow_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    remarks = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    silo = db.relationship("Silo", backref="inflows")

    def __repr__(self):
        return f"<SiloInflow {self.quantity_mt} MT into {self.silo.name}>"

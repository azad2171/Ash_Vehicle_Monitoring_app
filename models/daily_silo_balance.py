from database import db


class DailySiloBalance(db.Model):
    __tablename__ = "daily_silo_balance"

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date, nullable=False)
    silo_id = db.Column(db.Integer, db.ForeignKey("silo.id"), nullable=False)

    opening_stock = db.Column(db.Float, nullable=False)
    inflow_mt = db.Column(db.Float, nullable=False)
    dispatched_mt = db.Column(db.Float, nullable=False)
    closing_stock = db.Column(db.Float, nullable=False)

    remarks = db.Column(db.String(255))
    day_closed = db.Column(db.Boolean, default=False)

    silo = db.relationship("Silo")

    __table_args__ = (db.UniqueConstraint("date", "silo_id", name="uq_date_silo"),)

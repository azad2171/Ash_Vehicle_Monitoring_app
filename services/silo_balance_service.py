from datetime import date, timedelta
from sqlalchemy import func
from database import db
from models.silo import Silo
from models.trip import Trip
from models.silo_inflow import SiloInflow
from models.daily_silo_balance import DailySiloBalance


def calculate_daily_balance(target_date):
    silos = Silo.query.filter_by(active=True).all()

    for silo in silos:
        # Previous closing stock
        prev_day = target_date - timedelta(days=1)
        prev_balance = DailySiloBalance.query.filter_by(
            date=prev_day, silo_id=silo.id
        ).first()

        opening_stock = prev_balance.closing_stock if prev_balance else 0

        inflow = (
            db.session.query(func.coalesce(func.sum(SiloInflow.quantity_mt), 0))
            .filter(
                SiloInflow.silo_id == silo.id,
                func.date(SiloInflow.inflow_time) == target_date,
            )
            .scalar()
        )

        dispatch = (
            db.session.query(func.coalesce(func.sum(Trip.ash_quantity), 0))
            .filter(
                Trip.silo_id == silo.id, func.date(Trip.gate_out_time) == target_date
            )
            .scalar()
        )

        closing_stock = opening_stock + inflow - dispatch

        balance = DailySiloBalance.query.filter_by(
            date=target_date, silo_id=silo.id
        ).first()

        if not balance:
            balance = DailySiloBalance(
                date=target_date,
                silo_id=silo.id,
                opening_stock=opening_stock,
                inflow_mt=inflow,
                dispatched_mt=dispatch,
                closing_stock=closing_stock,
            )
            db.session.add(balance)
        else:
            balance.opening_stock = opening_stock
            balance.inflow_mt = inflow
            balance.dispatched_mt = dispatch
            balance.closing_stock = closing_stock

    db.session.commit()

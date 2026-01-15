from flask import Blueprint, render_template, request, redirect, url_for
from models.silo import Silo
from models.silo_inflow import SiloInflow
from database import db
from datetime import datetime

inflow_bp = Blueprint("inflow", __name__)


@inflow_bp.route("/inflow/add", methods=["GET", "POST"])
def add_inflow():
    silos = Silo.query.filter_by(active=True).all()

    if request.method == "POST":
        inflow = SiloInflow(
            silo_id=request.form["silo_id"],
            quantity_mt=float(request.form["quantity"]),
            inflow_time=datetime.now(),
            remarks=request.form.get("remarks"),
        )
        db.session.add(inflow)
        db.session.commit()

        return redirect(url_for("dashboard.daily_balance_view"))

    return render_template("add_inflow.html", silos=silos)

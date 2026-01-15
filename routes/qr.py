from flask import Blueprint, redirect, url_for, abort
from models.truck import Truck

qr_bp = Blueprint("qr", __name__)


@qr_bp.route("/qr/scan/<qr_code>")
def scan_qr(qr_code):
    truck = Truck.query.filter_by(qr_code=qr_code).first()

    if not truck:
        abort(404, description="Invalid QR code")

    # Redirect to Add Trip page with truck prefilled
    return redirect(url_for("trucks.add_trip", truck_id=truck.id))

from datetime import datetime, timedelta
from database import db
from models.truck import Truck
from models.trip import Trip


def get_or_create_truck(truck_number):
    truck = Truck.query.filter_by(truck_number=truck_number).first()
    if not truck:
        truck = Truck(truck_number=truck_number)
        db.session.add(truck)
        db.session.commit()
    return truck


def seed():
    print("🌱 Seeding sample data...")

    sample_days = [
        # date, bagging_nos, bagging_mt, bulkers_nos, bulkers_mt, rake_nos, rake_mt, remarks
        ("2025-04-01", 33, 1566.46, 28, 1566.46, 0, 0, ""),
        ("2025-04-02", 15, 63.00, 28, 1449.34, 0, 0, ""),
        ("2025-04-03", 41, 1738.80, 27, 1483.08, 1, 3997.57, ""),
        ("2025-04-04", 34, 1457.40, 31, 1562.58, 0, 0, "No demand from consumer"),
        ("2025-04-05", 4, 201.60, 20, 1026.98, 0, 0, "No demand from consumer"),
    ]

    for row in sample_days:
        date_str, b_nos, b_mt, bl_nos, bl_mt, r_nos, r_mt, remarks = row
        base_date = datetime.strptime(date_str, "%Y-%m-%d")

        # BAGGING
        for i in range(b_nos):
            truck = get_or_create_truck(f"BAG-{i + 1:03}")
            trip = Trip(
                truck_id=truck.id,
                trip_type="BAGGING",
                gate_in_time=base_date + timedelta(minutes=i * 10),
                gate_out_time=base_date + timedelta(minutes=i * 10 + 60),
                empty_weight=10,
                loaded_weight=10 + (b_mt / max(b_nos, 1)),
                ash_quantity=round(b_mt / max(b_nos, 1), 2),
                turnaround_minutes=60,
                status="completed",
                remarks=remarks,
            )
            db.session.add(trip)

        # BULKERS
        for i in range(bl_nos):
            truck = get_or_create_truck(f"BULK-{i + 1:03}")
            trip = Trip(
                truck_id=truck.id,
                trip_type="BULKERS",
                gate_in_time=base_date + timedelta(minutes=i * 12),
                gate_out_time=base_date + timedelta(minutes=i * 12 + 75),
                empty_weight=12,
                loaded_weight=12 + (bl_mt / max(bl_nos, 1)),
                ash_quantity=round(bl_mt / max(bl_nos, 1), 2),
                turnaround_minutes=75,
                status="completed",
                remarks=remarks,
            )
            db.session.add(trip)

        # RAKE
        for i in range(r_nos):
            truck = get_or_create_truck(f"RAKE-{i + 1:03}")
            trip = Trip(
                truck_id=truck.id,
                trip_type="RAKE",
                gate_in_time=base_date + timedelta(hours=2),
                gate_out_time=base_date + timedelta(hours=10),
                empty_weight=200,
                loaded_weight=200 + r_mt,
                ash_quantity=r_mt,
                turnaround_minutes=480,
                status="completed",
            )
            db.session.add(trip)

    db.session.commit()
    print("✅ Sample data seeded successfully.")

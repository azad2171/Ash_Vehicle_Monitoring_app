from database import db
from models.silo import Silo
from models.party import Party


def seed():
    print("🌱 Seeding silo and party master data...")

    # Silos
    silos = ["ST-I", "ST-II"]
    for name in silos:
        if not Silo.query.filter_by(name=name).first():
            db.session.add(Silo(name=name))

    # Sample parties (can be edited later)
    parties = [
        "ABC Cement Ltd",
        "XYZ Infra",
        "Road Construction Dept",
        "Railways Contractor",
    ]

    for name in parties:
        if not Party.query.filter_by(name=name).first():
            db.session.add(Party(name=name))

    db.session.commit()
    print("✅ Master data seeded successfully")

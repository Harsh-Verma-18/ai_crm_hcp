from app.database import SessionLocal, engine, Base
from app.models.hcp import HCP
from app.models.product import Product
from app.models.hospital import Hospital
 
Base.metadata.create_all(bind=engine)
 
db = SessionLocal()
 
try:
    if db.query(HCP).count() == 0:
        db.add_all(
            [
                HCP(
                    name="Aditi Rao",
                    speciality="Cardiology",
                    hospital="Fortis Hospital",
                    city="Mumbai",
                    email="aditi.rao@example.com",
                    phone="9876500001",
                ),
                HCP(
                    name="Sanjay Mehta",
                    speciality="Oncology",
                    hospital="Tata Memorial",
                    city="Mumbai",
                    email="sanjay.mehta@example.com",
                    phone="9876500002",
                ),
                HCP(
                    name="Priya Nair",
                    speciality="Endocrinology",
                    hospital="Apollo Hospital",
                    city="Chennai",
                    email="priya.nair@example.com",
                    phone="9876500003",
                ),
            ]
        )
 
    if db.query(Product).count() == 0:
        db.add_all(
            [
                Product(
                    name="CardioPlus 10mg",
                    description="Antihypertensive tablet",
                    usage="Once daily for hypertension management",
                ),
                Product(
                    name="OncoShield IV",
                    description="Targeted therapy infusion",
                    usage="Administered every 3 weeks per oncology protocol",
                ),
            ]
        )
 
    if db.query(Hospital).count() == 0:
        db.add_all(
            [
                Hospital(
                    name="Fortis Hospital",
                    address="Mulund, Mumbai",
                    city="Mumbai",
                    contact="022-12345678",
                ),
                Hospital(
                    name="Apollo Hospital",
                    address="Greams Road, Chennai",
                    city="Chennai",
                    contact="044-87654321",
                ),
            ]
        )
 
    db.commit()
    print("Seed data inserted.")
finally:
    db.close()
 
from app import app
from users.models import db, Citizen, GovEmployee, ServiceProvider

# Create the dummy data inside the App Context
with app.app_context():
    # 1. Clear old data (Optional, to start fresh)
    db.drop_all()
    db.create_all()
    print("🧹 Database cleared and recreated.")

    # 2. Create an ADMIN (Health Sector)
    admin = GovEmployee(
        full_name="Dr. Rajesh Gupta",
        email="admin@health.gov.in",
        password_hash="admin123",  # Plain text for now
        department="Health Ministry",
        sector="Health",
        role="admin"
    )

    # 3. Create a CITIZEN
    citizen = Citizen(
        full_name="Amit Sharma",
        email="amit@gmail.com",
        password_hash="citizen123",
        phone="9876543210"
    )

    # 4. Create a SERVICE PROVIDER (Contractor)
    provider = ServiceProvider(
        company_name="BuildWell Constructions",
        email="provider@contractor.com",
        password_hash="provider123",
        service_type="Construction",
        role="provider"
    )

    # 5. Add and Commit to DB
    db.session.add(admin)
    db.session.add(citizen)
    db.session.add(provider)
    db.session.commit()

    print("✅ Mock Users Added Successfully!")
    print("------------------------------------------------")
    print("Login as Admin:    admin@health.gov.in  / admin123")
    print("Login as Citizen:  amit@gmail.com       / citizen123")
    print("Login as Provider: provider@contractor.com / provider123")
    print("------------------------------------------------")
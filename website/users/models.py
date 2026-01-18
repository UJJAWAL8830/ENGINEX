from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize DB (This is the instance imported by app.py)
db = SQLAlchemy()

# 1. CITIZEN TABLE
class Citizen(UserMixin, db.Model):
    __tablename__ = 'citizens'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    # Add other citizen fields as needed

# 2. GOVERNMENT EMPLOYEE TABLE (Admins)
class GovEmployee(UserMixin, db.Model):
    __tablename__ = 'gov_employees'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(150))
    department = db.Column(db.String(100)) # e.g., 'Health', 'Agriculture'
    sector = db.Column(db.String(100))     # e.g., 'Health', 'Agriculture'
    role = db.Column(db.String(50), default='admin')

# 3. SERVICE PROVIDER TABLE (Contractors)
class ServiceProvider(UserMixin, db.Model):
    __tablename__ = 'service_providers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(150))
    service_type = db.Column(db.String(100)) # e.g., 'Construction', 'Plumbing'
    role = db.Column(db.String(50), default='provider')

# 4. HOSPITAL TABLE (For Admin Dashboard)
class Hospital(db.Model):
    __tablename__ = 'hospitals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300), nullable=True)
    type = db.Column(db.String(50), default="Govt Hospital")
    beds = db.Column(db.Integer, default=0)
    contact = db.Column(db.String(20), nullable=True)
    
    # Optional: Fields from your earlier request
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Hospital {self.name}>'

# 5. DOCTOR TABLE (Optional, keep if you need it later)
class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
# --- AGRICULTURE MODEL ---
class AgriMarket(db.Model):
    __tablename__ = 'agri_market'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)   # e.g. Wheat, Rice
    market_name = db.Column(db.String(150), nullable=False) # e.g. Azadpur Mandi
    price = db.Column(db.String(50), nullable=False)        # e.g. ₹2,400 / Quintal
    status = db.Column(db.String(50))                       # e.g. Rising / Falling / Stable
    updated_date = db.Column(db.String(50))                 # e.g. 18 Jan 2026

# class Citizen(UserMixin, db.Model):
#     __tablename__ = 'citizens'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True, nullable=False)
#     password_hash = db.Column(db.String(200), nullable=False)
#     full_name = db.Column(db.String(150))
#     phone = db.Column(db.String(20))
    
#     # Basic Profile Data (For later use)
#     age = db.Column(db.Integer)
#     occupation = db.Column(db.String(100))
#     state = db.Column(db.String(100))
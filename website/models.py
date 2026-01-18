from . import db
from flask_login import UserMixin
from datetime import datetime

class Citizens(db.Model, UserMixin):
    __tablename__ = 'citizens'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Govt(db.Model, UserMixin):
    __tablename__ = 'govt'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    national_id = db.Column(db.String(50), unique=True, nullable=False)
    # Sector: 'Health', 'Agriculture', 'Security' [cite: 21, 26]
    sector = db.Column(db.String(20), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServiceProviders(db.Model, UserMixin):
    __tablename__ = 'service_providers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Scheme(db.Model):
    __tablename__ = 'schemes'
    id = db.Column(db.Integer, primary_key=True)
    scheme_name = db.Column(db.String(255), nullable=False)
    scheme_description = db.Column(db.Text, nullable=False)
    
    # Target Stakeholders (e.g., "Farmers", "Low-income families", "Urban residents")
    end_user = db.Column(db.String(150), nullable=False) 
    
    # Department/Sector (e.g., "Health", "Agriculture", "Security")
    department = db.Column(db.String(50), nullable=False) 
    
    minister_handling = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


from . import db
from datetime import datetime

class Complaint(db.Model):
    __tablename__ = 'complaints'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False) # e.g., 'Waste', 'Roads', 'Water'
    status = db.Column(db.String(20), default='Pending') # 'Pending', 'In Progress', 'Resolved'
    
    # Location data to address urban digital divides [cite: 55]
    city = db.Column(db.String(100), nullable=False)
    
    # Relationship to the Citizen who filed it
    citizen_id = db.Column(db.Integer, db.ForeignKey('citizens.id'), nullable=False)
    date_filed = db.Column(db.DateTime, default=datetime.utcnow)
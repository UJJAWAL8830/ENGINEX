from .. import db # Imports from the central website/__init__.py
from datetime import datetime
from sqlalchemy.sql import func

class AgriCenter(db.Model):
    __tablename__ = 'agri_centers'
    
    id = db.Column(db.Integer, primary_key=True)
    center_name = db.Column(db.String(200), nullable=False)
    
    # Location details for regional diversity and rural connectivity 
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    village_block = db.Column(db.String(100)) # Specific to rural agricultural needs [cite: 55]
    
    # Contact and Management
    contact_number = db.Column(db.String(20), nullable=False)
    manager_name = db.Column(db.String(150))
    
    # Service capability [cite: 35]
    # Examples: 'Seed Distribution', 'Soil Testing', 'Equipment Rental'
    primary_service = db.Column(db.String(100), nullable=False)
    
    # System metadata for dashboard tracking 
    is_active = db.Column(db.Boolean, default=True)
    date_established = db.Column(db.DateTime, default=datetime.utcnow)
# <<<<<<< Database


# class AgriComplaint(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
    
#     # 1. Foreign Key linking to the Citizen
#     citizen_id = db.Column(db.Integer, db.ForeignKey('citizens.id'), nullable=False)
    
#     # 2. Form Fields based on UI image_34ff48.png
#     issue_type = db.Column(db.String(100), nullable=False) # e.g., 'Crop Insurance', 'Mandi Prices'
#     description = db.Column(db.Text, nullable=False)
#     evidence_url = db.Column(db.String(255)) # Stores path to the uploaded photo
    
#     # 3. Metadata for Tracking
#     status = db.Column(db.String(20), default='Pending') # Pending, In Progress, Resolved
#     date_submitted = db.Column(db.DateTime(timezone=True), default=func.now())
    
#     # Relationship to easily access citizen details from a complaint
#     citizen = db.relationship('Citizens', backref='agri_complaints')
# =======
# >>>>>>> main

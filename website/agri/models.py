from .. import db # Imports from the central website/__init__.py
from datetime import datetime

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

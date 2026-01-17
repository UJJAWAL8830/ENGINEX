from .. import db # Import the db instance from the website folder
from datetime import datetime

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    # Relationship to link doctors to this hospital
    doctors = db.relationship('Doctor', backref='hospital_location', lazy=True)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    specialization = db.Column(db.String(100)) # Bonus for medical detail
    
    # Foreign Key linking to Hospital
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    
    # Though hospital details are in the Hospital table, 
    # you can store city/state here if you want independent records
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
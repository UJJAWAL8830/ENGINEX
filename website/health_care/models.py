from . import db  # Importing db from the current package (users/__init__.py or similar)
# If your db is in the main website/__init__.py, use: from website import db

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
    # Fields from your request
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    
    # Fields needed for the Admin Dashboard to work
    address = db.Column(db.String(200), nullable=True) # Full address
    type = db.Column(db.String(50), default="Govt Hospital") # e.g. Private/Govt
    beds = db.Column(db.Integer, default=0)
    contact = db.Column(db.String(20), nullable=True)

    # Relationship to link doctors to this hospital
    doctors = db.relationship('Doctor', backref='hospital_location', lazy=True)

    def __repr__(self):
        return f'<Hospital {self.name} - {self.city}>'

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    
    # Foreign Key linking to Hospital
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    
    # Independent location records (as per your request)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Doctor {self.name} - {self.specialization}>'
from app import db

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_number = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False)
    start_point = db.Column(db.String(128), nullable=False)
    end_point = db.Column(db.String(128), nullable=False)
    color_code = db.Column(db.String(7), nullable=False, default="#007bff")  # Hex color code
    buses = db.relationship('Bus', backref='route', lazy=True)
    
    def __repr__(self):
        return f'<Route {self.route_number}: {self.name}>'

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    employee_id = db.Column(db.String(20), nullable=False, unique=True)
    license_number = db.Column(db.String(20), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="Available")  # Available, On Duty, Off Duty, On Leave
    buses = db.relationship('Bus', backref='assigned_driver', lazy=True)
    
    def __repr__(self):
        return f'<Driver {self.employee_id}: {self.name}>'

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(20), nullable=False, unique=True)
    registration = db.Column(db.String(20), nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Active")  # Active, Maintenance, Out of Service
    current_location_lat = db.Column(db.Float, nullable=True)
    current_location_lng = db.Column(db.Float, nullable=True)
    on_time_status = db.Column(db.String(20), nullable=False, default="On Time")  # On Time, Delayed, Ahead of Schedule
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=True)
    
    def __repr__(self):
        return f'<Bus {self.bus_number}>'

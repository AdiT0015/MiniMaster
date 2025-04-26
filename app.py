import os
import logging
import json

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "bus_management_system_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure the PostgreSQL database
database_url = os.environ.get("DATABASE_URL")
if database_url:
    # Fix for SQLAlchemy 1.4+ compatibility with postgres://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
else:
    database_url = "sqlite:///bus_management.db"
    logging.warning("DATABASE_URL not found, using SQLite as fallback")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Route definitions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/routes')
def routes():
    return render_template('routes.html')

@app.route('/drivers')
def drivers():
    return render_template('drivers.html')

@app.route('/buses')
def buses():
    from models import Bus, Route, Driver
    buses = Bus.query.all()
    
    # Count the number of buses by status
    active_buses = sum(1 for bus in buses if bus.status == 'Active')
    maintenance_buses = sum(1 for bus in buses if bus.status == 'Maintenance')
    
    for i, bus in enumerate(buses):
        # Add the driver and route as attributes directly
        bus.driver = Driver.query.get(bus.driver_id) if bus.driver_id else None
        bus.route = Route.query.get(bus.route_id) if bus.route_id else None
    
    return render_template('buses.html', 
                         buses=buses, 
                         active_buses=active_buses, 
                         maintenance_buses=maintenance_buses)

@app.route('/tracking')
def tracking():
    return render_template('tracking.html')

# API Endpoints
@app.route('/api/routes', methods=['GET'])
def get_routes():
    from models import Route
    routes_data = Route.query.all()
    routes_list = []
    for route in routes_data:
        routes_list.append({
            'id': route.id,
            'route_number': route.route_number,
            'name': route.name,
            'start_point': route.start_point,
            'end_point': route.end_point,
            'color_code': route.color_code
        })
    return jsonify(routes_list)

@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    from models import Driver
    drivers_data = Driver.query.all()
    drivers_list = []
    for driver in drivers_data:
        drivers_list.append({
            'id': driver.id,
            'name': driver.name,
            'employee_id': driver.employee_id,
            'license_number': driver.license_number,
            'phone': driver.phone,
            'email': driver.email,
            'status': driver.status
        })
    return jsonify(drivers_list)

@app.route('/api/buses', methods=['GET'])
def get_buses():
    from models import Bus, Route, Driver
    buses_data = Bus.query.all()
    buses_list = []
    for bus in buses_data:
        route_name = None
        route_number = None
        route_color = None
        driver_name = None
        
        if bus.route:
            route_name = bus.route.name
            route_number = bus.route.route_number
            route_color = bus.route.color_code
            
        if bus.assigned_driver:
            driver_name = bus.assigned_driver.name
            
        buses_list.append({
            'id': bus.id,
            'bus_number': bus.bus_number,
            'registration': bus.registration,
            'capacity': bus.capacity,
            'status': bus.status,
            'current_location_lat': bus.current_location_lat,
            'current_location_lng': bus.current_location_lng,
            'on_time_status': bus.on_time_status,
            'route_id': bus.route_id,
            'driver_id': bus.driver_id,
            'route_name': route_name,
            'route_number': route_number,
            'route_color': route_color,
            'driver_name': driver_name
        })
    return jsonify(buses_list)

@app.route('/api/buses/<int:bus_id>/location', methods=['PUT'])
def update_bus_location(bus_id):
    from models import Bus
    data = request.json
    bus = Bus.query.get_or_404(bus_id)
    
    if 'lat' in data and 'lng' in data:
        bus.current_location_lat = data['lat']
        bus.current_location_lng = data['lng']
        
        if 'on_time_status' in data:
            bus.on_time_status = data['on_time_status']
            
        db.session.commit()
        return jsonify({'success': True}), 200
    
    return jsonify({'error': 'Missing location data'}), 400

with app.app_context():
    # Import the models here to ensure tables are created
    import models  # noqa: F401
    db.create_all()
    
    # Initialize sample data if tables are empty
    if models.Route.query.count() == 0:
        # Add sample routes in Haryana, India
        routes = [
            models.Route(route_number="GH1", name="Gurugram-Hisar Express", start_point="Gurugram", end_point="Hisar", color_code="#e74c3c"),
            models.Route(route_number="FP2", name="Faridabad-Panipat Local", start_point="Faridabad", end_point="Panipat", color_code="#3498db"),
            models.Route(route_number="AR3", name="Ambala-Rohtak Express", start_point="Ambala", end_point="Rohtak", color_code="#2ecc71"),
            models.Route(route_number="KS4", name="Karnal-Sonipat Express", start_point="Karnal", end_point="Sonipat", color_code="#f39c12"),
            models.Route(route_number="YR5", name="Yamunanagar-Rewari", start_point="Yamunanagar", end_point="Rewari", color_code="#9b59b6")
        ]
        db.session.add_all(routes)
        db.session.commit()
        
        # Add sample drivers with Indian names
        drivers = [
            models.Driver(name="Rajesh Kumar", employee_id="D001", license_number="HR-12345", phone="(91) 9876-123456", email="rajesh.kumar@example.com", status="On Duty"),
            models.Driver(name="Priya Sharma", employee_id="D002", license_number="HR-23456", phone="(91) 9876-234567", email="priya.sharma@example.com", status="On Duty"),
            models.Driver(name="Amit Singh", employee_id="D003", license_number="HR-34567", phone="(91) 9876-345678", email="amit.singh@example.com", status="On Duty"),
            models.Driver(name="Sunita Patel", employee_id="D004", license_number="HR-45678", phone="(91) 9876-456789", email="sunita.patel@example.com", status="On Duty"),
            models.Driver(name="Vikram Verma", employee_id="D005", license_number="HR-56789", phone="(91) 9876-567890", email="vikram.verma@example.com", status="Available"),
            models.Driver(name="Anjali Gupta", employee_id="D006", license_number="HR-67890", phone="(91) 9876-678901", email="anjali.gupta@example.com", status="Available"),
            models.Driver(name="Manish Yadav", employee_id="D007", license_number="HR-78901", phone="(91) 9876-789012", email="manish.yadav@example.com", status="Off Duty"),
            models.Driver(name="Neha Malhotra", employee_id="D008", license_number="HR-89012", phone="(91) 9876-890123", email="neha.malhotra@example.com", status="On Leave")
        ]
        db.session.add_all(drivers)
        db.session.commit()
        
        # Get routes and drivers for reference
        route_gh1 = models.Route.query.filter_by(route_number="GH1").first()
        route_fp2 = models.Route.query.filter_by(route_number="FP2").first()
        route_ar3 = models.Route.query.filter_by(route_number="AR3").first()
        
        driver_rajesh = models.Driver.query.filter_by(employee_id="D001").first()
        driver_priya = models.Driver.query.filter_by(employee_id="D002").first()
        driver_amit = models.Driver.query.filter_by(employee_id="D003").first()
        
        # Add sample buses with Haryana locations
        buses = [
            models.Bus(bus_number="HR1001", registration="HR-1234", capacity=42, status="Active", 
                       current_location_lat=28.4595, current_location_lng=77.0266, 
                       on_time_status="On Time", route_id=route_gh1.id, driver_id=driver_rajesh.id),
            models.Bus(bus_number="HR1002", registration="HR-2345", capacity=36, status="Active", 
                       current_location_lat=29.1492, current_location_lng=76.6133, 
                       on_time_status="Delayed", route_id=route_fp2.id, driver_id=driver_priya.id),
            models.Bus(bus_number="HR1003", registration="HR-3456", capacity=42, status="Active", 
                       current_location_lat=29.6857, current_location_lng=76.9905, 
                       on_time_status="On Time", route_id=route_ar3.id, driver_id=driver_amit.id)
        ]
        db.session.add_all(buses)
        db.session.commit()
        
        logging.info("Sample data initialized successfully!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

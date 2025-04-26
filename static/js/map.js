// Map management for bus tracking functionality

let map;
let busMarkers = {};
let routes = {};

// Initialize the map
function initMap() {
    // Create map centered at a default location (can be adjusted based on your service area)
    map = L.map('map').setView([40.7128, -74.0060], 12);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Fetch initial bus locations
    fetchBusLocations();
    
    // Set up periodic updates (every 30 seconds)
    setInterval(fetchBusLocations, 30000);
    
    // Add route controls to the sidebar
    setupRouteControls();
}

// Custom bus icon
function createBusIcon(color = '#3498db') {
    return L.divIcon({
        className: 'bus-icon',
        html: `<div style="background-color: ${color}"></div>`,
        iconSize: [20, 20]
    });
}

// Fetch bus locations from the server
function fetchBusLocations() {
    // In a real implementation, this would make an API call to get real-time bus data
    // For this demo, we'll use simulated data
    
    const busLocations = simulateBusLocations();
    updateBusMarkers(busLocations);
    updateBusList(busLocations);
}

// Update bus markers on the map
function updateBusMarkers(buses) {
    buses.forEach(bus => {
        // Get route color for the bus
        const routeColor = bus.routeColor || '#3498db';
        
        if (busMarkers[bus.id]) {
            // Update existing marker
            busMarkers[bus.id].setLatLng([bus.lat, bus.lng]);
            
            // Update popup content
            const popupContent = createBusPopupContent(bus);
            busMarkers[bus.id].getPopup().setContent(popupContent);
        } else {
            // Create new marker
            const busIcon = createBusIcon(routeColor);
            const marker = L.marker([bus.lat, bus.lng], { icon: busIcon })
                .addTo(map)
                .bindPopup(createBusPopupContent(bus));
                
            busMarkers[bus.id] = marker;
        }
    });
    
    // Remove markers for buses no longer in the list
    Object.keys(busMarkers).forEach(id => {
        if (!buses.some(bus => bus.id.toString() === id)) {
            map.removeLayer(busMarkers[id]);
            delete busMarkers[id];
        }
    });
}

// Create popup content for bus markers
function createBusPopupContent(bus) {
    return `
        <div class="bus-popup">
            <h6>Bus ${bus.busNumber}</h6>
            <p>Route: ${bus.routeName} (${bus.routeNumber})</p>
            <p>Status: ${bus.status}</p>
            <p>Driver: ${bus.driverName}</p>
            <p>Speed: ${bus.speed} km/h</p>
            <p>Last Updated: ${bus.lastUpdated}</p>
        </div>
    `;
}

// Update the bus list in the sidebar
function updateBusList(buses) {
    const busList = document.getElementById('bus-list');
    if (!busList) return;
    
    busList.innerHTML = '';
    
    buses.forEach(bus => {
        const busElement = document.createElement('div');
        busElement.className = 'card mb-2';
        busElement.innerHTML = `
            <div class="card-body py-2">
                <h6 class="card-title mb-1">Bus ${bus.busNumber}</h6>
                <p class="card-text mb-1 small">
                    <span data-status="${bus.status}" class="d-inline-block me-2">${bus.status}</span>
                    Route: <span data-route-color="${bus.routeColor}" class="fw-bold">${bus.routeNumber}</span>
                </p>
                <button class="btn btn-sm btn-secondary mt-1" onclick="focusOnBus(${bus.id})">
                    Locate
                </button>
            </div>
        `;
        busList.appendChild(busElement);
        
        // Add status indicator and route color manually since the main.js event listener won't catch dynamically added elements
        const statusEl = busElement.querySelector('[data-status]');
        const status = statusEl.dataset.status.toLowerCase().replace(' ', '-');
        const indicator = document.createElement('span');
        indicator.classList.add('status-indicator', `status-${status}`);
        statusEl.prepend(indicator);
        
        const routeEl = busElement.querySelector('[data-route-color]');
        const routeIndicator = document.createElement('span');
        routeIndicator.classList.add('route-color-indicator');
        routeIndicator.style.backgroundColor = routeEl.dataset.routeColor;
        routeEl.prepend(routeIndicator);
    });
}

// Focus the map on a specific bus
function focusOnBus(busId) {
    const marker = busMarkers[busId];
    if (marker) {
        map.setView(marker.getLatLng(), 16);
        marker.openPopup();
    }
}

// Set up route filtering controls
function setupRouteControls() {
    const routeControls = document.getElementById('route-controls');
    if (!routeControls) return;
    
    // In a real implementation, fetch routes from the server
    const routes = simulateRoutes();
    
    routes.forEach(route => {
        const routeControl = document.createElement('div');
        routeControl.className = 'form-check form-switch mb-2';
        routeControl.innerHTML = `
            <input class="form-check-input" type="checkbox" id="route-${route.id}" checked data-route-id="${route.id}">
            <label class="form-check-label" for="route-${route.id}">
                <span data-route-color="${route.color}" class="fw-bold">${route.number}: ${route.name}</span>
            </label>
        `;
        routeControls.appendChild(routeControl);
        
        // Add route color indicator
        const routeEl = routeControl.querySelector('[data-route-color]');
        const routeIndicator = document.createElement('span');
        routeIndicator.classList.add('route-color-indicator');
        routeIndicator.style.backgroundColor = routeEl.dataset.routeColor;
        routeEl.prepend(routeIndicator);
        
        // Add event listener for route toggle
        const checkbox = routeControl.querySelector('input[type="checkbox"]');
        checkbox.addEventListener('change', function() {
            toggleRouteVisibility(route.id, this.checked);
        });
    });
}

// Toggle visibility of buses on a specific route
function toggleRouteVisibility(routeId, visible) {
    // In a real implementation, filter buses based on their route
    // For this demo, we'll just simulate it
    console.log(`Route ${routeId} visibility: ${visible}`);
    
    // This would update the map markers based on visibility
    Object.values(busMarkers).forEach(marker => {
        // In a real implementation, check if the marker belongs to this route
        // For now, we'll keep all markers visible
    });
}

// Simulate bus location data (for demo purposes)
function simulateBusLocations() {
    // This function would be replaced with actual API calls
    return [
        {
            id: 1,
            busNumber: "B1001",
            lat: 40.712, 
            lng: -74.006,
            routeName: "Downtown Express",
            routeNumber: "D1",
            routeColor: "#e74c3c",
            status: "On Time",
            driverName: "John Smith",
            speed: 35,
            lastUpdated: "2 min ago"
        },
        {
            id: 2,
            busNumber: "B1002",
            lat: 40.718, 
            lng: -73.996,
            routeName: "Uptown Local",
            routeNumber: "U2",
            routeColor: "#3498db",
            status: "Delayed",
            driverName: "Jane Doe",
            speed: 15,
            lastUpdated: "1 min ago"
        },
        {
            id: 3,
            busNumber: "B1003",
            lat: 40.725, 
            lng: -73.985,
            routeName: "Cross Town",
            routeNumber: "C3",
            routeColor: "#2ecc71",
            status: "On Time",
            driverName: "Robert Johnson",
            speed: 25,
            lastUpdated: "just now"
        }
    ];
}

// Simulate route data (for demo purposes)
function simulateRoutes() {
    // This function would be replaced with actual API calls
    return [
        {
            id: 1,
            number: "D1",
            name: "Downtown Express",
            color: "#e74c3c"
        },
        {
            id: 2,
            number: "U2",
            name: "Uptown Local",
            color: "#3498db"
        },
        {
            id: 3,
            number: "C3",
            name: "Cross Town",
            color: "#2ecc71"
        }
    ];
}

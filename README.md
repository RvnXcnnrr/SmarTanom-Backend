# SmarTanom Backend

A Django REST API backend for IoT hydroponic monitoring system with real-time WebSocket support.

## 🚀 Features

- **User Management**: Custom user model with email authentication
- **Device Management**: IoT device registration and monitoring
- **QR Code Integration**: Device registration via QR codes
- **Hydroponic Systems**: Track multiple hydroponic setups per device
- **Sensor Management**: Various sensor types (temperature, humidity, pH, EC, water level, light)
- **Sensor Data**: Real-time data collection and historical tracking
- **WebSocket Support**: Real-time streaming of sensor data
- **REST API**: Full CRUD operations with Django REST Framework
- **Admin Interface**: Django admin for easy data management

## 📋 Models

Based on your ERD, the following models are implemented:

1. **User** - Custom user model with email authentication
2. **Device** - IoT devices linked to users
3. **QrCode** - QR codes for device registration
4. **Hydroponic** - Hydroponic systems managed by devices
5. **Sensor** - Sensors attached to devices (6 types supported)
6. **SensorData** - Time-series data from sensors

## 🔌 API Endpoints

### REST API
- `/api/users/` - User management
- `/api/devices/` - Device management
- `/api/qrcodes/` - QR code management
- `/api/hydroponics/` - Hydroponic system management
- `/api/sensors/` - Sensor management
- `/api/sensor-data/` - Sensor data collection

### Special REST Endpoints
- `/api/devices/{id}/sensors/` - Get all sensors for a device
- `/api/devices/{id}/hydroponics/` - Get all hydroponic systems for a device
- `/api/sensors/{id}/latest_data/` - Get latest sensor reading
- `/api/sensors/{id}/data_history/` - Get sensor data history
- `/api/sensor-data/by_sensor_type/?type={sensor_type}` - Filter by sensor type
- `/api/sensor-data/by_device/?device_id={device_id}` - Filter by device
- `/api/sensor-data/websocket_info/` - Get WebSocket connection information

### WebSocket Endpoints
- `ws://localhost:8000/ws/sensor-data/` - Real-time sensor data stream
- `ws://localhost:8000/ws/device/{device_id}/` - Device-specific data stream
- `ws://localhost:8000/ws/sensor/{sensor_id}/` - Sensor-specific data stream

## 🌐 WebSocket Usage

### 1. General Sensor Data Stream
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/sensor-data/');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Sensor data:', data);
};

// Send new sensor data
ws.send(JSON.stringify({
    type: 'sensor_data',
    sensor_id: 1,
    value: 25.5
}));

// Send ping
ws.send(JSON.stringify({
    type: 'ping',
    timestamp: new Date().toISOString()
}));
```

### 2. Device-Specific Stream
```javascript
const deviceWs = new WebSocket('ws://localhost:8000/ws/device/1/');

deviceWs.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'device_connected') {
        console.log('Device info:', data.device);
    } else if (data.type === 'sensor_data') {
        console.log('Device sensor data:', data.data);
    }
};

// Update device status
deviceWs.send(JSON.stringify({
    type: 'device_status',
    status: 'active'
}));
```

### 3. Sensor-Specific Stream
```javascript
const sensorWs = new WebSocket('ws://localhost:8000/ws/sensor/1/');

sensorWs.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'sensor_connected') {
        console.log('Sensor info:', data.sensor);
    } else if (data.type === 'sensor_reading') {
        console.log('New reading:', data.data);
    }
};

// Send sensor reading
sensorWs.send(JSON.stringify({
    type: 'sensor_reading',
    value: 23.4
}));
```

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "SmarTanom Backend"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Seed sample data (optional)**
   ```bash
   python manage.py seed_data
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🧪 Testing WebSockets

Visit `/websocket-test/` in your browser for an interactive WebSocket testing interface.

**Example URLs:**
- http://localhost:8000/websocket-test/ - WebSocket test page
- http://localhost:8000/admin/ - Django admin interface
- http://localhost:8000/api/ - API root
- http://localhost:8000/api/sensor-data/websocket_info/ - WebSocket documentation

## 📊 Sensor Types Supported

1. **Temperature** (°C, °F)
2. **Humidity** (%)
3. **pH Level** (pH units)
4. **Electrical Conductivity** (EC units)
5. **Water Level** (cm)
6. **Light Intensity** (lux)

## 🔧 Project Structure

```
SmarTanom Backend/
├── core/                      # Main application
│   ├── models.py             # Database models
│   ├── serializers.py        # API serializers
│   ├── views.py              # API views
│   ├── admin.py              # Admin interface
│   ├── urls.py               # URL routing
│   ├── consumers.py          # WebSocket consumers
│   ├── routing.py            # WebSocket routing
│   ├── signals.py            # Django signals
│   ├── templates/            # HTML templates
│   └── management/commands/  # Custom commands
├── smartanom_backend/        # Project settings
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   └── asgi.py               # ASGI configuration
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔄 Real-time Features

### Automatic Broadcasting
The system automatically broadcasts sensor data via WebSockets when:
- New sensor data is saved to the database
- Device status changes
- Sensor readings are updated

### Message Types

**Incoming Messages:**
- `sensor_data` - Send new sensor data
- `device_status` - Update device status
- `sensor_reading` - Send sensor reading
- `ping` - Keep connection alive

**Outgoing Messages:**
- `connection_established` - Connection successful
- `sensor_data` - New sensor data broadcast
- `device_status` - Device status update
- `sensor_reading` - New sensor reading
- `pong` - Ping response
- `error` - Error messages

## 🚀 Production Deployment

For production, consider:

1. **Use Redis for Channel Layers**
   ```python
   CHANNEL_LAYERS = {
       'default': {
           'BACKEND': 'channels_redis.core.RedisChannelLayer',
           'CONFIG': {
               "hosts": [('127.0.0.1', 6379)],
           },
       },
   }
   ```

2. **Use Daphne ASGI Server**
   ```bash
   pip install daphne
   daphne smartanom_backend.asgi:application
   ```

3. **Environment Variables**
   - Set `DEBUG=False`
   - Configure proper `ALLOWED_HOSTS`
   - Use secure database settings
   - Set up proper CORS settings

## 🛠️ Development

### Adding New Sensor Types

Edit the `SENSOR_TYPE_CHOICES` in `core/models.py`:

```python
SENSOR_TYPE_CHOICES = [
    ('temperature', 'Temperature'),
    ('humidity', 'Humidity'),
    # Add new sensor types here
]
```

### Custom WebSocket Consumers

Create new consumers in `core/consumers.py` and add routes in `core/routing.py`.

## 📱 IoT Integration

### Sending Sensor Data via HTTP
```python
import requests

data = {
    'sensor': 1,
    'value': 25.5
}
response = requests.post('http://localhost:8000/api/sensor-data/', json=data)
```

### Sending Sensor Data via WebSocket
```python
import websocket
import json

ws = websocket.WebSocket()
ws.connect("ws://localhost:8000/ws/sensor-data/")
ws.send(json.dumps({
    'type': 'sensor_data',
    'sensor_id': 1,
    'value': 25.5
}))
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

[Add your license information here]

---

**Happy Coding! 🌱**

# WebSocket Documentation

## Overview
SmarTanom Backend provides real-time WebSocket connections for live sensor data streaming and device status updates.

## WebSocket Endpoints

### General Sensor Data Stream
- **URL**: `ws://127.0.0.1:8000/ws/sensor-data/`
- **Purpose**: Receive all sensor data updates in real-time

### Device-Specific Stream
- **URL**: `ws://127.0.0.1:8000/ws/device/{device_id}/`
- **Purpose**: Receive updates for a specific device

### Sensor-Specific Stream
- **URL**: `ws://127.0.0.1:8000/ws/sensor/{sensor_id}/`
- **Purpose**: Receive updates for a specific sensor

## Message Format

### Incoming Messages (from client)
```json
{
  "type": "sensor_data",
  "sensor_id": 1,
  "value": 25.5,
  "timestamp": "2025-09-11T15:30:00Z"
}
```

### Outgoing Messages (to client)
```json
{
  "type": "sensor_data_update",
  "sensor_id": 1,
  "sensor_type": "temperature",
  "device_id": 1,
  "device_name": "Hydroponic System 1",
  "value": 25.5,
  "unit": "celsius",
  "timestamp": "2025-09-11T15:30:00Z"
}
```

### Device Status Updates
```json
{
  "type": "device_status",
  "device_id": 1,
  "device_name": "Hydroponic System 1",
  "status": "active",
  "timestamp": "2025-09-11T15:30:00Z"
}
```

## Connection Examples

### JavaScript (Browser)
```javascript
const socket = new WebSocket('ws://127.0.0.1:8000/ws/sensor-data/');

socket.onopen = function(event) {
    console.log('WebSocket connected');
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

socket.onclose = function(event) {
    console.log('WebSocket disconnected');
};

// Send sensor data
socket.send(JSON.stringify({
    type: 'sensor_data',
    sensor_id: 1,
    value: 25.5
}));
```

### Python (websocket-client)
```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"Received: {data}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")
    # Send test data
    ws.send(json.dumps({
        "type": "sensor_data",
        "sensor_id": 1,
        "value": 25.5
    }))

ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/sensor-data/",
                          on_open=on_open,
                          on_message=on_message,
                          on_error=on_error,
                          on_close=on_close)

ws.run_forever()
```

## Authentication
WebSocket connections currently don't require authentication, but this can be implemented using Django's authentication middleware.

## Error Handling
If an error occurs, the WebSocket will send an error message:
```json
{
  "type": "error",
  "message": "Error description",
  "code": "ERROR_CODE"
}
```

## Testing
Use the built-in WebSocket test interface at:
`http://127.0.0.1:8000/websocket-test/`

# API Documentation

## Overview
SmarTanom Backend provides a RESTful API for managing IoT hydroponic systems with real-time WebSocket capabilities.

## Base URL
- Development: `http://127.0.0.1:8000/api/`
- Production: `https://yourdomain.com/api/`

## Authentication
The API uses session-based authentication. Include the session cookie in your requests.

## Endpoints

### Users
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details
- `POST /api/users/` - Create new user
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Devices
- `GET /api/devices/` - List all devices
- `GET /api/devices/{id}/` - Get device details
- `POST /api/devices/` - Create new device
- `PUT /api/devices/{id}/` - Update device
- `DELETE /api/devices/{id}/` - Delete device

### Sensors
- `GET /api/sensors/` - List all sensors
- `GET /api/sensors/{id}/` - Get sensor details
- `POST /api/sensors/` - Create new sensor
- `PUT /api/sensors/{id}/` - Update sensor
- `DELETE /api/sensors/{id}/` - Delete sensor

### Sensor Data
- `GET /api/sensor-data/` - List all sensor data
- `GET /api/sensor-data/{id}/` - Get sensor data details
- `POST /api/sensor-data/` - Create new sensor data
- `PUT /api/sensor-data/{id}/` - Update sensor data
- `DELETE /api/sensor-data/{id}/` - Delete sensor data

### QR Codes
- `GET /api/qr-codes/` - List all QR codes
- `GET /api/qr-codes/{id}/` - Get QR code details
- `POST /api/qr-codes/` - Create new QR code
- `PUT /api/qr-codes/{id}/` - Update QR code
- `DELETE /api/qr-codes/{id}/` - Delete QR code

### Hydroponic Systems
- `GET /api/hydroponics/` - List all hydroponic systems
- `GET /api/hydroponics/{id}/` - Get hydroponic system details
- `POST /api/hydroponics/` - Create new hydroponic system
- `PUT /api/hydroponics/{id}/` - Update hydroponic system
- `DELETE /api/hydroponics/{id}/` - Delete hydroponic system

## Query Parameters

### Filtering
- Use query parameters to filter results:
  - `?sensor_type=temperature` - Filter sensors by type
  - `?status=active` - Filter devices by status
  - `?created_at__gte=2025-01-01` - Filter by creation date

### Pagination
- `?page=1` - Page number
- `?page_size=20` - Number of items per page (default: 20)

### Ordering
- `?ordering=created_at` - Order by creation date (ascending)
- `?ordering=-created_at` - Order by creation date (descending)

## Response Format

All responses follow this format:

```json
{
  "count": 100,
  "next": "http://example.com/api/endpoint/?page=2",
  "previous": null,
  "results": [
    // ... array of objects
  ]
}
```

## Error Handling

Error responses include:
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

Error response format:
```json
{
  "error": "Error message",
  "details": "Detailed error information"
}
```

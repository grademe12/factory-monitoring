# Factory Monitoring System

Real-time IoT sensor monitoring system using Grafana, Telegraf, InfluxDB, and MQTT.

## 🏭 Overview

This project implements a comprehensive factory monitoring solution that collects, processes, and visualizes sensor data from IoT devices. The system is designed to handle multiple sensor types including temperature, humidity, vibration, pressure, and production metrics.

## 🛠️ Tech Stack

- **MQTT Broker (Mosquitto)**: Secure message broker with TLS/SSL support
- **InfluxDB**: Time-series database for sensor data storage
- **Telegraf**: Data collection agent that subscribes to MQTT topics
- **Grafana**: Real-time data visualization and monitoring dashboard
- **Python**: Edge device simulator for testing

## 📁 Project Structure

```
factory-monitoring/
├── edge-device/              # Edge device simulators
│   ├── mass_publisher.py     # Multi-sensor MQTT publisher
│   └── requirements.txt      # Python dependencies
├── server/                   # Server-side components
│   ├── docker-compose.yaml   # Container orchestration
│   ├── mosquitto.conf        # MQTT broker configuration
│   ├── telegraf.conf         # Data collection configuration
│   └── dashboard-overview.json # Grafana dashboard template
└── README.md
```

## 🚀 Features

- **Secure MQTT Communication**: TLS/SSL encryption with certificate-based authentication
- **Multi-Sensor Support**: Handles 5 different sensor types simultaneously
- **Real-time Processing**: 5-second data collection and visualization intervals
- **Scalable Architecture**: Supports 500+ concurrent sensor connections
- **Comprehensive Dashboard**: 
  - Real-time message flow monitoring
  - Active sensor count
  - Sensor health status visualization
  - Average metrics for all sensor types
  - Customizable gauge displays

## 📊 Monitored Metrics

| Sensor Type | Data Range | Unit |
|------------|------------|------|
| Temperature | 20-30 | °C |
| Humidity | 40-60 | % |
| Vibration | 0-10 | Scale |
| Pressure | 1000-1020 | hPa |
| Production | 50-150 | Units/h |

## 🔧 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.8+ (for edge device simulator)
- SSL certificates (CA, server cert, server key)

### Server Setup

1. Generate SSL certificates:
```bash
# Generate CA certificate
openssl req -new -x509 -days 365 -key ca.key -out ca.crt

# Generate server certificate
openssl req -new -key server.key -out server.csr
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -out server.crt
```

2. Create MQTT user credentials:
```bash
mosquitto_passwd -c pwfile sensor
```

3. Start the services:
```bash
cd server/
docker-compose up -d
```

4. Access Grafana:
- URL: http://localhost:3000
- Username: admin
- Password: admin

### Edge Device Setup

1. Install dependencies:
```bash
cd edge-device/
pip install -r requirements.txt
```

2. Copy CA certificate from server:
```bash
scp server:/path/to/ca.crt ~/mqtt/
```

3. Run the sensor simulator:
```bash
python mass_publisher.py
```

## 📈 Data Flow

```
Edge Devices → MQTT Broker → Telegraf → InfluxDB → Grafana
     ↓              ↓            ↓          ↓          ↓
   Publish      TLS/SSL     Subscribe    Store    Visualize
```

## 🔒 Security Features

- TLS/SSL encryption for MQTT communication
- Password-based authentication
- Certificate validation
- Isolated Docker network
- Configurable access controls

## 🎯 Use Cases

- Industrial IoT monitoring
- Smart factory implementation
- Equipment health tracking
- Production line optimization
- Predictive maintenance systems

## 📝 Configuration

### MQTT Topics
- `factory/sensor/temperature`
- `factory/sensor/humidity`
- `factory/sensor/vibration`
- `factory/sensor/pressure`
- `factory/sensor/production`

### Default Ports
- MQTT (SSL): 8883
- InfluxDB: 8086
- Grafana: 3000

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📄 License

This project is open source and available under the MIT License.

# This page written by Claude.ai

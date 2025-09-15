# mass_publisher.py
import asyncio
import json
import random
import ssl
from datetime import datetime
import paho.mqtt.client as mqtt

# === 설정 ===
BROKER_IP = "192.168.45.48"  # 데비안 서버 IP
BROKER_PORT = 8883  # SSL 포트
USERNAME = "sensor"  # Telegraf와 같은 계정 사용
PASSWORD = "sensorpass"
CA_CERT = "/home/woosupar/mqtt/ca.crt"  # 라즈베리파이에 복사한 CA 인증서 경로
NUM_SENSORS = 500
PUBLISH_INTERVAL = 5  # Telegraf interval과 맞춤

class SecurePublisher:
    def __init__(self):
        """보안 MQTT 연결"""
        self.client = mqtt.Client(client_id=f"rpi_publisher_{random.randint(1000,9999)}")
        
        # 사용자 인증
        self.client.username_pw_set(USERNAME, PASSWORD)
        
        # TLS/SSL 설정
        self.client.tls_set(
            ca_certs=CA_CERT,
            certfile=None,  # 클라이언트 인증서 불필요 (require_certificate false)
            keyfile=None,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        
        # 자체 서명 인증서인 경우 (개발 환경)
        self.client.tls_insecure_set(True)  # insecure_skip_verify = true와 같음
        
        try:
            self.client.connect(BROKER_IP, BROKER_PORT, 60)
            self.client.loop_start()
            print(f"🔒 Secure connection established to {BROKER_IP}:{BROKER_PORT}")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            exit(1)
    
    async def publish_sensor_data(self, sensor_type, sensor_id):
        """Telegraf가 구독하는 토픽으로 발행"""
        topic = f"factory/sensor/{sensor_type}"
        
        while True:
            # 센서 타입별 데이터 범위
            if sensor_type == "temperature":
                value = round(random.uniform(20, 30), 2)
            elif sensor_type == "humidity":
                value = round(random.uniform(40, 60), 2)
            elif sensor_type == "vibration":
                value = round(random.uniform(0, 10), 2)
            elif sensor_type == "pressure":
                value = round(random.uniform(1000, 1020), 2)
            elif sensor_type == "production":
                value = random.randint(50, 150)  # 생산량

            data = {
                "sensor_id": sensor_id,
                "senor_type": sensor_type,
                "value": value,
                "timestamp": datetime.now().isoformat()
            }
            
            # Telegraf data_format = id와 value를 함께 json으로 발행
            self.client.publish(topic, json.dumps(data), qos=0)
            
            print(f"📡 {sensor_id}: {value} @ {data['timestamp']}")
            await asyncio.sleep(PUBLISH_INTERVAL)
    
    async def start(self):
        """여러 센서 시뮬레이션"""
        print(f"🚀 Starting {NUM_SENSORS} sensors (5 types)...")
        
        tasks = []
        sensor_types = ["temperature", "humidity", "vibration", "pressure", "production"]
        sensors_per_type = NUM_SENSORS // len(sensor_types)
        
        for sensor_type in sensor_types:
            for i in range(sensors_per_type):
                sensor_id = f"{sensor_type}_{i:03d}"
                task = asyncio.create_task(
                    self.publish_sensor_data(sensor_type, sensor_id)
                )
                tasks.append(task)
                await asyncio.sleep(0.01)  # 시작 시간 분산
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    # CA 인증서 확인
    import os
    if not os.path.exists(CA_CERT):
        print(f"⚠️  CA 인증서가 없습니다: {CA_CERT}")
        print("데비안에서 복사하세요:")
        print("scp debian:/mosquitto/certs/ca.crt /home/pi/certs/")
        exit(1)
    
    publisher = SecurePublisher()
    asyncio.run(publisher.start())
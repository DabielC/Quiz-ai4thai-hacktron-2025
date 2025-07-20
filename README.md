# Quiz-ai4thai-hacktron-2025

**จงสร้าง API 2 ตัว โดยมีเงื่อนไขดังนี้**\n
• สร้างโดยภาษาไดก็ได้\n
• Listen ที่ port ไดก็ได้\n
• User Request ไปที่ API1 แล้ว API 1 request ต่อไปที่ API2 แล้วนำคำตอบส่งกลับไปที่ User\n
• มีการ Print logs ทั้งบน API1 และ 2\n
• endpoint ของ api และคำตอบ จะเป็นอะไรก็ได้ แค่ print hello world ก็ได้\n
• deploy ทุกอย่างบน docker-compose.yml\n
• ส่งงานผ่าน github หรือ gitlab เปิด public access\n
• เขียน Readme.md บอกวิธี deploy และทดสอบ\n
<image src='image.png'></image>

## Flow การทำงาน

```
User Request → Container แรก (Port 8000) → Container ที่สอง (Port 8001) → Response
```

## คุณสมบัติเด่น

- Container ทั้งสองจะบันทึก Log ของทุก Request พร้อมเวลา
- Container แรกทำหน้าที่เป็น API Gateway
- Container ที่สองเป็น Backend API สำหรับประมวลผลจริง
- มี Endpoint สำหรับ Health Check ของทั้งสอง Container
- จัดการ Service ทั้งหมดด้วย Docker Compose

## วิธีใช้งาน

### 1. Build และ Start Service

```bash
docker-compose up --build
```

### 2. ทดสอบ API

ยิง Request ไปที่ Container แรก:

```bash
curl http://localhost:8000/
```

Response ที่คาดหวัง:
```json
{
  "message": "hello from second api",
  "forwarded_by": "first-container"
}
```

### 3. ตรวจสอบ Health Endpoints

```bash
# Health Check ของ Container แรก
curl http://localhost:8000/health

# Health Check ของ Container ที่สอง (ยิงตรง)
curl http://localhost:8001/health
```

### 4. ดู Logs

```bash
# ดู Log ทั้งหมด
docker-compose logs

# ดู Log ของ Container ที่ต้องการ
docker-compose logs first-container
docker-compose logs second-container

# ดู Log แบบ Real-time
docker-compose logs -f
```

## รายละเอียดของแต่ละ Container

### Container แรก (API Gateway)
- **Port**: 8000 (ภายนอก), 8000 (ภายใน)
- **หน้าที่**: รับ Request และส่งต่อไปยัง Container ที่สอง
- **Endpoints**: `/`, `/health`

### Container ที่สอง (Backend API)
- **Port**: 8001 (ภายนอก), 8001 (ภายใน)
- **หน้าที่**: ประมวลผล Request และส่ง Response
- **Endpoints**: `/`, `/health`

## ตัวอย่าง Log

เมื่อคุณยิง Request ไปที่ `http://localhost:8000/` จะเห็น Log แสดงผลตามลำดับดังนี้:

```
first-container_1  | [2024-01-15 10:30:45] First Container: Received request to root endpoint
first-container_1  | [2024-01-15 10:30:45] First Container: Forwarding request to http://second-container:8001
second-container_1 | [2024-01-15 10:30:45] Second Container: Received request to root endpoint
first-container_1  | [2024-01-15 10:30:45] First Container: Successfully received response from second container
```

## การหยุดใช้งาน Service

```bash
docker-compose down
```

## การแก้ปัญหา (Troubleshooting)

### ปัญหาที่เจอบ่อย
1.  **Port ชน / Port in use**: ตรวจสอบว่าไม่มีโปรแกรมอื่นใช้ Port 8000 และ 8001 อยู่
2.  **Container คุยกันไม่ได้**: ตรวจสอบการตั้งค่า Network ใน `docker-compose.yaml`
3.  **Build Image ไม่ผ่าน**: ตรวจสอบว่าติดตั้ง Docker และ Docker Compose ถูกต้อง

### คำสั่งมีประโยชน์
```bash
# เช็คสถานะของ Container ทั้งหมด
docker-compose ps

# Restart เฉพาะ Service ที่ต้องการ
docker-compose restart first-container

# เข้าไปใน Shell ของ Container
docker-compose exec first-container bash

# ลบ Container และ Volume ทั้งหมด
docker-compose down -v
```

# 🐳 Docker Command Cheat-Sheet

ยินดีต้อนรับสู่คลังรวบรวมคำสั่ง Docker ที่ใช้บ่อยในชีวิตประจำวัน เหมาะสำหรับผู้เริ่มต้นและนักพัฒนาที่ต้องการเปิดดูคำสั่งแบบด่วน (Cheat-Sheet)

👉 **[เปิดดูคำสั่งทั้งหมดที่ docker.md](docker.md)**

---

## 🚀 โปรเจกต์นี้ทำอะไร?
* รวบรวมคำสั่งพื้นฐานในการจัดการ Containers, Images, Volumes และ Networks
* คำสั่งสำหรับ debug และล้างพื้นที่ พร้อมขั้นตอนเช็กเมื่อ container ล่ม
* ตัวอย่างการสร้าง image เองด้วย Dockerfile
* Lab WordPress + MySQL + phpMyAdmin ทั้งแบบ `docker run` และ Docker Compose
* แนวทาง Security ของ Docker เช่น สแกนช่องโหว่, ไม่รันเป็น root, จัดการรหัสผ่าน

## 📁 โครงสร้างไฟล์
```
.
├── docker.md              # cheat-sheet: all commands, grouped by topic
├── docker-compose.yml     # WordPress + MySQL + phpMyAdmin lab
├── .env.example           # sample passwords for docker-compose (copy to .env)
└── examples/
    └── hello-app/         # minimal Dockerfile example (non-root, small image)
        ├── Dockerfile
        ├── .dockerignore
        └── app.py
```

## 🛠️ เครื่องมือที่ใช้ (Prerequisites)
ก่อนเริ่มใช้งาน คุณจำเป็นต้องติดตั้งเครื่องมือเหล่านี้ในเครื่องของคุณก่อน:
* **Docker** (Desktop หรือ Engine)
* **Docker Compose** v2 (มากับ Docker Desktop อยู่แล้ว ใช้คำสั่ง `docker compose`)
* Git (สำหรับ clone โปรเจกต์นี้)

---

## 📦 รัน WordPress Lab ด้วย Docker Compose
```bash
cp .env.example .env      # แล้วแก้รหัสผ่านในไฟล์ .env
docker compose up -d      # รันทุก service
docker compose ps         # ดูสถานะ
docker compose down       # หยุดและลบ container (ข้อมูลยังอยู่ใน volume)
docker compose down -v    # ลบ volume ของฐานข้อมูลด้วย
```

* WordPress: http://localhost:8080
* phpMyAdmin: http://localhost:8888

> * ไฟล์ `.env` ถูกใส่ไว้ใน `.gitignore` รหัสผ่านจริงจึงไม่ถูก commit ขึ้น Git
> * พอร์ตถูก bind กับ `127.0.0.1` เข้าได้จากเครื่องตัวเองเท่านั้น ไม่เปิด phpMyAdmin ให้คนอื่นใน network เข้าได้

## 🐍 ลอง build image เอง
```bash
cd examples/hello-app
docker build -t hello-app:1.0 .
docker run -d --rm -p 8000:8000 --name hello hello-app:1.0
curl http://localhost:8000      # Hello from Docker!
docker stop hello
```
คำอธิบายแต่ละบรรทัดของ Dockerfile อยู่ใน [docker.md หัวข้อที่ 3](docker.md#3-images-และ-dockerfile)

---

## 👥 สมาชิกผู้พัฒนา (Developers)
* **Nuttaphat** ([@Catboyz-45](https://github.com/Catboyz-45))

*(หมายเหตุ: โปรเจกต์นี้เป็นส่วนหนึ่งของรายวิชา Information Assurance and Security (02739352) ในภาคการศึกษา 2568 กลุ่มเรียน 820)*

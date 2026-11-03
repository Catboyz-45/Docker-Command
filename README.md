# 🐳 Docker Command Cheat-Sheet

ยินดีต้อนรับสู่คลังรวบรวมคำสั่ง Docker ที่ใช้บ่อยในชีวิตประจำวัน เหมาะสำหรับผู้เริ่มต้นและนักพัฒนาที่ต้องการเปิดดูคำสั่งแบบด่วน (Cheat-Sheet)

---

## 🚀 โปรเจกต์นี้ทำอะไร?
* รวบรวมคำสั่งพื้นฐานในการจัดการ Containers, Images, Volumes และ Networks
* มีตัวอย่างการใช้งานจริงเพื่อความเข้าใจง่าย
* แหล่งอ้างอิงและบันทึกช่วยจำสำหรับทีมพัฒนา

## 🛠️ เครื่องมือที่ใช้ (Prerequisites)
ก่อนเริ่มใช้งาน คุณจำเป็นต้องติดตั้งเครื่องมือเหล่านี้ในเครื่องของคุณก่อน:
* **Docker** (Desktop หรือ Engine)
* **Docker Compose** (ถ้ามีคำสั่งเกี่ยวกับ compose)
* Git (สำหรับ clone โปรเจกต์นี้)

---

## 📦 รัน WordPress Lab ด้วย Docker Compose
`docker-compose.yml` คือ lab WordPress + MySQL + phpMyAdmin แบบเดียวกับใน `docker.txt` แต่รวมไว้ในไฟล์เดียว

```bash
cp .env.example .env      # แล้วแก้รหัสผ่านในไฟล์ .env
docker compose up -d      # รันทุก service
docker compose ps         # ดูสถานะ
docker compose down       # หยุดและลบ container (ข้อมูลยังอยู่ใน volume)
docker compose down -v    # ลบ volume ของฐานข้อมูลด้วย
```

* WordPress: http://localhost:8080
* phpMyAdmin: http://localhost:8888

> ไฟล์ `.env` ถูกใส่ไว้ใน `.gitignore` รหัสผ่านจริงจึงไม่ถูก commit ขึ้น Git

---

## 👥 สมาชิกผู้พัฒนา (Developers)
* **Nuttaphat** ([@Catboyz-45](https://github.com/Catboyz-45))

*(หมายเหตุ: โปรเจกต์นี้เป็นส่วนหนึ่งของรายวิชาInformation Assurance and Security(02739352)ในภาคการศึกษา 2568 กลุ่มเรียน 820)*

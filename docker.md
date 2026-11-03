# 🐳 Docker Commands

> `<container>` ใส่ได้ทั้ง container ID (ดูจาก `docker ps`) หรือชื่อที่ตั้งด้วย `--name`
> ID ไม่ต้องพิมพ์ครบ พิมพ์แค่ 3–4 ตัวแรกที่ไม่ซ้ำกับตัวอื่นก็พอ

## สารบัญ
1. [เริ่มต้น](#1-เริ่มต้น)
2. [Containers](#2-containers)
3. [Images และ Dockerfile](#3-images-และ-dockerfile)
4. [Volumes](#4-volumes)
5. [Networks](#5-networks)
6. [Debug](#6-debug)
7. [ล้างพื้นที่ (Cleanup)](#7-ล้างพื้นที่-cleanup)
8. [Docker Compose](#8-docker-compose)
9. [Lab: WordPress + MySQL + phpMyAdmin](#9-lab-wordpress--mysql--phpmyadmin)
10. [Security](#10-security)

---

## 1. เริ่มต้น

| คำสั่ง | ความหมาย |
|---|---|
| `docker -v` | แสดงเวอร์ชันของ Docker |
| `docker info` | ข้อมูลของ Docker daemon เช่น จำนวน container, storage driver |
| `docker run hello-world` | ทดสอบว่า Docker รัน container ได้หรือไม่ |

---

## 2. Containers

### รันและดูสถานะ
| คำสั่ง | ความหมาย |
|---|---|
| `docker run busybox ls` | รัน container จาก image `busybox` แล้วสั่ง `ls` (ถ้าเครื่องยังไม่มี image จะ pull ให้เอง) |
| `docker run busybox ping google.com` | รัน container แล้วสั่ง `ping` (กด `Ctrl+C` เพื่อหยุด) |
| `docker run nginx` | รัน web server nginx แบบ foreground (จอค้างที่ log) |
| `docker run -d -p 8080:80 nginx` | รันแบบ background (`-d` = detached) และ map พอร์ต `host:container` เปิดดูที่ http://localhost:8080 |
| `docker run -d --name web nginx` | ตั้งชื่อ container จะได้ใช้ชื่อแทน ID |
| `docker run --rm -it busybox sh` | เข้า shell ใน container ใหม่ (`-it` = interactive + terminal) และลบ container ทิ้งเองเมื่อออก (`--rm`) |
| `docker run -e KEY=value <image>` | ส่ง environment variable เข้า container |
| `docker ps` | แสดง container ที่กำลังทำงาน |
| `docker ps -a` | แสดง container ทั้งหมด รวมตัวที่หยุดแล้ว (เหมือน `--all`) |

### วงจรชีวิตของ container
`docker run` = `docker create` + `docker start` ในคำสั่งเดียว

| คำสั่ง | ความหมาย |
|---|---|
| `docker create busybox ping google.com` | สร้าง container แต่ยังไม่เริ่มทำงาน (ได้ container ID กลับมา) |
| `docker start <container>` | เริ่มทำงาน container ที่สร้างไว้หรือที่หยุดไปแล้ว |
| `docker start -a <container>` | เริ่มทำงานและแสดง output ออกมาที่จอ (`-a` = attach) |
| `docker stop <container>` | หยุด container แบบสุภาพ (ส่ง `SIGTERM` รอ 10 วินาที แล้วค่อย `SIGKILL`) |
| `docker kill <container>` | หยุดทันที (ส่ง `SIGKILL`) ใช้ตอน `stop` ไม่ยอมหยุด |
| `docker restart <container>` | หยุดแล้วเริ่มใหม่ |
| `docker rm <container>` | ลบ container ที่หยุดแล้ว |
| `docker rm -f <container>` | บังคับลบ แม้ container ยังทำงานอยู่ |

### สั่งงานใน container ที่กำลังทำงาน
| คำสั่ง | ความหมาย |
|---|---|
| `docker exec <container> ls` | รันคำสั่ง `ls` ใน container |
| `docker exec -it <container> sh` | เข้า shell ของ container |
| `docker exec -it <container> bash` | เข้า bash (ใช้ได้เฉพาะ image ที่มี bash เช่น ubuntu; image เล็กอย่าง alpine/busybox มีแค่ `sh`) |

---

## 3. Images และ Dockerfile

### จัดการ image
| คำสั่ง | ความหมาย |
|---|---|
| `docker pull busybox` | ดึง image จาก Docker Hub (ไม่ระบุ tag = ใช้ `latest`) |
| `docker pull mysql:8.4` | ดึง image แบบระบุเวอร์ชัน (tag) |
| `docker images` | แสดง image ทั้งหมดในเครื่อง (เหมือน `docker image ls`) |
| `docker rmi <image>` | ลบ image (ต้องไม่มี container ใช้อยู่) |
| `docker history <image>` | ดู layer ของ image ว่าแต่ละขั้นสร้างจากคำสั่งอะไรและใหญ่เท่าไหร่ |

### สร้าง image เองจาก Dockerfile
ตัวอย่างอยู่ที่ [`examples/hello-app/`](examples/hello-app/)

```bash
cd examples/hello-app
docker build -t hello-app:1.0 .                # build an image named hello-app, tag 1.0
docker run -d --rm -p 8000:8000 --name hello hello-app:1.0
curl http://localhost:8000                     # -> Hello from Docker!
docker stop hello
```

`.` ท้าย `docker build` คือ **build context** หมายถึงโฟลเดอร์ที่ส่งให้ Docker ใช้ตอน build คำสั่ง `COPY` ใน Dockerfile จะมองเห็นได้แค่ไฟล์ในโฟลเดอร์นี้

| คำสั่งใน Dockerfile | ความหมาย |
|---|---|
| `FROM` | image ตั้งต้น เช่น `python:3.13-slim` |
| `WORKDIR` | โฟลเดอร์ทำงานใน image (สร้างให้ถ้ายังไม่มี) |
| `COPY` | ก๊อปไฟล์จาก build context เข้า image |
| `RUN` | รันคำสั่งตอน **build** เช่น ติดตั้งแพ็กเกจ แต่ละ `RUN` จะได้ 1 layer |
| `USER` | เปลี่ยน user ที่ใช้รันคำสั่งถัดไปและตอนรัน container |
| `EXPOSE` | บอกว่าแอปฟังพอร์ตไหน (เป็นแค่เอกสาร ยังต้องใช้ `-p` ตอนรันอยู่ดี) |
| `CMD` | คำสั่งที่รันตอน **start container** |

> **Layer cache:** Docker จะ build ซ้ำเฉพาะขั้นที่ไฟล์เปลี่ยนและขั้นหลังจากนั้น
> ให้วางขั้นที่เปลี่ยนน้อย เช่น ติดตั้ง dependencies ไว้ก่อน ส่วน `COPY` โค้ดที่แก้บ่อยไว้ท้าย จะ build ใหม่ได้เร็วขึ้นมาก

> **ทำไม `docker stop` ใช้เวลา 10 วินาที:** แอปใน container เป็น PID 1 ซึ่ง Linux ไม่ให้ default signal handler
> ถ้าแอปไม่ได้เขียนรับ `SIGTERM` เอง จะไม่มีอะไรเกิดขึ้น Docker ต้องรอครบ 10 วินาทีแล้วค่อย `SIGKILL`
> แก้ได้ 2 ทาง: เขียนรับ `SIGTERM` ในแอป (แบบใน [`app.py`](examples/hello-app/app.py)) หรือรันด้วย `docker run --init` ให้มี init process เล็กๆ เป็น PID 1 คอยส่งต่อ signal
> และต้องใช้ `CMD` แบบ JSON array `["python", "app.py"]` ถ้าเขียน `CMD python app.py` จะรันผ่าน `/bin/sh` ซึ่งไม่ส่งต่อ signal ให้แอป

> **`.dockerignore`:** ใช้บอกว่าไฟล์ไหนไม่ต้องส่งเข้า build context เช่น `.env`, `.git` ช่วยให้ build เร็วขึ้นและกันรหัสผ่านหลุดเข้าไปใน image

### อัปโหลดขึ้น Docker Hub
```bash
docker login
docker tag hello-app:1.0 <dockerhub-username>/hello-app:1.0   # add a name that points to your account
docker push <dockerhub-username>/hello-app:1.0
```

---

## 4. Volumes

ข้อมูลที่เขียนลงใน container จะหายไปเมื่อลบ container ถ้าต้องการเก็บไว้ต้องใช้ volume

| คำสั่ง | ความหมาย |
|---|---|
| `docker volume create mydata` | สร้าง named volume (Docker เป็นคนจัดการที่เก็บให้) |
| `docker volume ls` | แสดง volume ทั้งหมด |
| `docker volume inspect mydata` | ดูรายละเอียด เช่น เก็บอยู่ที่ไหนบน host |
| `docker volume rm mydata` | ลบ volume (ข้อมูลหายถาวร) |
| `docker volume prune` | ลบ volume ที่ไม่มี container ไหนใช้ |

### 2 แบบที่ใช้บ่อย
```bash
# Named volume: best for databases, Docker manages the storage location
docker run -d -v mydata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret mysql:8.4

# Bind mount: share a folder from the host, good for live-editing code
docker run --rm -v "$(pwd)":/app -w /app python:3.13-slim python app.py

# Read-only mount: the container can read but not modify the files
docker run --rm -v "$(pwd)":/data:ro busybox ls /data
```

---

## 5. Networks

container ที่อยู่ใน network เดียวกัน (ที่สร้างเอง) เรียกหากันด้วย **ชื่อ container** ได้เลย เพราะ Docker มี DNS ภายในให้

| คำสั่ง | ความหมาย |
|---|---|
| `docker network create mynet` | สร้าง network (แบบ `bridge`) |
| `docker network ls` | แสดง network ทั้งหมด |
| `docker network inspect mynet` | ดูว่ามี container ไหนอยู่ใน network บ้าง และได้ IP อะไร |
| `docker run -d --network mynet --name api <image>` | รัน container ใน network ที่กำหนด |
| `docker network connect mynet <container>` | เพิ่ม container ที่รันอยู่แล้วเข้า network |
| `docker network rm mynet` | ลบ network |

> network `bridge` ที่เป็น default **ไม่มี** DNS ด้วยชื่อ container ต้องสร้าง network เองถึงจะเรียกด้วยชื่อได้

---

## 6. Debug

| คำสั่ง | ความหมาย |
|---|---|
| `docker logs <container>` | ดู output ของ container (ใช้บ่อยที่สุดตอนหาสาเหตุว่า container ล่ม) |
| `docker logs -f --tail 100 <container>` | ดู 100 บรรทัดล่าสุดแล้วตามดูต่อแบบ real-time (`-f` = follow) |
| `docker inspect <container>` | ดูการตั้งค่าทั้งหมดเป็น JSON เช่น IP, env, mounts, exit code |
| `docker inspect -f '{{.State.ExitCode}}' <container>` | ดึงเฉพาะค่าที่ต้องการ |
| `docker stats` | ดูการใช้ CPU / RAM / network ของแต่ละ container แบบ real-time |
| `docker top <container>` | ดู process ที่รันอยู่ใน container |
| `docker port <container>` | ดูว่า map พอร์ตอะไรไว้บ้าง |
| `docker cp <container>:/path/file .` | ก๊อปไฟล์ออกจาก container มาที่เครื่อง (สลับซ้าย-ขวาเพื่อก๊อปเข้า) |
| `docker events` | ดู event ของ Docker แบบ real-time เช่น container start/stop/die |

**ขั้นตอนเช็กเมื่อ container ล่ม**
1. `docker ps -a` ดูสถานะและ exit code (`Exited (1)` = แอป error, `Exited (137)` = ถูก `SIGKILL` เช่น RAM เกิน limit หรือโดน `docker kill` เช็กได้จาก `docker inspect -f '{{.State.OOMKilled}}' <container>`)
2. `docker logs <container>` อ่าน error message
3. `docker inspect <container>` เช็ก env, พอร์ต, volume ว่าตั้งถูกไหม
4. `docker run --rm -it --entrypoint sh <image>` เข้าไปดูข้างใน image โดยไม่รันแอป

---

## 7. ล้างพื้นที่ (Cleanup)

| คำสั่ง | ความหมาย |
|---|---|
| `docker system df` | ดูว่า image, container, volume, build cache ใช้พื้นที่เท่าไหร่ |
| `docker container prune` | ลบ container ที่หยุดแล้วทั้งหมด |
| `docker image prune` | ลบ image ที่ไม่มี tag (dangling) |
| `docker image prune -a` | ลบ image ที่ไม่มี container ใช้ทั้งหมด |
| `docker system prune` | ลบ container ที่หยุดแล้ว, network ที่ไม่ได้ใช้, dangling image และ build cache **(ไม่ลบ volume)** |
| `docker system prune -a --volumes` | ลบทุกอย่างที่ไม่ได้ใช้ **รวม volume** ⚠️ ข้อมูลใน volume หายถาวร |

---

## 8. Docker Compose

เขียนการตั้งค่าหลาย container ไว้ในไฟล์ `docker-compose.yml` ไฟล์เดียว แล้วสั่งทั้งหมดพร้อมกัน (ตัวอย่างจริงดู [`docker-compose.yml`](docker-compose.yml) ในหัวข้อที่ 9)

| คำสั่ง | ความหมาย |
|---|---|
| `docker compose up -d` | สร้างและรันทุก service แบบ background |
| `docker compose up -d --build` | build image ใหม่ก่อนรัน (ใช้ตอนแก้ Dockerfile) |
| `docker compose ps` | ดูสถานะของแต่ละ service |
| `docker compose logs -f <service>` | ดู log ของ service |
| `docker compose exec <service> sh` | เข้า shell ของ service |
| `docker compose restart <service>` | restart เฉพาะ service ที่ระบุ |
| `docker compose pull` | ดึง image เวอร์ชันล่าสุดของทุก service |
| `docker compose config` | ตรวจ syntax และแสดงไฟล์หลังแทนค่าตัวแปรแล้ว ⚠️ จะแสดงรหัสผ่านจาก `.env` ด้วย |
| `docker compose down` | หยุดและลบ container กับ network (volume ยังอยู่) |
| `docker compose down -v` | ลบ volume ด้วย ⚠️ ข้อมูลในฐานข้อมูลหาย |

> คำสั่งเก่าคือ `docker-compose` (มีขีด) เป็น v1 ที่เลิกพัฒนาแล้ว ปัจจุบันใช้ `docker compose` (เว้นวรรค)

---

## 9. Lab: WordPress + MySQL + phpMyAdmin

### แบบที่ 1: Docker Compose (แนะนำ)
```bash
cp .env.example .env      # then edit the passwords in .env
docker compose up -d
```
- WordPress: http://localhost:8080
- phpMyAdmin: http://localhost:8888

### แบบที่ 2: ใช้ `docker run` ทีละตัว
เป็นแบบที่ทำใน lab ของวิชา ช่วยให้เข้าใจว่า Compose ทำอะไรให้บ้าง
รหัสผ่าน `111` ใช้สำหรับฝึกในเครื่องตัวเองเท่านั้น

```bash
docker network create wordpress

# MySQL: creates database wordpress_db and user wp_user
docker run -d --name mysql --network wordpress \
  -e MYSQL_ROOT_PASSWORD=111 \
  -e MYSQL_DATABASE=wordpress_db \
  -e MYSQL_USER=wp_user \
  -e MYSQL_PASSWORD=111 \
  mysql:8.4

# phpMyAdmin: http://localhost:8888
docker run -d --name pma --network wordpress -p 127.0.0.1:8888:80 \
  -e PMA_HOST=mysql \
  phpmyadmin/phpmyadmin

# WordPress: http://localhost:8080
# DB user/password must match MYSQL_USER/MYSQL_PASSWORD above
docker run -d --name wordpress --network wordpress -p 127.0.0.1:8080:80 \
  -e WORDPRESS_DB_HOST=mysql \
  -e WORDPRESS_DB_USER=wp_user \
  -e WORDPRESS_DB_PASSWORD=111 \
  -e WORDPRESS_DB_NAME=wordpress_db \
  wordpress
```

`WORDPRESS_DB_HOST=mysql` ใช้ได้เพราะทั้งสอง container อยู่ใน network `wordpress` เดียวกัน (ดูหัวข้อที่ 5)

ลบ lab ทิ้ง:
```bash
docker rm -f wordpress pma mysql
docker network rm wordpress
```

---

## 10. Security

### สแกนหาช่องโหว่ใน image
```bash
docker scout quickview nginx   # summary (Docker Scout: built into Docker Desktop, needs docker login)
docker scout cves nginx        # list each CVE
trivy image nginx              # open-source alternative (install trivy separately)
```

### ลดสิทธิ์ของ container
```bash
# Run as a non-root user instead of root (default)
docker run --rm --user 1000:1000 busybox id

# Read-only root filesystem; give a writable /tmp only
docker run --rm --read-only --tmpfs /tmp busybox touch /tmp/ok

# Drop all Linux capabilities and block privilege escalation (e.g. via setuid).
# Still uid 0, but root without capabilities cannot do privileged actions:
docker run --rm busybox chown 1000 /tmp                         # works
docker run --rm --cap-drop ALL --security-opt no-new-privileges \
  busybox chown 1000 /tmp                                       # Operation not permitted

# Limit resources so one container cannot take down the host
docker run -d --memory 512m --cpus 1 nginx
```

### เปิดพอร์ตเฉพาะที่จำเป็น
```bash
docker run -d -p 8080:80 nginx            # reachable from any network the host is on
docker run -d -p 127.0.0.1:8080:80 nginx  # reachable only from this machine
```
Docker แก้กฎ firewall (iptables) เอง พอร์ตที่เปิดด้วย `-p` จึงอาจข้าม firewall อย่าง `ufw` ได้ เครื่องมือที่ไม่ควรเปิดให้คนอื่นเข้า เช่น phpMyAdmin หรือฐานข้อมูล ควร bind กับ `127.0.0.1`

### สิ่งที่ไม่ควรทำ
| ไม่ควร | เพราะ |
|---|---|
| `docker run --privileged` | container ได้สิทธิ์เกือบเท่า root ของ host |
| `-v /var/run/docker.sock:/var/run/docker.sock` | ใครคุม container นี้ได้ = คุม Docker ทั้งเครื่อง = เป็น root ของ host |
| ใช้ tag `latest` | build วันนี้กับพรุ่งนี้อาจได้คนละเวอร์ชัน ควรระบุเวอร์ชัน เช่น `mysql:8.4` |
| ใส่รหัสผ่านใน `ENV`/`ARG` ของ Dockerfile | ใครมี image ก็เห็นได้ด้วย `docker history` หรือ `docker inspect` |
| commit ไฟล์ `.env` ที่มีรหัสผ่านจริง | ใช้ `.env.example` เป็นตัวอย่าง แล้วใส่ `.env` ไว้ใน `.gitignore` (แบบใน repo นี้) |
| ใช้ image จากคนที่ไม่รู้จัก | ใช้ Docker Official Image หรือ Verified Publisher และสแกนก่อนใช้ |

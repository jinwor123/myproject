**รหัสโครงงาน:** 68-1_14_nrc-r1

**ชื่อโครงงาน (ไทย):** ระบบจัดการข้อมูลเพื่อการบริหารธุรกิจร้านค้าอาหารสัตว์

**Project Title (Eng):** Data platform for managing pet food stores

**อาจารย์ที่ปรึกษาโครงงาน:** อาจารย์ ด.ร นวฤกษ์ ชลารักษ์

**ผู้จัดทำโครงงาน:** (โปรดเขียนข้อมูลผู้จัดทำโครงงานตามฟอร์แมตดังแสดงในตัวอย่างด้านล่าง)
1. นายจิณณ์ วรสุทธิพิศาล  6309681762  jin.wor@dome.tu.ac.th
   
Manual / Instructions for your projects starts here !


## รายละเอียดโครงงาน
โครงงานนี้เป็นระบบสารสนเทศสำหรับจัดการสินค้าคงคลังและการขายหน้าร้าน พัฒนาด้วยภาษา Python และ Django Framework เพื่อช่วยให้ผู้ประกอบการสามารถจัดเก็บข้อมูลสินค้า ตรวจสอบสต็อก บันทึกการขาย และดูสรุปข้อมูลได้อย่างเป็นระบบ

## ความสามารถของระบบ
- จัดการข้อมูลสินค้า
- จัดการหมวดหมู่สินค้า
- จัดการหน่วยนับสินค้า
- ตรวจสอบจำนวนสินค้าคงเหลือ
- ระบบขายหน้าร้าน (POS)
- ออกใบเสร็จการขาย
- ยกเลิกใบเสร็จและคืนสินค้าเข้าสต็อก
- ดูประวัติการขาย
- สรุปยอดขายและกำไร

## เทคโนโลยีที่ใช้
- Python
- Django
- HTML
- CSS
- MySQL

## โครงสร้างโฟลเดอร์ย่อย
```text
myproject/
├── dashboard/
   ├──__pycache__
   ├──migrations
   ├──__init__.py
   ├──apps.py
   ├──forms.py
   ├──models.py
   ├──tests.py
   ├──urls.py
   ├──views.py
├──inventoryproject
   ├──__pycache__
   ├──__init__.py
   ├──asgi.py
   ├──settings.py
   ├──urls.py
   ├──wsgi.py
├── pos/
   ├──__pycache__
   ├──migrations
   ├──__init__.py
   ├──apps.py
   ├──forms.py
   ├──models.py
   ├──tests.py
   ├──urls.py
   ├──views.py
├── templates/
   ├── dashboard/
      ├──category.html
      ├──index.html
      ├──order.html
      ├──product.html
      ├──summary.html
      ├──unit.html
   ├── partials/
      ├──base.html
      ├──nav.html
      ├──topnav.html
   ├── pos/
      ├──cashier.html
      ├──receipt.html
├── static/
   ├──style.css
├── db.sqlite3
├── manage.py
└── requirements.txt
```

## โปรแกรมที่ต้องติดตั้ง
- Python 3
- pip
- Git
- Web Browser
- Mysql workbench (กรณีใช้งาน MySQL)

## วิธีติดตั้งและตั้งค่า
1. Clone โปรเจกต์
```bash
git clone https://github.com/ComSciThammasatU/2568-2-cs403-final-submission-68-1_14_nrc-r1
```
```bash
cd 2568-2-cs403-final-submission-68-1_14_nrc-r1
```
```bash
cd myproject
```
```bash
code .
```
2.  สร้าง virtual environment
```cmd
python -m venv venv 
```
```cmd
py -m venv venv
```
3. เปิดใช้งาน virtual environment

### Windows
```cmd
venv\Scripts\activate
```

4. ติดตั้ง package ที่จำเป็น
```cmd
pip install -r requirements.txt
```

5. ติดตั้ง MySQL Workbench 8.0 CE
### Url
```cmd
https://dev.mysql.com/downloads/installer/

```
## การตั้งค่าฐานข้อมูล MySQL ใน settings.py
ให้แก้ไขไฟล์ `myproject/settings.py` ในส่วน `DATABASES` ให้ตรงกับเครื่องที่ใช้

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### ตัวอย่างการสร้างฐานข้อมูล MySQL Workbench
```MySQL Workbench
    CREATE DATABASE myproject_db ;
```

> หมายเหตุ: ต้องสร้างฐานข้อมูลใน MySQL ให้เรียบร้อยก่อน แล้วจึงค่อยรัน migration

6. ทำ migration
```cmd
python manage.py makemigrations 
```
หรือ
```cmd
 py manage.py makemigrations
```
```cmd
python manage.py migrate
```
หรือ
```cmd
 py manage.py migrate
```

7. รันโปรแกรม
```cmd
python manage.py runserver
```
```cmd
py manage.py runserver
```
## วิธีใช้งาน
- เข้าใช้งานผ่าน browser ที่ `http://127.0.0.1:8000/`
- ใช้เมนู Product เพื่อจัดการสินค้า
- ใช้เมนู Category เพื่อจัดการหมวดหมู่
- ใช้เมนู Unit เพื่อจัดการหน่วยนับ
- ใช้หน้า POS สำหรับขายสินค้า
- ใช้หน้า Order History เพื่อตรวจสอบประวัติการขาย
- ใช้หน้า Summary เพื่อดูสรุปยอดขายและกำไร

## การทดสอบระบบ
```cmd
python manage.py test
```
```cmd
py manage.py test
```

<h1>วิธีส่ง Email ด้วย SMTP ในโค้ด Python</h1>

<h3 style="color:red;">ตัวอย่างโค้ด</h3>

### Email ผู้ส่ง:
sender_email = "xxxxx@gmail.com"

#### ใส่ Google App Password
#### 1. เปิด 2-Factor Authentication ของ Google
#### 2. ไป generate APP Password ที่ลิงค์นี้ https://myaccount.google.com/apppasswords
#### 3. เอา APP Password ที่ได้มาจาก Google มาใส่ที่ตัวแปร sender_password (App Password เป็นคนละตัวกับ Password ปกติที่ Login Gmail)
sender_password = "lahhkhaadxzevduo"

### Email ผู้รับ
recipient_email = "aaaa@gmail.com"

### หัวข้อ
subject = "Test Email"

### ข้อความ
message = "This is a test email sent from Python."

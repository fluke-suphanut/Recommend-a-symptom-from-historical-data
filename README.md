# Recommend a symptom from historical data

โปรเจกต์นี้พัฒนาระบบ **แนะนำอาการ** จากข้อมูลผู้ป่วยย้อนหลัง  
เมื่อผู้ใช้ระบุข้อมูลส่วนตัว (เพศ, อายุ) และอาการที่มี ระบบจะเสนออาการเพิ่มเติมที่ผู้ป่วยซึ่งมีลักษณะคล้ายกันเคยรายงาน

## Data Preparation

- ทำความสะอาดและเตรียมข้อมูลผู้ป่วย 1,000 ราย
- แปลง `search_term` ให้เป็นรายการอาการ (list)
- เข้ารหัสเพศ (ชาย=0, หญิง=1)

## Basic Recommender

- ค้นหาผู้ป่วยที่มีอาการบางส่วนเหมือนกับผู้ใช้
- แนะนำอาการที่มักเกิดร่วมกัน แต่ผู้ใช้ยังไม่ได้เลือก

## Advanced Recommender

- แปลงอาการเป็นเวกเตอร์ด้วย `MultiLabelBinarizer`
- จัดกลุ่มผู้ป่วยด้วย `KMeans` จำนวน 5 กลุ่ม
- แนะนำอาการที่พบมากในกลุ่มเดียวกัน

## API Interface

**Method:** `POST`  
**Description:** แนะนำอาการเพิ่มเติมจากอาการที่ผู้ใช้กรอก โดยใช้วิธี Content-Based Filtering
**Example Input**

```json
{
  "gender": "female",
  "age": 30,
  "symptoms": ["ไอ", "มีเสมหะ"]
}
```

**Example Output**

```json
{
  "recommendations": ["ไข้", "แน่นจมูก", "เจ็บคอ"]
}
```

## recommend-advanced

Method: POST
Description: แนะนำอาการจากกลุ่มผู้ป่วยที่มีลักษณะคล้ายกัน
**Example Input**

```json
{
  "gender": "female",
  "age": 30,
  "symptoms": ["ไอ", "มีเสมหะ"]
}
```

**Example Output**

```json
{
  "recommendations": ["Fever", "แน่นจมูก", "เสมหะไหลลงคอ"]
}
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Start API Server

```bash
uvicorn api_main:app --reload
```

## Test API

เปิดเบราว์เซอร์ไปที่ http://127.0.0.1:8000/docs
เพื่อใช้งาน Swagger UI และทดสอบ API

## Tech Stack

- Python 3.10+
- FastAPI – ใช้สร้าง REST API
- scikit-learn – ใช้จัดกลุ่มด้วย KMeans
- pandas – จัดการและวิเคราะห์ข้อมูล
- Uvicorn – รัน API Server

## output

[here](output.pdf)

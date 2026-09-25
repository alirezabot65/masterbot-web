from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests

app = FastAPI(title="MASTERBOT Platform API")

URL = "https://messengerg2c1.rubika.ir/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-A057F) AppleWebKit/537.36",
    "Content-Type": "application/json"
}

class SendCodeRequest(BaseModel):
    phone_number: str

class VerifyCodeRequest(BaseModel):
    phone_number: str
    phone_code_hash: str
    user_code: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/send-code")
async def send_code(data: SendCodeRequest):
    payload = {
        "api_version": "5",
        "client": {"app_name": "Main", "app_version": "4.3.3", "platform": "Android", "package": "ir.resaneh1.iptv"},
        "data": {"phone_number": data.phone_number, "send_type": "SMS"},
        "method": "sendCode"
    }
    res = requests.post(URL, json=payload, headers=HEADERS, timeout=10).json()
    phone_code_hash = res.get("data", {}).get("phone_code_hash")
    
    if not phone_code_hash:
        raise HTTPException(status_code=400, detail="ارسال کد با خطا مواجه شد. شماره را بررسی کنید.")
        
    return {"status": "success", "phone_code_hash": phone_code_hash}

@app.post("/api/verify-code")
async def verify_code(data: VerifyCodeRequest):
    payload = {
        "api_version": "5",
        "client": {"app_name": "Main", "app_version": "4.3.3", "platform": "Android", "package": "ir.resaneh1.iptv"},
        "data": {
            "phone_code": data.user_code,
            "phone_code_hash": data.phone_code_hash,
            "phone_number": data.phone_number
        },
        "method": "signIn"
    }
    res = requests.post(URL, json=payload, headers=HEADERS, timeout=10).json()
    auth_token = res.get("data", {}).get("auth")
    
    if not auth_token:
        raise HTTPException(status_code=400, detail="کد وارد شده اشتباه است.")
        
    return {
        "status": "success", 
        "message": "ورود موفقیت‌آمیز بود! ربات فعال شد.",
        "auth_token": auth_token
    }

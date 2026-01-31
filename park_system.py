from typing import Optional
from fastapi import FastAPI, HTTPException, Path, Depends ,status, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timedelta
import jwt
import uuid
from datetime import datetime

def gen_token():
    return uuid.uuid4().hex

def gen_code():
    return uuid.uuid4().hex[:6].upper()

def gen_id():
    return str(uuid.uuid4())


admin_key = 'ADMIN123'
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users = {}
admins = {}
session = {}
sesh = {}
payments = {}

def authenticate_user(username: str, password: str, role :dict):
    user = role.get(username)
    if not user:
        return None
    if password != user['password']:
        return None
    return user

class UserCreate(BaseModel):
    username: str = Field(..., min_length=2)
    password: str = Field(...,min_length=8)

class AdminCreate(BaseModel):
    username: str = Field(..., min_length=2)
    password: str = Field(...,min_length=8)
    secret_key: str

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=2)
    password: str = Field(...,min_length=8)

class VehicleCreate(BaseModel):
    number_plate: str
    vehicle_type: str

class SeshCreate(BaseModel):
    vehicle_id: str

class VerifyCodeRequest(BaseModel):
    code: str

class PaymentByPlate(BaseModel):
    plate_number: str
    amount: int



@app.post("/register/user",status_code=201)
def create_user(data: UserCreate):
    if data.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = {
        'username':data.username,
        'password':data.password,
        'vehicles': {},
        'created_at':datetime.now()
    }
    users[data.username] = new_user
    return {
        "message": "User registered",
        "user_id": data.username
    }

@app.post("/register/admin")
def register_admin(data: AdminCreate):

    if data.secret_key != admin_key:
        raise HTTPException(403, "Not allowed to create admin")
    new_admin = {
        'username':data.username,
        'password':data.password,
        'created_at':datetime.now()
    }
    admins[data.username] = new_admin
    return {
        "message": "User registered",
        "user_id": data.username
    }

@app.post('/login/user',status_code=201)
def login_user(data: LoginRequest):
    user = authenticate_user(data.username,data.password,users)
    if user :
        token = gen_token()
        session[token] = {
                "role": "user",
                "user_id": user["username"]
            }
        return {
                "message": "Login successful",
                "token": token,
                "user_id": user["username"]
            }
    else:
        raise HTTPException(401, "Invalid username or password")
    

@app.post('/login/admin',status_code=201)
def login_admin(data: LoginRequest):
    admin = authenticate_user(data.username,data.password,users)
    if admin :
        token = gen_token()
        session[token] = {
                "role": "admin",
                "user_id": admin["username"]
            }
        return {
                "message": "Login successful",
                "token": token,
                "user_id": admin["username"]
            }
    else:
        raise HTTPException(401, "Invalid username or password")
    
def get_current_user(token: str = Header(...)):

    if token not in session:
        raise HTTPException(401, "Invalid or expired token")

    session = session[token]

    if session["role"] != "user":
        raise HTTPException(403, "User access only")

    return session["user_id"]

def get_current_admin(token: str = Header(...)):

    if token not in session:
        raise HTTPException(401, "Invalid or expired token")

    session = session[token]

    if session["role"] != "admin":
        raise HTTPException(403, "Admin access only")

    return session["admin_id"]

@app.post("/vehicles")
def add_vehicle(
    data: VehicleCreate,
    user_id: str = Depends(get_current_user)
):
    new_vehicle = {
        "user_id": user_id,
        "plate_number": data.number_plate,
        "vehicle_type": data.vehicle_type
    }
    users[user_id]['vehicles'][data.number_plate] = new_vehicle

    return {
        "message": "Vehicle added",
    }

@app.post("/visits/checkin")
def create_visit(
    data: SeshCreate,
    user_id: str = Depends(get_current_user)
):

    
    if data.vehicle_id not in users[user_id]['vehicles']:
        raise HTTPException(404, "Vehicle not found")

    vehicle = users[user_id]['vehicles'][data.vehicle_id]

    if vehicle["user_id"] != user_id:
        raise HTTPException(403, "This is not your vehicle")

   
    for v in sesh.values():
        if (
            v["plate_number"] == vehicle["plate_number"]
            and v["is_active"]
        ):
            raise HTTPException(400, "Vehicle already checked in")


    code = gen_code()

    sesh[data.vehicle_id] = {
        "user_id": user_id,
        "vehicle_id": data.vehicle_id,
        "plate_number": vehicle["plate_number"],
        "code": code,
        "checkin_time": datetime.now(),
        "is_active": False,
        "checkout_time": None
    }

    return {
        "message": "Check-in created",
        "code": code,
    }

@app.post("/admin/verify-code")
def verify_code(
    data: VerifyCodeRequest,
    admin_id: str = Depends(get_current_admin)
):

    for visit in sesh.values():
        if visit["code"] == data.code:

            if visit["checkout_time"] is not None:
                raise HTTPException(400, "session already closed")

            if visit["is_active"]:
                raise HTTPException(400, "session already active")

            visit["is_active"] = True

            return {
                "message": "Visit activated",
                "plate_number": visit["plate_number"]
            }

    raise HTTPException(404, "Invalid code")

@app.post("/payments/by-visit")
def pay_by_visit(
    data: PaymentByPlate,
    admin_id: str = Depends(get_current_admin)
):

    if data.plate_number not in sesh:
        raise HTTPException(404, "session not found")

    visit = sesh[data.plate_number]

    if visit["checkout_time"] is not None:
        raise HTTPException(400, "Already paid")

    if not visit["is_active"]:
        raise HTTPException(400, "session not active")

    payment_id = gen_id()

    payments[payment_id] = {
        "id": payment_id,
        "plate_number": visit["plate_number"],
        "amount": data.amount,
        "paid_at": datetime.now()
    }

    visit["is_active"] = False
    visit["checkout_time"] = datetime.nowow()

    return {
        "message": "Payment successful",
        "payment_id": payment_id,
        "plate_number": visit["plate_number"]
    }

@app.post("/payments/by-plate")
def pay_by_plate(
    data: PaymentByPlate,
    admin_id: str = Depends(get_current_admin)
):

    active_visit = None

    for visit in sesh.values():
        if (
            visit["plate_number"] == data.plate_number
            and visit["is_active"]
            and visit["checkout_time"] is None
        ):
            active_visit = visit
            break

    if not active_visit:
        raise HTTPException(404, "No active visit for this plate")

    payment_id = gen_id()

    payments[payment_id] = {
        "id": payment_id,
        "visit_id": active_visit["id"],
        "plate_number": data.plate_number,
        "amount": data.amount,
        "paid_at": datetime.now()
    }

    
    active_visit["is_active"] = False
    active_visit["checkout_time"] = datetime.now()

    return {
        "message": "Payment successful",
        "payment_id": payment_id,
        "plate_number": data.plate_number
    }


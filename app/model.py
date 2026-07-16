from pydantic import BaseModel, EmailStr


# -------------------------
# Product Model
# -------------------------

class Product(BaseModel):

    product_name: str
    category: str
    stock: int
    price: float


# -------------------------
# Prediction Model
# -------------------------

class Prediction(BaseModel):

    product_name: str
    category: str
    price: float
    stock: int
    daily_sales: int
    lead_time: int


# -------------------------
# Prediction History Model
# -------------------------

class PredictionHistory(BaseModel):

    product_name: str
    category: str
    predicted_demand: int
    recommended_stock: int
    restock_status: str
    demand_level: str


# -------------------------
# User Register Model
# -------------------------

class UserRegister(BaseModel):

    name: str
    email: EmailStr
    password: str


# -------------------------
# User Login Model
# -------------------------

class UserLogin(BaseModel):

    email: EmailStr
    password: str
    
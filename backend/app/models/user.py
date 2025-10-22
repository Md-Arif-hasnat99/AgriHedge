"""
Pydantic models for user authentication and profiles
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration"""
    FARMER = "farmer"
    FPO = "fpo"
    ADMIN = "admin"


class CropType(str, Enum):
    """Supported crop types"""
    SOYBEAN = "soybean"
    MUSTARD = "mustard"
    GROUNDNUT = "groundnut"
    SUNFLOWER = "sunflower"


class UserBase(BaseModel):
    """Base user model"""
    email: Optional[EmailStr] = None
    phone: str = Field(..., description="Phone number with country code")
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole = UserRole.FARMER
    preferred_language: str = Field(default="en", description="ISO language code")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format"""
        # Basic validation for Indian phone numbers
        if not v.startswith('+'):
            v = '+91' + v
        if len(v) < 10:
            raise ValueError('Invalid phone number')
        return v


class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=6, max_length=100)
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Ensure passwords match"""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class UserLogin(BaseModel):
    """User login model"""
    username: str = Field(..., description="Email or phone number")
    password: str


class Token(BaseModel):
    """JWT token response model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token data model"""
    user_id: str
    role: UserRole


class FarmerProfile(BaseModel):
    """Farmer-specific profile data"""
    farm_size: float = Field(..., description="Farm size in acres")
    crops: List[CropType] = Field(default=[CropType.SOYBEAN])
    state: str
    district: str
    village: Optional[str] = None
    pincode: str
    fpo_member: bool = False
    fpo_name: Optional[str] = None
    annual_production: Optional[float] = None


class FPOProfile(BaseModel):
    """FPO-specific profile data"""
    fpo_name: str = Field(..., min_length=2, max_length=200)
    registration_number: str
    member_count: int = Field(..., ge=0)
    state: str
    district: str
    primary_crops: List[CropType]
    total_acreage: Optional[float] = None


class UserInDB(UserBase):
    """User model as stored in database"""
    id: str = Field(alias="_id")
    hashed_password: str
    farmer_profile: Optional[FarmerProfile] = None
    fpo_profile: Optional[FPOProfile] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "email": "farmer@example.com",
                "phone": "+919876543210",
                "full_name": "Ramesh Kumar",
                "role": "farmer",
                "preferred_language": "hi",
                "is_active": True,
                "is_verified": True
            }
        }


class UserResponse(UserBase):
    """User response model (without sensitive data)"""
    id: str
    farmer_profile: Optional[FarmerProfile] = None
    fpo_profile: Optional[FPOProfile] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """User update model"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    preferred_language: Optional[str] = None
    farmer_profile: Optional[FarmerProfile] = None
    fpo_profile: Optional[FPOProfile] = None


class PasswordChange(BaseModel):
    """Password change model"""
    current_password: str
    new_password: str = Field(..., min_length=6)
    confirm_new_password: str
    
    @validator('confirm_new_password')
    def passwords_match(cls, v, values):
        """Ensure new passwords match"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('New passwords do not match')
        return v

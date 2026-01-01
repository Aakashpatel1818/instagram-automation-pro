"""MongoDB database models using Pydantic and Motor"""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid objectid {v}")
        return ObjectId(v)

    def __repr__(self):
        return f"ObjectId('{self}')" 


class StatusEnum(str, Enum):
    """Status enum for actions"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    SKIPPED = "skipped"


class AutomationModeEnum(str, Enum):
    """Automation mode enum"""
    COMMENT_ONLY = "comment_only"
    COMMENT_AND_DM = "comment_and_dm"


class User(BaseModel):
    """User model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    instagram_user_id: str
    instagram_access_token: str
    instagram_token_expiry: Optional[datetime] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "instagram_user_id": "123456789"
            }
        }


class AutomationRule(BaseModel):
    """Automation rule model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    name: str
    description: Optional[str] = None
    keyword_trigger: str  # Trigger word/phrase
    response_message: str  # Template message to send
    automation_mode: AutomationModeEnum = AutomationModeEnum.COMMENT_ONLY
    is_active: bool = True
    case_sensitive: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_schema_extra = {
            "example": {
                "name": "Auto Reply to Orders",
                "keyword_trigger": "@order",
                "response_message": "Thanks for your interest! DM us for more details.",
                "automation_mode": "comment_and_dm"
            }
        }


class CommentLog(BaseModel):
    """Comment activity log model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    rule_id: Optional[str] = None
    instagram_post_id: str
    commenter_id: str
    commenter_username: str
    comment_text: str
    response_sent: str  # The message we sent back
    status: StatusEnum
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True


class DMLog(BaseModel):
    """DM activity log model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    rule_id: Optional[str] = None
    recipient_id: str
    recipient_username: str
    message_text: str
    automation_mode: AutomationModeEnum
    status: StatusEnum
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True

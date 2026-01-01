"""Pydantic schemas for API requests/responses"""

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class AutomationModeEnum(str, Enum):
    COMMENT_ONLY = "comment_only"
    COMMENT_AND_DM = "comment_and_dm"


class StatusEnum(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    SKIPPED = "skipped"


# Auth Schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


# Rule Schemas
class CreateRuleRequest(BaseModel):
    name: str
    description: Optional[str] = None
    keyword_trigger: str
    response_message: str
    automation_mode: AutomationModeEnum = AutomationModeEnum.COMMENT_ONLY
    case_sensitive: bool = False


class UpdateRuleRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    keyword_trigger: Optional[str] = None
    response_message: Optional[str] = None
    automation_mode: Optional[AutomationModeEnum] = None
    case_sensitive: Optional[bool] = None
    is_active: Optional[bool] = None


class RuleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    keyword_trigger: str
    response_message: str
    automation_mode: AutomationModeEnum
    is_active: bool
    case_sensitive: bool
    created_at: datetime
    updated_at: datetime


# Log Schemas
class CommentLogSchema(BaseModel):
    _id: Optional[str] = None
    instagram_post_id: str
    commenter_username: str
    comment_text: str
    response_sent: str
    status: StatusEnum
    error_message: Optional[str]
    created_at: datetime


class DMLogSchema(BaseModel):
    _id: Optional[str] = None
    recipient_username: str
    message_text: str
    automation_mode: AutomationModeEnum
    status: StatusEnum
    error_message: Optional[str]
    created_at: datetime


class PaginationSchema(BaseModel):
    total: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool
    total_pages: int


class PaginatedLogsSchema(BaseModel):
    data: List[dict]
    pagination: PaginationSchema


class DashboardStatsSchema(BaseModel):
    total_comments: int
    total_dms_sent: int
    active_rules: int
    engagement_rate: float
    today_comments: int
    today_dms_sent: int
    response_time_avg: float
    success_rate: float
    failed_actions: int
    weekly_activity: List[dict]
    today_date: str


# Webhook Schemas
class WebhookEntry(BaseModel):
    id: str
    changes: List[dict]


class WebhookRequest(BaseModel):
    object: str
    entry: List[WebhookEntry]


# Error Response
class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int

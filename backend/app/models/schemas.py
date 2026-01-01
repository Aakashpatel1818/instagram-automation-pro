"""Pydantic schemas for API requests and responses"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class AutomationModeEnum(str, Enum):
    """Automation mode types"""
    COMMENT_ONLY = "comment_only"
    COMMENT_AND_DM = "comment_and_dm"


# ============================================================================
# LOG & ACTIVITY SCHEMAS
# ============================================================================

class CommentLogSchema(BaseModel):
    """Schema for comment logs"""
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    post_id: str
    comment_id: str
    username: str
    comment_text: str
    reply_sent: str
    timestamp: datetime
    rule_applied: str
    status: str = "sent"  # sent, failed, pending

    class Config:
        populate_by_name = True


class DMLogSchema(BaseModel):
    """Schema for DM logs"""
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    recipient_id: str
    recipient_username: str
    message_sent: str
    timestamp: datetime
    rule_applied: str
    status: str = "sent"  # sent, failed, pending
    mode: AutomationModeEnum = AutomationModeEnum.COMMENT_AND_DM

    class Config:
        populate_by_name = True


class ActivityLogSchema(BaseModel):
    """Schema for general activity logs"""
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    action: str  # comment_sent, dm_sent, rule_created, rule_deleted
    details: dict
    timestamp: datetime
    status: str = "success"

    class Config:
        populate_by_name = True


# ============================================================================
# STATISTICS & ANALYTICS SCHEMAS
# ============================================================================

class DailyStatsSchema(BaseModel):
    """Schema for daily statistics"""
    user_id: str
    date: str  # YYYY-MM-DD format
    comments_count: int = 0
    dms_count: int = 0
    failed_comments: int = 0
    failed_dms: int = 0
    active_rules: int = 0
    engagement_rate: float = 0.0


class ChartDataPointSchema(BaseModel):
    """Schema for chart data point"""
    date: str
    comments: int
    dms: int
    failed: int = 0


class WeeklyActivitySchema(BaseModel):
    """Schema for weekly activity data"""
    data_points: List[ChartDataPointSchema]
    total_comments: int
    total_dms: int
    average_daily_comments: float
    average_daily_dms: float


class DashboardStatsSchema(BaseModel):
    """Schema for dashboard statistics response"""
    total_comments: int
    total_dms_sent: int
    active_rules: int
    engagement_rate: float
    today_comments: int
    today_dms_sent: int
    response_time_avg: float  # in seconds
    success_rate: float  # percentage
    failed_actions: int
    weekly_activity: WeeklyActivitySchema
    today_date: str


class EngagementMetricsSchema(BaseModel):
    """Schema for engagement metrics"""
    total_actions: int
    successful_actions: int
    failed_actions: int
    success_rate: float
    avg_response_time: float
    engagement_rate: float
    conversion_rate: float


# ============================================================================
# RULES SCHEMAS
# ============================================================================

class AutomationRuleSchema(BaseModel):
    """Schema for automation rules"""
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    name: str
    keyword_trigger: str
    comment_reply: str
    dm_message: Optional[str] = None
    mode: AutomationModeEnum = AutomationModeEnum.COMMENT_ONLY
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    total_triggered: int = 0
    successful_executions: int = 0

    class Config:
        populate_by_name = True


# ============================================================================
# PAGINATION SCHEMAS
# ============================================================================

class PaginationSchema(BaseModel):
    """Schema for paginated responses"""
    total: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool
    total_pages: int


class PaginatedLogsSchema(BaseModel):
    """Schema for paginated logs response"""
    data: List[CommentLogSchema]
    pagination: PaginationSchema


# ============================================================================
# TIME RANGE SCHEMAS
# ============================================================================

class TimeRangeSchema(BaseModel):
    """Schema for time range queries"""
    start_date: Optional[str] = None  # YYYY-MM-DD
    end_date: Optional[str] = None    # YYYY-MM-DD
    days: Optional[int] = 7  # Last N days (default 7)

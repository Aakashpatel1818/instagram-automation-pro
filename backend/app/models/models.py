"""MongoDB document models for the application"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class AutomationModeEnum(str, Enum):
    """Automation mode types"""
    COMMENT_ONLY = "comment_only"
    COMMENT_AND_DM = "comment_and_dm"


class StatusEnum(str, Enum):
    """Status types for logs"""
    SENT = "sent"
    FAILED = "failed"
    PENDING = "pending"
    SKIPPED = "skipped"


class CommentLog:
    """MongoDB document for comment logs"""

    def __init__(
        self,
        user_id: str,
        post_id: str,
        comment_id: str,
        username: str,
        comment_text: str,
        reply_sent: str,
        rule_applied: str,
        status: str = StatusEnum.SENT,
        timestamp: datetime = None,
        _id: Optional[str] = None
    ):
        self._id = _id
        self.user_id = user_id
        self.post_id = post_id
        self.comment_id = comment_id
        self.username = username
        self.comment_text = comment_text
        self.reply_sent = reply_sent
        self.rule_applied = rule_applied
        self.status = status
        self.timestamp = timestamp or datetime.utcnow()
        self.created_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB"""
        data = {
            "user_id": self.user_id,
            "post_id": self.post_id,
            "comment_id": self.comment_id,
            "username": self.username,
            "comment_text": self.comment_text,
            "reply_sent": self.reply_sent,
            "rule_applied": self.rule_applied,
            "status": self.status,
            "timestamp": self.timestamp,
            "created_at": self.created_at
        }
        if self._id:
            data["_id"] = self._id
        return data


class DMLog:
    """MongoDB document for DM logs"""

    def __init__(
        self,
        user_id: str,
        recipient_id: str,
        recipient_username: str,
        message_sent: str,
        rule_applied: str,
        mode: str = AutomationModeEnum.COMMENT_AND_DM,
        status: str = StatusEnum.SENT,
        timestamp: datetime = None,
        _id: Optional[str] = None
    ):
        self._id = _id
        self.user_id = user_id
        self.recipient_id = recipient_id
        self.recipient_username = recipient_username
        self.message_sent = message_sent
        self.rule_applied = rule_applied
        self.mode = mode
        self.status = status
        self.timestamp = timestamp or datetime.utcnow()
        self.created_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB"""
        data = {
            "user_id": self.user_id,
            "recipient_id": self.recipient_id,
            "recipient_username": self.recipient_username,
            "message_sent": self.message_sent,
            "rule_applied": self.rule_applied,
            "mode": self.mode,
            "status": self.status,
            "timestamp": self.timestamp,
            "created_at": self.created_at
        }
        if self._id:
            data["_id"] = self._id
        return data


class ActivityLog:
    """MongoDB document for activity logs"""

    def __init__(
        self,
        user_id: str,
        action: str,
        details: Dict[str, Any],
        status: str = "success",
        timestamp: datetime = None,
        _id: Optional[str] = None
    ):
        self._id = _id
        self.user_id = user_id
        self.action = action  # comment_sent, dm_sent, rule_created, etc.
        self.details = details
        self.status = status
        self.timestamp = timestamp or datetime.utcnow()
        self.created_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB"""
        data = {
            "user_id": self.user_id,
            "action": self.action,
            "details": self.details,
            "status": self.status,
            "timestamp": self.timestamp,
            "created_at": self.created_at
        }
        if self._id:
            data["_id"] = self._id
        return data


class DailyStats:
    """MongoDB document for daily statistics"""

    def __init__(
        self,
        user_id: str,
        date: str,  # YYYY-MM-DD
        comments_count: int = 0,
        dms_count: int = 0,
        failed_comments: int = 0,
        failed_dms: int = 0,
        active_rules: int = 0,
        engagement_rate: float = 0.0,
        _id: Optional[str] = None
    ):
        self._id = _id
        self.user_id = user_id
        self.date = date
        self.comments_count = comments_count
        self.dms_count = dms_count
        self.failed_comments = failed_comments
        self.failed_dms = failed_dms
        self.active_rules = active_rules
        self.engagement_rate = engagement_rate
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB"""
        data = {
            "user_id": self.user_id,
            "date": self.date,
            "comments_count": self.comments_count,
            "dms_count": self.dms_count,
            "failed_comments": self.failed_comments,
            "failed_dms": self.failed_dms,
            "active_rules": self.active_rules,
            "engagement_rate": self.engagement_rate,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if self._id:
            data["_id"] = self._id
        return data


class AutomationRule:
    """MongoDB document for automation rules"""

    def __init__(
        self,
        user_id: str,
        name: str,
        keyword_trigger: str,
        comment_reply: str,
        dm_message: Optional[str] = None,
        mode: str = AutomationModeEnum.COMMENT_ONLY,
        is_active: bool = True,
        _id: Optional[str] = None
    ):
        self._id = _id
        self.user_id = user_id
        self.name = name
        self.keyword_trigger = keyword_trigger
        self.comment_reply = comment_reply
        self.dm_message = dm_message
        self.mode = mode
        self.is_active = is_active
        self.total_triggered = 0
        self.successful_executions = 0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB"""
        data = {
            "user_id": self.user_id,
            "name": self.name,
            "keyword_trigger": self.keyword_trigger,
            "comment_reply": self.comment_reply,
            "dm_message": self.dm_message,
            "mode": self.mode,
            "is_active": self.is_active,
            "total_triggered": self.total_triggered,
            "successful_executions": self.successful_executions,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if self._id:
            data["_id"] = self._id
        return data

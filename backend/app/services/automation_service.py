"""Core automation service for executing comment/DM automation"""

from typing import Optional, List
from datetime import datetime
from app.services.instagram_service import InstagramService
from app.db.mongodb import get_database
from app.models.models import StatusEnum, AutomationModeEnum, CommentLog, DMLog
import logging
import re

logger = logging.getLogger(__name__)


class AutomationService:
    """Service for executing automation rules"""

    def __init__(self):
        self.db = get_database()
        self.instagram_service = InstagramService()

    async def process_comment(
        self,
        comment_id: str,
        post_id: str,
        comment_text: str,
        commenter_id: str,
        commenter_username: str
    ) -> bool:
        """
        Process a new comment and check if automation rules apply

        Args:
            comment_id: Instagram comment ID
            post_id: Instagram post ID
            comment_text: Text of the comment
            commenter_id: ID of the user who commented
            commenter_username: Username of the commenter

        Returns:
            True if automation executed, False otherwise
        """
        try:
            # Get post owner to find matching rules
            post = await self.db.posts.find_one({"instagram_post_id": post_id})
            if not post:
                logger.warning(f"Post not found: {post_id}")
                return False

            user_id = post["user_id"]

            # Find matching automation rules
            rules = await self.db.automation_rules.find({
                "user_id": user_id,
                "is_active": True
            }).to_list(None)

            matched_rule = None
            for rule in rules:
                if self._check_keyword_match(comment_text, rule):
                    matched_rule = rule
                    break

            if not matched_rule:
                logger.info(f"No matching rule for comment: {comment_id}")
                return False

            # Get user's Instagram token
            user = await self.db.users.find_one({"_id": user_id})
            if not user or not user.get("instagram_access_token"):
                logger.error(f"User not found or no token: {user_id}")
                return False

            access_token = user["instagram_access_token"]

            # Send comment reply
            comment_sent = await self.instagram_service.send_comment_reply(
                comment_id=comment_id,
                message=matched_rule["response_message"],
                access_token=access_token
            )

            # Log comment activity
            comment_log = CommentLog(
                user_id=user_id,
                rule_id=str(matched_rule["_id"]),
                instagram_post_id=post_id,
                commenter_id=commenter_id,
                commenter_username=commenter_username,
                comment_text=comment_text,
                response_sent=matched_rule["response_message"],
                status=StatusEnum.SENT if comment_sent else StatusEnum.FAILED
            )

            await self.db.comment_logs.insert_one(comment_log.dict())

            # Handle DM if automation mode is set
            if matched_rule["automation_mode"] == AutomationModeEnum.COMMENT_AND_DM:
                await self.process_auto_dm(
                    user_id=user_id,
                    rule_id=str(matched_rule["_id"]),
                    recipient_id=commenter_id,
                    recipient_username=commenter_username,
                    message=matched_rule["response_message"],
                    access_token=access_token
                )

            logger.info(f"✅ Automation executed for comment: {comment_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to process comment: {str(e)}")
            return False

    async def process_auto_dm(
        self,
        user_id: str,
        rule_id: str,
        recipient_id: str,
        recipient_username: str,
        message: str,
        access_token: str
    ) -> bool:
        """
        Send automatic DM based on rule
        """
        try:
            # Get user's business account ID
            user = await self.db.users.find_one({"_id": user_id})
            business_account_id = user.get("instagram_business_account_id")

            if not business_account_id:
                logger.error(f"No business account ID for user: {user_id}")
                return False

            # Send DM
            dm_sent = await self.instagram_service.send_dm(
                recipient_id=recipient_id,
                message=message,
                access_token=access_token,
                instagram_business_account_id=business_account_id
            )

            # Log DM activity
            dm_log = DMLog(
                user_id=user_id,
                rule_id=rule_id,
                recipient_id=recipient_id,
                recipient_username=recipient_username,
                message_text=message,
                automation_mode=AutomationModeEnum.COMMENT_AND_DM,
                status=StatusEnum.SENT if dm_sent else StatusEnum.FAILED
            )

            await self.db.dm_logs.insert_one(dm_log.dict())

            logger.info(f"✅ Auto DM sent to: {recipient_username}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to process auto DM: {str(e)}")
            return False

    def _check_keyword_match(self, text: str, rule: dict) -> bool:
        """
        Check if comment text matches the rule's keyword trigger
        """
        trigger = rule["keyword_trigger"]
        case_sensitive = rule.get("case_sensitive", False)

        if not case_sensitive:
            text = text.lower()
            trigger = trigger.lower()

        # Check for exact phrase match or word match
        return trigger in text or re.search(r'\b' + re.escape(trigger) + r'\b', text)

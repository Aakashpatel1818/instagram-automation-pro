"""Webhook processing service for Instagram events"""

from typing import Dict, Any, Optional
from app.services.automation_service import AutomationService
from app.db.mongodb import get_database
import logging

logger = logging.getLogger(__name__)


class WebhookService:
    """Service for processing Instagram webhooks"""

    def __init__(self):
        self.db = get_database()
        self.automation_service = AutomationService()

    async def process_webhook_event(self, event_data: Dict[str, Any]) -> bool:
        """
        Process incoming webhook event from Instagram

        Args:
            event_data: Webhook event data from Meta

        Returns:
            True if processed successfully
        """
        try:
            if "entry" not in event_data:
                logger.warning("Invalid webhook format")
                return False

            for entry in event_data["entry"]:
                changes = entry.get("changes", [])
                for change in changes:
                    field = change.get("field")
                    value = change.get("value", {})

                    # Process different event types
                    if field == "comments":
                        await self._process_comment_event(value)
                    elif field == "messages":
                        await self._process_message_event(value)

            logger.info("✅ Webhook processed successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to process webhook: {str(e)}")
            return False

    async def _process_comment_event(self, event_data: Dict[str, Any]):
        """
        Process comment event from webhook
        """
        try:
            comment_id = event_data.get("id")
            post_id = event_data.get("media", {}).get("id")
            text = event_data.get("text")
            from_user = event_data.get("from", {})
            user_id = from_user.get("id")
            username = from_user.get("username")

            logger.info(f"📝 New comment from {username}: {text}")

            # Trigger automation
            await self.automation_service.process_comment(
                comment_id=comment_id,
                post_id=post_id,
                comment_text=text,
                commenter_id=user_id,
                commenter_username=username
            )
        except Exception as e:
            logger.error(f"❌ Failed to process comment event: {str(e)}")

    async def _process_message_event(self, event_data: Dict[str, Any]):
        """
        Process message/DM event from webhook
        """
        try:
            message_text = event_data.get("text")
            from_user = event_data.get("from", {})
            user_id = from_user.get("id")
            username = from_user.get("username")

            logger.info(f"💬 New DM from {username}: {message_text}")
            # Additional DM processing logic can be added here
        except Exception as e:
            logger.error(f"❌ Failed to process message event: {str(e)}")

"""Instagram/Meta Graph API integration service"""

import httpx
from typing import Optional, Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class InstagramService:
    """Service for interacting with Instagram/Meta Graph API"""

    def __init__(self):
        self.base_url = settings.META_GRAPH_API_URL
        self.api_version = settings.META_API_VERSION
        self.timeout = settings.WEBHOOK_TIMEOUT_SECONDS

    async def send_comment_reply(
        self,
        comment_id: str,
        message: str,
        access_token: str
    ) -> bool:
        """
        Send a reply to an Instagram comment

        Args:
            comment_id: Instagram comment ID
            message: Reply message text
            access_token: User's Instagram access token

        Returns:
            True if successful, False otherwise
        """
        try:
            url = f"{self.base_url}/{self.api_version}/{comment_id}/replies"
            payload = {
                "message": message,
                "access_token": access_token
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                logger.info(f"✅ Comment reply sent: {comment_id}")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to send comment reply: {str(e)}")
            return False

    async def send_dm(
        self,
        recipient_id: str,
        message: str,
        access_token: str,
        instagram_business_account_id: str
    ) -> bool:
        """
        Send a direct message to an Instagram user

        Args:
            recipient_id: Recipient Instagram user ID
            message: DM message text
            access_token: User's Instagram access token
            instagram_business_account_id: Business account ID

        Returns:
            True if successful, False otherwise
        """
        try:
            url = f"{self.base_url}/{self.api_version}/{instagram_business_account_id}/messages"
            payload = {
                "recipient": {"id": recipient_id},
                "message": {"text": message},
                "access_token": access_token
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                logger.info(f"✅ DM sent to: {recipient_id}")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to send DM: {str(e)}")
            return False

    async def get_user_info(
        self,
        user_id: str,
        access_token: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get Instagram user information

        Args:
            user_id: Instagram user ID
            access_token: Instagram access token

        Returns:
            User info dictionary or None if failed
        """
        try:
            url = f"{self.base_url}/{self.api_version}/{user_id}"
            params = {
                "fields": "id,username,name,biography,followers_count,website",
                "access_token": access_token
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                logger.info(f"✅ User info retrieved: {user_id}")
                return response.json()
        except Exception as e:
            logger.error(f"❌ Failed to get user info: {str(e)}")
            return None

    def verify_webhook_token(self, token: str) -> bool:
        """
        Verify webhook verification token from Meta

        Args:
            token: Token from webhook request

        Returns:
            True if token matches, False otherwise
        """
        return token == settings.META_VERIFY_TOKEN

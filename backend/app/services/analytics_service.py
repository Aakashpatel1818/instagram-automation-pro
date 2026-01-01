"""Analytics and reporting service"""

from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any
from app.db.mongodb import get_database
from app.models.models import StatusEnum
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for analytics and reporting"""

    def __init__(self):
        self.db = get_database()

    async def get_dashboard_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get comprehensive dashboard statistics
        """
        try:
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            week_ago = today - timedelta(days=7)

            # Get counts
            total_comments = await self.db.comment_logs.count_documents({
                "user_id": user_id,
                "status": StatusEnum.SENT
            })

            total_dms = await self.db.dm_logs.count_documents({
                "user_id": user_id,
                "status": StatusEnum.SENT
            })

            active_rules = await self.db.automation_rules.count_documents({
                "user_id": user_id,
                "is_active": True
            })

            today_comments = await self.db.comment_logs.count_documents({
                "user_id": user_id,
                "status": StatusEnum.SENT,
                "created_at": {"$gte": today}
            })

            today_dms = await self.db.dm_logs.count_documents({
                "user_id": user_id,
                "status": StatusEnum.SENT,
                "created_at": {"$gte": today}
            })

            failed_actions = await self.db.comment_logs.count_documents({
                "user_id": user_id,
                "status": StatusEnum.FAILED
            }) + await self.db.dm_logs.count_documents({
                "user_id": user_id,
                "status": StatusEnum.FAILED
            })

            total_actions = total_comments + total_dms + failed_actions
            success_rate = (total_comments + total_dms) / total_actions * 100 if total_actions > 0 else 0

            # Get weekly activity
            weekly_data = await self._get_weekly_activity(user_id, week_ago)

            return {
                "total_comments": total_comments,
                "total_dms_sent": total_dms,
                "active_rules": active_rules,
                "engagement_rate": round((total_comments + total_dms) / max(total_comments + total_dms + failed_actions, 1) * 100, 2),
                "today_comments": today_comments,
                "today_dms_sent": today_dms,
                "response_time_avg": 0.5,  # Placeholder
                "success_rate": round(success_rate, 2),
                "failed_actions": failed_actions,
                "weekly_activity": weekly_data,
                "today_date": today.strftime("%Y-%m-%d")
            }
        except Exception as e:
            logger.error(f"Failed to get dashboard stats: {str(e)}")
            raise

    async def get_comment_logs(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        days: int = 7
    ) -> Tuple[List[Dict], int]:
        """
        Get paginated comment logs
        """
        try:
            date_filter = datetime.utcnow() - timedelta(days=days)
            
            query = {
                "user_id": user_id,
                "created_at": {"$gte": date_filter}
            }

            total = await self.db.comment_logs.count_documents(query)
            logs = await self.db.comment_logs.find(query)\
                .sort("created_at", -1)\
                .skip(skip)\
                .limit(limit)\
                .to_list(None)

            return logs, total
        except Exception as e:
            logger.error(f"Failed to get comment logs: {str(e)}")
            return [], 0

    async def get_dm_logs(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        days: int = 7
    ) -> Tuple[List[Dict], int]:
        """
        Get paginated DM logs
        """
        try:
            date_filter = datetime.utcnow() - timedelta(days=days)
            
            query = {
                "user_id": user_id,
                "created_at": {"$gte": date_filter}
            }

            total = await self.db.dm_logs.count_documents(query)
            logs = await self.db.dm_logs.find(query)\
                .sort("created_at", -1)\
                .skip(skip)\
                .limit(limit)\
                .to_list(None)

            return logs, total
        except Exception as e:
            logger.error(f"Failed to get DM logs: {str(e)}")
            return [], 0

    async def _get_weekly_activity(self, user_id: str, start_date: datetime) -> List[Dict]:
        """
        Get weekly activity breakdown
        """
        try:
            weekly_activity = []
            for i in range(7):
                date = start_date + timedelta(days=i)
                next_date = date + timedelta(days=1)

                comments = await self.db.comment_logs.count_documents({
                    "user_id": user_id,
                    "created_at": {"$gte": date, "$lt": next_date}
                })

                dms = await self.db.dm_logs.count_documents({
                    "user_id": user_id,
                    "created_at": {"$gte": date, "$lt": next_date}
                })

                weekly_activity.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "comments": comments,
                    "dms": dms,
                    "total": comments + dms
                })

            return weekly_activity
        except Exception as e:
            logger.error(f"Failed to get weekly activity: {str(e)}")
            return []

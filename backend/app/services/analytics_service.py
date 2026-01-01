"""Service for analytics and statistics operations"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from app.db.mongodb import get_db
from app.models.models import CommentLog, DMLog, DailyStats, StatusEnum
from bson import ObjectId


class AnalyticsService:
    """Service for handling analytics and dashboard statistics"""

    def __init__(self):
        self.db = get_db()

    async def get_dashboard_stats(self, user_id: str) -> Dict:
        """
        Get comprehensive dashboard statistics for a user
        Returns: total_comments, total_dms, active_rules, engagement_rate, etc.
        """
        today = datetime.utcnow().strftime("%Y-%m-%d")

        # Get today's stats
        today_stats = await self._get_today_stats(user_id)
        # Get all-time stats
        all_time_stats = await self._get_all_time_stats(user_id)
        # Get weekly activity data
        weekly_data = await self._get_weekly_activity(user_id)
        # Get engagement metrics
        metrics = await self._get_engagement_metrics(user_id)

        return {
            "total_comments": all_time_stats["total_comments"],
            "total_dms_sent": all_time_stats["total_dms_sent"],
            "active_rules": all_time_stats["active_rules"],
            "engagement_rate": metrics["engagement_rate"],
            "today_comments": today_stats["comments"],
            "today_dms_sent": today_stats["dms"],
            "response_time_avg": metrics["avg_response_time"],
            "success_rate": metrics["success_rate"],
            "failed_actions": all_time_stats["failed_actions"],
            "weekly_activity": weekly_data,
            "today_date": today
        }

    async def _get_today_stats(self, user_id: str) -> Dict:
        """
        Get today's statistics
        """
        today = datetime.utcnow().strftime("%Y-%m-%d")
        today_start = datetime.strptime(today, "%Y-%m-%d")
        today_end = today_start + timedelta(days=1)

        comments_col = self.db["comment_logs"]
        dms_col = self.db["dm_logs"]

        comments = await comments_col.count_documents({
            "user_id": user_id,
            "timestamp": {
                "$gte": today_start,
                "$lt": today_end
            }
        })

        dms = await dms_col.count_documents({
            "user_id": user_id,
            "timestamp": {
                "$gte": today_start,
                "$lt": today_end
            }
        })

        return {
            "comments": comments,
            "dms": dms
        }

    async def _get_all_time_stats(self, user_id: str) -> Dict:
        """
        Get all-time statistics
        """
        comments_col = self.db["comment_logs"]
        dms_col = self.db["dm_logs"]
        rules_col = self.db["automation_rules"]

        total_comments = await comments_col.count_documents({
            "user_id": user_id,
            "status": StatusEnum.SENT
        })

        total_dms = await dms_col.count_documents({
            "user_id": user_id,
            "status": StatusEnum.SENT
        })

        failed_comments = await comments_col.count_documents({
            "user_id": user_id,
            "status": StatusEnum.FAILED
        })

        failed_dms = await dms_col.count_documents({
            "user_id": user_id,
            "status": StatusEnum.FAILED
        })

        active_rules = await rules_col.count_documents({
            "user_id": user_id,
            "is_active": True
        })

        return {
            "total_comments": total_comments,
            "total_dms_sent": total_dms,
            "failed_actions": failed_comments + failed_dms,
            "active_rules": active_rules
        }

    async def _get_weekly_activity(self, user_id: str) -> Dict:
        """
        Get weekly activity data for charts
        """
        comments_col = self.db["comment_logs"]
        dms_col = self.db["dm_logs"]

        # Get last 7 days
        data_points = []
        total_comments = 0
        total_dms = 0

        for i in range(6, -1, -1):  # Last 7 days
            day = datetime.utcnow() - timedelta(days=i)
            day_start = datetime(day.year, day.month, day.day)
            day_end = day_start + timedelta(days=1)
            day_str = day_start.strftime("%a")  # Mon, Tue, etc.

            comments = await comments_col.count_documents({
                "user_id": user_id,
                "status": StatusEnum.SENT,
                "timestamp": {
                    "$gte": day_start,
                    "$lt": day_end
                }
            })

            dms = await dms_col.count_documents({
                "user_id": user_id,
                "status": StatusEnum.SENT,
                "timestamp": {
                    "$gte": day_start,
                    "$lt": day_end
                }
            })

            failed = await comments_col.count_documents({
                "user_id": user_id,
                "status": StatusEnum.FAILED,
                "timestamp": {
                    "$gte": day_start,
                    "$lt": day_end
                }
            }) + await dms_col.count_documents({
                "user_id": user_id,
                "status": StatusEnum.FAILED,
                "timestamp": {
                    "$gte": day_start,
                    "$lt": day_end
                }
            })

            data_points.append({
                "date": day_str,
                "comments": comments,
                "dms": dms,
                "failed": failed
            })

            total_comments += comments
            total_dms += dms

        avg_daily_comments = total_comments / 7 if total_comments > 0 else 0
        avg_daily_dms = total_dms / 7 if total_dms > 0 else 0

        return {
            "data_points": data_points,
            "total_comments": total_comments,
            "total_dms": total_dms,
            "average_daily_comments": round(avg_daily_comments, 2),
            "average_daily_dms": round(avg_daily_dms, 2)
        }

    async def _get_engagement_metrics(self, user_id: str) -> Dict:
        """
        Get engagement metrics
        """
        comments_col = self.db["comment_logs"]
        dms_col = self.db["dm_logs"]

        # Get all logs for the user
        comment_logs = await comments_col.find({
            "user_id": user_id
        }).to_list(length=None)

        dm_logs = await dms_col.find({
            "user_id": user_id
        }).to_list(length=None)

        total_actions = len(comment_logs) + len(dm_logs)
        successful_actions = len([l for l in comment_logs if l["status"] == StatusEnum.SENT]) + \
                           len([l for l in dm_logs if l["status"] == StatusEnum.SENT])
        failed_actions = total_actions - successful_actions

        success_rate = (successful_actions / total_actions * 100) if total_actions > 0 else 0
        engagement_rate = (successful_actions / max(1, len(set([l.get("username", "") for l in comment_logs])))) if comment_logs else 0
        conversion_rate = (len([l for l in dm_logs if l["status"] == StatusEnum.SENT]) / max(1, len(comment_logs))) if comment_logs else 0

        # Calculate average response time (mock data)
        avg_response_time = 2.5  # Mock: 2.5 seconds

        return {
            "total_actions": total_actions,
            "successful_actions": successful_actions,
            "failed_actions": failed_actions,
            "success_rate": round(success_rate, 2),
            "avg_response_time": avg_response_time,
            "engagement_rate": round(engagement_rate, 2),
            "conversion_rate": round(conversion_rate, 2)
        }

    async def get_comment_logs(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        days: int = 7
    ) -> Tuple[List[Dict], int]:
        """
        Get comment logs with pagination
        """
        comments_col = self.db["comment_logs"]

        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        query = {
            "user_id": user_id,
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date
            }
        }

        total = await comments_col.count_documents(query)
        logs = await comments_col.find(query).sort("timestamp", -1).skip(skip).limit(limit).to_list(length=limit)

        return logs, total

    async def get_dm_logs(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        days: int = 7
    ) -> Tuple[List[Dict], int]:
        """
        Get DM logs with pagination
        """
        dms_col = self.db["dm_logs"]

        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        query = {
            "user_id": user_id,
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date
            }
        }

        total = await dms_col.count_documents(query)
        logs = await dms_col.find(query).sort("timestamp", -1).skip(skip).limit(limit).to_list(length=limit)

        return logs, total

    async def record_comment_log(self, comment_log: CommentLog) -> str:
        """
        Record a comment log in the database
        """
        comments_col = self.db["comment_logs"]
        result = await comments_col.insert_one(comment_log.to_dict())
        return str(result.inserted_id)

    async def record_dm_log(self, dm_log: DMLog) -> str:
        """
        Record a DM log in the database
        """
        dms_col = self.db["dm_logs"]
        result = await dms_col.insert_one(dm_log.to_dict())
        return str(result.inserted_id)

    async def update_daily_stats(self, user_id: str, date: str) -> None:
        """
        Update or create daily statistics for a specific date
        """
        daily_stats_col = self.db["daily_stats"]
        comments_col = self.db["comment_logs"]
        dms_col = self.db["dm_logs"]
        rules_col = self.db["automation_rules"]

        date_start = datetime.strptime(date, "%Y-%m-%d")
        date_end = date_start + timedelta(days=1)

        comments = await comments_col.count_documents({
            "user_id": user_id,
            "status": StatusEnum.SENT,
            "timestamp": {"$gte": date_start, "$lt": date_end}
        })

        dms = await dms_col.count_documents({
            "user_id": user_id,
            "status": StatusEnum.SENT,
            "timestamp": {"$gte": date_start, "$lt": date_end}
        })

        failed_comments = await comments_col.count_documents({
            "user_id": user_id,
            "status": StatusEnum.FAILED,
            "timestamp": {"$gte": date_start, "$lt": date_end}
        })

        failed_dms = await dms_col.count_documents({
            "user_id": user_id,
            "status": StatusEnum.FAILED,
            "timestamp": {"$gte": date_start, "$lt": date_end}
        })

        active_rules = await rules_col.count_documents({
            "user_id": user_id,
            "is_active": True
        })

        engagement_rate = (comments / max(1, comments + failed_comments)) * 100 if comments > 0 else 0

        daily_stats = DailyStats(
            user_id=user_id,
            date=date,
            comments_count=comments,
            dms_count=dms,
            failed_comments=failed_comments,
            failed_dms=failed_dms,
            active_rules=active_rules,
            engagement_rate=engagement_rate
        )

        await daily_stats_col.update_one(
            {"user_id": user_id, "date": date},
            {"$set": daily_stats.to_dict()},
            upsert=True
        )

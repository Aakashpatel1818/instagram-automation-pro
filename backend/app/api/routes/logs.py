"""Logs and analytics routes"""

from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from datetime import datetime
from app.services.analytics_service import AnalyticsService
from app.models.schemas import (
    DashboardStatsSchema,
    PaginatedLogsSchema,
    CommentLogSchema,
    DMLogSchema,
    PaginationSchema
)
from app.core.security import get_current_user

router = APIRouter()


@router.get("/stats", response_model=DashboardStatsSchema)
async def get_statistics(current_user: str = Depends(get_current_user)):
    """
    Get comprehensive dashboard statistics
    
    Returns:
    - total_comments: Total comments processed
    - total_dms_sent: Total DMs sent
    - active_rules: Number of active automation rules
    - engagement_rate: Overall engagement rate
    - today_comments: Comments processed today
    - today_dms_sent: DMs sent today
    - response_time_avg: Average response time in seconds
    - success_rate: Success rate percentage
    - failed_actions: Total failed actions
    - weekly_activity: Weekly activity data for charts
    - today_date: Today's date (YYYY-MM-DD)
    """
    try:
        analytics = AnalyticsService()
        stats = await analytics.get_dashboard_stats(current_user)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch statistics: {str(e)}")


@router.get("/comments", response_model=PaginatedLogsSchema)
async def get_comment_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    days: int = Query(7, ge=1, le=90),
    current_user: str = Depends(get_current_user)
):
    """
    Get paginated comment activity logs
    
    Parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Number of records to return (default: 20, max: 100)
    - days: Filter logs from last N days (default: 7)
    
    Returns paginated comment logs with timestamps and details
    """
    try:
        analytics = AnalyticsService()
        logs, total = await analytics.get_comment_logs(
            user_id=current_user,
            skip=skip,
            limit=limit,
            days=days
        )

        # Convert ObjectId to string for response
        for log in logs:
            if "_id" in log:
                log["_id"] = str(log["_id"])

        # Calculate pagination info
        total_pages = (total + limit - 1) // limit
        current_page = (skip // limit) + 1
        has_next = current_page < total_pages
        has_previous = current_page > 1

        return {
            "data": logs,
            "pagination": {
                "total": total,
                "page": current_page,
                "page_size": limit,
                "has_next": has_next,
                "has_previous": has_previous,
                "total_pages": total_pages
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch comment logs: {str(e)}")


@router.get("/dms", response_model=PaginatedLogsSchema)
async def get_dm_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    days: int = Query(7, ge=1, le=90),
    current_user: str = Depends(get_current_user)
):
    """
    Get paginated DM activity logs
    
    Parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Number of records to return (default: 20, max: 100)
    - days: Filter logs from last N days (default: 7)
    
    Returns paginated DM logs with automation mode and status
    """
    try:
        analytics = AnalyticsService()
        logs, total = await analytics.get_dm_logs(
            user_id=current_user,
            skip=skip,
            limit=limit,
            days=days
        )

        # Convert ObjectId to string for response
        for log in logs:
            if "_id" in log:
                log["_id"] = str(log["_id"])

        # Calculate pagination info
        total_pages = (total + limit - 1) // limit
        current_page = (skip // limit) + 1
        has_next = current_page < total_pages
        has_previous = current_page > 1

        return {
            "data": logs,
            "pagination": {
                "total": total,
                "page": current_page,
                "page_size": limit,
                "has_next": has_next,
                "has_previous": has_previous,
                "total_pages": total_pages
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch DM logs: {str(e)}")


@router.get("/activity-summary")
async def get_activity_summary(
    days: int = Query(7, ge=1, le=90),
    current_user: str = Depends(get_current_user)
):
    """
    Get activity summary for specified number of days
    
    Parameters:
    - days: Number of days to include (default: 7)
    
    Returns:
    - total_comments: Total comments in period
    - total_dms: Total DMs in period
    - success_rate: Success rate percentage
    - failed_count: Number of failed actions
    - avg_daily_comments: Average comments per day
    - avg_daily_dms: Average DMs per day
    """
    try:
        analytics = AnalyticsService()
        logs, _ = await analytics.get_comment_logs(
            user_id=current_user,
            skip=0,
            limit=1000,
            days=days
        )
        dm_logs, _ = await analytics.get_dm_logs(
            user_id=current_user,
            skip=0,
            limit=1000,
            days=days
        )

        from app.models.models import StatusEnum
        
        total_comments = len([l for l in logs if l["status"] == StatusEnum.SENT])
        total_dms = len([l for l in dm_logs if l["status"] == StatusEnum.SENT])
        failed_comments = len([l for l in logs if l["status"] == StatusEnum.FAILED])
        failed_dms = len([l for l in dm_logs if l["status"] == StatusEnum.FAILED])

        total_actions = total_comments + total_dms + failed_comments + failed_dms
        success_count = total_comments + total_dms
        success_rate = (success_count / total_actions * 100) if total_actions > 0 else 0

        return {
            "total_comments": total_comments,
            "total_dms": total_dms,
            "success_rate": round(success_rate, 2),
            "failed_count": failed_comments + failed_dms,
            "avg_daily_comments": round(total_comments / days, 2),
            "avg_daily_dms": round(total_dms / days, 2),
            "days": days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch activity summary: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint for logs service
    """
    return {
        "status": "healthy",
        "service": "logs_analytics",
        "timestamp": datetime.utcnow().isoformat()
    }

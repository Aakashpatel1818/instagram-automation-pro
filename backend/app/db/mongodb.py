"""MongoDB connection and utilities"""

from motor.motor_asyncio import AsyncClient, AsyncDatabase
from app.core.config import settings

# Global database instance
db_client: AsyncClient = None
db: AsyncDatabase = None


async def connect_to_mongo():
    """
    Connect to MongoDB database
    """
    global db_client, db
    try:
        db_client = AsyncClient(settings.MONGODB_URL)
        db = db_client[settings.DATABASE_NAME]
        # Verify connection
        await db_client.admin.command('ping')
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection
    """
    global db_client
    if db_client:
        db_client.close()
        print("✅ Disconnected from MongoDB")


def get_database() -> AsyncDatabase:
    """
    Get database instance
    """
    return db

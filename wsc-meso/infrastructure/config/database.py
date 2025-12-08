"""
MongoDB Configuration

Database connection and settings for MongoDB.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional


class MongoDBConfig:
    """MongoDB configuration and connection management"""
    
    def __init__(
        self,
        connection_string: str = "mongodb://localhost:27017",
        database_name: str = "mesocycle_planner",
    ):
        self.connection_string = connection_string
        self.database_name = database_name
        self._client: Optional[AsyncIOMotorClient] = None
        self._database: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self) -> None:
        """Connect to MongoDB"""
        self._client = AsyncIOMotorClient(self.connection_string)
        self._database = self._client[self.database_name]
        print(f"Connected to MongoDB: {self.database_name}")
    
    async def disconnect(self) -> None:
        """Disconnect from MongoDB"""
        if self._client:
            self._client.close()
            print("Disconnected from MongoDB")
    
    @property
    def database(self) -> AsyncIOMotorDatabase:
        """Get database instance"""
        if self._database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._database
    
    async def create_indexes(self) -> None:
        """Create database indexes for optimal performance"""
        db = self.database
        
        # Users indexes
        await db.users.create_index("email", unique=True)
        await db.users.create_index("username", unique=True)
        
        # Exercises indexes
        await db.exercises.create_index("muscle_group")
        await db.exercises.create_index("type")
        await db.exercises.create_index([("name", "text"), ("execution", "text")])
        
        # Mesocycles indexes
        await db.mesocycles.create_index("user_id")
        await db.mesocycles.create_index([("user_id", 1), ("status", 1)])
        
        # Workouts indexes
        await db.workouts.create_index("mesocycle_id")
        await db.workouts.create_index([("mesocycle_id", 1), ("completed", 1)])
        await db.workouts.create_index("scheduled_date")
        
        # Progress indexes
        await db.progress.create_index([("user_id", 1), ("metric_type", 1)])
        await db.progress.create_index([("user_id", 1), ("date", -1)])
        
        print("Database indexes created")


# Global database instance
_db_config: Optional[MongoDBConfig] = None


def get_database_config() -> MongoDBConfig:
    """Get global database configuration"""
    global _db_config
    if _db_config is None:
        _db_config = MongoDBConfig()
    return _db_config


async def init_database(connection_string: str = "mongodb://localhost:27017") -> None:
    """Initialize database connection"""
    global _db_config
    _db_config = MongoDBConfig(connection_string=connection_string)
    await _db_config.connect()
    await _db_config.create_indexes()


async def close_database() -> None:
    """Close database connection"""
    if _db_config:
        await _db_config.disconnect()

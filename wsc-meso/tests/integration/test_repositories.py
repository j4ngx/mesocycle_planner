"""
Integration Tests for MongoDB Repositories

Tests for repository implementations with MongoDB.
"""
import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import date
from uuid import uuid4

from domain.entities.user import User, TrainingLevel
from domain.entities.mesocycle import Mesocycle, MesocycleStatus, TrainingGoal, PeriodizationModel
from infrastructure.persistence.repositories.user_repository_impl import UserRepository
from infrastructure.persistence.repositories.mesocycle_repository_impl import MesocycleRepository


@pytest_asyncio.fixture
async def mongodb_client():
    """Create MongoDB test client"""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    yield client
    client.close()


@pytest_asyncio.fixture
async def test_database(mongodb_client):
    """Create test database"""
    db = mongodb_client.mesocycle_planner_test
    yield db
    # Cleanup
    await mongodb_client.drop_database("mesocycle_planner_test")


@pytest_asyncio.fixture
async def user_repository(test_database):
    """Create user repository"""
    return UserRepository(test_database)


@pytest_asyncio.fixture
async def mesocycle_repository(test_database):
    """Create mesocycle repository"""
    return MesocycleRepository(test_database)


class TestUserRepository:
    """Test User Repository"""
    
    @pytest.mark.asyncio
    async def test_save_and_find_user(self, user_repository):
        """Test saving and finding a user"""
        user = User.create(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_pwd",
            training_level=TrainingLevel.INTERMEDIATE
        )
        
        # Save user
        saved_user = await user_repository.save(user)
        assert saved_user.id == user.id
        
        # Find by ID
        found_user = await user_repository.find_by_id(user.id)
        assert found_user is not None
        assert found_user.email == "test@example.com"
        assert found_user.username == "testuser"
    
    @pytest.mark.asyncio
    async def test_find_by_email(self, user_repository):
        """Test finding user by email"""
        user = User.create(
            email="email@test.com",
            username="user1",
            hashed_password="pwd"
        )
        
        await user_repository.save(user)
        
        found = await user_repository.find_by_email("email@test.com")
        assert found is not None
        assert found.username == "user1"
    
    @pytest.mark.asyncio
    async def test_update_user(self, user_repository):
        """Test updating a user"""
        user = User.create(
            email="update@test.com",
            username="updateuser",
            hashed_password="pwd"
        )
        
        await user_repository.save(user)
        
        user.update_profile(full_name="Updated Name")
        await user_repository.update(user)
        
        found = await user_repository.find_by_id(user.id)
        assert found.full_name == "Updated Name"
    
    @pytest.mark.asyncio
    async def test_exists_by_email(self, user_repository):
        """Test checking if user exists by email"""
        user = User.create(
            email="exists@test.com",
            username="existsuser",
            hashed_password="pwd"
        )
        
        await user_repository.save(user)
        
        exists = await user_repository.exists_by_email("exists@test.com")
        assert exists is True
        
        not_exists = await user_repository.exists_by_email("notexists@test.com")
        assert not_exists is False


class TestMesocycleRepository:
    """Test Mesocycle Repository"""
    
    @pytest.mark.asyncio
    async def test_save_and_find_mesocycle(self, mesocycle_repository):
        """Test saving and finding a mesocycle"""
        user_id = uuid4()
        mesocycle = Mesocycle.create(
            user_id=user_id,
            name="Test Mesocycle",
            periodization_model=PeriodizationModel.LINEAR,
            goal=TrainingGoal.HYPERTROPHY,
            duration_weeks=12,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 3, 24),
            training_level="intermediate",
            weekly_frequency=5
        )
        
        # Save
        saved = await mesocycle_repository.save(mesocycle)
        assert saved.id == mesocycle.id
        
        # Find by ID
        found = await mesocycle_repository.find_by_id(mesocycle.id)
        assert found is not None
        assert found.name == "Test Mesocycle"
        assert found.goal == TrainingGoal.HYPERTROPHY
    
    @pytest.mark.asyncio
    async def test_find_by_user_id(self, mesocycle_repository):
        """Test finding mesocycles by user ID"""
        user_id = uuid4()
        
        # Create multiple mesocycles
        for i in range(3):
            mesocycle = Mesocycle.create(
                user_id=user_id,
                name=f"Mesocycle {i}",
                periodization_model=PeriodizationModel.LINEAR,
                goal=TrainingGoal.STRENGTH,
                duration_weeks=8,
                start_date=date(2025, 1, 1),
                end_date=date(2025, 2, 26),
                training_level="intermediate",
                weekly_frequency=4
            )
            await mesocycle_repository.save(mesocycle)
        
        # Find all for user
        mesocycles = await mesocycle_repository.find_by_user_id(user_id)
        assert len(mesocycles) == 3
    
    @pytest.mark.asyncio
    async def test_find_active_mesocycle(self, mesocycle_repository):
        """Test finding active mesocycle"""
        user_id = uuid4()
        
        mesocycle = Mesocycle.create(
            user_id=user_id,
            name="Active Mesocycle",
            periodization_model=PeriodizationModel.DAILY_UNDULATING,
            goal=TrainingGoal.HYPERTROPHY,
            duration_weeks=12,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 3, 24),
            training_level="intermediate",
            weekly_frequency=5
        )
        
        mesocycle.start()  # Make it active
        await mesocycle_repository.save(mesocycle)
        
        active = await mesocycle_repository.find_active_by_user_id(user_id)
        assert active is not None
        assert active.status == MesocycleStatus.ACTIVE
    
    @pytest.mark.asyncio
    async def test_update_mesocycle(self, mesocycle_repository):
        """Test updating a mesocycle"""
        user_id = uuid4()
        
        mesocycle = Mesocycle.create(
            user_id=user_id,
            name="Original Name",
            periodization_model=PeriodizationModel.LINEAR,
            goal=TrainingGoal.STRENGTH,
            duration_weeks=8,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 2, 26),
            training_level="intermediate",
            weekly_frequency=4
        )
        
        await mesocycle_repository.save(mesocycle)
        
        # Update
        mesocycle.start()
        await mesocycle_repository.update(mesocycle)
        
        # Verify
        found = await mesocycle_repository.find_by_id(mesocycle.id)
        assert found.status == MesocycleStatus.ACTIVE
    
    @pytest.mark.asyncio
    async def test_delete_mesocycle(self, mesocycle_repository):
        """Test deleting a mesocycle"""
        user_id = uuid4()
        
        mesocycle = Mesocycle.create(
            user_id=user_id,
            name="To Delete",
            periodization_model=PeriodizationModel.LINEAR,
            goal=TrainingGoal.STRENGTH,
            duration_weeks=8,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 2, 26),
            training_level="intermediate",
            weekly_frequency=4
        )
        
        await mesocycle_repository.save(mesocycle)
        
        # Delete
        deleted = await mesocycle_repository.delete(mesocycle.id)
        assert deleted is True
        
        # Verify
        found = await mesocycle_repository.find_by_id(mesocycle.id)
        assert found is None

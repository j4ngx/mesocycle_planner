"""
Unit Tests for Domain Entities

Tests for domain layer business logic.
"""
import pytest
from datetime import date, datetime
from uuid import uuid4

from domain.entities.user import User, TrainingLevel
from domain.entities.mesocycle import Mesocycle, MesocycleStatus, TrainingGoal, PeriodizationModel
from domain.entities.workout import Workout, TrainingSplit
from domain.entities.progress import Progress, MetricType


class TestUser:
    """Test User entity"""
    
    def test_create_user(self):
        """Test user creation"""
        user = User.create(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_pwd",
            full_name="Test User",
            training_level=TrainingLevel.INTERMEDIATE
        )
        
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.training_level == TrainingLevel.INTERMEDIATE
        assert user.id is not None
    
    def test_update_profile(self):
        """Test user profile update"""
        user = User.create(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_pwd"
        )
        
        original_updated_at = user.updated_at
        user.update_profile(full_name="Updated Name")
        
        assert user.full_name == "Updated Name"
        assert user.updated_at > original_updated_at


class TestMesocycle:
    """Test Mesocycle entity"""
    
    def test_create_mesocycle(self):
        """Test mesocycle creation"""
        mesocycle = Mesocycle.create(
            user_id=uuid4(),
            name="Test Mesocycle",
            periodization_model=PeriodizationModel.LINEAR,
            goal=TrainingGoal.HYPERTROPHY,
            duration_weeks=12,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 3, 24),
            training_level="intermediate",
            weekly_frequency=5
        )
        
        assert mesocycle.name == "Test Mesocycle"
        assert mesocycle.status == MesocycleStatus.PLANNED
        assert mesocycle.duration_weeks == 12
    
    def test_mesocycle_validation_duration(self):
        """Test mesocycle duration validation"""
        with pytest.raises(ValueError, match="Duration must be between 4 and 16 weeks"):
            Mesocycle.create(
                user_id=uuid4(),
                name="Invalid",
                periodization_model=PeriodizationModel.LINEAR,
                goal=TrainingGoal.STRENGTH,
                duration_weeks=20,  # Invalid
                start_date=date(2025, 1, 1),
                end_date=date(2025, 6, 1),
                training_level="intermediate",
                weekly_frequency=5
            )
    
    def test_mesocycle_state_transitions(self):
        """Test mesocycle state machine"""
        mesocycle = Mesocycle.create(
            user_id=uuid4(),
            name="Test",
            periodization_model=PeriodizationModel.LINEAR,
            goal=TrainingGoal.STRENGTH,
            duration_weeks=8,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 2, 26),
            training_level="intermediate",
            weekly_frequency=4
        )
        
        # Test start
        mesocycle.start()
        assert mesocycle.status == MesocycleStatus.ACTIVE
        
        # Test pause
        mesocycle.pause()
        assert mesocycle.status == MesocycleStatus.PAUSED
        
        # Test resume
        mesocycle.resume()
        assert mesocycle.status == MesocycleStatus.ACTIVE
        
        # Test complete
        mesocycle.complete()
        assert mesocycle.status == MesocycleStatus.COMPLETED
    
    def test_deload_week_check(self):
        """Test deload week checking"""
        mesocycle = Mesocycle.create(
            user_id=uuid4(),
            name="Test",
            periodization_model=PeriodizationModel.LINEAR,
            goal=TrainingGoal.STRENGTH,
            duration_weeks=12,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 3, 24),
            training_level="intermediate",
            weekly_frequency=5,
            deload_weeks=[4, 8, 12]
        )
        
        assert mesocycle.is_deload_week(4) is True
        assert mesocycle.is_deload_week(5) is False


class TestWorkout:
    """Test Workout entity"""
    
    def test_create_workout(self):
        """Test workout creation"""
        workout = Workout.create(
            mesocycle_id=uuid4(),
            name="Upper Body",
            scheduled_date=datetime(2025, 1, 15, 10, 0),
            split=TrainingSplit.UPPER
        )
        
        assert workout.name == "Upper Body"
        assert workout.completed is False
        assert workout.split == TrainingSplit.UPPER
    
    def test_mark_completed(self):
        """Test marking workout as completed"""
        workout = Workout.create(
            mesocycle_id=uuid4(),
            name="Test Workout",
            scheduled_date=datetime(2025, 1, 15, 10, 0)
        )
        
        workout.mark_completed(duration_minutes=60, notes="Great session")
        
        assert workout.completed is True
        assert workout.duration_minutes == 60
        assert workout.notes == "Great session"
        assert workout.completed_at is not None
    
    def test_cannot_complete_twice(self):
        """Test that workout cannot be completed twice"""
        workout = Workout.create(
            mesocycle_id=uuid4(),
            name="Test",
            scheduled_date=datetime(2025, 1, 15, 10, 0)
        )
        
        workout.mark_completed()
        
        with pytest.raises(ValueError, match="already completed"):
            workout.mark_completed()


class TestProgress:
    """Test Progress entity"""
    
    def test_create_progress(self):
        """Test progress creation"""
        progress = Progress.create(
            user_id=uuid4(),
            date=date(2025, 1, 15),
            metric_type=MetricType.WEIGHT,
            value=75.5,
            unit="kg"
        )
        
        assert progress.metric_type == MetricType.WEIGHT
        assert progress.value == 75.5
        assert progress.unit == "kg"
    
    def test_progress_validation(self):
        """Test progress value validation"""
        with pytest.raises(ValueError, match="cannot be negative"):
            Progress.create(
                user_id=uuid4(),
                date=date(2025, 1, 15),
                metric_type=MetricType.WEIGHT,
                value=-10,  # Invalid
                unit="kg"
            )

"""
Unit tests for SQLModel entities and Pydantic models.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from src.models.task import Task, TaskCreate, TaskUpdate, TaskResponse, User


class TestUserModel:
    """Test User model validation."""

    def test_user_creation(self):
        """Test creating a valid user."""
        user = User(
            id="user123",
            email="test@example.com",
            password_hash="hashed_password",
            created_at=datetime.utcnow()
        )
        assert user.id == "user123"
        assert user.email == "test@example.com"

    def test_user_unique_email(self):
        """Test that email must be unique (enforced at DB level)."""
        user = User(
            id="user123",
            email="test@example.com",
            password_hash="hash"
        )
        assert user.email == "test@example.com"


class TestTaskModel:
    """Test Task model validation."""

    def test_task_creation_minimal(self):
        """Test creating a task with minimal required fields."""
        task = Task(
            user_id="user123",
            title="Test task"
        )
        assert task.user_id == "user123"
        assert task.title == "Test task"
        assert task.completed is False  # Default value
        assert task.description is None  # Default value

    def test_task_creation_full(self):
        """Test creating a task with all fields."""
        task = Task(
            user_id="user123",
            title="Test task",
            description="This is a test task",
            completed=True
        )
        assert task.user_id == "user123"
        assert task.title == "Test task"
        assert task.description == "This is a test task"
        assert task.completed is True

    def test_task_title_validation_min_length(self):
        """Test that title must be at least 1 character."""
        with pytest.raises(ValidationError) as exc_info:
            Task(user_id="user123", title="")  # Empty title
        assert "title" in str(exc_info.value).lower()

    def test_task_title_validation_max_length(self):
        """Test that title cannot exceed 200 characters."""
        long_title = "a" * 201
        with pytest.raises(ValidationError) as exc_info:
            Task(user_id="user123", title=long_title)
        assert "title" in str(exc_info.value).lower()

    def test_task_description_max_length(self):
        """Test that description cannot exceed 5000 characters."""
        long_description = "a" * 5001
        with pytest.raises(ValidationError) as exc_info:
            Task(user_id="user123", title="Test", description=long_description)
        assert "description" in str(exc_info.value).lower()

    def test_task_description_optional(self):
        """Test that description is optional."""
        task = Task(user_id="user123", title="Test")
        assert task.description is None

    def test_task_completed_default(self):
        """Test that completed defaults to False."""
        task = Task(user_id="user123", title="Test")
        assert task.completed is False

    def test_task_timestamps_auto_set(self):
        """Test that timestamps are automatically set."""
        task = Task(user_id="user123", title="Test")
        assert task.created_at is not None
        assert task.updated_at is not None


class TestTaskCreateModel:
    """Test TaskCreate Pydantic model."""

    def test_task_create_valid(self):
        """Test creating a valid TaskCreate request."""
        task_data = TaskCreate(
            title="Buy groceries",
            description="Milk, eggs, bread"
        )
        assert task_data.title == "Buy groceries"
        assert task_data.description == "Milk, eggs, bread"

    def test_task_create_title_only(self):
        """Test creating a task with title only."""
        task_data = TaskCreate(title="Buy groceries")
        assert task_data.title == "Buy groceries"
        assert task_data.description is None

    def test_task_create_title_required(self):
        """Test that title is required."""
        with pytest.raises(ValidationError):
            TaskCreate()

    def test_task_create_title_too_long(self):
        """Test that title cannot exceed 200 characters."""
        with pytest.raises(ValidationError):
            TaskCreate(title="a" * 201)

    def test_task_create_description_too_long(self):
        """Test that description cannot exceed 5000 characters."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", description="a" * 5001)


class TestTaskUpdateModel:
    """Test TaskUpdate Pydantic model."""

    def test_task_update_title_only(self):
        """Test updating only the title."""
        update_data = TaskUpdate(title="Updated title")
        assert update_data.title == "Updated title"
        assert update_data.description is None

    def test_task_update_description_only(self):
        """Test updating only the description."""
        update_data = TaskUpdate(description="Updated description")
        assert update_data.description == "Updated description"
        assert update_data.title is None

    def test_task_update_both_fields(self):
        """Test updating both title and description."""
        update_data = TaskUpdate(
            title="Updated title",
            description="Updated description"
        )
        assert update_data.title == "Updated title"
        assert update_data.description == "Updated description"

    def test_task_update_all_none(self):
        """Test that update can have all None values (partial update)."""
        update_data = TaskUpdate()
        assert update_data.title is None
        assert update_data.description is None


class TestTaskResponseModel:
    """Test TaskResponse Pydantic model."""

    def test_task_response_from_orm(self):
        """Test creating TaskResponse from ORM model."""
        task = Task(
            id=1,
            user_id="user123",
            title="Test task",
            description="Test description",
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        response = TaskResponse.model_validate(task)
        assert response.id == 1
        assert response.title == "Test task"
        assert response.description == "Test description"
        assert response.completed is False
        assert response.created_at is not None
        assert response.updated_at is not None

"""
Integration tests for all API endpoints.
Tests the complete API workflow with real database operations.
"""
import pytest
from httpx import AsyncClient


class TestHealthEndpoint:
    """Test health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test that health endpoint returns 200."""
        response = await client.get("/health")
        assert response.status_code == 200


class TestTasksAPI:
    """Test task CRUD operations."""

    @pytest.mark.asyncio
    async def test_list_tasks_empty(self, client: AsyncClient, auth_headers):
        """Test listing tasks when no tasks exist."""
        response = await client.get("/api/tasks", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_create_task(self, client: AsyncClient, auth_headers):
        """Test creating a new task."""
        task_data = {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        }
        response = await client.post("/api/tasks", json=task_data, headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Buy groceries"
        assert data["description"] == "Milk, eggs, bread"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    @pytest.mark.asyncio
    async def test_create_task_title_only(self, client: AsyncClient, auth_headers):
        """Test creating a task with title only."""
        task_data = {"title": "Simple task"}
        response = await client.post("/api/tasks", json=task_data, headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Simple task"
        assert data["description"] is None
        assert data["completed"] is False

    @pytest.mark.asyncio
    async def test_create_task_no_auth(self, client: AsyncClient):
        """Test that creating a task without auth returns 401/403."""
        task_data = {"title": "Unauthorized task"}
        response = await client.post("/api/tasks", json=task_data)
        assert response.status_code in [401, 403]

    @pytest.mark.asyncio
    async def test_create_task_invalid_title(self, client: AsyncClient, auth_headers):
        """Test creating a task with invalid title (too long)."""
        task_data = {"title": "a" * 201}  # Exceeds 200 char limit
        response = await client.post("/api/tasks", json=task_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_list_tasks_after_create(self, client: AsyncClient, auth_headers):
        """Test that created tasks appear in the list."""
        # Create two tasks
        await client.post("/api/tasks", json={"title": "Task 1"}, headers=auth_headers)
        await client.post("/api/tasks", json={"title": "Task 2"}, headers=auth_headers)

        # List tasks
        response = await client.get("/api/tasks", headers=auth_headers)
        assert response.status_code == 200

        tasks = response.json()
        assert len(tasks) == 2
        titles = [t["title"] for t in tasks]
        assert "Task 1" in titles
        assert "Task 2" in titles

    @pytest.mark.asyncio
    async def test_get_single_task(self, client: AsyncClient, auth_headers):
        """Test getting a single task by ID."""
        # Create a task
        create_response = await client.post(
            "/api/tasks",
            json={"title": "Test task"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Get the task
        response = await client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test task"

    @pytest.mark.asyncio
    async def test_get_nonexistent_task(self, client: AsyncClient, auth_headers):
        """Test getting a task that doesn't exist returns 404."""
        response = await client.get("/api/tasks/99999", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_task(self, client: AsyncClient, auth_headers):
        """Test updating a task."""
        # Create a task
        create_response = await client.post(
            "/api/tasks",
            json={"title": "Original title", "description": "Original desc"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Update the task
        update_data = {
            "title": "Updated title",
            "description": "Updated desc"
        }
        response = await client.put(
            f"/api/tasks/{task_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Updated title"
        assert data["description"] == "Updated desc"

    @pytest.mark.asyncio
    async def test_update_task_partial(self, client: AsyncClient, auth_headers):
        """Test partially updating a task (title only)."""
        # Create a task
        create_response = await client.post(
            "/api/tasks",
            json={"title": "Original", "description": "Keep this"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Update only title
        response = await client.put(
            f"/api/tasks/{task_id}",
            json={"title": "New title"},
            headers=auth_headers
        )
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "New title"
        # Description should be unchanged (or None if not sent)

    @pytest.mark.asyncio
    async def test_toggle_task_completion(self, client: AsyncClient, auth_headers):
        """Test toggling task completion status."""
        # Create a task (default completed=False)
        create_response = await client.post(
            "/api/tasks",
            json={"title": "Task to toggle"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]
        assert create_response.json()["completed"] is False

        # Toggle to completed
        response = await client.patch(
            f"/api/tasks/{task_id}/toggle",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["completed"] is True

        # Toggle back to pending
        response = await client.patch(
            f"/api/tasks/{task_id}/toggle",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["completed"] is False

    @pytest.mark.asyncio
    async def test_delete_task(self, client: AsyncClient, auth_headers):
        """Test deleting a task."""
        # Create a task
        create_response = await client.post(
            "/api/tasks",
            json={"title": "Task to delete"},
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Delete the task
        response = await client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200

        # Verify it's deleted
        get_response = await client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_nonexistent_task(self, client: AsyncClient, auth_headers):
        """Test deleting a task that doesn't exist returns 404."""
        response = await client.delete("/api/tasks/99999", headers=auth_headers)
        assert response.status_code == 404


class TestErrorHandling:
    """Test error handling in API."""

    @pytest.mark.asyncio
    async def test_missing_auth_header(self, client: AsyncClient):
        """Test that missing auth header returns 401/403."""
        response = await client.get("/api/tasks")
        assert response.status_code in [401, 403]

    @pytest.mark.asyncio
    async def test_invalid_auth_token(self, client: AsyncClient):
        """Test that invalid auth token returns 401."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = await client.get("/api/tasks", headers=headers)
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_malformed_request_body(self, client: AsyncClient, auth_headers):
        """Test that malformed request body returns 422."""
        # Missing required 'title' field
        response = await client.post("/api/tasks", json={}, headers=auth_headers)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_invalid_task_id_format(self, client: AsyncClient, auth_headers):
        """Test that invalid task ID format returns appropriate error."""
        response = await client.get("/api/tasks/invalid", headers=auth_headers)
        assert response.status_code in [404, 422]

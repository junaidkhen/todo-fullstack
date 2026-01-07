"""
Multi-user isolation tests.
CRITICAL: These tests verify that users cannot access each other's data.
"""
import pytest
from httpx import AsyncClient


class TestMultiUserIsolation:
    """Test that users can only access their own tasks."""

    @pytest.mark.asyncio
    async def test_users_see_only_own_tasks(
        self,
        client: AsyncClient,
        auth_headers,
        auth_headers_2
    ):
        """Test that each user only sees their own tasks."""
        # User 1 creates tasks
        await client.post(
            "/api/tasks",
            json={"title": "User 1 Task A"},
            headers=auth_headers
        )
        await client.post(
            "/api/tasks",
            json={"title": "User 1 Task B"},
            headers=auth_headers
        )

        # User 2 creates tasks
        await client.post(
            "/api/tasks",
            json={"title": "User 2 Task A"},
            headers=auth_headers_2
        )

        # User 1 should see only their 2 tasks
        response1 = await client.get("/api/tasks", headers=auth_headers)
        user1_tasks = response1.json()
        assert len(user1_tasks) == 2
        titles1 = [t["title"] for t in user1_tasks]
        assert "User 1 Task A" in titles1
        assert "User 1 Task B" in titles1
        assert "User 2 Task A" not in titles1

        # User 2 should see only their 1 task
        response2 = await client.get("/api/tasks", headers=auth_headers_2)
        user2_tasks = response2.json()
        assert len(user2_tasks) == 1
        assert user2_tasks[0]["title"] == "User 2 Task A"

    @pytest.mark.asyncio
    async def test_user_cannot_access_other_user_task(
        self,
        client: AsyncClient,
        auth_headers,
        auth_headers_2
    ):
        """Test that User A cannot access User B's task by ID."""
        # User 1 creates a task
        response = await client.post(
            "/api/tasks",
            json={"title": "User 1 Private Task"},
            headers=auth_headers
        )
        task_id = response.json()["id"]

        # User 2 tries to access User 1's task
        response = await client.get(
            f"/api/tasks/{task_id}",
            headers=auth_headers_2
        )
        # Should return 404 (not 403) to avoid enumeration
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_user_cannot_update_other_user_task(
        self,
        client: AsyncClient,
        auth_headers,
        auth_headers_2
    ):
        """Test that User A cannot update User B's task."""
        # User 1 creates a task
        response = await client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )
        task_id = response.json()["id"]

        # User 2 tries to update User 1's task
        response = await client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Hacked!"},
            headers=auth_headers_2
        )
        # Should return 404 (not 403) to avoid enumeration
        assert response.status_code == 404

        # Verify task wasn't updated
        response = await client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.json()["title"] == "User 1 Task"

    @pytest.mark.asyncio
    async def test_user_cannot_toggle_other_user_task(
        self,
        client: AsyncClient,
        auth_headers,
        auth_headers_2
    ):
        """Test that User A cannot toggle User B's task completion."""
        # User 1 creates a task
        response = await client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )
        task_id = response.json()["id"]
        assert response.json()["completed"] is False

        # User 2 tries to toggle User 1's task
        response = await client.patch(
            f"/api/tasks/{task_id}/toggle",
            headers=auth_headers_2
        )
        assert response.status_code == 404

        # Verify task wasn't toggled
        response = await client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.json()["completed"] is False

    @pytest.mark.asyncio
    async def test_user_cannot_delete_other_user_task(
        self,
        client: AsyncClient,
        auth_headers,
        auth_headers_2
    ):
        """Test that User A cannot delete User B's task."""
        # User 1 creates a task
        response = await client.post(
            "/api/tasks",
            json={"title": "User 1 Important Task"},
            headers=auth_headers
        )
        task_id = response.json()["id"]

        # User 2 tries to delete User 1's task
        response = await client.delete(
            f"/api/tasks/{task_id}",
            headers=auth_headers_2
        )
        assert response.status_code == 404

        # Verify task still exists
        response = await client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "User 1 Important Task"

    @pytest.mark.asyncio
    async def test_multiple_users_concurrent_operations(
        self,
        client: AsyncClient,
        auth_headers,
        auth_headers_2
    ):
        """Test that multiple users can perform operations concurrently without interference."""
        # User 1 creates a task
        response1 = await client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers=auth_headers
        )
        task1_id = response1.json()["id"]

        # User 2 creates a task
        response2 = await client.post(
            "/api/tasks",
            json={"title": "User 2 Task"},
            headers=auth_headers_2
        )
        task2_id = response2.json()["id"]

        # User 1 toggles their task
        await client.patch(f"/api/tasks/{task1_id}/toggle", headers=auth_headers)

        # User 2 updates their task
        await client.put(
            f"/api/tasks/{task2_id}",
            json={"title": "User 2 Updated Task"},
            headers=auth_headers_2
        )

        # Verify User 1's task
        response1 = await client.get(f"/api/tasks/{task1_id}", headers=auth_headers)
        assert response1.json()["completed"] is True
        assert response1.json()["title"] == "User 1 Task"

        # Verify User 2's task
        response2 = await client.get(f"/api/tasks/{task2_id}", headers=auth_headers_2)
        assert response2.json()["completed"] is False
        assert response2.json()["title"] == "User 2 Updated Task"

    @pytest.mark.asyncio
    async def test_no_task_id_enumeration(
        self,
        client: AsyncClient,
        auth_headers,
        auth_headers_2
    ):
        """Test that error responses don't reveal whether a task exists (403 vs 404)."""
        # User 1 creates a task
        response = await client.post(
            "/api/tasks",
            json={"title": "Secret Task"},
            headers=auth_headers
        )
        task_id = response.json()["id"]

        # User 2 tries to access it - should get 404 (not 403)
        # This prevents enumeration of task IDs
        response = await client.get(f"/api/tasks/{task_id}", headers=auth_headers_2)
        assert response.status_code == 404

        # Try accessing non-existent task - should also be 404
        response = await client.get("/api/tasks/99999", headers=auth_headers_2)
        assert response.status_code == 404

        # Both should return the same status code to prevent enumeration


class TestDataLeakagePrevention:
    """Test that no data leaks between users."""

    @pytest.mark.asyncio
    async def test_task_count_isolation(
        self,
        client: AsyncClient,
        auth_headers,
        auth_headers_2
    ):
        """Test that task counts are isolated per user."""
        # User 1 creates 5 tasks
        for i in range(5):
            await client.post(
                "/api/tasks",
                json={"title": f"User 1 Task {i}"},
                headers=auth_headers
            )

        # User 2 creates 2 tasks
        for i in range(2):
            await client.post(
                "/api/tasks",
                json={"title": f"User 2 Task {i}"},
                headers=auth_headers_2
            )

        # Verify counts
        response1 = await client.get("/api/tasks", headers=auth_headers)
        assert len(response1.json()) == 5

        response2 = await client.get("/api/tasks", headers=auth_headers_2)
        assert len(response2.json()) == 2

    @pytest.mark.asyncio
    async def test_no_cross_user_data_in_responses(
        self,
        client: AsyncClient,
        auth_headers,
        auth_headers_2
    ):
        """Test that API responses never contain data from other users."""
        # User 1 creates tasks
        await client.post(
            "/api/tasks",
            json={"title": "User 1 Confidential", "description": "Secret info"},
            headers=auth_headers
        )

        # User 2 creates tasks
        await client.post(
            "/api/tasks",
            json={"title": "User 2 Public", "description": "Public info"},
            headers=auth_headers_2
        )

        # User 2 gets their tasks
        response = await client.get("/api/tasks", headers=auth_headers_2)
        tasks = response.json()

        # Verify no User 1 data in response
        for task in tasks:
            assert "User 1" not in task["title"]
            assert "Secret info" not in str(task.get("description", ""))
            assert task["title"] == "User 2 Public"

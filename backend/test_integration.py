"""
Integration test for the Todo API.
Tests authentication and task CRUD operations.
"""
import asyncio
import sys
from httpx import AsyncClient
import jwt
from datetime import datetime, timedelta

# Base URL for the API
BASE_URL = "http://localhost:8000"

# Test credentials
TEST_USER = {
    "email": "test@example.com",
    "password": "password123"
}

async def test_auth_and_tasks():
    """Test the complete authentication and task workflow."""
    async with AsyncClient(base_url=BASE_URL) as client:
        print("=" * 60)
        print("INTEGRATION TEST: Todo API")
        print("=" * 60)

        # Step 1: Create test JWT token (simulating Better Auth)
        print("\n1. Creating test JWT token...")
        import os
        secret = os.getenv("BETTER_AUTH_SECRET", "ywcrxx0dDGovAcKd69vHcj9dw5zxrNNxVH-gq0Rwols")

        # Create a JWT token with user_id
        test_user_id = f"user_test_{int(datetime.utcnow().timestamp())}"
        token_payload = {
            "sub": test_user_id,
            "email": TEST_USER["email"],
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow().timestamp()
        }
        token = jwt.encode(token_payload, secret, algorithm="HS256")
        print(f"✓ Token created for user: {test_user_id}")

        # Headers with auth token
        headers = {"Authorization": f"Bearer {token}"}

        # Step 2: Test GET /api/tasks (should return empty list)
        print("\n2. Testing GET /api/tasks (should be empty)...")
        response = await client.get("/api/tasks", headers=headers)
        if response.status_code == 200 and response.json() == []:
            print("✓ GET /api/tasks successful - empty list")
        else:
            print(f"✗ GET /api/tasks failed: {response.status_code} - {response.text}")
            return False

        # Step 3: Test POST /api/tasks (create task)
        print("\n3. Testing POST /api/tasks (create task)...")
        task_data = {
            "title": "Test task",
            "description": "This is a test task"
        }
        response = await client.post("/api/tasks", json=task_data, headers=headers)
        if response.status_code == 200:
            task = response.json()
            task_id = task["id"]
            print(f"✓ POST /api/tasks successful - created task {task_id}")
            print(f"  Title: {task['title']}")
            print(f"  Completed: {task['completed']}")
        else:
            print(f"✗ POST /api/tasks failed: {response.status_code} - {response.text}")
            return False

        # Step 4: Test GET /api/tasks (should return 1 task)
        print("\n4. Testing GET /api/tasks (should have 1 task)...")
        response = await client.get("/api/tasks", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            if len(tasks) == 1:
                print(f"✓ GET /api/tasks successful - found {len(tasks)} task")
            else:
                print(f"✗ Expected 1 task, got {len(tasks)}")
                return False
        else:
            print(f"✗ GET /api/tasks failed: {response.status_code}")
            return False

        # Step 5: Test GET /api/tasks/{id}
        print(f"\n5. Testing GET /api/tasks/{task_id}...")
        response = await client.get(f"/api/tasks/{task_id}", headers=headers)
        if response.status_code == 200:
            task = response.json()
            print(f"✓ GET /api/tasks/{task_id} successful")
            print(f"  Title: {task['title']}")
        else:
            print(f"✗ GET /api/tasks/{task_id} failed: {response.status_code}")
            return False

        # Step 6: Test PATCH /api/tasks/{id}/toggle
        print(f"\n6. Testing PATCH /api/tasks/{task_id}/toggle...")
        response = await client.patch(f"/api/tasks/{task_id}/toggle", headers=headers)
        if response.status_code == 200:
            task = response.json()
            if task["completed"]:
                print(f"✓ PATCH toggle successful - task marked complete")
            else:
                print(f"✗ Toggle failed - task not marked complete")
                return False
        else:
            print(f"✗ PATCH toggle failed: {response.status_code}")
            return False

        # Step 7: Test PUT /api/tasks/{id}
        print(f"\n7. Testing PUT /api/tasks/{task_id} (update)...")
        update_data = {
            "title": "Updated test task",
            "description": "This task has been updated"
        }
        response = await client.put(f"/api/tasks/{task_id}", json=update_data, headers=headers)
        if response.status_code == 200:
            task = response.json()
            if task["title"] == update_data["title"]:
                print(f"✓ PUT update successful")
                print(f"  New title: {task['title']}")
            else:
                print(f"✗ Update failed - title not changed")
                return False
        else:
            print(f"✗ PUT update failed: {response.status_code}")
            return False

        # Step 8: Test DELETE /api/tasks/{id}
        print(f"\n8. Testing DELETE /api/tasks/{task_id}...")
        response = await client.delete(f"/api/tasks/{task_id}", headers=headers)
        if response.status_code == 200:
            print(f"✓ DELETE successful")
        else:
            print(f"✗ DELETE failed: {response.status_code}")
            return False

        # Step 9: Verify task is deleted
        print("\n9. Verifying task is deleted...")
        response = await client.get("/api/tasks", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            if len(tasks) == 0:
                print(f"✓ Task deleted successfully - list is empty")
            else:
                print(f"✗ Task not deleted - still {len(tasks)} tasks")
                return False
        else:
            print(f"✗ GET failed: {response.status_code}")
            return False

        # Step 10: Test auth error (no token)
        print("\n10. Testing authentication error (no token)...")
        response = await client.get("/api/tasks")
        if response.status_code == 401 or response.status_code == 403:
            print(f"✓ Auth check successful - got {response.status_code} without token")
        else:
            print(f"✗ Auth check failed - expected 401/403, got {response.status_code}")
            return False

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return True

if __name__ == "__main__":
    # Run the async test
    result = asyncio.run(test_auth_and_tasks())
    sys.exit(0 if result else 1)

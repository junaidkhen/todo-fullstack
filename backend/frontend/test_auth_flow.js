// Simple test to verify the authentication flow
const testAuthFlow = async () => {
  console.log("Testing authentication flow...");

  // First, let's try to sign up
  console.log("1. Testing signup...");
  try {
    const signupResponse = await fetch('http://localhost:3000/api/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'testuser@example.com',
        password: 'password123'
      })
    });

    const signupData = await signupResponse.json();
    console.log("Signup response:", signupData);
    console.log("Signup status:", signupResponse.status);
  } catch (error) {
    console.error("Signup error:", error);
  }

  console.log("\n2. Testing task creation (should fail without proper auth headers)...");
  try {
    const taskResponse = await fetch('http://localhost:3000/api/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: 'Test task from frontend route',
        description: 'Created via frontend API route'
      })
    });

    const taskData = await taskResponse.json();
    console.log("Task creation response:", taskData);
    console.log("Task creation status:", taskResponse.status);
  } catch (error) {
    console.error("Task creation error:", error);
  }
};

// Run the test
testAuthFlow();
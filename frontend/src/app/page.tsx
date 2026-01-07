import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export default async function Home() {
  // Check if user is authenticated by looking for auth token in cookies
  const cookieStore = await cookies();
  const authToken = cookieStore.get('auth-token');

  if (authToken) {
    // If authenticated, redirect to tasks page
    redirect('/tasks');
  } else {
    // If not authenticated, redirect to signin page
    redirect('/signin');
  }
}
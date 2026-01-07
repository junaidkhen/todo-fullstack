# Next.js App Router & Full-Stack Integration

## Overview
Building modern, full-stack web applications with Next.js 14+ App Router, integrating server and client components, API routes, and backend services.

## Key Features
- **App Router**: File-based routing with layouts and nested routes
- **Server Components**: React Server Components by default for better performance
- **Client Components**: Interactive components with "use client" directive
- **API Integration**: Fetch backend APIs with proper authentication
- **TypeScript**: Full type safety across frontend
- **Tailwind CSS**: Utility-first styling

## Application in This Project
- Next.js frontend in `frontend/` directory
- Server-side rendering for initial page loads
- Client components for interactive task management
- API client for backend communication
- JWT token management in cookies/headers
- Responsive UI with Tailwind CSS

## Project Structure
```
frontend/
├── app/
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Home page
│   ├── dashboard/
│   │   └── page.tsx      # Dashboard page
│   └── api/              # API routes (if needed)
├── components/
│   ├── TaskList.tsx      # Task display
│   └── AuthForm.tsx      # Login/signup
├── lib/
│   └── api.ts            # API client
└── package.json
```

## Best Practices
- Use Server Components by default
- Add "use client" only when needed (state, effects, events)
- Implement proper loading and error states
- Handle authentication state globally
- Use TypeScript for type safety
- Optimize images and fonts
- Implement proper SEO metadata

# JWT-Based Authentication & Authorization

## Overview
Implementing secure, stateless authentication and authorization using JSON Web Tokens (JWT) for user identity management and access control.

## Key Components
- **Token Generation**: Creating signed JWT tokens with user claims
- **Token Validation**: Verifying token signatures and expiration
- **Token Storage**: Secure storage in httpOnly cookies or Authorization headers
- **Refresh Strategy**: Managing token expiration and renewal
- **Claims-Based Authorization**: Role and permission validation

## Application in This Project
- JWT token generation at signup/signin
- Bearer token authentication for protected routes
- User identity extraction from token claims
- Secure password hashing with bcrypt
- Session management with token expiration

## Security Best Practices
- Use strong secret keys (stored in environment variables)
- Implement reasonable token expiration times
- Never expose tokens in URLs
- Validate tokens on every protected request
- Hash passwords before storage
- Implement rate limiting for auth endpoints

## Token Structure
```
Header: {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "user_id", "email": "user@example.com", "exp": timestamp}
Signature: HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
```

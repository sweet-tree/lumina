# NextAuth.js Implementation Plan

## Baby Steps for Authentication Integration

### 1. Setup and Installation

- Install NextAuth.js: `npm install next-auth`
- Create API route directory: `client/src/app/api/auth`
- Set up environment variables:
  - `NEXTAUTH_SECRET` (generate with `openssl rand -base64 32`)
  - `NEXTAUTH_URL` (set to development URL)

### 2. API Route Configuration (App Router)

- Create `[...nextauth]/route.ts` in `client/src/app/api/auth`
- Implement Route Handler pattern for App Router:

```typescript
import NextAuth from "next-auth";

const handler = NextAuth({
  // Configuration will be added in next steps
});

export { handler as GET, handler as POST };
```

### 3. Provider Integration

- Add Google OAuth provider:
  - Register application in Google Cloud Console
  - Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` environment variables
  - Configure in NextAuth options
- Add GitHub OAuth provider:
  - Register OAuth application in GitHub
  - Set `GITHUB_ID` and `GITHUB_SECRET` environment variables
  - Configure in NextAuth options

### 4. Authentication Configuration

- Configure basic options in `[...nextauth]/route.ts`:

```typescript
import GoogleProvider from "next-auth/providers/google";
import GitHubProvider from "next-auth/providers/github";

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
    GitHubProvider({
      clientId: process.env.GITHUB_ID,
      clientSecret: process.env.GITHUB_SECRET,
    }),
  ],
  // Additional configuration will be added
};
```

### 5. Session Management

- Implement TypeScript module augmentation:
  - Create `types/next-auth.d.ts` file
  - Extend Session interface to include custom user properties
- Configure session strategy (JWT or database)
- Set up secure cookie configuration

### 6. Client-Side Integration

- Create `app/components/Providers.tsx` for SessionProvider:

```typescript
"use client";

import { SessionProvider } from "next-auth/react";

export function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}
```

- Wrap layout with Providers component
- Implement `useSession` hook in client components

### 7. Authentication Pages

- Create sign-in page at `app/signin/page.tsx`
- Add provider sign-in buttons
- Implement error handling
- Create sign-out functionality

### 8. Protected Routes

- Create middleware for authentication checks
- Implement server-side session validation with `getServerSession`
- Set up protected API routes

### 9. UI Integration

- Update navigation to show user profile when authenticated
- Add login/logout buttons based on authentication state
- Create user profile page
- Implement loading states

### 10. Testing and Security

- Test Google OAuth flow
- Test GitHub OAuth flow
- Verify session persistence
- Test protected routes
- Implement CSRF protection
- Configure secure cookies

### 11. Deployment Preparation

- Set `NEXTAUTH_URL` for production
- Configure production callback URLs
- Set up environment variables in deployment platform
- Implement logging

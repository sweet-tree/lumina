"use client";

import { useSession, signOut } from "next-auth/react";
import Link from "next/link";

export function AuthButton() {
  const { data: session } = useSession();

  if (session) {
    return (
      <div className="flex items-center gap-4">
        <span className="text-sm text-muted-foreground">
          {session.user?.email}
        </span>
        <button
          onClick={() => signOut()}
          className="rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-red-700"
        >
          Sign out
        </button>
      </div>
    );
  }

  return (
    <Link
      href="/signin"
      className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
    >
      Sign in
    </Link>
  );
}

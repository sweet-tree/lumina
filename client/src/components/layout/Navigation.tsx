"use client";

import { signIn, signOut, useSession } from "next-auth/react";
import Link from "next/link";

export function Navigation() {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return <div>Loading...</div>;
  }

  return (
    <nav className="flex items-center gap-4">
      {session ? (
        <>
          <Link href="/dashboard" className="text-sm font-medium">
            Dashboard
          </Link>
          <button
            onClick={() => signOut({ callbackUrl: "/" })}
            className="text-sm font-medium"
          >
            Sign Out
          </button>
        </>
      ) : (
        <button
          onClick={() => signIn("google")}
          className="text-sm font-medium"
        >
          Sign In
        </button>
      )}
    </nav>
  );
}

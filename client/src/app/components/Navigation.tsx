"use client";

import { useSession } from "next-auth/react";
import Link from "next/link";
import { AuthButton } from "./AuthButton";

export function Navigation() {
  const { data: session } = useSession();

  return (
    <nav className="flex items-center gap-8">
      <Link
        href="/"
        className="text-sm font-medium transition-colors hover:text-primary"
      >
        Home
      </Link>
      <Link
        href="/features"
        className="text-sm font-medium transition-colors hover:text-primary"
      >
        Features
      </Link>
      <Link
        href="/contact"
        className="text-sm font-medium transition-colors hover:text-primary"
      >
        Contact
      </Link>
      <AuthButton />
      {session && (
        <Link
          href="/dashboard"
          className="text-sm font-medium transition-colors hover:text-primary"
        >
          Dashboard
        </Link>
      )}
    </nav>
  );
}

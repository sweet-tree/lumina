"use client";

import { useSession } from "next-auth/react";
import Link from "next/link";

export default function Dashboard() {
  const { data: session } = useSession();

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      <div className="rounded-lg border p-6">
        <h2 className="text-xl font-semibold mb-4">
          Welcome to your dashboard
        </h2>
        <p className="text-gray-600 mb-4">
          This is your personal workspace where you can manage your documents
          and access your spiritual guidance.
        </p>
        {session && (
          <div className="mt-4">
            <p className="text-sm text-gray-500">
              Signed in as{" "}
              <span className="font-medium">{session.user?.email}</span>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

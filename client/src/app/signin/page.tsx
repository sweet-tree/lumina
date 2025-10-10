"use client";

import { signIn } from "next-auth/react";

export default function SignIn() {
  return (
    <div className="container px-4 py-12">
      <div className="flex flex-col items-center justify-center space-y-8">
        <h1 className="text-3xl font-bold">Sign In</h1>
        <button
          onClick={() => signIn("google", { callbackUrl: "/dashboard" })}
          className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          Sign in with Google
        </button>
      </div>
    </div>
  );
}

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import { Providers } from "./components/Providers";
import { AuthButton } from "./components/AuthButton";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Lumina AI",
  description: "AI-powered document processing and analysis platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased`}>
        <Providers>
          <div className="flex min-h-screen flex-col">
            <header className="border-b">
              <div className="container flex h-16 items-center justify-between px-4">
                <div className="mr-8 flex items-center">
                  <span className="font-bold">Lumina AI</span>
                </div>
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
                </nav>
              </div>
            </header>
            <main className="flex-1">{children}</main>
            <footer className="border-t">
              <div className="container flex h-16 items-center justify-center px-4">
                <p className="text-sm text-muted-foreground">
                  © {new Date().getFullYear()} Lumina AI. All rights reserved.
                </p>
              </div>
            </footer>
          </div>
        </Providers>
      </body>
    </html>
  );
}

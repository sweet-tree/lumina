import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Providers } from "../components/providers/Providers";
import { Navigation } from "../components/layout/Navigation";
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
                <Navigation />
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

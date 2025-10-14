import { AppSidebar } from "@/features/sidebar/app-sidebar";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <AppSidebar />
        <main className="flex-1">
          {/* Mobile menu trigger */}
          <div className="sticky top-0 z-10 flex items-center gap-2 border-b bg-background p-4 lg:hidden">
            <SidebarTrigger />
            <h1 className="text-lg font-semibold">Lumina</h1>
          </div>
          {/* Main content */}
          <div className="p-4 lg:p-8">{children}</div>
        </main>
      </div>
    </SidebarProvider>
  );
}

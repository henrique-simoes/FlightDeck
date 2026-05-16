import { createFileRoute } from "@tanstack/react-router";
import { Navbar } from "@/components/Navbar";
import { EventFilters } from "@/components/EventFilters";
import { EventList } from "@/components/EventList";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <header className="mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-foreground">
            Discover amazing events
          </h1>
          <p className="mt-2 text-muted-foreground">
            Concerts, conferences, talks and more near you.
          </p>
        </header>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <aside className="lg:col-span-1">
            <EventFilters />
          </aside>
          <section className="lg:col-span-2">
            <EventList />
          </section>
        </div>
      </main>
    </div>
  );
}

import { createFileRoute } from "@tanstack/react-router";
import { Navbar } from "@/components/Navbar";
import { loadAssignment } from "@/gen-ui/api";
import { fallbackAssignment, isPersona } from "@/gen-ui/fallback";
import { GenUIRenderer } from "@/gen-ui/GenUIRenderer";
import type { PersonaId } from "@/gen-ui/types";

export const Route = createFileRoute("/")({
  validateSearch: (search: Record<string, unknown>): { persona: PersonaId } => ({
    persona: isPersona(search.persona) ? search.persona : "scanner",
  }),
  loaderDeps: ({ search }) => ({ persona: search.persona }),
  loader: ({ deps }) => loadAssignment(deps.persona),
  component: Index,
});

function Index() {
  const search = Route.useSearch();
  const assignment = Route.useLoaderData() ?? fallbackAssignment(search.persona);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <GenUIRenderer assignment={assignment} />
      </main>
    </div>
  );
}

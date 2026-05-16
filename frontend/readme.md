# Eventinkerer Frontend

Eventinkerer is an initial TanStack Start frontend for discovering events and buying tickets. The current app includes a branded home screen with a sticky navbar, event filters, and a responsive event list for concerts, conferences, talks, and festivals.

## Tech Stack
- React 19
- TanStack Start and TanStack Router
- Vite
- TypeScript
- Tailwind CSS 4
- Radix UI primitives
- lucide-react icons

## Getting Started

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend expects the FastAPI backend at `http://localhost:8000`. Override it with:

```bash
VITE_FLIGHTDECK_API_BASE_URL=http://localhost:8000 npm run dev
```

Build for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Available Scripts
- `npm run dev`: starts the Vite development server.
- `npm run build`: creates a production build.
- `npm run build:dev`: creates a development-mode build.
- `npm run preview`: previews the built app locally.
- `npm run lint`: runs ESLint.
- `npm run format`: formats the project with Prettier.

## Project Structure

```text
frontend/
  public/               Static assets
  src/
    components/         App-specific and shared UI components
    components/ui/      Radix-based UI primitives
    hooks/              Shared React hooks
    lib/                Utilities and app helpers
    routes/             TanStack Router routes
    router.tsx          Router setup
    start.ts            Client entry
    server.ts           Server entry
    styles.css          Global styles and theme tokens
  design.md             Brand and UI direction
```

## Current Product Surface

The initial experience is the event discovery home page. It provides:
- A branded sticky navigation bar.
- Search, category, area, date, and price filters.
- A responsive event list with venue, date, attendance, and ticket pricing metadata.
- Gradient-driven brand styling documented in `design.md`.

## Design Direction

The visual identity is documented in `design.md`. Keep future UI work aligned with the violet-to-cyan brand gradient, soft rounded controls, clear metadata hierarchy, and generous spacing.

import * as React from "react";
import { Calendar, MapPin, Search, Tag, Users } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { postTelemetry } from "./api";
import type { AssignmentResponse, EventItem } from "./types";

type GenUIRendererProps = {
  assignment: AssignmentResponse;
};

function getSessionId() {
  const key = "flightdeck_session_id";
  const existing = window.sessionStorage.getItem(key);
  if (existing) return existing;
  const created = `sess_${crypto.randomUUID()}`;
  window.sessionStorage.setItem(key, created);
  return created;
}

function useTelemetry(assignment: AssignmentResponse) {
  const firstActionSent = React.useRef(false);

  React.useEffect(() => {
    const started = performance.now();
    postTelemetry("ui-rendered", {
      event_type: "ui-rendered",
      session_id: getSessionId(),
      experiment_id: assignment.experiment.id,
      variant_id: assignment.variant.id,
      blueprint_id: assignment.blueprint.id,
      persona_id: assignment.blueprint.persona_id,
      surface_id: "event_discovery",
      target_component: "event-discovery-surface",
      latency_ms: Math.round(performance.now() - started),
      metadata: {
        catalog_version: assignment.blueprint.catalog_version,
        design_md_hash: assignment.blueprint.design_md_hash,
      },
    });
  }, [assignment]);

  return React.useCallback(
    (eventPath: "first-action" | "task-completed" | "feedback", target: string, metadata = {}) => {
      if (eventPath === "first-action" && firstActionSent.current) return;
      if (eventPath === "first-action") firstActionSent.current = true;

      postTelemetry(eventPath, {
        event_type: eventPath,
        session_id: getSessionId(),
        experiment_id: assignment.experiment.id,
        variant_id: assignment.variant.id,
        blueprint_id: assignment.blueprint.id,
        persona_id: assignment.blueprint.persona_id,
        surface_id: "event_discovery",
        target_component: target,
        first_action_expected: assignment.variant.expected_first_action,
        first_action_actual: target,
        metadata,
      });
    },
    [assignment],
  );
}

function orderedEvents(events: EventItem[], order: string[]) {
  if (!order.length) return events;
  const byId = new Map(events.map((event) => [event.id, event]));
  const ordered = order.flatMap((eventId) => {
    const event = byId.get(eventId);
    return event ? [event] : [];
  });
  const remaining = events.filter((event) => !order.includes(event.id));
  return [...ordered, ...remaining];
}

export function GenUIRenderer({ assignment }: GenUIRendererProps) {
  const spec = assignment.blueprint.spec;
  const track = useTelemetry(assignment);
  const events = orderedEvents(spec.events, spec.event_list.event_order);
  const isCompact = spec.event_list.density === "compact";
  const filtersFirst = spec.layout === "filters_top";
  const compactToolbar = spec.layout === "compact_toolbar";

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="text-xs font-semibold uppercase text-primary">
            {spec.persona_id.replace("_", " ")} variant
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-foreground">
            {spec.event_list.title}
          </h1>
          <p className="mt-2 text-muted-foreground">{spec.event_list.summary}</p>
        </div>
        <div className="rounded-full border border-border bg-card px-3 py-1.5 text-xs text-muted-foreground">
          {assignment.variant.guardrail_status === "passed" ? "Critique passed" : "Critique failed"}
        </div>
      </header>

      <div
        className={
          filtersFirst || compactToolbar
            ? "grid grid-cols-1 gap-6"
            : "grid grid-cols-1 lg:grid-cols-3 gap-6"
        }
      >
        <aside className={filtersFirst || compactToolbar ? "" : "lg:col-span-1"}>
          <GeneratedFilters assignment={assignment} compact={compactToolbar} onTrack={track} />
        </aside>
        <section className={filtersFirst || compactToolbar ? "" : "lg:col-span-2"}>
          <div className="space-y-5">
            <div className="flex items-center justify-between gap-3">
              <p className="text-sm text-muted-foreground">
                <span className="font-semibold text-foreground">{events.length}</span> events found
                in Miami
              </p>
              <select
                defaultValue={spec.event_list.default_sort}
                onChange={(event) =>
                  track("first-action", "sort_change", { value: event.target.value })
                }
                className="text-sm bg-card border border-border rounded-full px-4 py-1.5 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/30"
              >
                {spec.event_list.sort_options.map((option) => (
                  <option key={option}>{option}</option>
                ))}
              </select>
            </div>

            {events.map((event) => (
              <GeneratedEventCard
                key={event.id}
                event={event}
                compact={isCompact}
                cta={spec.event_list.primary_action_label}
                onTrack={track}
              />
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

function GeneratedFilters({
  assignment,
  compact,
  onTrack,
}: {
  assignment: AssignmentResponse;
  compact: boolean;
  onTrack: ReturnType<typeof useTelemetry>;
}) {
  const filters = assignment.blueprint.spec.filters;
  const wrapperClass = compact
    ? "rounded-3xl border border-border/60 bg-card p-4 shadow-sm"
    : "sticky top-24 rounded-3xl border border-border/60 bg-card p-6 shadow-sm";

  return (
    <div className={wrapperClass}>
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-lg font-semibold text-foreground">{filters.title}</h2>
        <Button variant="ghost" size="sm" className="text-xs text-muted-foreground rounded-full">
          Clear
        </Button>
      </div>

      <div className={compact ? "grid gap-4 md:grid-cols-4" : "space-y-6"}>
        <div className="space-y-2">
          <Label className="text-xs font-medium text-muted-foreground flex items-center gap-1.5">
            <Search className="h-3.5 w-3.5" /> {filters.search_label}
          </Label>
          <Input
            placeholder={filters.search_placeholder}
            className="rounded-2xl"
            onFocus={() => onTrack("first-action", "search_focus")}
          />
        </div>

        <div className="space-y-3">
          <Label className="text-xs font-medium text-muted-foreground flex items-center gap-1.5">
            <Tag className="h-3.5 w-3.5" /> Category
          </Label>
          <div className={compact ? "flex flex-wrap gap-2" : "space-y-2.5"}>
            {filters.categories.map((category) => (
              <div key={category} className="flex items-center gap-2.5">
                <Checkbox
                  id={category}
                  defaultChecked={filters.selected_categories.includes(category)}
                  className="rounded-md"
                  onCheckedChange={() => onTrack("first-action", "category_filter", { category })}
                />
                <label htmlFor={category} className="text-sm text-foreground cursor-pointer">
                  {category}
                </label>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-3">
          <Label className="text-xs font-medium text-muted-foreground flex items-center gap-1.5">
            <MapPin className="h-3.5 w-3.5" /> Area in Miami
          </Label>
          <div className="flex flex-wrap gap-2">
            {filters.areas.map((area) => (
              <button
                type="button"
                key={area}
                onClick={() => onTrack("first-action", "area_filter", { area })}
                className={`px-3 py-1 rounded-full text-xs font-medium cursor-pointer transition-colors ${
                  area === filters.selected_area
                    ? "bg-primary text-primary-foreground"
                    : "bg-secondary text-secondary-foreground hover:bg-secondary/70"
                }`}
              >
                {area}
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <Label className="text-xs font-medium text-muted-foreground">Max price</Label>
            <span className="text-xs font-semibold text-primary">${filters.max_price}</span>
          </div>
          <Slider
            defaultValue={[filters.max_price]}
            max={500}
            step={10}
            onValueChange={(value) => onTrack("first-action", "price_filter", { value })}
          />
          <Button
            onClick={() => onTrack("first-action", "apply_filters")}
            className="w-full rounded-full bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-opacity"
          >
            {filters.primary_action_label}
          </Button>
        </div>
      </div>
    </div>
  );
}

function GeneratedEventCard({
  event,
  compact,
  cta,
  onTrack,
}: {
  event: EventItem;
  compact: boolean;
  cta: string;
  onTrack: ReturnType<typeof useTelemetry>;
}) {
  return (
    <article
      className={`group flex flex-col sm:flex-row gap-5 rounded-3xl border border-border/60 bg-card p-4 shadow-sm hover:shadow-lg hover:border-primary/30 transition-all duration-300 ${
        compact ? "sm:gap-4 sm:p-3" : ""
      }`}
    >
      <button
        type="button"
        onClick={() => onTrack("first-action", "open_event", { event_id: event.id })}
        className={`relative flex-shrink-0 sm:w-48 h-40 sm:h-auto rounded-2xl bg-gradient-to-br ${event.gradient} flex items-center justify-center text-5xl overflow-hidden`}
      >
        <span className="drop-shadow-lg">{event.emoji}</span>
        <span className="absolute top-3 left-3 text-[10px] font-semibold uppercase bg-background/90 text-foreground px-2.5 py-1 rounded-full">
          {event.category}
        </span>
      </button>

      <div className="flex-1 flex flex-col justify-between gap-3">
        <div>
          <h3 className="text-lg font-bold text-foreground group-hover:text-primary transition-colors">
            {event.title}
          </h3>
          <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-sm text-muted-foreground">
            <span className="inline-flex items-center gap-1.5">
              <Calendar className="h-3.5 w-3.5" /> {event.date}
            </span>
            <span className="inline-flex items-center gap-1.5">
              <MapPin className="h-3.5 w-3.5" /> {event.venue}, {event.area}
            </span>
            <span className="inline-flex items-center gap-1.5">
              <Users className="h-3.5 w-3.5" /> {event.attending} attending
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between pt-2 border-t border-border/50">
          <span className="text-sm font-semibold text-foreground">{event.price} USD</span>
          <Button
            onClick={() => onTrack("first-action", "buy_tickets", { event_id: event.id })}
            className="rounded-full bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-opacity"
          >
            {cta}
          </Button>
        </div>
      </div>
    </article>
  );
}

export type PersonaId = "scanner" | "comparer" | "explorer" | "expert_operator";

export type EventItem = {
  id: string;
  title: string;
  category: string;
  date: string;
  area: string;
  venue: string;
  price: string;
  attending: string;
  gradient: string;
  emoji: string;
};
export type FilterConfig = {
  type: "filters";
  title: string;
  search_label: string;
  search_placeholder: string;
  categories: string[];
  selected_categories: string[];
  areas: string[];
  selected_area: string;
  date_options: string[];
  max_price: number;
  primary_action_label: string;
};

export type EventListConfig = {
  type: "event_list";
  title: string;
  summary: string;
  sort_options: string[];
  default_sort: string;
  density: "comfortable" | "compact" | "editorial";
  event_order: string[];
  primary_action_label: string;
};

export type BlueprintSpec = {
  schema_version: "flightdeck.blueprint.v1";
  persona_id: PersonaId;
  surface_id: "event_discovery";
  catalog_version: string;
  design_md_hash: string;
  hypothesis: string;
  primary_metric: string;
  layout: "filters_left" | "filters_top" | "compact_toolbar";
  expected_first_action: string;
  filters: FilterConfig;
  event_list: EventListConfig;
  events: EventItem[];
};

export type VariantRecord = {
  id: string;
  experiment_id: string;
  blueprint_id: string;
  persona_id: PersonaId;
  surface_id: "event_discovery";
  status: "draft" | "active" | "archived" | "failed";
  expected_first_action: string;
  guardrail_status: "passed" | "failed";
  created_at: string;
  activated_at: string | null;
};

export type ExperimentRecord = {
  id: string;
  surface_id: "event_discovery";
  name: string;
  hypothesis: string;
  primary_metric: string;
  status: "draft" | "active" | "paused" | "archived";
  created_at: string;
  updated_at: string;
  variants: VariantRecord[];
  metrics: Record<string, unknown>;
};

export type BlueprintRecord = {
  id: string;
  persona_id: PersonaId;
  surface_id: "event_discovery";
  status: "draft" | "validated" | "failed" | "archived";
  spec: BlueprintSpec;
  critique: {
    status: "passed" | "failed";
    checks: Record<string, boolean>;
    summary: string;
  };
  catalog_version: string;
  design_md_hash: string;
  created_at: string;
};

export type AssignmentResponse = {
  experiment: ExperimentRecord;
  variant: VariantRecord;
  blueprint: BlueprintRecord;
};

CREATE TABLE IF NOT EXISTS personas (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  md_path TEXT NOT NULL,
  summary TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blueprints (
  id TEXT PRIMARY KEY,
  persona_id TEXT NOT NULL,
  surface_id TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft', 'validated', 'failed', 'archived')),
  spec_json TEXT NOT NULL,
  critique_json TEXT NOT NULL,
  catalog_version TEXT NOT NULL,
  design_md_hash TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (persona_id) REFERENCES personas(id)
);

CREATE TABLE IF NOT EXISTS experiments (
  id TEXT PRIMARY KEY,
  surface_id TEXT NOT NULL,
  name TEXT NOT NULL,
  hypothesis TEXT NOT NULL,
  primary_metric TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft', 'active', 'paused', 'archived')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS variants (
  id TEXT PRIMARY KEY,
  experiment_id TEXT NOT NULL,
  blueprint_id TEXT NOT NULL,
  persona_id TEXT NOT NULL,
  surface_id TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft', 'active', 'archived', 'failed')),
  expected_first_action TEXT NOT NULL,
  guardrail_status TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  activated_at TEXT,
  FOREIGN KEY (experiment_id) REFERENCES experiments(id),
  FOREIGN KEY (blueprint_id) REFERENCES blueprints(id),
  FOREIGN KEY (persona_id) REFERENCES personas(id)
);

CREATE TABLE IF NOT EXISTS telemetry_events (
  id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  session_id TEXT NOT NULL,
  experiment_id TEXT,
  variant_id TEXT,
  blueprint_id TEXT,
  persona_id TEXT NOT NULL,
  surface_id TEXT NOT NULL,
  target_component TEXT,
  first_action_expected TEXT,
  first_action_actual TEXT,
  task_completed INTEGER,
  latency_ms INTEGER,
  metadata_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (experiment_id) REFERENCES experiments(id),
  FOREIGN KEY (variant_id) REFERENCES variants(id),
  FOREIGN KEY (blueprint_id) REFERENCES blueprints(id),
  FOREIGN KEY (persona_id) REFERENCES personas(id)
);

CREATE TABLE IF NOT EXISTS reasoning_bank_entries (
  id TEXT PRIMARY KEY,
  experiment_id TEXT,
  variant_id TEXT,
  blueprint_id TEXT,
  persona_id TEXT NOT NULL,
  surface_id TEXT NOT NULL,
  hypothesis TEXT NOT NULL,
  metrics_observed_json TEXT NOT NULL,
  outcome_summary TEXT NOT NULL,
  proposed_design_rule TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('accepted', 'rejected', 'needs-review')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (experiment_id) REFERENCES experiments(id),
  FOREIGN KEY (variant_id) REFERENCES variants(id),
  FOREIGN KEY (blueprint_id) REFERENCES blueprints(id),
  FOREIGN KEY (persona_id) REFERENCES personas(id)
);

CREATE INDEX IF NOT EXISTS idx_blueprints_persona ON blueprints(persona_id, surface_id, created_at);
CREATE INDEX IF NOT EXISTS idx_variants_assignment ON variants(experiment_id, persona_id, status);
CREATE INDEX IF NOT EXISTS idx_events_variant ON telemetry_events(variant_id, event_type, created_at);


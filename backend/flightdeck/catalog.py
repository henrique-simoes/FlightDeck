from __future__ import annotations

from .models import BlueprintSpec, CritiqueResult

CATALOG_VERSION = "flightdeck-event-discovery-v1"
ALLOWED_LAYOUTS = {"filters_left", "filters_top", "compact_toolbar"}
ALLOWED_GRADIENT_PREFIXES = (
    "from-fuchsia",
    "from-cyan",
    "from-amber",
    "from-emerald",
    "from-pink",
    "from-violet",
    "from-sky",
)


def critique_blueprint(spec: BlueprintSpec) -> CritiqueResult:
    event_ids = {event.id for event in spec.events}
    ordered_ids_exist = all(event_id in event_ids for event_id in spec.event_list.event_order)
    selected_area_exists = spec.filters.selected_area in spec.filters.areas
    selected_categories_exist = all(
        category in spec.filters.categories for category in spec.filters.selected_categories
    )
    gradients_allowed = all(
        event.gradient.startswith(ALLOWED_GRADIENT_PREFIXES) for event in spec.events
    )

    checks = {
        "catalog_version": spec.catalog_version == CATALOG_VERSION,
        "layout_allowed": spec.layout in ALLOWED_LAYOUTS,
        "ordered_event_ids_exist": ordered_ids_exist,
        "selected_area_exists": selected_area_exists,
        "selected_categories_exist": selected_categories_exist,
        "gradients_allowed": gradients_allowed,
        "no_html_payloads": "<" not in spec.model_dump_json(),
    }
    status = "passed" if all(checks.values()) else "failed"
    return CritiqueResult(
        status=status,
        checks=checks,
        summary=(
            "Blueprint passed catalog, schema, and safety checks."
            if status == "passed"
            else "Blueprint failed one or more catalog, schema, or safety checks."
        ),
    )


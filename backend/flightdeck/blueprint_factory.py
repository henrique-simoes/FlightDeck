from __future__ import annotations

from hashlib import sha256
from typing import Any

from .catalog import CATALOG_VERSION
from .config import FRONTEND_DESIGN_PATH
from .models import BlueprintSpec, PersonaId

BASE_EVENTS = [
    {
        "id": "bad-bunny",
        "title": "Bad Bunny - Most Wanted Tour",
        "category": "Concert",
        "date": "Sat, Jun 14 - 9:00 PM",
        "area": "Downtown Miami",
        "venue": "Kaseya Center",
        "price": "From $120",
        "attending": "12.4k",
        "gradient": "from-fuchsia-500 via-violet-500 to-indigo-500",
        "emoji": "🎤",
    },
    {
        "id": "reactconf",
        "title": "ReactConf US 2026",
        "category": "Conference",
        "date": "Thu, Jul 3 - 8:30 AM",
        "area": "Brickell",
        "venue": "Miami Convention Center",
        "price": "From $95",
        "attending": "1.8k",
        "gradient": "from-cyan-400 via-sky-500 to-blue-600",
        "emoji": "💻",
    },
    {
        "id": "simplicity-talk",
        "title": "Talk: The Art of Simplicity",
        "category": "Talk",
        "date": "Fri, May 22 - 7:00 PM",
        "area": "Coconut Grove",
        "venue": "Coconut Grove Playhouse",
        "price": "From $35",
        "attending": "640",
        "gradient": "from-amber-400 via-orange-500 to-rose-500",
        "emoji": "🎭",
    },
    {
        "id": "ultra",
        "title": "Ultra Music Festival",
        "category": "Festival",
        "date": "Fri, Mar 27 - 2:00 PM",
        "area": "Downtown Miami",
        "venue": "Bayfront Park",
        "price": "From $320",
        "attending": "45k",
        "gradient": "from-emerald-400 via-teal-500 to-cyan-600",
        "emoji": "🎶",
    },
    {
        "id": "standup-night",
        "title": "Standup Night - Trevor Noah",
        "category": "Talk",
        "date": "Sat, May 31 - 8:30 PM",
        "area": "South Beach",
        "venue": "Fillmore Miami Beach",
        "price": "From $60",
        "attending": "1.2k",
        "gradient": "from-pink-400 via-rose-500 to-red-500",
        "emoji": "🎙️",
    },
]

COMMON_FILTERS = {
    "categories": ["Concerts", "Conferences", "Talks", "Theater", "Sports", "Festivals"],
    "areas": ["Downtown", "Wynwood", "South Beach", "Brickell", "Coconut Grove"],
    "date_options": ["Today", "This week", "This month", "Custom"],
}


def design_hash() -> str:
    digest = sha256(FRONTEND_DESIGN_PATH.read_bytes()).hexdigest()
    return f"sha256:{digest}"


DEFAULT_BLUEPRINT_CONFIG: dict[PersonaId, dict[str, Any]] = {
    "scanner": {
        "primary_metric": "first_action_rate",
        "expected_first_actions": ["buy_tickets", "open_event", "buy_tickets"],
        "hypotheses": [
            "Scanner users will act faster when a compact filter row appears above a short event list.",
            "Scanner users will act faster when high-energy events are emphasized first.",
            "Scanner users will commit faster when lower-price picks are surfaced first.",
        ],
        "layouts": ["filters_top", "compact_toolbar", "filters_left"],
        "filter_titles": ["Quick filters", "Fast path", "Simple filters"],
        "search_placeholders": ["Search by event", "Find an event fast", "Search quick picks"],
        "selected_categories": [["Concerts"], ["Concerts", "Festivals"], ["Talks", "Conferences"]],
        "selected_areas": ["Downtown", "Downtown", "Coconut Grove"],
        "max_prices": [250, 350, 120],
        "filter_ctas": ["Apply quick filters", "Show top picks", "Apply"],
        "list_titles": ["Best matches now", "Fast picks near you", "Easy decisions"],
        "summaries": [
            "5 streamlined picks in Miami",
            "High-signal events sorted for quick action",
            "Lower-price options first, with fewer distractions",
        ],
        "densities": ["comfortable", "editorial", "comfortable"],
        "event_orders": [
            ["bad-bunny", "reactconf", "standup-night", "simplicity-talk", "ultra"],
            ["ultra", "bad-bunny", "standup-night", "reactconf", "simplicity-talk"],
            ["simplicity-talk", "standup-night", "reactconf", "bad-bunny", "ultra"],
        ],
        "list_ctas": ["Buy tickets", "Open event", "Buy now"],
    },
    "comparer": {
        "primary_metric": "filter_use_rate",
        "expected_first_actions": ["apply_filters", "sort_change", "apply_filters"],
        "hypotheses": [
            "Comparer users will find relevant events faster when filters remain persistent beside comparable cards.",
            "Comparer users will compare faster when filtering and sorting are compressed into one control band.",
            "Comparer users will filter earlier when criteria are presented before the event list.",
        ],
        "layouts": ["filters_left", "compact_toolbar", "filters_top"],
        "filter_titles": ["Compare by criteria", "Compare controls", "Set your criteria"],
        "search_placeholders": [
            "Search title, venue, or category",
            "Filter options",
            "Search candidates",
        ],
        "selected_categories": [["Concerts", "Conferences"], ["Conferences", "Talks"], ["Concerts", "Festivals"]],
        "selected_areas": ["Brickell", "Brickell", "Downtown"],
        "max_prices": [180, 150, 300],
        "filter_ctas": ["Apply filters", "Run comparison", "Update matches"],
        "list_titles": ["Compare event options", "Side-by-side candidates", "Filtered shortlist"],
        "summaries": [
            "Sorted by relevance with attendance and price visible",
            "Compact comparison mode prioritizing price and attendance",
            "Results emphasize category, location, price, and crowd signal",
        ],
        "densities": ["comfortable", "compact", "comfortable"],
        "event_orders": [
            ["reactconf", "bad-bunny", "simplicity-talk", "standup-night", "ultra"],
            ["reactconf", "simplicity-talk", "standup-night", "bad-bunny", "ultra"],
            ["bad-bunny", "ultra", "reactconf", "standup-night", "simplicity-talk"],
        ],
        "list_ctas": ["View details", "Compare", "Inspect"],
    },
    "explorer": {
        "primary_metric": "event_open_rate",
        "expected_first_actions": ["open_event", "category_filter", "area_filter"],
        "hypotheses": [
            "Explorer users will engage more when the list starts with varied categories and discovery-oriented copy.",
            "Explorer users will open more events when categories feel like discovery paths beside the list.",
            "Explorer users will sample more options when controls stay compact and the list changes quickly.",
        ],
        "layouts": ["filters_top", "filters_left", "compact_toolbar"],
        "filter_titles": ["Start exploring", "Discovery paths", "Discovery controls"],
        "search_placeholders": [
            "Try music, talks, or festivals",
            "Search a mood or category",
            "Jump to a category",
        ],
        "selected_categories": [["Festivals", "Talks"], ["Concerts", "Theater"], ["Festivals", "Conferences"]],
        "selected_areas": ["Wynwood", "South Beach", "Downtown"],
        "max_prices": [320, 260, 500],
        "filter_ctas": ["Refresh discoveries", "Explore paths", "Shuffle ideas"],
        "list_titles": ["Fresh paths to explore", "Unexpected finds", "Try a different night"],
        "summaries": [
            "A varied set across music, tech, talks, and culture",
            "A mixed path through live music, comedy, theater, and tech",
            "High-variety layout with quick exploration controls",
        ],
        "densities": ["editorial", "editorial", "compact"],
        "event_orders": [
            ["ultra", "simplicity-talk", "reactconf", "bad-bunny", "standup-night"],
            ["standup-night", "bad-bunny", "simplicity-talk", "ultra", "reactconf"],
            ["ultra", "reactconf", "bad-bunny", "standup-night", "simplicity-talk"],
        ],
        "list_ctas": ["Explore event", "See why", "Preview"],
    },
    "expert_operator": {
        "primary_metric": "time_to_first_correct_action",
        "expected_first_actions": ["sort_change", "search_focus", "sort_change"],
        "hypotheses": [
            "Expert Operator users will move faster when controls are compact and metadata is dense.",
            "Expert Operator users will complete tasks faster with persistent controls and compact rows.",
            "Expert Operator users will scan faster when controls precede an attendance-prioritized list.",
        ],
        "layouts": ["compact_toolbar", "filters_left", "filters_top"],
        "filter_titles": ["Controls", "Query controls", "Batch controls"],
        "search_placeholders": ["Filter dataset", "Query events", "Search inventory"],
        "selected_categories": [["Concerts", "Conferences", "Talks"], ["Conferences"], ["Festivals", "Concerts"]],
        "selected_areas": ["Downtown", "Brickell", "Downtown"],
        "max_prices": [500, 200, 500],
        "filter_ctas": ["Run filter", "Execute", "Apply batch"],
        "list_titles": ["Event inventory", "Filtered inventory", "High-signal inventory"],
        "summaries": [
            "Operational view informed by captured interactions",
            "Dense operational layout with persistent controls",
            "Attendance-prioritized view for rapid triage",
        ],
        "densities": ["compact", "compact", "compact"],
        "event_orders": [
            ["reactconf", "simplicity-talk", "standup-night", "bad-bunny", "ultra"],
            ["reactconf", "simplicity-talk", "bad-bunny", "standup-night", "ultra"],
            ["ultra", "bad-bunny", "reactconf", "standup-night", "simplicity-talk"],
        ],
        "list_ctas": ["Select", "Open", "Select"],
    },
}


def _configured(config: dict[str, Any], fallback: dict[str, Any]) -> dict[str, Any]:
    merged = fallback.copy()
    for key, value in config.items():
        if value not in (None, [], ""):
            merged[key] = value
    return merged


def _pick(config: dict[str, Any], key: str, index: int) -> Any:
    value = config[key]
    if isinstance(value, list):
        return value[index % len(value)]
    return value


def build_blueprint(
    persona_id: PersonaId,
    metrics: dict[str, object] | None = None,
    generation_index: int = 0,
    blueprint_config: dict[str, Any] | None = None,
) -> BlueprintSpec:
    metrics = metrics or {}
    total_events = int(metrics.get("total_events", 0) or 0)
    hash_value = design_hash()
    config = _configured(blueprint_config or {}, DEFAULT_BLUEPRINT_CONFIG[persona_id])
    summary = _pick(config, "summaries", generation_index)
    if persona_id == "expert_operator":
        summary = f"{summary}; {total_events} captured interactions inform ordering"

    return BlueprintSpec.model_validate(
        {
            "persona_id": persona_id,
            "catalog_version": CATALOG_VERSION,
            "design_md_hash": hash_value,
            "hypothesis": _pick(config, "hypotheses", generation_index),
            "primary_metric": config["primary_metric"],
            "layout": _pick(config, "layouts", generation_index),
            "expected_first_action": _pick(config, "expected_first_actions", generation_index),
            "filters": {
                "title": _pick(config, "filter_titles", generation_index),
                "search_placeholder": _pick(config, "search_placeholders", generation_index),
                "categories": COMMON_FILTERS["categories"],
                "selected_categories": _pick(config, "selected_categories", generation_index),
                "areas": COMMON_FILTERS["areas"],
                "selected_area": _pick(config, "selected_areas", generation_index),
                "date_options": COMMON_FILTERS["date_options"],
                "max_price": _pick(config, "max_prices", generation_index),
                "primary_action_label": _pick(config, "filter_ctas", generation_index),
            },
            "event_list": {
                "title": _pick(config, "list_titles", generation_index),
                "summary": summary,
                "sort_options": ["Most relevant", "Upcoming", "Price: low to high", "Most attended"],
                "default_sort": "Most relevant",
                "density": _pick(config, "densities", generation_index),
                "event_order": _pick(config, "event_orders", generation_index),
                "primary_action_label": _pick(config, "list_ctas", generation_index),
            },
            "events": BASE_EVENTS,
        }
    )

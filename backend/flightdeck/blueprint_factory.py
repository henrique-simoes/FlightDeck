from __future__ import annotations

from hashlib import sha256

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


def build_blueprint(persona_id: PersonaId, metrics: dict[str, object] | None = None) -> BlueprintSpec:
    metrics = metrics or {}
    total_events = int(metrics.get("total_events", 0) or 0)
    hash_value = design_hash()

    templates = {
        "scanner": {
            "layout": "filters_top",
            "hypothesis": "Scanner users will act faster when a compact filter row appears above a short event list.",
            "primary_metric": "first_action_rate",
            "expected_first_action": "buy_tickets",
            "filter_title": "Quick filters",
            "search_placeholder": "Search by event",
            "selected_categories": ["Concerts"],
            "selected_area": "Downtown",
            "max_price": 250,
            "filter_cta": "Apply quick filters",
            "list_title": "Best matches now",
            "summary": "5 streamlined picks in Miami",
            "density": "comfortable",
            "event_order": ["bad-bunny", "reactconf", "standup-night", "simplicity-talk", "ultra"],
            "list_cta": "Buy tickets",
        },
        "comparer": {
            "layout": "filters_left",
            "hypothesis": "Comparer users will find relevant events faster when filters remain persistent beside comparable cards.",
            "primary_metric": "filter_use_rate",
            "expected_first_action": "apply_filters",
            "filter_title": "Compare by criteria",
            "search_placeholder": "Search title, venue, or category",
            "selected_categories": ["Concerts", "Conferences"],
            "selected_area": "Brickell",
            "max_price": 180,
            "filter_cta": "Apply filters",
            "list_title": "Compare event options",
            "summary": "Sorted by relevance with attendance and price visible",
            "density": "comfortable",
            "event_order": ["reactconf", "bad-bunny", "simplicity-talk", "standup-night", "ultra"],
            "list_cta": "View details",
        },
        "explorer": {
            "layout": "filters_top",
            "hypothesis": "Explorer users will engage more when the list starts with varied categories and discovery-oriented copy.",
            "primary_metric": "event_open_rate",
            "expected_first_action": "open_event",
            "filter_title": "Start exploring",
            "search_placeholder": "Try music, talks, or festivals",
            "selected_categories": ["Festivals", "Talks"],
            "selected_area": "Wynwood",
            "max_price": 320,
            "filter_cta": "Refresh discoveries",
            "list_title": "Fresh paths to explore",
            "summary": "A varied set across music, tech, talks, and culture",
            "density": "editorial",
            "event_order": ["ultra", "simplicity-talk", "reactconf", "bad-bunny", "standup-night"],
            "list_cta": "Explore event",
        },
        "expert_operator": {
            "layout": "compact_toolbar",
            "hypothesis": "Expert Operator users will move faster when controls are compact and metadata is dense.",
            "primary_metric": "time_to_first_correct_action",
            "expected_first_action": "sort_change",
            "filter_title": "Controls",
            "search_placeholder": "Filter dataset",
            "selected_categories": ["Concerts", "Conferences", "Talks"],
            "selected_area": "Downtown",
            "max_price": 500,
            "filter_cta": "Run filter",
            "list_title": "Event inventory",
            "summary": f"Operational view; {total_events} captured interactions inform ordering",
            "density": "compact",
            "event_order": ["reactconf", "simplicity-talk", "standup-night", "bad-bunny", "ultra"],
            "list_cta": "Select",
        },
    }
    template = templates[persona_id]

    return BlueprintSpec.model_validate(
        {
            "persona_id": persona_id,
            "catalog_version": CATALOG_VERSION,
            "design_md_hash": hash_value,
            "hypothesis": template["hypothesis"],
            "primary_metric": template["primary_metric"],
            "layout": template["layout"],
            "expected_first_action": template["expected_first_action"],
            "filters": {
                "title": template["filter_title"],
                "search_placeholder": template["search_placeholder"],
                "categories": COMMON_FILTERS["categories"],
                "selected_categories": template["selected_categories"],
                "areas": COMMON_FILTERS["areas"],
                "selected_area": template["selected_area"],
                "date_options": COMMON_FILTERS["date_options"],
                "max_price": template["max_price"],
                "primary_action_label": template["filter_cta"],
            },
            "event_list": {
                "title": template["list_title"],
                "summary": template["summary"],
                "sort_options": ["Most relevant", "Upcoming", "Price: low to high", "Most attended"],
                "default_sort": "Most relevant",
                "density": template["density"],
                "event_order": template["event_order"],
                "primary_action_label": template["list_cta"],
            },
            "events": BASE_EVENTS,
        }
    )


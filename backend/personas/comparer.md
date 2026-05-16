# Comparer

## Description
Comparer users want visible criteria, stable controls, and enough evidence to evaluate tradeoffs before acting.

## Active Hypothesis
Comparer users will find relevant events faster when filters remain persistent beside comparable event cards.

## Active Blueprint
- Blueprint: none
- Variant: none

## Metrics Summary
- Total events captured: 0
- Most common first action: none
- Current primary metric: filter_use_rate

## Accepted Learnings
- Keep filters visible.
- Preserve venue, price, date, category, and attendance metadata.
- Prefer stable ordering controls over surprise recommendations.

## Blueprint Configuration
Internal generation controls for this archetype. Edit this JSON to change future Blueprint output; users should never see this metadata.

```json
{
  "layouts": ["filters_left", "compact_toolbar", "filters_top"],
  "list_titles": ["Compare event options", "Side-by-side candidates", "Filtered shortlist"],
  "summaries": [
    "Sorted by relevance with attendance and price visible",
    "Compact comparison mode prioritizing price and attendance",
    "Results emphasize category, location, price, and crowd signal"
  ],
  "selected_categories": [["Concerts", "Conferences"], ["Conferences", "Talks"], ["Concerts", "Festivals"]],
  "selected_areas": ["Brickell", "Brickell", "Downtown"],
  "max_prices": [180, 150, 300],
  "event_orders": [
    ["reactconf", "bad-bunny", "simplicity-talk", "standup-night", "ultra"],
    ["reactconf", "simplicity-talk", "standup-night", "bad-bunny", "ultra"],
    ["bad-bunny", "ultra", "reactconf", "standup-night", "simplicity-talk"]
  ],
  "list_ctas": ["View details", "Compare", "Inspect"]
}
```

## Changelog

- 2026-05-16 19:49:11 UTC: Activated `bp_a9776516def7` as `var_4c2bbf18ac73` for `exp_b2104e267eb9`. Total telemetry events considered: 2. Generation index: 4.

- 2026-05-16 19:45:53 UTC: Activated `bp_ce9c990261f2` as `var_28cbf3610cea` for `exp_b2104e267eb9`. Total telemetry events considered: 2. Generation index: 3.

- 2026-05-16 19:45:33 UTC: Activated `bp_dc89572fb959` as `var_4711de8007ea` for `exp_b2104e267eb9`. Total telemetry events considered: 2. Generation index: 2.

- 2026-05-16 19:44:42 UTC: Activated `bp_3e27212f253f` as `var_aa5f1a9293c2` for `exp_b2104e267eb9`. Total telemetry events considered: 2. Generation index: 1.

- 2026-05-16 18:54:27 UTC: Activated `bp_6731af4864e8` as `var_3a9c383e2ac3` for `exp_7a8ebdfda671`. Total telemetry events considered: 0.

- 2026-05-16 18:54:27 UTC: Activated `bp_c4a219536030` as `var_b417ac06e948` for `exp_7d3bf28a434a`. Total telemetry events considered: 0.

- 2026-05-16 18:53:09 UTC: Activated `bp_7d36744de2b4` as `var_2fad5e8d2f23` for `exp_e9816685b13f`. Total telemetry events considered: 0.

- 2026-05-16 18:53:09 UTC: Activated `bp_7d13d0556119` as `var_6bfef6e271ae` for `exp_2cfbcdd9f8ad`. Total telemetry events considered: 0.

- 2026-05-16 18:52:07 UTC: Activated `bp_e713fc3c2bdd` as `var_3a91c2bc98bf` for `exp_b2104e267eb9`. Total telemetry events considered: 0.

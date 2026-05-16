# Scanner

## Description
Scanner users want to understand the page quickly, identify the best match, and act with minimal decision overhead.

## Active Hypothesis
Scanner users will act faster when a compact filter row appears above a short event list with obvious CTAs.

## Active Blueprint
- Blueprint: none
- Variant: none

## Metrics Summary
- Total events captured: 0
- Most common first action: none
- Current primary metric: first_action_rate

## Accepted Learnings
- Keep the first screen concise.
- Make the primary action visually obvious.
- Avoid dense comparison copy before the first click.

## Blueprint Configuration
Internal generation controls for this archetype. Edit this JSON to change future Blueprint output; users should never see this metadata.

```json
{
  "layouts": ["filters_top", "compact_toolbar", "filters_left"],
  "list_titles": ["Best matches now", "Fast picks near you", "Easy decisions"],
  "summaries": [
    "5 streamlined picks in Miami",
    "High-signal events sorted for quick action",
    "Lower-price options first, with fewer distractions"
  ],
  "selected_categories": [["Concerts"], ["Concerts", "Festivals"], ["Talks", "Conferences"]],
  "selected_areas": ["Downtown", "Downtown", "Coconut Grove"],
  "max_prices": [250, 350, 120],
  "event_orders": [
    ["bad-bunny", "reactconf", "standup-night", "simplicity-talk", "ultra"],
    ["ultra", "bad-bunny", "standup-night", "reactconf", "simplicity-talk"],
    ["simplicity-talk", "standup-night", "reactconf", "bad-bunny", "ultra"]
  ],
  "list_ctas": ["Buy tickets", "Open event", "Buy now"]
}
```

## Changelog

- 2026-05-16 19:37:11 UTC: Activated `bp_53d3b97243f4` as `var_b8fce4424c00` for `exp_b2104e267eb9`. Total telemetry events considered: 3.

- 2026-05-16 19:36:59 UTC: Activated `bp_b9247c2e963d` as `var_0d4306c306e8` for `exp_b2104e267eb9`. Total telemetry events considered: 3.

- 2026-05-16 18:54:27 UTC: Activated `bp_1892ebef775f` as `var_5b820d855a5f` for `exp_7a8ebdfda671`. Total telemetry events considered: 0.

- 2026-05-16 18:54:27 UTC: Activated `bp_912fb9d342d7` as `var_09d72f0babba` for `exp_7d3bf28a434a`. Total telemetry events considered: 0.

- 2026-05-16 18:53:09 UTC: Activated `bp_bd853a0c42c7` as `var_7f9662927e21` for `exp_e9816685b13f`. Total telemetry events considered: 0.

- 2026-05-16 18:53:09 UTC: Activated `bp_0c7328a2bf88` as `var_ba5365f31d3b` for `exp_2cfbcdd9f8ad`. Total telemetry events considered: 0.

- 2026-05-16 18:52:07 UTC: Activated `bp_2ba45288bb4e` as `var_d80e128087ee` for `exp_b2104e267eb9`. Total telemetry events considered: 0.

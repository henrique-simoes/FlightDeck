# Expert Operator

## Description
Expert Operator users want dense controls, direct manipulation, and minimal explanatory copy.

## Active Hypothesis
Expert Operator users will move faster when controls are compact and event metadata is dense.

## Active Blueprint
- Blueprint: none
- Variant: none

## Metrics Summary
- Total events captured: 0
- Most common first action: none
- Current primary metric: time_to_first_correct_action

## Accepted Learnings
- Reduce instructional copy.
- Keep controls compact and predictable.
- Prioritize fast sort/filter actions over guided discovery.

## Blueprint Configuration
Internal generation controls for this archetype. Edit this JSON to change future Blueprint output; users should never see this metadata.

```json
{
  "layouts": ["compact_toolbar", "filters_left", "filters_top"],
  "list_titles": ["Event inventory", "Filtered inventory", "High-signal inventory"],
  "summaries": [
    "Operational view informed by captured interactions",
    "Dense operational layout with persistent controls",
    "Attendance-prioritized view for rapid triage"
  ],
  "selected_categories": [["Concerts", "Conferences", "Talks"], ["Conferences"], ["Festivals", "Concerts"]],
  "selected_areas": ["Downtown", "Brickell", "Downtown"],
  "max_prices": [500, 200, 500],
  "event_orders": [
    ["reactconf", "simplicity-talk", "standup-night", "bad-bunny", "ultra"],
    ["reactconf", "simplicity-talk", "bad-bunny", "standup-night", "ultra"],
    ["ultra", "bad-bunny", "reactconf", "standup-night", "simplicity-talk"]
  ],
  "list_ctas": ["Select", "Open", "Select"]
}
```

## Changelog

- 2026-05-16 18:54:27 UTC: Activated `bp_49ebbcc8d42b` as `var_ecb7f1f12548` for `exp_7a8ebdfda671`. Total telemetry events considered: 0.

- 2026-05-16 18:54:27 UTC: Activated `bp_2f9487b58eb7` as `var_22d04303aede` for `exp_7d3bf28a434a`. Total telemetry events considered: 0.

- 2026-05-16 18:53:09 UTC: Activated `bp_3833abeec8ad` as `var_3969144d6e03` for `exp_e9816685b13f`. Total telemetry events considered: 0.

- 2026-05-16 18:53:09 UTC: Activated `bp_46f3efb99b17` as `var_983fa0961b52` for `exp_2cfbcdd9f8ad`. Total telemetry events considered: 0.

- 2026-05-16 18:52:07 UTC: Activated `bp_3e6f9a634cb3` as `var_92f049ae0943` for `exp_b2104e267eb9`. Total telemetry events considered: 0.

# P02B 24-cell diagnostic

One input per family; K=2 per mode/cap. All primary scores preserved. This is not formal cap selection.

| Family | Mode | Cap | Planned/executed/retained | Strict FINAL | Perfect | Native scores | Wrapper subtype | Syntax / cap-no-final / timeout | Output tokens | Worker seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| number_sorting | D | 1024 | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | ['missing_both_tags', 'missing_both_tags'] | 0/0/0 | [20, 20] | [13.65, 13.538] |
| number_sorting | R | 1024 | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [None, None] | 0/0/0 | [478, 528] | [32.773, 34.592] |
| number_format | D | 1024 | 2/2/2 | 2/2 | 0/2 | [0.0, 0.0] | [None, None] | 0/0/0 | [23, 23] | [12.802, 13.647] |
| number_format | R | 1024 | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | [None, None] | 0/2/0 | [1024, 1024] | [46.052, 55.482] |
| letter_counting | D | 1024 | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [None, None] | 0/0/0 | [8, 8] | [12.638, 13.137] |
| letter_counting | R | 1024 | 2/2/2 | 1/2 | 1/2 | [1.0, 0.0] | [None, None] | 0/1/0 | [677, 1024] | [34.572, 55.406] |
| graph_color | D | 1024 | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | ['missing_both_tags', 'missing_both_tags'] | 0/0/0 | [61, 61] | [14.389, 15.259] |
| graph_color | R | 1024 | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | [None, None] | 0/2/0 | [1024, 1024] | [45.949, 55.892] |
| shortest_path | D | 1024 | 2/2/2 | 1/2 | 0/2 | [0.0, 0.0] | ['missing_close_tag', None] | 0/1/0 | [1024, 20] | [45.841, 13.189] |
| shortest_path | R | 1024 | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | [None, None] | 0/2/0 | [1024, 1024] | [45.843, 46.17] |
| knights_knaves | D | 1024 | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [None, None] | 0/0/0 | [18, 18] | [13.547, 12.978] |
| knights_knaves | R | 1024 | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [None, None] | 0/0/0 | [819, 615] | [47.997, 32.76] |
| number_sorting | D | 2048 | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | ['missing_both_tags', 'missing_both_tags'] | 0/0/0 | [20, 20] | [13.026, 13.445] |
| number_sorting | R | 2048 | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [None, None] | 0/0/0 | [586, 444] | [36.905, 31.616] |
| number_format | D | 2048 | 2/2/2 | 2/2 | 0/2 | [0.0, 0.0] | [None, None] | 0/0/0 | [23, 23] | [13.028, 13.847] |
| number_format | R | 2048 | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [None, None] | 0/0/0 | [946, 1867] | [43.426, 91.514] |
| letter_counting | D | 2048 | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [None, None] | 0/0/0 | [8, 8] | [12.449, 13.08] |
| letter_counting | R | 2048 | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [None, None] | 0/0/0 | [791, 806] | [38.149, 46.921] |
| graph_color | D | 2048 | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | ['missing_both_tags', 'missing_both_tags'] | 0/0/0 | [61, 61] | [14.666, 15.377] |
| graph_color | R | 2048 | 2/2/2 | 1/2 | 0/2 | [0.01, 0.0] | [None, None] | 0/1/0 | [2048, 2048] | [80.179, 100.145] |
| shortest_path | D | 2048 | 2/2/2 | 1/2 | 0/2 | [0.0, 0.0] | [None, 'missing_close_tag'] | 0/1/0 | [20, 2048] | [12.804, 94.911] |
| shortest_path | R | 2048 | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | [None, None] | 0/2/0 | [2048, 2048] | [80.41, 99.671] |
| knights_knaves | D | 2048 | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [None, None] | 0/0/0 | [18, 18] | [13.124, 13.249] |
| knights_knaves | R | 2048 | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [None, None] | 0/0/0 | [555, 586] | [30.566, 31.935] |

Missing/unexecuted records and incidents are listed explicitly in incomplete_and_incident_inventory.json. None is imputed as a zero. Per-request generation/load times and allocated/reserved memory are in observations.json.

## Cap-specific input-cluster targets

| Family | Cap | T_b | T_h | h_DD | d_0.10 | d_0.25 |
|---|---|---|---|---|---|---|
| number_sorting | 1024 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| number_sorting | 2048 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| number_format | 1024 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| number_format | 2048 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| letter_counting | 1024 | -0.5 | 0.5 | 0.0 | 0.5 | 0.5 |
| letter_counting | 2048 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| graph_color | 1024 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| graph_color | 2048 | 0.005 | 0.0 | 0.0 | 0.0 | 0.0 |
| shortest_path | 1024 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| shortest_path | 2048 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| knights_knaves | 1024 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| knights_knaves | 2048 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

No cross-cap pooling. Independent stochastic draws share each native input; an observed 2,048 output is not a continuation of an observed 1,024 output. Cross-pairs are not independent samples.

## Offline payload-only diagnostics — never primary scores

| Request | Primary score | Diagnostic native score | Eligibility |
|---|---|---|---|
| 00_number_sorting_D_1024_0 | 0.0 | 1.0 | bare_native_payload_diagnostic |
| 02_number_sorting_D_2048_0 | 0.0 | 1.0 | bare_native_payload_diagnostic |
| 12_graph_color_D_2048_0 | 0.0 | 1.0 | bare_native_payload_diagnostic |
| 14_graph_color_D_1024_0 | 0.0 | 1.0 | bare_native_payload_diagnostic |
| 25_number_sorting_D_2048_1 | 0.0 | 1.0 | bare_native_payload_diagnostic |
| 27_number_sorting_D_1024_1 | 0.0 | 1.0 | bare_native_payload_diagnostic |
| 37_graph_color_D_1024_1 | 0.0 | 1.0 | bare_native_payload_diagnostic |
| 39_graph_color_D_2048_1 | 0.0 | 1.0 | bare_native_payload_diagnostic |

Only an already bare, syntactically valid payload or one uniquely tagged payload with outside prose is eligible. No selection among competing answers, thinking-channel text, extraction from explanatory prose, rewriting or deployment repair. Text-native bare diagnostics require unmistakable count/assignment syntax. Primary completion counts and scores remain unchanged.

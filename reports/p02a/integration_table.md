# P02A twelve-cell integration

Planned denominator is two in every cell. DEVELOPMENT diagnostic only; not the formal cap study.

| Family | Mode | Executed / retained / planned | Strict FINAL | Perfect | Native scores | Failure flags | Output tokens | Generation seconds | Worker seconds (cost) | Peak allocated / reserved MiB |
|---|---|---|---|---|---|---|---|---|---|---|
| number_sorting | D | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | [['outer_wrapper_failure'], ['outer_wrapper_failure']] | [44, 44] | [2.669, 2.464] | [15.565, 14.539] | 15716.22 / 15886.0 |
| number_sorting | R | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [[], []] | [634, 583] | [27.738, 26.077] | [40.348, 38.173] | 15827.48 / 15942.0 |
| number_format | D | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | [['outer_wrapper_failure'], ['outer_wrapper_failure']] | [22, 22] | [1.617, 1.578] | [13.982, 13.884] | 15686.32 / 15846.0 |
| number_format | R | 2/2/2 | 1/2 | 1/2 | [1.0, 0.0] | [[], ['native_delimiter_failure', 'cap_without_valid_final']] | [836, 1024] | [30.211, 41.158] | [42.316, 53.096] | 15868.97 / 16072.0 |
| letter_counting | D | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [[], []] | [8, 8] | [0.801, 0.893] | [12.571, 12.551] | 15667.42 / 15816.0 |
| letter_counting | R | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [[], []] | [750, 814] | [28.017, 35.61] | [40.106, 47.627] | 15829.26 / 15978.0 |
| graph_color | D | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | [['outer_wrapper_failure'], ['outer_wrapper_failure']] | [61, 61] | [2.639, 3.157] | [14.189, 14.963] | 15689.26 / 15852.0 |
| graph_color | R | 2/2/2 | 2/2 | 2/2 | [1.0, 1.0] | [[], []] | [843, 510] | [28.65, 21.829] | [40.331, 34.06] | 15834.64 / 15976.0 |
| shortest_path | D | 2/2/2 | 1/2 | 0/2 | [0.0, 0.0] | [['outer_wrapper_failure'], []] | [251, 23] | [8.997, 1.55] | [20.692, 13.305] | 15761.23 / 15914.0 |
| shortest_path | R | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | [['native_delimiter_failure', 'cap_without_valid_final'], ['native_delimiter_failure', 'cap_without_valid_final']] | [1024, 1024] | [34.846, 43.469] | [46.6, 55.408] | 15892.6 / 16136.0 |
| knights_knaves | D | 2/2/2 | 0/2 | 0/2 | [0.0, 0.0] | [['outer_wrapper_failure'], ['outer_wrapper_failure']] | [327, 536] | [14.819, 23.212] | [26.943, 35.338] | 15776.11 / 15916.0 |
| knights_knaves | R | 2/2/2 | 1/2 | 1/2 | [0.0, 1.0] | [['native_delimiter_failure', 'cap_without_valid_final'], []] | [1024, 825] | [44.893, 34.504] | [56.98, 46.554] | 15869.8 / 16070.0 |

Full precision, failure flags, individual generation times and memory are in twelve_cells.json and integration_observations.json. All cells retain their planned denominators; missing rows are not imputed.

## Complete-cluster target checks

| Family | T_b | T_h | h_DD | d_0.10 | d_0.25 |
|---|---|---|---|---|---|
| number_sorting | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| number_format | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 |
| letter_counting | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| graph_color | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| shortest_path | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| knights_knaves | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 |
